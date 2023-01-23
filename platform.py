import math

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
    "fall-through": False,  # you can jump on it from below and crouch to fall through, disable "solid" first
    "durability": {
        "on": False,  # allow
        "reset": 60,  # how long is fallen (-1 is infinite) TODO
        "durability": 60,  # how long can you stand on it (-1 is infinite) TODO
        "regeneration": True,
    },
    "moving": {
        "on": False,
        "path": [(0, 0), (50, 50), (500, 100), (200, 0), (50, 50)],
        "function": "sin",  # defines how it moves (linear, sin)
        "speed": 60,  # how many frames it takes to get from one point to another
        "one-way": True,  # if true: platform teleports to the starting location after completing path
        "wait": 20,  # waits for x frames on each point
        "sticky": True,  # if entities stick to the moving platform
        "cycles": "none"  # how to repeat path (rotation, reset, reset-smooth)
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
        self.time = 0
        self.durability_data = {
            "durability": 0,
            "reset": 0,
        }
        self.first_collision = True
        self.init()

    def init(self):
        if self.get_nested_attrib("moving", "cycles") == "rotation":
            path = self.get_nested_attrib("moving", "path")
            i = len(path) - 2
            while i >= 0:
                path.append(path[i])
                i -= 1
        elif self.get_nested_attrib("moving", "cycles") == "reset-smooth":
            path = self.get_nested_attrib("moving", "path")
            path.append(path[0])

    def update(self, entities):
        if self.get_nested_attrib("moving", "on"):
            path = self.get_nested_attrib("moving", "path")
            speed = self.get_nested_attrib("moving", "speed")
            wait = self.get_nested_attrib("moving", "wait")
            segment = self.get_moving_segment(path, speed, wait)
            fraction = self.get_moving_fraction(speed, wait, reversed=segment[1])
            self.move(entities, self.get_new_pos(segment[0], fraction, path))
        self.time += 1

    def get_moving_segment(self, path, speed, wait):
        cycles = self.get_nested_attrib("moving", "cycles")
        seg = math.floor(self.time / (speed + wait))
        return seg % (len(path) - 1), False
        # if cycles == "reset":
        #     seg = math.floor(self.time / (speed + wait))
        #     return seg % (len(path) - 1), False
        # if cycles == "rotation":  # TODO: not working xd
        #     seg = math.floor(self.time / (speed + wait))
        #     seg = seg % (len(path) * 2 - 2)
        #     if seg < len(path):
        #         return seg, False
        #     return len(path) * 2 - seg - len(path), True

    def get_moving_fraction(self, speed, wait, reversed= False):
        if self.time % (speed + wait) < wait:
            return 0
        speed = speed + wait
        constant = (self.time % speed - wait) / (speed - wait)
        function = self.get_nested_attrib("moving", "function")
        result = 0
        if function == "linear":
            result = constant
        if function == "sin":
            result = math.sin(0.5 * math.pi * constant)
        return 1 - result if reversed else result

    def get_new_pos(self, segment, fraction, path):
        if segment == len(path) - 1 and self.get_nested_attrib("moving", "one-way"):
            return path[segment][0], path[segment][1]
        x1 = path[segment][0]
        y1 = path[segment][1]
        x2 = path[segment + 1][0]
        y2 = path[segment + 1][1]
        return (x2 - x1) * fraction + x1, (y2 - y1) * fraction + y1

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
        solid = self.trigger_durability(on_top)
        if entity.x - self.w < self.x < entity.x + entity.w and entity.y - self.h < self.y < entity.y + entity.h:
            if not self.get_attrib("fall-through") and on_top and not input.key_down(entity.keyset["down"]) and solid:
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
