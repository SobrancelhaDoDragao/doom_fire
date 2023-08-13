"""
Arquivo principal, aqui fica a classe jogo
"""
import sys

import pygame as pg

from fire import DoomFire


class Game:
    WIDTH, HEIGHT = 600, 600
    WIN_SIZE = WIDTH, HEIGHT
    FPS = 60

    def __init__(self):
        self.screen = pg.display.set_mode(size=self.WIN_SIZE)
        self.clock = pg.time.Clock()
        self.doom_fire = DoomFire(self)

    def update(self):
        self.doom_fire.update()
        self.clock.tick(self.FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.screen.fill("black")
        self.doom_fire.draw()
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = Game()
    app.run()
