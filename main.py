import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    # init pygame
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # sprite groupds
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # add constraints
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    asteroidField = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # main game loop
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
        # Asteroid vs Asteroid Physics
        asteroid_list = list(asteroids)
        for i in range(len(asteroid_list)):
            for j in range(i + 1, len(asteroid_list)):
                a1 = asteroid_list[i]
                a2 = asteroid_list[j]

                if a1.collides_with(a2):
                    # Calculate the distance vector
                    direction = a1.position - a2.position

                    # Handle the "Zero Length" case (happens on split)
                    if direction.length() == 0:
                        import random
                        # Create a random unit vector for direction
                        direction = pygame.Vector2(
                            0, 1).rotate(random.uniform(0, 360))
                        # Nudge them apart slightly so they aren't on the same pixel
                        a1.position += direction * 0.5
                        a2.position -= direction * 0.5

                    log_event("asteroid_collision")

                    # 1. Use our safe direction vector to get the normal
                    normal = direction.normalize()

                    # 2. Resolve Overlap (The "Nudge")
                    # This prevents asteroids from overlapping/getting stuck
                    distance = a1.position.distance_to(a2.position)
                    overlap = (a1.radius + a2.radius) - distance

                    if distance > 0:
                        a1.position += normal * (overlap / 2)
                        a2.position -= normal * (overlap / 2)

                    # 3. Elastic Velocity Swap
                    # Project velocities onto the normal vector
                    relative_velocity = a1.velocity - a2.velocity
                    velocity_along_normal = relative_velocity.dot(normal)

                    # Only resolve if they are moving towards each other
                    if velocity_along_normal < 0:
                        # Calculate impulse (assuming equal mass)
                        impulse = velocity_along_normal * normal
                        a1.velocity -= impulse
                        a2.velocity += impulse

        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
