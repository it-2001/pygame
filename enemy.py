import pygame as pg


specification = {
    "visible": True,
    "solid": True,
    "thorns": {
        "on": True,
        "knock-back": 5,
        "dmg": 1,
    },
    "texture": None,
    "color": (160, 160, 0),
    "damaged-color": (100, 100, 0),
    "ai": {
        "type": "vacuum-cleaner",  # vacuum-cleaner(bounces if collides with walls)
        # follow (follows player on land)
        # follow-blind (follows player if in proximity)
        # marksman (tries to stay in safe distance from player)
        # coward (runs away to the safe distance on hit)
        # ghost-follow (floats in the air towards player, ignoring collisions)
        # ghost (floats in the air, ignoring collisions)
        # float (floats in the air, collisions work)
        # float-follow (floats in the air towards player, collisions work)
        "safe-distance": 300,
        "speed": 5,
    },
    # note that some attributes are ignored for certain combat type
    "combat": {
        "type": "normal",  # normal (strikes an enemy in proximity)
        # none (enemy is unable to attack)
        # archer (enemy shoots arrows)
        "cooldown": 130,
        "dmg": 1,
        "knock-back": 5,
        "cast-time": 10,
        "accuracy": 5
    }
}


class Enemy:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.data = data
        if data is None:
            self.data = {}
        self.time = 0

    def draw(self, ctx):
        if self.get_attrib("visible"):
            return pg.draw.rect(ctx, self.get_color(), (self.x, self.y, self.w, self.h))
        return False

    def get_color(self):
        return self.get_attrib("color")

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

    def collision(self, entity):
        on_top = self.on_top(entity)
        solid = self.trigger_durability(on_top)
        if entity.x - self.w < self.x < entity.x + entity.w and entity.y - self.h < self.y < entity.y + entity.h:
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

    def on_top(self, entity):
        return entity.last_y + entity.h <= self.y <= entity.y + entity.h and self.x <= entity.x + entity.w <= self.x + self.w + entity.w

    def fully_on_top(self, entity):
        return entity.last_y + entity.h <= self.y <= entity.y + entity.h and self.x < entity.x < self.x + self.w - entity.w

    def move(self):
        self.last_x = self.x
        self.last_y = self.y
        self.x += self.xs
        self.y += self.ys