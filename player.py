import pygame as pg
import input


SPEED_CAP = 12
PLAYER_ACCELERATION = 1.6
AIR_RESISTANCE = 0.98
SLIDE_SLOWDOWN = 0.85
GRAVITY = 0.9
JUMP_STRENGTH = 21
MAX_JUMPS = 2


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xs = 0
        self.ys = 0
        self.w = 20
        self.h = 40
        self.color = (0, 200, 20)
        self.jumps = MAX_JUMPS
        self.lock_jump = False

    def draw(self, ctx):
        pg.draw.rect(ctx, self.color, (self.x, self.y, self.w, self.h))

    def input(self):
        if input.key_down("left") and -SPEED_CAP < self.xs < SPEED_CAP:
            self.xs -= PLAYER_ACCELERATION
        if input.key_down("right") and -SPEED_CAP < self.xs < SPEED_CAP:
            self.xs += PLAYER_ACCELERATION
        if input.key_down("up") and self.jumps > 0 and not self.lock_jump:
            self.jumps -= 1
            self.ys = -JUMP_STRENGTH
            self.lock_jump = True
        if not input.key_down("up"):
            self.lock_jump = False

    def move(self):
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
            if not input.key_down("up"):
                self.lock_jump = False

    def on_ground(self):
        self.jumps = MAX_JUMPS
        self.lock_jump = False
