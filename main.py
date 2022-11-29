import pygame as pg
import input
import player
import platform


def main():
    pg.init()
    pg.display.set_caption("program")
    ctx = pg.display.set_mode((900, 900))
    clock = pg.time.Clock()
    running = True
    plr = player.Player()
    plt = platform.Platform(600, 600, 100, 100)
    plt1 = platform.Platform(500, 600, 100, 10, {"color": (200, 0, 0), "solid": False, "durability":{"on": True}})
    while running:
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
        plr.move()
        plr.world_interaction()
        plt.collision(plr)
        plt1.collision(plr)
        plt.draw(ctx)
        plt1.draw(ctx)
        plr.draw(ctx)

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
