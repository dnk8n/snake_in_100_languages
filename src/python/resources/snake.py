# coding=utf-8

"""
snake.py
"""

import pygame as pg

from resources.colors import (
    GREEN,
    GREEN_DARK,
    BLACK
)

__author__ = 'Adrian Antonana'

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

BLOCK_SIZE = 30
BLOCK_SIZE_INNER = 20


class Snake:
    def __init__(self, surface, head_pos_x=10, head_pos_y=10):
        self.surface = surface
        self.length = 10
        self.pos_list = [
            (head_pos_x, y) for y in reversed(
                range(head_pos_y - self.length + 1, head_pos_y + 1)
            )
        ]
        self.mot_dir = RIGHT
        self.crashed = False

        self.snake_block = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.snake_block.set_alpha(255)
        self.snake_block.fill(GREEN)
        self.snake_block_dark = pg.Surface((BLOCK_SIZE_INNER, BLOCK_SIZE_INNER))
        self.snake_block_dark.set_alpha(255)
        self.snake_block_dark.fill(GREEN_DARK)

        self.back_block = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.back_block.set_alpha(255)
        self.back_block.fill(BLACK)

    def get_head_pos(self):
        return self.pos_list[0]

    def get_motion_dir(self):
        return self.mot_dir

    def get_pos_list(self):
        return self.pos_list

    def set_motion_dir(self, mot_dir):
        self.mot_dir = mot_dir

    def inc_length(self):
        self.length += 1

    def move(self):
        mot_dir = self.get_motion_dir()
        head_pos = self.get_head_pos()

        if mot_dir == UP:
            pos_list = [(head_pos[0] - 1, head_pos[1])]
        elif mot_dir == DOWN:
            pos_list = [(head_pos[0] + 1, head_pos[1])]
        elif mot_dir == LEFT:
            pos_list = [(head_pos[0], head_pos[1] - 1)]
        elif mot_dir == RIGHT:
            pos_list = [(head_pos[0], head_pos[1] + 1)]
        else:
            pos_list = []

        pos_list.extend(self.pos_list[:-1])
        self.pos_list = pos_list

        if self.get_head_pos() in self.get_pos_list()[1:]:
            self.crashed = True

    def crashed(self):
        return self.crashed

    def grow(self):
        last_pos = self.get_pos_list()[-1]
        self.length += 1
        self.pos_list.append((last_pos[0]-1, last_pos[1]))

    def draw(self):
        for block_pos in self.get_pos_list():
            self.surface.blit(self.snake_block, (block_pos[1] * BLOCK_SIZE,
                                                 block_pos[0] * BLOCK_SIZE))
            self.surface.blit(
                self.snake_block_dark, (block_pos[1] * BLOCK_SIZE + 5,
                                        block_pos[0] * BLOCK_SIZE + 5)
            )

    def remove(self):
        for block_pos in self.get_pos_list():
            self.surface.blit(self.back_block, (block_pos[1] * BLOCK_SIZE,
                                                block_pos[0] * BLOCK_SIZE))
