import numpy as np

class Gravity:
    def __init__(self,
        name="G1",
        position=[0.0, 0.0, 0.0],
        normal=[0.0, 1.0, 0.0],
        width=5.0,
        depth=5.0,
        gravity_strength=9.8,
        design="Fill",
        plane_color=[255, 255, 255],
        plane_opacity=100,
        line_color=[255, 255, 255],
        line_opacity=100,
        collision=True
    ):
        self.name = name
        self.position = np.array(position, dtype=float)
        self.normal = np.array(normal, dtype=float) / np.linalg.norm(np.array(normal))
        self.gravity_strength = float(gravity_strength)
        self.height = self.gravity_strength * 1000
        self.width = width
        self.depth = depth
        self.design = design
        self.plane_color = plane_color
        self.plane_opacity = plane_opacity
        self.line_color = line_color
        self.line_opacity = line_opacity
        self.collision = collision

        self.vertices = np.array([
            # Bottom face
            [-self.width / 2, 0, -self.depth / 2],
            [self.width / 2, 0, -self.depth / 2],
            [self.width / 2, 0, self.depth / 2],
            [-self.width / 2, 0, self.depth / 2],
            
            # Top face
            [-self.width / 2, self.height, -self.depth / 2],
            [self.width / 2, self.height, -self.depth / 2],
            [self.width / 2, self.height, self.depth / 2],
            [-self.width / 2, self.height, self.depth / 2],
        ], dtype=float)

    def normalize_vector(self, vector):
        """Normalize a vector to unit length"""
        vector = np.array(vector, dtype='float32')
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

    def rotation_matrix_formula(self, axis, angle):
        """Create a rotation matrix from an axis and angle using Rodrigues formula"""

        axis = self.normalize_vector(axis)
        
        # Rodrigues rotation formula
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        k_cross = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        
        rotation_matrix = (np.eye(3) * cos_theta + sin_theta * k_cross + (1 - cos_theta) * np.outer(axis, axis))
        
        return rotation_matrix

    def rotation_matrix_value(self, default_normal):
        """Uses Rodrigues' formula to get the rotation matrix"""
        
        # If the normal vectors are already aligned, return the identity matrix (no rotation)
        rotated_normal = self.normal

        if np.allclose(default_normal, rotated_normal):
            return np.eye(3)
        
        # If the normal vectors are opposite, use a perpendicular axis to perform a 180-degree rotation
        if np.allclose(default_normal, -rotated_normal):
            perp_axis = np.array([1, 0, 0]) if not np.allclose(default_normal, [1, 0, 0]) else np.array([0, 1, 0])
            perp_axis = self.normalize_vector(np.cross(default_normal, perp_axis))
            return self.rotation_matrix_formula(perp_axis, np.pi)
        
        # Otherwise, calculate the rotation axis and angle between the normals
        rotation_axis = self.normalize_vector(np.cross(default_normal, rotated_normal))
        cos_angle = np.dot(default_normal, rotated_normal)
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        
        return self.rotation_matrix_formula(rotation_axis, angle)

    def fix_numerical_error(self, matrix, tolerance=1e-10):
        """Fix small numerical errors by setting values close to zero to zero"""
        if isinstance(matrix, np.ndarray):
            matrix[np.abs(matrix) < tolerance] = 0

        return matrix

    def create_plane(self):
        """Rotate and position the gravity plane"""
        default_normal = np.array([0, 1, 0])
        rotation_matrix = self.rotation_matrix_value(default_normal)
        rotated_vertices = np.dot(self.vertices, rotation_matrix.T)  # Apply rotation

        rotated_vertices = self.fix_numerical_error(rotated_vertices)

        self.vertices = rotated_vertices + self.position

    def is_within_bounds(self, particle):
        """Check if the position is within the boundary-defined area on the tilted plane"""

        position = particle.position_dynamic
        rotation_matrix = self.rotation_matrix_value(self.normal)  # Based on current normal
        
        relative_position = position - self.position
        distance_to_plane = np.dot(relative_position, self.normal)
        
        if distance_to_plane < 0 or distance_to_plane > self.height:
            return False  # Particle is below the plane; no gravity should apply
        
        projected_position = position - distance_to_plane * self.normal
        
        transformed_vertices = np.dot(self.vertices - self.position, rotation_matrix.T)
        transformed_projected_position = np.dot(projected_position - self.position, rotation_matrix.T)
        
        x_min, x_max = np.min(transformed_vertices[:, 0]), np.max(transformed_vertices[:, 0])
        y_min, y_max = np.min(transformed_vertices[:, 1]), np.max(transformed_vertices[:, 1])
        z_min, z_max = np.min(transformed_vertices[:, 2]), np.max(transformed_vertices[:, 2])

        within_bounds = (x_min <= transformed_projected_position[0] <= x_max and
                        y_min <= transformed_projected_position[1] <= y_max and
                        z_min <= transformed_projected_position[2] <= z_max)
        
        if within_bounds:
            particle.potential_energy_gravity_plane += particle.mass * self.gravity_strength * distance_to_plane
        
        return within_bounds

    def apply_gravity(self, particle):
        """Apply gravity to the particle if it is within the gravity volume"""

        if self.is_within_bounds(particle) and particle.gravity_plane:
            acceleration = -(self.gravity_strength * self.normal)
            return acceleration
        else:
            return np.array([0.0, 0.0, 0.0])

    def transform_to_local_space(self, position):
        """Transform a world space position to plane's local space"""

        relative_pos = position - self.position
        rotation_matrix = self.rotation_matrix_value(self.normal)
        return np.dot(relative_pos, rotation_matrix.T)

    def check_collision_with_plane(self, particle):
        """Collision detection and resolution for a gravity plane with an arbitrary normal"""

        if not self.collision:
            return False

        # Distance of the particle from the plane
        dist_to_plane = np.dot(particle.position_dynamic - self.position, self.normal)
        if dist_to_plane < -particle.radius:
            return False

        projected_position = particle.position_dynamic - dist_to_plane * self.normal

        relative_projected_position = projected_position - self.position
        local_projected_position = np.dot(relative_projected_position, self.rotation_matrix_value([0, 1, 0]).T)
        self.fix_numerical_error(local_projected_position)

        local_vertices = np.dot(self.vertices - self.position, self.rotation_matrix_value([0, 1, 0]).T)
        self.fix_numerical_error(local_vertices)

        x_min, x_max = np.min(local_vertices[:, 0]), np.max(local_vertices[:, 0])
        y_min, y_max = np.min(local_vertices[:, 1]), np.max(local_vertices[:, 1])
        z_min, z_max = np.min(local_vertices[:, 2]), np.max(local_vertices[:, 2])

        if x_min <= local_projected_position[0] <= x_max and y_min <= local_projected_position[1] <= y_max and z_min <= local_projected_position[2] <= z_max:

            velocity_toward_plane = np.dot(particle.velocity_dynamic, self.normal)
            if velocity_toward_plane < 0:
                # Penetration depth
                if dist_to_plane < particle.radius:
                    penetration_depth = particle.radius - dist_to_plane

                    normal_velocity = np.dot(particle.velocity_dynamic, self.normal) * self.normal
                    tangent_velocity = particle.velocity_dynamic - normal_velocity
                    reflected_velocity = -particle.elasticity * normal_velocity * 0.99
                    
                    particle.position_dynamic += self.normal * penetration_depth
                    particle.velocity_dynamic = tangent_velocity + reflected_velocity
                    return True

        return False