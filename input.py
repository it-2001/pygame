import pygame as pg


class Key:
    def __init__(self, code):
        self.hold = -1
        self.code = code

    def reset(self):
        self.hold = -1

    def update(self):
        if self.hold > -1:
            self.hold += 1


keys = {
    "up": Key(pg.K_w),  # 1073741906
    "left": Key(pg.K_a),  # 1073741904
    "down": Key(pg.K_s),  # 1073741905
    "right": Key(pg.K_d),  # 1073741903
}


class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.lastx = 0
        self.lasty = 0
        self.hold = -1
        self.consumed = False

    def update(self):
        position = pg.mouse.get_pos()
        if self.hold > -1:
            self.hold += 1
        self.lastx = self.x
        self.lasty = self.y
        self.x = position[0]
        self.y = position[1]
        if not pg.mouse.get_pressed()[0]:
            self.hold = -1
        elif self.hold == -1:
            self.hold = 0
        self.consumed = False


mouse = Mouse()


def handle_keys(code, down=True):
    value = -1
    if down:
        value = 0
    for key in keys:
        if code == keys[key].code:
            keys[key].hold = value


def update():
    for key in keys:
        keys[key].update()


def key_down(code):
    return keys[code].hold != -1