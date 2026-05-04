import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")

        # calculate new angles and velocities randomly
        angle = random.uniform(20, 50)
        velocityA = self.velocity.rotate(angle)
        velocityB = self.velocity.rotate(-angle)

        newRadius = self.radius - ASTEROID_MIN_RADIUS

        # create new asteroid objects and assign velocities
        asteroidA = Asteroid(self.position.x, self.position.y, newRadius)
        asteroidB = Asteroid(self.position.x, self.position.y, newRadius)

        asteroidA.velocity = velocityA * 1.2
        asteroidB.velocity = velocityB * 1.2


