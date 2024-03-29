import pygame as pg
import input
import player
import platform
import button


def main():
    pg.init()
    pg.display.set_caption("program")
    ctx = pg.display.set_mode((900, 900))
    clock = pg.time.Clock()
    running = True
    construction = None
    plr = player.Player({"down":"down", "up":"up", "right":"right", "left":"left"})
    plr2 = player.Player({"down":"down1", "up":"up1", "right":"right1", "left":"left1"})
    platforms = [platform.Platform(600, 600, 100, 100, {"moving": {"sticky": True, "on": True, "cycles":"rotation"}}),
                 platform.Platform(500, 600, 100, 10,
                                   {"color": (200, 0, 0), "solid": False, "durability": {"on": True, "regeneration": 1},
                                    "moving": {"sticky": True}}),
                 platform.Platform(0, 0, 100, 10,
                                   {"color": (200, 0, 0), "solid": True,
                                    "moving": {"on": True, "sticky": True, "path": [(50, 200), (600, 200)], "cycles":"rotation", "function":"sin", "wait": 0, "speed": 300}})
                 ]
    def printsmth():
        print("you clicked on button")
    buttons = [button.Button(50, 50, 100, 50, {"colors": {"normal":(60, 30, 90)}}, onclick=printsmth)]
    while running:
        input.mouse.update()
        if input.mouse.hold > -1:
            if construction is None:
                construction = (input.mouse.x, input.mouse.y, 0, 0)
            else:
                construction = (
                construction[0], construction[1], input.mouse.x - construction[0], input.mouse.y - construction[1])
        else:
            if construction is not None:
                x = construction[0] if construction[2] >= 0 else construction[0] + construction[2]
                y = construction[1] if construction[3] >= 0 else construction[1] + construction[3]
                w = construction[2] if construction[2] >= 0 else construction[2] * -1
                h = construction[3] if construction[3] >= 0 else construction[3] * -1
                platforms.append(platform.Platform(x, y, w, h, {}))
                construction = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                input.handle_keys(event.key, True)
            if event.type == pg.KEYUP:
                input.handle_keys(event.key, False)
        input.update()
        ctx.fill((0, 0, 0))
        plr.input()
        plr.world_interaction()

        plr.move()
        plr2.input()
        plr2.world_interaction()

        plr2.move()

        for butt in buttons:
            if butt.draw(ctx, input.mouse):
                break
        for plt in platforms:
            plt.update([plr, plr2])
            plt.collision(plr)
            plt.collision(plr2)
        for plt in platforms:
            plt.draw(ctx)

        plr.draw(ctx)
        plr2.draw(ctx)

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
