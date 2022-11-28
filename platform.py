import pygame as pg
import input

specification = {
    "visible": True,
    "solid": True,
    "texture": None,
    "color": (160, 160, 0),
    "fall-through": False
}
CALC_ACCURACY = 1.2


class Platform:
    def __init__(self, x, y, w, h, data={}):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.data = data

    def get_attrib(self, attrib):
        if attrib in self.data:
            return self.data[attrib]
        return specification[attrib]

    def draw(self, ctx):
        if self.get_attrib("visible"):
            pg.draw.rect(ctx, self.get_attrib("color"), (self.x, self.y, self.w, self.h))

    def collision(self, entity):
        if entity.x - self.w < self.x < entity.x + entity.w and entity.y - self.w < self.y < entity.y + entity.h:
            if not self.get_attrib("fall-through") and entity.ys >= 0 and not input.key_down("down") and self.y < entity.y + entity.h < self.y + entity.ys * CALC_ACCURACY:
                entity.ys = 0
                entity.y = self.y - entity.h
                entity.on_ground()
            if self.get_attrib("solid"):
                if entity.xs > 0 and self.x < entity.x + entity.w < self.x + entity.xs * CALC_ACCURACY:
                    entity.x = self.x - entity.w
                if entity.ys > 0 and self.y < entity.y + entity.h < self.y + entity.ys * CALC_ACCURACY:
                    entity.ys = 0
                    entity.y = self.y - entity.h
                if entity.x < self.x + self.w < entity.x - entity.xs * CALC_ACCURACY:
                    entity.x = self.x + self.w
                if entity.y < self.y + self.h < entity.y - entity.ys * CALC_ACCURACY:
                    entity.ys = 0
                    entity.y = self.y + self.h
