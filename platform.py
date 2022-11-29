import pygame as pg
import input

specification = {
    "visible": True,
    "solid": True,
    "texture": None,
    "color": (160, 160, 0),
    "damaged-color": (100, 100, 0),
    "fallen-color": (50, 50, 0),
    "fall-through": False,  # you can jump on it from below and crouch to fall through
    "durability": {
        "on": False,  # allow
        "reset": 60,  # how long is fallen (-1 is infinite)
        "durability": 60,  # how long can you stand on it (-1 is infinite)
    }
}
CALC_ACCURACY = 1.2


class Platform:
    def __init__(self, x, y, w, h, data={}):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.data = data
        self.durability_data = {
            "durability": 0,
            "reset": 0,
        }

    def get_attrib(self, attrib):
        if attrib in self.data:
            return self.data[attrib]
        return specification[attrib]

    def get_nested_attrib(self, location, attribute):
        if location not in self.data:
            return specification[location][attribute]
        if attribute in self.data[location]:
            return self.data[location][attribute]
        return specification[location][attribute]

    def draw(self, ctx):
        if self.get_attrib("visible"):
            pg.draw.rect(ctx, self.get_color(), (self.x, self.y, self.w, self.h))

    def get_color(self):
        if self.durability_data["durability"] == self.get_nested_attrib("durability", "durability"):
            return self.get_attrib("fallen-color")
        elif self.durability_data["durability"] > 0:
            return self.get_attrib("damaged-color")
        return self.get_attrib("color")

    def trigger_durability(self, player_on=False):
        print(self.durability_data)
        if not self.get_nested_attrib("durability", "on"):
            return True
        if self.durability_data["durability"] >= self.get_nested_attrib("durability", "durability"):
            self.durability_data["reset"] += 1
            if self.durability_data["reset"] >= self.get_nested_attrib("durability", "reset"):
                self.durability_data["reset"] = 0
                self.durability_data["durability"] = 0
            return False
        elif player_on:
            self.durability_data["durability"] += 1
            return True
        elif self.durability_data["durability"] > 0:
            self.durability_data["durability"] -= 1
        return False

    def collision(self, entity):
        if entity.x - self.w < self.x < entity.x + entity.w and entity.y - self.w < self.y < entity.y + entity.h:
            solid = self.trigger_durability(True)
            if not self.get_attrib("fall-through") and entity.ys >= 0 and not input.key_down("down") and self.y <= entity.y + entity.h <= self.y + entity.ys * CALC_ACCURACY and solid:
                entity.ys = 0
                entity.y = self.y - entity.h
                entity.on_ground()
            if self.get_attrib("solid") and solid:
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
            return
        else:
            self.trigger_durability(False)

