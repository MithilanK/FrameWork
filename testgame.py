import sys
import time

import pygame
from pygame.locals import *

from data.scripts.FrameWork import *


def testgame():
    pygame.display.set_caption('game base')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500), 0, 32)
    player = Entity(50, 50, 75, 75)
    tiles = [pygame.Rect(0, 400, 500, 100), pygame.Rect(0, 200, 400, 100)]
    framerate = 60

    last_time = time.time()
    vel = [0, 0]
    # Loop ------------------------------------------------------- #
    while True:

        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # PlayerUpdate ------------------------------------------- #
        keys = pygame.key.get_pressed()
        vel[1] += 0.2 * dt
        if keys[K_w] & player.isonground:
            vel[1] = -8 * dt
        vel[0] = int(keys[K_d]) - int(keys[K_a])
        vel[0] *= 6 * dt
        vel = player.move(vel, tiles)

        # Background --------------------------------------------- #
        screen.fill((0, 0, 0))

        # Buttons ------------------------------------------------ #
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.draw.rect(screen, (255, 255, 255), player.hitbox)
        for tile in tiles:
            pygame.draw.rect(screen, (255, 255, 0), tile)
        # Update ------------------------------------------------- #
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    testgame()