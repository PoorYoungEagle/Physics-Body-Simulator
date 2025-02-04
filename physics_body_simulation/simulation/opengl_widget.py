import utils.geometry as geometry
from simulation.camera import Camera
import constants.universe_settings as universe_settings
import constants.visual_settings as visual_settings

from PyQt5 import QtOpenGL, QtCore
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

"""
Performance Limitations:

1. OpenGL Implementation:
   - Uses deprecated OpenGL version
   - Not optimized for modern GPU acceleration

2. Computational Complexity:
   - Particle interactions use O(n^2) time complexity
   - Each particle must check against every other particle
   - Performance degrades significantly as particle count increases

This creates a bottleneck when simulating large numbers of particles,
making the simulation unsuitable for scenarios requiring thousands of particles.
Its mainly used for quick testing and plotting out values on graphs.
"""

class OpenGLWidget(QtOpenGL.QGLWidget): #Use QtWidgets.QOpenGLWidget for newer modern GL versions
    def __init__(
            self,
            parent=None,
            fullscreen_signal=None,
            start_simulation = None,
            stop_simulation = None,
            reset_simulation = None,
            particle_variables=None,
            particle_classes=None,
            gravity_classes=None,
            boundary=None
        ):
        super(QtOpenGL.QGLWidget, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        self.camera = Camera()
        self.keys_pressed = set()
        self.last_mouse_position = None

        self.fullscreen_signal = fullscreen_signal
        self.start_simulation_opengl = start_simulation
        self.stop_simulation_opengl = stop_simulation
        self.reset_simulation_opengl = reset_simulation

        self.sprint = 1

        self.particle_classes = particle_classes
        self.particle_variables = particle_variables
        self.gravity_classes = gravity_classes
        self.boundary = boundary

        # For camera/user movement
        self.timer_movement = QtCore.QTimer()
        self.timer_movement.timeout.connect(self.update_movement)
        self.timer_movement.start(16)

        # For the actual simulation
        self.timer_speed = 16
        self.timer_simulation = QtCore.QTimer()
        self.timer_simulation.timeout.connect(self.update_physics)


    def initializeGL(self):
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_MULTISAMPLE)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, width / height, 0.01, universe_settings.RENDER_DISTANCE)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Creates and displays the elements mentioned by the simulation"""

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*visual_settings.COLOR_BACKGROUND, 1)

        # Camera view matrix logic
        view_matrix = self.camera.get_view_matrix()
        glLoadMatrixf(view_matrix.flatten())

        glDepthMask(GL_TRUE)
        if self.particle_classes.values():
            for particle in self.particle_classes.values():
                
                if visual_settings.SHOW_PARTICLE_TRAIL:
                    if particle.trail:
                        geometry.particle_trail_effect(particle)

                # Creates a sphere for each particle created in simulation
                glPushMatrix()
                glColor4f(*particle.color, 1)
                glTranslatef(*particle.position_dynamic)
                gluSphere(particle.quadric, particle.radius, 64, 64)
                glPopMatrix()

            if visual_settings.SHOW_CONNECTING_LINES:
                particle_list = list(self.particle_classes.values())
                for i in range(len(self.particle_classes.values())):
                    for j in range(i + 1, len(self.particle_classes.values())):
                        geometry.particle_connecting_lines(particle_list[i], particle_list[j])
        
        glDepthMask(GL_FALSE)
        if self.gravity_classes.values():
            for gravity in self.gravity_classes.values():
                vertices = gravity.vertices

                glPushMatrix()
                glEnable(GL_LINE_SMOOTH)
                if gravity.design == 'Fill':
                    transparency = gravity.plane_opacity / 100.0
                    glColor4f(*gravity.plane_color, transparency)
                    glBegin(GL_QUADS)
                    for i in range(4):
                        glVertex3fv(vertices[i])
                    glEnd()

                if gravity.design == 'Outline':
                    transparency = gravity.plane_opacity / 100.0
                    glColor4f(*gravity.plane_color, transparency)
                    glBegin(GL_LINE_LOOP)
                    for i in range(4):
                        glVertex3fv(vertices[i])
                    glEnd()
                
                transparency = gravity.line_opacity / 100.0
                glColor4f(*gravity.line_color, transparency)
                
                glBegin(GL_LINES)
                for i in range(4):
                    glVertex3fv(vertices[i])
                    glVertex3fv(vertices[i + 4])
                glEnd()
                
                glBegin(GL_LINE_LOOP)
                for i in range(4, 8):
                    glVertex3fv(vertices[i])
                glEnd()
                glPopMatrix()

        glDepthMask(GL_TRUE)
        if self.boundary:
            boundary = self.boundary[1]
            vertices = boundary.vertices
            glPushMatrix()
            glEnable(GL_LINE_SMOOTH)
                
            transparency = boundary.opacity / 100.0
            glColor4f(*boundary.color, transparency)

            glBegin(GL_LINES)
            for i in range(4):
                glVertex3fv(vertices[i])
                glVertex3fv(vertices[i + 4])
            glEnd()
            
            # Bottom face outline
            glBegin(GL_LINE_LOOP)
            for i in range(4):
                glVertex3fv(vertices[i])
            glEnd()
            
            # Top face outline
            glBegin(GL_LINE_LOOP)
            for i in range(4, 8):
                glVertex3fv(vertices[i])
            glEnd()
            glPopMatrix()

        glColor4f(1, 1, 1, 1)

        if visual_settings.SHOW_XYZ_LINES:
            geometry.Lines3D()

        if visual_settings.SHOW_3D_GRID:
            geometry.infinite_grid_xyz(self.camera.camera_pos)

        # Graphing Updates

        for particle, variable in self.particle_variables.values():
            try:
                variable.update_particle_variables(particle)
            except:
                pass



    def update_physics(self):
        """
        Updates particle gravity and collision
        Implements an O(n^2) algorithm to iterate each particle to every other particle for gravity
        """

        particle_list = list(self.particle_classes.values())
        gravity_list = list(self.gravity_classes.values())
        for particle in particle_list:

            if visual_settings.SHOW_PARTICLE_TRAIL:
                particle.update_trail()
            
            particle.update_linear()
            if self.boundary:
                self.boundary[1].check_boundary_collision(particle)

        for i, particle in enumerate(particle_list):    
            for j in range(i + 1, len(particle_list)):
                other_particle = particle_list[j]
                particle.particle_collision(other_particle)

                if universe_settings.PARTICLE_GRAVITY :
                    particle_parent = particle.parent_particle
                    other_particle_parent = other_particle.parent_particle

                    # If a particle has a parent particle
                    #   - the parent particle's gravity is not influenced by the child particle, 
                    #   - the child particle's gravity is influenced only by the parent particle

                    if particle_parent != "None" and other_particle_parent != "None":
                        particle.particle_gravity(particle_parent)
                        other_particle.particle_gravity(other_particle_parent)
                    elif particle_parent != "None":
                        particle.particle_gravity(particle_parent)
                    elif other_particle_parent != "None":
                        other_particle.particle_gravity(other_particle_parent)
                    else:
                        particle.particle_gravity(other_particle)


        if gravity_list:
            for particle in particle_list:
                total_force = np.array([0.0, 0.0, 0.0])
                for gravity in gravity_list:
                    # For multiple gravity planes, it calculates the total force applied on the particle
                    total_force += gravity.apply_gravity(particle)
                    gravity.check_collision_with_plane(particle)
                particle.acceleration_dynamic = total_force

        self.update()

    def reset_simulation(self):
        """Resets the simulation back to its original state"""
        self.timer_simulation.stop()
        universe_settings.set_time_multiplier(1)
        for particle in self.particle_classes.values():
            particle.reset()
        self.update()

    """Controls and key inputs"""

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

        # Fullscreen signal when F is pressed
        if event.key() == QtCore.Qt.Key_F:
            if self.fullscreen_signal:
                self.fullscreen_signal()

        if event.key() == QtCore.Qt.Key_Q:
            self.start_simulation_opengl()

        if event.key() == QtCore.Qt.Key_E:
            self.stop_simulation_opengl()

        if event.key() == QtCore.Qt.Key_R:
            self.reset_simulation_opengl()

    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_mouse_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_position is not None:
            dx = event.x() - self.last_mouse_position.x()
            dy = event.y() - self.last_mouse_position.y()
            self.camera.process_mouse_movement(dx, dy)
            self.last_mouse_position = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_mouse_position = None

    def update_movement(self):
        velocity = universe_settings.CAMERA_SPEED * self.sprint  # Adjust for speed

        if QtCore.Qt.Key_W in self.keys_pressed:
            self.camera.process_keyboard("FORWARD", velocity)
        if QtCore.Qt.Key_S in self.keys_pressed:
            self.camera.process_keyboard("BACKWARD", velocity)
        if QtCore.Qt.Key_A in self.keys_pressed:
            self.camera.process_keyboard("LEFT", velocity)
        if QtCore.Qt.Key_D in self.keys_pressed:
            self.camera.process_keyboard("RIGHT", velocity)
        if QtCore.Qt.Key_Space in self.keys_pressed:
            self.camera.process_keyboard("UP", velocity)
        if QtCore.Qt.Key_Control in self.keys_pressed:
            self.camera.process_keyboard("DOWN",velocity)
        if QtCore.Qt.Key_Shift in self.keys_pressed:
            self.sprint = 2
        else:
            self.sprint = 1
        
        self.update()