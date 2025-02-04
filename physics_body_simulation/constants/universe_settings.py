TIME_MULTIPLIER = 1.0
TIME_STEP = 0.016
MOUSE_SENSITIVITY = 0.25
CAMERA_SPEED = 0.05
RENDER_DISTANCE = 1000.0
GRAVITATIONAL_CONSTANT = 0.01
PARTICLE_GRAVITY = 1


def set_time_multiplier(new_value):

    global TIME_MULTIPLIER

    TIME_MULTIPLIER = new_value

def update_time_multiplier(add_sub):

    global TIME_MULTIPLIER

    new_value = TIME_MULTIPLIER + add_sub
    if 0.1 <= new_value <= 5.0:
        TIME_MULTIPLIER = new_value
    else:
        TIME_MULTIPLIER = max(0.1, min(new_value, 5.0))

def set_time_step(new_value):

    global TIME_STEP

    TIME_STEP = new_value * TIME_MULTIPLIER

def set_mouse_sensitivity(new_value):

    global MOUSE_SENSITIVITY

    MOUSE_SENSITIVITY = new_value

def set_camera_speed(new_value):

    global CAMERA_SPEED

    CAMERA_SPEED = new_value

def set_render_distance(new_value):

    global RENDER_DISTANCE

    RENDER_DISTANCE = new_value

def set_gravitational_constant(new_value):

    global GRAVITATIONAL_CONSTANT
    
    GRAVITATIONAL_CONSTANT = new_value

def set_particle_gravity(new_value):

    global PARTICLE_GRAVITY

    PARTICLE_GRAVITY = new_value