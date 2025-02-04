import constants.visual_settings as visual_settings

from OpenGL.GL import *
from OpenGL.GLU import *
import math

"""Geometry and logic present in the simulation"""

def Lines3D():
    """Displays the XYZ Lines present in the simulation"""

    grid_3d = (
        (0, 0, 0),   # Origin
        (50, 0, 0), # Positive X
        (0, 50, 0), # Positive Y
        (0, 0, 50), # Positive Z
        (-50, 0, 0),# Negative X
        (0, -50, 0),# Negative Y
        (0, 0, -50) # Negative Z
    )
    edges = (
        (0, 1),  # Positive X
        (0, 2),  # Positive Y
        (0, 3),  # Positive Z
        (0, 4),  # Negative X
        (0, 5),  # Negative Y
        (0, 6)   # Negative Z
    )

    arrow_length = 1.0
    arrow_base_radius = 0.2
    segments = 16
    
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(5.0)
    
    # Draw lines
    for edge in edges:
        if edge == (0, 1) or edge == (0, 4):        # X-axis
            glColor4f(0.6, 0, 0, 1)         # Red
        elif edge == (0, 2) or edge == (0, 5):      # Y-axis
            glColor4f(0, 0.6, 0, 1)         # Green
        elif edge == (0, 3) or edge == (0, 6):      # Z-axis
            glColor4f(0, 0, 0.6, 1)         # Blue

        start, end = grid_3d[edge[0]], grid_3d[edge[1]]
        
        # Calculate direction vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        
        # Normalize direction
        length = (dx**2 + dy**2 + dz**2)**0.5
        if length == 0:
            continue
        
        dx, dy, dz = dx/length, dy/length, dz/length
        
        # Create a coordinate system
        if abs(dz) > 0.9:  # If pointing mostly up/down
            ux, uy, uz = 1, 0, 0
            vx, vy, vz = 0, 1, 0
        else:
            ux = -dy
            uy = dx
            uz = 0
            vx = -dx*dz
            vy = -dy*dz
            vz = dx**2 + dy**2
        
        # Normalize perpendicular vectors
        ulength = (ux**2 + uy**2 + uz**2)**0.5
        vlength = (vx**2 + vy**2 + vz**2)**0.5
        
        ux, uy, uz = ux/ulength, uy/ulength, uz/ulength
        vx, vy, vz = vx/vlength, vy/vlength, vz/vlength
        
        # Cone tip
        cone_tip = (
            end[0] + arrow_length * dx,
            end[1] + arrow_length * dy,
            end[2] + arrow_length * dz
        )
        
        # Draw cone base
        glBegin(GL_TRIANGLE_FAN)
        glVertex3fv(end)  # Center of base
        
        for i in range(segments + 1):
            angle = 2 * 3.14159 * i / segments
            base_x = end[0] + arrow_base_radius * (ux * math.cos(angle) + vx * math.sin(angle))
            base_y = end[1] + arrow_base_radius * (uy * math.cos(angle) + vy * math.sin(angle))
            base_z = end[2] + arrow_base_radius * (uz * math.cos(angle) + vz * math.sin(angle))
            glVertex3f(base_x, base_y, base_z)
        glEnd()
        
        # Draw cone surface
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(segments + 1):
            angle = 2 * 3.14159 * i / segments
            base_x = end[0] + arrow_base_radius * (ux * math.cos(angle) + vx * math.sin(angle))
            base_y = end[1] + arrow_base_radius * (uy * math.cos(angle) + vy * math.sin(angle))
            base_z = end[2] + arrow_base_radius * (uz * math.cos(angle) + vz * math.sin(angle))
            glVertex3f(base_x, base_y, base_z)
            glVertex3fv(cone_tip)
        glEnd()

        glBegin(GL_LINES)
        for vertex in edge:
            glVertex3fv(grid_3d[vertex])
        glEnd()
    
    glLineWidth(1.0)

def infinite_grid_xyz(camera_position):
    """Implements an infinite grid logic and display"""

    glPushMatrix()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glLineWidth(1.5)
    
    camera_x, camera_y, camera_z = camera_position
    
    grid_range_x = int(camera_x / 50) * 50
    grid_range_z = int(camera_z / 50) * 50
    
    grid_height = 0.0
    
    grid_min_x = grid_range_x - 250
    grid_max_x = grid_range_x + 250
    grid_min_z = grid_range_z - 250
    grid_max_z = grid_range_z + 250
    
    base_color = visual_settings.COLOR_3D_GRID
    
    def calculate_fog_fade(point, camera_pos):
        dx = point[0] - camera_pos[0]
        dz = point[2] - camera_pos[2]
        distance = (dx * dx + dz * dz) ** 0.5
        
        fog_end = 300.0
        fog_density = 0.8
        
        if distance > fog_end:
            return 0.0
        return 1.0 - (distance / fog_end) ** fog_density
    
    glBegin(GL_LINES)
    
    # Draw X-aligned lines
    for i in range(int(grid_min_x), int(grid_max_x) + 1):
        start_point = (float(i), grid_height, float(grid_min_z))
        end_point = (float(i), grid_height, float(grid_max_z))
        
        fade_factor = calculate_fog_fade(start_point, camera_position)
        base_alpha = 0.9 if i % 10 == 0 else 0.5
        alpha = base_alpha * fade_factor
        
        if alpha > 0.01:
            glColor4f(*base_color, alpha)
            glVertex3f(*start_point)
            glVertex3f(*end_point)
    
    # Draw Z-aligned lines
    for j in range(int(grid_min_z), int(grid_max_z) + 1):
        start_point = (float(grid_min_x), grid_height, float(j))
        end_point = (float(grid_max_x), grid_height, float(j))
        
        fade_factor = calculate_fog_fade(start_point, camera_position)
        base_alpha = 0.9 if j % 10 == 0 else 0.5
        alpha = base_alpha * fade_factor
        
        if alpha > 0.01:
            glColor4f(*base_color, alpha)
            glVertex3f(*start_point)
            glVertex3f(*end_point)
    
    # Draw axes
    z_start = (0.0, grid_height, float(grid_min_z))
    z_end = (0.0, grid_height, float(grid_max_z))
    z_fade = calculate_fog_fade(z_start, camera_position)
    if z_fade > 0.01:
        glColor4f(0.0, 0.0, 1.0, min(1.0, z_fade))
        glVertex3f(*z_start)
        glVertex3f(*z_end)
    
    x_start = (float(grid_min_x), grid_height, 0.0)
    x_end = (float(grid_max_x), grid_height, 0.0)
    x_fade = calculate_fog_fade(x_start, camera_position)
    if x_fade > 0.01:
        glColor4f(1.0, 0.0, 0.0, min(1.0, x_fade))
        glVertex3f(*x_start)
        glVertex3f(*x_end)
    
    glEnd()
    
    glPopMatrix()

def particle_trail_effect(particle):
    """Displays a trail effect on each particle"""
    
    glPushMatrix()
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(5.0)
    glBegin(GL_LINE_STRIP)
    for i, pos in enumerate(particle.trail):
        # Fade out the trail from current to old positions
        alpha = 0.8 * (i / len(particle.trail))
        glColor4f(*particle.color, alpha)
        glVertex3fv(pos)
    glEnd()
    glPopMatrix()
    glLineWidth(1.5)

def particle_connecting_lines(particle1, particle2):
    """Connects two particles with a line"""

    glPushMatrix()
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor4f(*visual_settings.COLOR_CONNECTING_LINES, 1)
    glVertex3fv(particle1.position_dynamic)
    glVertex3fv(particle2.position_dynamic)
    glEnd()
    glPopMatrix()
    glLineWidth(1.5)