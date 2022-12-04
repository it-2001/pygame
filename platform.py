import pygame as pg
import input
from player import PLAYER_ACCELERATION

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
        "regeneration": True,
    },
    "moving": {
        "on": False,
        "path": [(0, 0), (50, 50)],
        "function": "linear",  # defines how it moves (linear, sin)
        "speed": 60,  # how many frames it takes to get from one point to another
        "one-way": False,  # if true: platform teleports to the starting location after completing path
        "wait": 10,  # waits for x frames on each point
        "sticky": False,  # if entities stick to the moving platform
    }
}
CALC_ACCURACY = 1 * PLAYER_ACCELERATION


class Platform:
    def __init__(self, x, y, w, h, data=None):
        if data is None:
            data = {}
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
        if self.durability_data["durability"] >= self.get_nested_attrib("durability", "durability"):
            return self.get_attrib("fallen-color")
        elif self.durability_data["durability"] > 0:
            return self.get_attrib("damaged-color")
        return self.get_attrib("color")

    def trigger_durability(self, player_on=False):
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
            self.durability_data["durability"] -= self.get_nested_attrib("durability", "regeneration")
        return False

    def durability_imut(self, player_on=False):
        if not self.get_nested_attrib("durability", "on"):
            return True
        if self.durability_data["durability"] >= self.get_nested_attrib("durability", "durability"):
            return False
        elif player_on:
            return True
        return False

    def move(self, entities, coords):
        if self.get_nested_attrib("moving", "sticky"):
            for entity in entities:
                print(entity.last_x)
                if self.on_top(entity):
                    entity.x = coords[0] + entity.x - self.x
                    entity.y = coords[1] + entity.y - self.y
        self.x = coords[0]
        self.y = coords[1]

    def on_top(self, entity):
        return entity.last_y + entity.h <= self.y <= entity.y + entity.h and self.x <= entity.x + entity.w <= self.x + self.w + entity.w

    def fully_on_top(self, entity):
        return entity.last_y + entity.h <= self.y <= entity.y + entity.h and self.x < entity.x < self.x + self.w - entity.w

    def collision(self, entity):
        on_top = self.on_top(entity)
        fully_on_top = self.fully_on_top(entity)
        solid = self.trigger_durability(fully_on_top)
        if entity.x - self.w < self.x < entity.x + entity.w and entity.y - self.h < self.y < entity.y + entity.h:
            if not self.get_attrib("fall-through") and on_top and not input.key_down("down") and solid:
                entity.ys = 0
                entity.y = self.y - entity.h
                entity.on_ground()
                return True
            if self.get_attrib("solid") and solid:
                if entity.x > entity.last_x and entity.last_x + entity.w <= self.x <= entity.x + entity.w:
                    entity.x = self.x - entity.w
                    if not on_top:
                        entity.xs = 0
                elif entity.x < entity.last_x and entity.x <= self.x + self.w <= entity.last_x:
                    entity.x = self.x + self.w
                    if not on_top:
                        entity.xs = 0
                elif entity.y > entity.last_y and entity.last_y + entity.h <= self.y <= entity.y + entity.h:
                    entity.ys = 0
                    entity.y = self.y - entity.h
                elif entity.y < entity.last_y and entity.y <= self.y + self.h <= entity.last_y:
                    entity.ys = 0
                    entity.y = self.y + self.h
                return True
        return False
