import pygame as pg
import input


SPEED_CAP = 10
PLAYER_ACCELERATION = 1.4
AIR_RESISTANCE = 0.94
SLIDE_SLOWDOWN = 0.8
GRAVITY = 0.7
JUMP_STRENGTH = 16
MAX_JUMPS = 1


class Player:
    def __init__(self, keyset):
        self.x = 0
        self.y = 0
        self.xs = 0
        self.ys = 0
        self.w = 20
        self.h = 40
        self.keyset = keyset
        self.color = (0, 200, 20)
        self.jumps = MAX_JUMPS
        self.lock_jump = False
        self.last_x = self.x
        self.last_y = self.y

    def draw(self, ctx):
        pg.draw.rect(ctx, self.color, (self.x, self.y, self.w, self.h))

    def input(self):
        if input.key_down(self.keyset["left"]) and -SPEED_CAP < self.xs < SPEED_CAP:
            self.xs -= PLAYER_ACCELERATION
        if input.key_down(self.keyset["right"]) and -SPEED_CAP < self.xs < SPEED_CAP:
            self.xs += PLAYER_ACCELERATION
        if input.key_down(self.keyset["up"]) and self.jumps > 0 and not self.lock_jump:
            self.jumps -= 1
            self.ys = -JUMP_STRENGTH
            self.lock_jump = True
        if not input.key_down(self.keyset["up"]):
            self.lock_jump = False

    def move(self):
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.xs
        self.y += self.ys

    def world_interaction(self):
        self.ys += GRAVITY
        self.ys *= AIR_RESISTANCE
        self.xs *= SLIDE_SLOWDOWN
        if self.y > 900 - self.h:
            self.y = 900 - self.h
            self.ys = 0
            self.jumps = MAX_JUMPS
            if not input.key_down(self.keyset["up"]):
                self.lock_jump = False

    def on_ground(self):
        self.jumps = MAX_JUMPS
        self.lock_jump = False