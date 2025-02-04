SHOW_XYZ_LINES = 1
SHOW_3D_GRID = 1
SHOW_PARTICLE_TRAIL = 0
SHOW_CONNECTING_LINES = 0

COLOR_BACKGROUND = [0.003, 0.04, 0.15]
COLOR_3D_GRID = [0.4, 0.4, 1.0]
COLOR_DEFAULT_PARTICLE = [255, 255, 255]
COLOR_CONNECTING_LINES = [1, 1, 1]


def set_xyz_lines(new_value):
    
    global SHOW_XYZ_LINES

    SHOW_XYZ_LINES = new_value

def set_3d_grid(new_value):

    global SHOW_3D_GRID

    SHOW_3D_GRID = new_value

def set_particle_trail(new_value):
    
    global SHOW_PARTICLE_TRAIL

    SHOW_PARTICLE_TRAIL = new_value

def set_connecting_lines(new_value):

    global SHOW_CONNECTING_LINES

    SHOW_CONNECTING_LINES = new_value

def set_background_color(new_value):

    global COLOR_BACKGROUND

    COLOR_BACKGROUND = new_value

def set_3d_grid_color(new_value):

    global COLOR_3D_GRID
    
    COLOR_3D_GRID = new_value

def set_default_particle(new_value):

    global COLOR_DEFAULT_PARTICLE

    COLOR_DEFAULT_PARTICLE = [new_value[0] * 255, new_value[1] * 255, new_value[2] * 255]

def set_connecting_lines_color(new_value):

    global COLOR_CONNECTING_LINES

    COLOR_CONNECTING_LINES = new_value