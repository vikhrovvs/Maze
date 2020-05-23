from itertools import product

import pygame
from pygame import Surface

import datetime

from src.maze import Maze
from src.consts import *

def blit_text(screen: Surface, text: str):
    font = pygame.font.Font(None, 100)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        screen.blit(font.render(line, 1, YELLOW, LIGHT_BLUE), (120, 240 + 69*i))


def draw_maze(screen: Surface, pos_x: int, pos_y: int, elem_size: int, maze: Maze):
    for y, x in product(range(8), range(8)):
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        color = WHITE
        if maze.walkthrough[x][y] == START:
            color = PINK
        if maze.walkthrough[x][y] == FINISH:
            color = GREEN
        if maze.walkthrough[x][y] == VISITED:
            color = RED
        if maze.walkthrough[x][y] == HINT:
            color = LIGHT_BLUE
        pygame.draw.rect(screen, color, position)
        if maze.get_wall_number(x, y, x, y - 1) is None or maze.walls[maze.get_wall_number(x, y, x, y - 1)]:
            position_top = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size / 10
            pygame.draw.rect(screen, BLACK, position_top)
        if maze.get_wall_number(x, y, x - 1, y) is None or maze.walls[maze.get_wall_number(x, y, x - 1, y)]:
            position_left = pos_x + x * elem_size, pos_y + y * elem_size, elem_size/10, elem_size
            pygame.draw.rect(screen, BLACK, position_left)
        if y == 7:
            position_bottom = pos_x + x * elem_size, pos_y + y * elem_size + elem_size * 9 / 10, elem_size, elem_size / 10
            pygame.draw.rect(screen, BLACK, position_bottom)
        if x == 7:
            position_right = pos_x + x * elem_size + elem_size * 9 / 10, pos_y + y * elem_size, elem_size / 10, elem_size
            pygame.draw.rect(screen, BLACK, position_right)


def game_loop(screen: Surface, maze: Maze, finished: bool):
    grid_size = screen.get_size()[0] // 8

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return
            if finished == False:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    x, y = [p // grid_size for p in event.pos]
                    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        wall = maze.get_wall_number(x, y, x + i, y + j)
                        if wall is not None and maze.walls[wall] == False and maze.walkthrough[x + i][y + j] > 0:
                            if maze.walkthrough[x][y] in (NOT_VISITED, HINT):
                                maze.walkthrough[x][y] = VISITED
                            if maze.walkthrough[x][y] == FINISH:
                                finished = True
                                global start_time
                                time = datetime.datetime.now() - start_time

                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    x, y = [p // grid_size for p in event.pos]
                    if maze.walkthrough[x][y] == VISITED:
                        neighbours = 0
                        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            wall = maze.get_wall_number(x, y, x + i, y + j)
                            if wall is not None and maze.walls[wall] == False and maze.walkthrough[x + i][y + j] > 0:
                                neighbours += 1
                        if neighbours == 1:
                            maze.walkthrough[x][y] = NOT_VISITED
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        maze.get_next_move()

            ###finished == false section end
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    finished = False
                    start_time = datetime.datetime.now()
                    maze.create_random_maze()

        draw_maze(screen, 0, 0, grid_size, maze)
        if finished:
            blit_text(screen, str(time) + '\nHints used: ' + str(maze.hints))
        pygame.display.flip()





pygame.init()

screen: Surface = pygame.display.set_mode([720, 720])

finished = False
maze = Maze(8, 8)
maze.create_random_maze()
maze.solve()
start_time = datetime.datetime.now()
game_loop(screen, maze, finished)

pygame.quit()
