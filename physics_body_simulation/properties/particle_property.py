import constants.universe_settings as universe_settings

import numpy as np
from OpenGL.GLU import gluNewQuadric

class Particle:
    def __init__(
        self,
        id=0,
        name="P1",
        parent_particle = "None",
        position=[1.0, 1.0, 1.0], 
        velocity=[0.0, 0.0, 0.0], 
        acceleration=[0.0, 0.0, 0.0], 
        mass=1.0, 
        radius=1.0, 
        collision=False,
        elasticity=0.0,
        gravity_plane=True,
        color = [255, 255, 255]
    ):

        super().__init__()

        # Defined Properties
        self.id = id
        self.name = name
        self.position = np.array(position, dtype = float)
        self.velocity = np.array(velocity, dtype = float)
        self.acceleration = np.array(acceleration, dtype = float)
        self.mass = mass
        self.radius = radius
        self.collision = collision
        self.elasticity = elasticity
        self.gravity_plane = gravity_plane
        self.color = color
        
        # Dynamic Values
        self.position_dynamic = np.array(position, dtype = float)
        self.velocity_dynamic = np.array(velocity, dtype = float)
        self.acceleration_dynamic = np.array([0.0, 0.0, 0.0], dtype = float)
        self.acceleration_gravity_particle = np.array([0.0, 0.0, 0.0], dtype = float)
        self.acceleration_total = self.acceleration
        self.momentum_dynamic = self.mass * self.velocity
        self.force_dynamic = self.mass * self.acceleration_total

        # Magnitude of Properties
        self.velocity_magnitude = np.linalg.norm(self.velocity_dynamic)
        self.acceleration_magnitude = np.linalg.norm(self.acceleration)
        self.momentum_magnitude = np.linalg.norm(self.momentum_dynamic)
        self.force_magnitude = np.linalg.norm(self.force_dynamic)

        # Energy
        self.kinetic_energy_dynamic = 0.5 * self.mass * self.velocity_magnitude**2
        self.potential_energy_gravity_plane = 0.0
        self.potential_energy_gravity_particle = 0.0
        self.potential_energy_dynamic = 0.0
        self.total_energy_dynamic = 0.0

        self.quadric = gluNewQuadric()

        self.parent_particle = parent_particle
        self.parent_executed_indicator = False

        self.trail = []
        self.max_trail_length = 50  # Adjust this for longer/shorter trails
        self.trail_update_rate = 1  # Store position every N frames
        self.frame_counter = 0

    def update_trail(self):
        """Updates the logic for the trail left by the particle"""

        self.frame_counter += 1
        if self.frame_counter >= self.trail_update_rate:
            self.trail.append(list(self.position_dynamic))  # Store current position
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)  # Remove oldest position
            self.frame_counter = 0

    def reset(self):
        """Reset particle to its initial state"""

        self.position_dynamic = self.position.copy()
        self.velocity_dynamic = self.velocity.copy()
        self.acceleration_dynamic = np.array([0.0, 0.0, 0.0], dtype = float)
        self.momentum_dynamic = self.mass * self.velocity

        self.velocity_magnitude = np.linalg.norm(self.velocity_dynamic)
        self.acceleration_magnitude = np.linalg.norm(self.acceleration_total)
        self.momentum_magnitude = np.linalg.norm(self.momentum_dynamic)
        self.kinetic_energy_dynamic = 0.0
        self.potential_energy_gravity_particle = 0.0
        self.potential_energy_gravity_plane = 0.0
        self.total_energy_dynamic = 0.0
        self.trail = []

    def total_calculations(self):
        """Calculates the total values of individual properties"""

        self.acceleration_total = self.acceleration_dynamic + self.acceleration + self.acceleration_gravity_particle
        self.potential_energy_dynamic = self.potential_energy_gravity_particle + self.potential_energy_gravity_plane
        self.potential_energy_gravity_plane = 0.0
        self.force_dynamic = self.mass * self.acceleration_total

    def update_linear(self):
        """Updates properties with each time step"""

        self.total_calculations()

        # Uses Leapfrog Integration Algorithm for accurate values
        self.velocity_dynamic += 0.5 * self.acceleration_total * universe_settings.TIME_STEP
        self.position_dynamic += self.velocity_dynamic * universe_settings.TIME_STEP
        self.velocity_dynamic += 0.5 * self.acceleration_total * universe_settings.TIME_STEP

        # Calculate kinetic energy
        self.kinetic_energy_dynamic = 0.5 * self.mass * np.linalg.norm(self.velocity_dynamic) ** 2
        self.total_energy_dynamic = self.kinetic_energy_dynamic + self.potential_energy_dynamic
        self.momentum_dynamic = self.mass * self.velocity_dynamic

        # Calculate Magnitudes
        self.velocity_magnitude = np.linalg.norm(self.velocity_dynamic)
        self.acceleration_magnitude = np.linalg.norm(self.acceleration_total)
        self.momentum_magnitude = np.linalg.norm(self.momentum_dynamic)
        self.force_magnitude = np.linalg.norm(self.force_dynamic)

        self.parent_executed_indicator = False

        self.acceleration_gravity_particle = np.array([0.0, 0.0, 0.0], dtype = float)

    def particle_collision(self, other):
        """
        Calculates the post-collision velocities of two particles using the impulse-based collision response

        The formulas used:

            v1_a = v0_a + (j / M_a) * n   (for self particle)
            v1_b = v0_b - (j / M_b) * n   (for other particle)

            j = (-(1 + e) * <v1_a - v1_b, n>) / ( <n, n> * (1 / M_a + 1 / M_b) )

        where:
            v1_a, v0_a : Final and initial velocity of the self particle
            v1_b, v0_b : Final and initial velocity of the other particle
            M_a, M_b   : Mass of self and other particle
            n          : Normal vector, calculated as (position_self - position_other)
            j          : Impulse (change in momentum)
            e          : Coefficient of restitution (elasticity factor)

        Energy correction:
            To conserve kinetic energy, we apply a correction factor:
            
                correction_factor = sqrt(initial_kinetic_energy / final_kinetic_energy)
        """

        if not (self.collision and other.collision):
            return
        
        epsilon = 0.0001
        diff_position = self.position_dynamic - other.position_dynamic
        distance_norm = np.linalg.norm(diff_position)

        if distance_norm <= (self.radius + other.radius):
            
            normal = diff_position / (distance_norm + epsilon)
            relative_velocity = self.velocity_dynamic - other.velocity_dynamic

            kinetic_energy_initial = 0.5 * ((self.mass * (np.linalg.norm(self.velocity_dynamic)**2)) + (other.mass * (np.linalg.norm(other.velocity_dynamic)**2)))

            e_self = self.elasticity
            e_other = other.elasticity

            j_self = -(1 + e_self) * np.dot(relative_velocity, normal)
            j_self /= (1 / self.mass) + (1 / other.mass)
            j_other = -(1 + e_other) * np.dot(relative_velocity, normal)
            j_other /= (1 / self.mass) + (1 / other.mass)

            self.velocity_dynamic += (j_self * normal) / self.mass
            other.velocity_dynamic -= (j_other * normal) / other.mass

            kinetic_energy_final = 0.5 * ((self.mass * (np.linalg.norm(self.velocity_dynamic)**2)) + (other.mass * (np.linalg.norm(other.velocity_dynamic)**2)))
            energy_diff = kinetic_energy_final - kinetic_energy_initial
            float_tolerance = 0.0001

            if abs(energy_diff) > float_tolerance:
                correction_factor = np.sqrt(kinetic_energy_initial / kinetic_energy_final)
                self.velocity_dynamic *= correction_factor
                other.velocity_dynamic *= correction_factor

            overlap = (self.radius + other.radius - distance_norm) / 2
            self.position_dynamic += overlap * normal / 2
            other.position_dynamic -= overlap * normal / 2

    def particle_gravity(self, other):

        """
        Calculate the gravitational force between two particles using Newton's law of universal gravitation

        The formula used:
        
            F = (G * m_a * m_b) / r^2

        where:
            F  : Force between the two objects
            G  : Gravitational constant
            m_a: Mass of particle a
            m_b: Mass of particle b
            r  : Distance between the two particles
        """

        diff_position = other.position_dynamic - self.position_dynamic
        r = np.linalg.norm(diff_position)

        if r < 0.1:
            r = 0.1

        force_magnitude = universe_settings.GRAVITATIONAL_CONSTANT * self.mass * other.mass / (r ** 2)
        force_direction = diff_position / r
        self_acceleration = force_magnitude * force_direction / self.mass
        other_acceleration = -force_magnitude * force_direction / other.mass

        # Parent particle logic
        if ((self.parent_particle != "None" and other.parent_particle == "None") or (self.parent_particle != "None" and other.parent_particle != "None")) and self.parent_executed_indicator == False:
            self.acceleration_gravity_particle += self_acceleration
            self.parent_executed_indicator = True
        elif self.parent_particle == "None" and other.parent_particle != "None" and other.parent_executed_indicator == False:
            other.acceleration_gravity_particle += other_acceleration
            other.parent_executed_indicator = True
        elif self.parent_particle == "None" and other.parent_particle == "None":
            self.acceleration_gravity_particle += self_acceleration
            other.acceleration_gravity_particle += other_acceleration

        potential_energy = -universe_settings.GRAVITATIONAL_CONSTANT * self.mass * other.mass / r
        self.potential_energy_gravity_particle = potential_energy / 2
        other.potential_energy_gravity_particle = potential_energy / 2
