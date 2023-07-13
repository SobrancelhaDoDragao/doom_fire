"""
Estudando o algoritmo Doom fire

Desempenho inicial: 30 fps de media
Desempenho com numpay + numba: 50 fps de media
"""
import pygame as pg
import numpy as np
from pygame import gfxdraw
from random import randint
from numba import njit

class DoomFire:

    STEPS_BETWEEN_COLORS = 6
    COLORS = ['black','red','orange','yellow','white']
    PIXEL_SIZE = 5
  
    def __init__(self,app):
        self.app = app

        self.FIRE_WIDTH = self.app.WIDTH // self.PIXEL_SIZE
        self.FIRE_HEIGHT = self.app.HEIGHT  // self.PIXEL_SIZE

        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()

    @staticmethod
    @njit(fastmath=True)
    def do_fire(array,fire_width,fire_height):
        """
        Atualiza o fire_array com novas cores do frame atual
        """
        for x in range(fire_width):
            for y in range(1, fire_height):
                color_index = array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    array[y - 1][(x - rnd + 1) % fire_width] = color_index - rnd % 2
                else:
                    array[y - 1][x] = 0
        return array
    
    @staticmethod
    @njit()
    def calc_fire(array):
        """
        Função geradora que foi isolada para poder acelerar com numba
        """
        for y, row in enumerate(array):
            for x, color_index in enumerate(row):
                if color_index:
                    yield x,y,color_index

    def draw_fire(self):
        """
        Função que pinta a tela de acordo com os valores do fire array.
        """
        for (x,y,color_index) in self.calc_fire(self.fire_array):  
            gfxdraw.box(self.app.screen, (x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE), self.palette[color_index])
          
    def get_fire_array(self):
        """
        Retorna um array com os indices das cores. Atenção não retorna as cores no formato rgb
        retorna uma lista com indexes dos valores da palleta 'COLORS'
        """
        fire_array = [[0 for i in range(self.FIRE_WIDTH)] for j in range(self.FIRE_HEIGHT)]
        for i in range(self.FIRE_WIDTH):
            fire_array[self.FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return np.array(fire_array)
        
    def draw_pallete(self):
        size = 50
        for i, color in enumerate(self.palette):
            pg.draw.rect(self.app.screen, color, (i * size, self.app.HEIGHT // 2, size -5, size - 5))

    def get_palette(self):
        """
        Gera um gradiente de cores de acordo com as cores escolhida na palleta
        """
        pallete = [(0,0,0)]
        for i, color in enumerate(self.COLORS[:-1]):
            c1,c2 = color, self.COLORS[i+1]
            for step in range(self.STEPS_BETWEEN_COLORS):
                c = pg.Color(c1).lerp(c2,(step + 0.5) / self.STEPS_BETWEEN_COLORS)
                pallete.append(c)
        return pallete

    def update(self):
        self.fire_array = self.do_fire(self.fire_array,self.FIRE_WIDTH,self.FIRE_HEIGHT)
    
    def draw(self):
        #self.draw_pallete()
        self.draw_fire()


