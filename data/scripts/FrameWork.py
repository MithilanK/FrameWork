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


LOOP = 0
ONCE = 1


class Anim:
    def __init__(self, frames, mode=LOOP):
        self.frames = frames
        self.playmode = mode


class AnimCursor:
    def __init__(self):
        self.anim = None
        self.frame_num = 0
        self.current = None
        self.next = None
        self.played = []
        self.transition = 0.0
        self.playing = False
        self.playtime = 0.0

        self.frame_time = 0.0
        self.timeleft = 0.0
        self.playspeed = 1.0

    def use_anim(self, anim):
        self.anim = anim
        self.reset()

    def reset(self):
        self.current = self.anim.frames[0][0]
        self.timeleft = self.anim.frames[0][1]
        self.frame_time = self.timeleft
        self.next_frame = (self.frame_num + 1) % len(self.anim.frames)
        self.next = self.anim.frames[self.next_frame][0]
        self.frame_num = 0
        self.playtime = 0.0
        self.transition = 0.0

    def play(self, playspeed=1.0):
        self.playspeed = playspeed
        self.reset()
        self.unpause()

    def pause(self):
        self.playing = False

    def unpause(self):
        self.playing = True

    def update(self, td):
        td = td * self.playspeed
        self.played = []
        if self.playing:
            self.playtime += td
            self.timeleft -= td
            self.transition = self.timeleft / self.frame_time

            while self.timeleft:
                self.frame_num = (self.frame_num + 1) % len(self.anim.frames)
                if self.anim.playmode == ONCE and self.frame_num == 0:
                    self.pause()
                    return

                next_frame = (self.frame_num + 1) % len(self.anim.frames)

                frame, time = self.anim.frames[self.frame_num]
                self.frame_time = time
                self.timeleft += time
                self.current = frame
                self.next = self.anim.frames[next_frame][0]
                self.played.append(frame)
                self.transition = self.timeleft / time

                if self.frame_num == 0:
                    self.playtime = self.timeleft


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