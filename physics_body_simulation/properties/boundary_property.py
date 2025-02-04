import numpy as np

class Boundary:
    """A boundary region where a particle can't exist outside its bounds"""
    
    def __init__(self,
        width = 25,
        depth = 25,
        height = 25,
        restitution = 1.0,
        color = [255, 255, 255],
        opacity = 100
    ):
        self.width = width
        self.depth = depth
        self.height = height
        self.color = np.array(color, dtype = float)
        self.restitution = restitution
        self.opacity = opacity

        self.bounds = [width / 2, height / 2, depth / 2]
        self.vertices = np.array([
            # Bottom face
            [-self.width / 2, -self.height / 2, -self.depth / 2],
            [self.width / 2, -self.height / 2, -self.depth / 2],
            [self.width / 2, -self.height / 2, self.depth / 2],
            [-self.width / 2, -self.height / 2, self.depth / 2],
            
            # Top face
            [-self.width / 2, self.height / 2, -self.depth / 2],
            [self.width / 2, self.height / 2, -self.depth / 2],
            [self.width / 2, self.height / 2, self.depth / 2],
            [-self.width / 2, self.height / 2, self.depth / 2],
        ], dtype=float)
    
    def check_boundary_collision(self, particle):
        for i in range(3):
            if particle.position_dynamic[i] - particle.radius < -self.bounds[i]:
                particle.position_dynamic[i] = -self.bounds[i] + particle.radius
                particle.velocity_dynamic[i] *= -self.restitution
            elif particle.position_dynamic[i] + particle.radius > self.bounds[i]:
                particle.position_dynamic[i] = self.bounds[i] - particle.radius
                particle.velocity_dynamic[i] *= -self.restitution