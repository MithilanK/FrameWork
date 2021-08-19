import sys
import time

import pygame
from pygame.locals import *

from data.scripts.FrameWork import *


def testgame():
    pygame.display.set_caption('game base')
    clock = pygame.time.Clock()
    main = pygame.Surface((100, 100))
    screen = pygame.display.set_mode((500, 500), 0, 32)
    player = Entity(50, 50, 16, 16)
    tiles = [pygame.Rect(0, 80, 100, 20), pygame.Rect(0, 40, 100, 20)]
    framerate = 60
    vel = [0, 0]
    playerrun = Animation([load_img("data/assets/player/run/img_0.png"),load_img("data/assets/player/run/img_1.png"),load_img("data/assets/player/run/img_2.png"),load_img("data/assets/player/run/img_3.png") ], 0.4, "loop")
    playerrun.play()
    last_time = time.time()

    # Loop ------------------------------------------------------- #
    while True:

        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # PlayerUpdate ------------------------------------------- #
        keys = pygame.key.get_pressed()
        vel[0] = (keys[K_d]) - (keys[K_a])
        vel[0] *= 2
        vel[1] += 0.5

        if keys[K_w] & player.isonground:
            vel[1] = -4
        vel = player.move(vel, tiles)

        # Background --------------------------------------------- #
        main.fill((0, 0, 0))

        # Buttons ------------------------------------------------ #
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #pygame.draw.rect(main, (255, 255, 255), player.hitbox)
        for tile in tiles:
            pygame.draw.rect(main, (255, 255, 0), tile)
        playerrun.update()

        if player.mode == "RunLeft":
            playerrun.update()
            playerrun.draw(main, (player.hitbox.x, player.hitbox.y))
        if player.mode == "RunRight":
            playerrun.update()
            main.blit(pygame.transform.flip(playerrun.img, True, False), (player.hitbox.x, player.hitbox.y))
        if player.mode == "Idle":
            playerrun.update()
            playerrun.draw(main, (player.hitbox.x, player.hitbox.y))


        print(player.mode)

        # Update ------------------------------------------------- #
        screen.blit(pygame.transform.scale(main, (500, 500)), (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    testgame()