import constants.universe_settings as universe_settings

from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([5.0, 5.0, 15.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.yaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset, yoffset, constraint_pitch=True):
        xoffset *= universe_settings.MOUSE_SENSITIVITY
        yoffset *= universe_settings.MOUSE_SENSITIVITY

        self.yaw += xoffset
        self.pitch -= yoffset

        if constraint_pitch:
            self.pitch = max(-90, min(90, self.pitch))

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ])
        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity
        if direction == "UP":
            self.camera_pos += Vector3([0.0, 1.0, 0.0]) * velocity
        if direction =="DOWN":
            self.camera_pos -= Vector3([0.0, 1.0, 0.0]) * velocity