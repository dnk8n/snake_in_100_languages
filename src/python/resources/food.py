# coding=utf-8

"""
food.py
"""

import random as rnd

import pygame as pg

from resources.colors import (
    RED,
    RED_DARK
)

__author__ = 'Adrian Antonana'

BLOCK_SIZE = 30
BLOCK_SIZE_INNER = 20


class Food:
    def __init__(self, surface, min_x, max_x, min_y, max_y):
        self.surface = surface
        self.pos_x = rnd.randint(min_x, max_x-1)
        self.pos_y = rnd.randint(min_y, max_y-1)

        self.food_block = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.food_block.set_alpha(255)
        self.food_block.fill(RED)
        self.food_block_dark = pg.Surface((BLOCK_SIZE_INNER, BLOCK_SIZE_INNER))
        self.food_block_dark.set_alpha(255)
        self.food_block_dark.fill(RED_DARK)

    def get_pos(self):
        return self.pos_x, self.pos_y

    def draw(self):
        food_pos = self.get_pos()
        self.surface.blit(self.food_block, (food_pos[1] * BLOCK_SIZE,
                                            food_pos[0] * BLOCK_SIZE))
        self.surface.blit(self.food_block_dark, (food_pos[1] * BLOCK_SIZE + 5,
                                                 food_pos[0] * BLOCK_SIZE + 5))
