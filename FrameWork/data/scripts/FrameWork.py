import math
import os

import pygame
import json
import sys
import time
from pygame.locals import *

# Setup pygame/window ---------------------------------------- #
pygame.init()


# Import -----------------------------------------------------------  #

def load_img(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0, 0, 0))
    return img


class Animation:
    def __init__(self, frames, speed, mode):
        self.frames = frames
        self.frame = 0
        self.speed = speed
        self.playing = False
        self.mode = mode
        self.tbf = self.speed / len(self.frames)
        self.lastframetime = time.time()
        self.img = frames[0]

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def unpause(self):
        self.playing = True

    def restart(self):
        self.frame = 0
        self.playing = True

    def update(self):
        if self.playing:
            if self.lastframetime + self.tbf < time.time():
                self.lastframetime = time.time()
                self.frame += 1
                if self.frame > len(self.frames):
                    if self.mode == "loop":
                        self.frame = 1
            self.img = self.frames[self.frame - 1]

    def draw(self, surf, coords):
        surf.blit(self.img, coords)








class Entity:
    def collidecheck(self, rect, tiles):
        hitlist = []
        for tile in tiles:
            if rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist

    def __init__(self, x, y, width, height):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.touching = []
        self.isonground = False
        self.mode = "Idle"

    def move(self, motion, tiles):
        self.touching = []
        self.hitbox.x += motion[0]
        self.touching = self.collidecheck(self.hitbox, tiles)
        self.isonground = False

        self.mode = "Idle"
        if motion[0] != 0:
            if motion[0] > 0:
                self.mode = "RunRight"
            if motion[0] < 0:
                self.mode = "RunLeft"
        if motion[1] < 0:
            self.mode = "Up"

        for tile in self.touching:
            if motion[0] > 0:
                motion[0] = 0
                self.hitbox.right = tile.left
            if motion[0] < 0:
                motion[0] = 0
                self.hitbox.left = tile.right
        self.touching = []
        self.hitbox.y += motion[1]
        self.touching = self.collidecheck(self.hitbox, tiles)
        for tile in self.touching:
            if motion[1] > 0:
                motion[1] = 0
                self.hitbox.bottom = tile.top
                self.isonground = True

            if motion[1] < 0:
                motion[1] = 0
                self.hitbox.top = tile.bottom
        return motion


    def update(self):
        pass