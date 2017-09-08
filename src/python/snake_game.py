# coding=utf-8

"""
snake_game.py
"""

import os
import sys

import pygame as pg

import resources.food as fd
import resources.snake as snk
from resources.colors import (
    BLUE,
    BLUE_DARK,
    WHITE,
    BLACK,
)

__author__ = 'Adrian Antonana'

WIDTH = 25
HEIGHT = 25
SPEED = 8
SPEED_TICK = 2
SPEED_INC = 5
SHORT = 12
LONG = 1

wall_block = pg.Surface((snk.BLOCK_SIZE, snk.BLOCK_SIZE))
wall_block.set_alpha(255)
wall_block.fill(BLUE)
wall_block_dark = pg.Surface((snk.BLOCK_SIZE_INNER, snk.BLOCK_SIZE_INNER))
wall_block_dark.set_alpha(255)
wall_block_dark.fill(BLUE_DARK)


def in_limits(s):
    head_pos = s.get_head_pos()
    return not (head_pos[0] < 1
                or head_pos[1] < 1
                or head_pos[0] >= HEIGHT + 1
                or head_pos[1] >= WIDTH + 1)


def draw_walls(surface):
    for y in range(HEIGHT + 1):
        surface.blit(wall_block, (0, y * snk.BLOCK_SIZE))
        surface.blit(wall_block_dark, (5, y * snk.BLOCK_SIZE+5))
        surface.blit(wall_block, ((WIDTH + 1) * snk.BLOCK_SIZE, y *
                                  snk.BLOCK_SIZE))
        surface.blit(wall_block_dark, ((WIDTH + 1) * snk.BLOCK_SIZE + 5, y *
                                       snk.BLOCK_SIZE + 5))
    for x in range(WIDTH + 2):
        surface.blit(wall_block, (x * snk.BLOCK_SIZE, 0))
        surface.blit(wall_block_dark, (x*snk.BLOCK_SIZE+5, 5))
        surface.blit(wall_block, (x * snk.BLOCK_SIZE, (HEIGHT + 1) *
                                  snk.BLOCK_SIZE,))
        surface.blit(wall_block_dark, (x * snk.BLOCK_SIZE + 5, (HEIGHT + 1) *
                                       snk.BLOCK_SIZE + 5))

pg.init()
pg.mixer.init()
eat_sound = pg.mixer.Sound(os.path.abspath(os.path.join(__file__, '../..',
                                                        'snake_eat.wav')))
crash_sound = pg.mixer.Sound(os.path.abspath(os.path.join(__file__, '../..',
                                                          'snake_crash.wav')))
clock = pg.time.Clock()
screen = pg.display.set_mode(((WIDTH + 2) * snk.BLOCK_SIZE, (HEIGHT + 2) *
                              snk.BLOCK_SIZE))
pg.display.set_caption('snake')
font = pg.font.SysFont(pg.font.get_default_font(), 40)
game_over_text = font.render('GAME OVER', 1, WHITE)
start_text = font.render('PRESS ANY KEY TO START', 1, WHITE)
screen.fill(BLACK)

snake = snk.Snake(screen, WIDTH // 2, HEIGHT // 2)
food = fd.Food(screen, 1, HEIGHT + 1, 1, WIDTH + 1)

while food.get_pos() in snake.get_pos_list():
    food.__init__(screen, 1, HEIGHT + 1, 1, WIDTH + 1)

pg.event.set_blocked([pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN])

eaten = 0

draw_walls(screen)
screen.blit(start_text, ((WIDTH - 10) * snk.BLOCK_SIZE / 2, HEIGHT *
                         snk.BLOCK_SIZE / 2))
pg.display.flip()
waiting = True
while waiting:
    event = pg.event.wait()
    if event.type == pg.KEYDOWN:
        waiting = False
screen.fill(BLACK)

running = True
while running:
    if not in_limits(snake) or snake.crashed:
        running = False
        crash_sound.play()
    else:
        food.draw()
        snake.draw()
        draw_walls(screen)
        pg.display.flip()

        if food.get_pos() == snake.get_head_pos():
            eat_sound.play()
            snake.grow()

            food.__init__(screen, 1, HEIGHT + 1, 1, WIDTH + 1)
            while food.get_pos() in snake.get_pos_list():
                food.__init__(screen,  1, HEIGHT + 1, 1, WIDTH + 1)
            eaten += 1

            if eaten % SPEED_INC == 0:
                SPEED += SPEED_TICK

        clock.tick(SPEED)

        event = pg.event.poll()
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            act_mot_dir = snake.get_motion_dir()
            if event.key == pg.K_ESCAPE:
                sys.exit()
            elif event.key == pg.K_UP and act_mot_dir != snk.DOWN:
                snake.set_motion_dir(snk.UP)
            elif event.key == pg.K_DOWN and act_mot_dir != snk.UP:
                snake.set_motion_dir(snk.DOWN)
            elif event.key == pg.K_RIGHT and act_mot_dir != snk.LEFT:
                snake.set_motion_dir(snk.RIGHT)
            elif event.key == pg.K_LEFT and act_mot_dir != snk.RIGHT:
                snake.set_motion_dir(snk.LEFT)

        snake.remove()
        snake.move()

clock.tick(LONG)
snake.draw()
draw_walls(screen)
snake_pos_list = snake.get_pos_list()
black_block = snake.back_block
for pos in snake_pos_list[1:]:
    screen.blit(black_block, (pos[1] * snk.BLOCK_SIZE, pos[0] * snk.BLOCK_SIZE))
    pg.display.flip()
    clock.tick(SHORT)

while True:
    screen.blit(game_over_text, ((WIDTH - 4) * snk.BLOCK_SIZE / 2, HEIGHT *
                                 snk.BLOCK_SIZE / 2))
    pg.display.flip()
    event = pg.event.wait()
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            sys.exit()
