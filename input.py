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
