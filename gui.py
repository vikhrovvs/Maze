from itertools import product

import pygame
from pygame import Surface

import datetime

from src.maze import Maze

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (255, 255, 0)
PINK = (230, 50, 230)
RED = (255, 0, 0)

NOT_VISITED = 0
VISITED = 1
START = 2
FINISH = -1


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
                            if maze.walkthrough[x][y] == NOT_VISITED:
                                maze.walkthrough[x][y] = VISITED
                            if maze.walkthrough[x][y] == FINISH:
                                finished = True
                                time = datetime.datetime.now() - start_time
                                print(time)

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
                    if event.key == pygame.K_r:
                        maze.create_random_maze()
            #finished == false section end
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    finished = False
                    maze.create_random_maze()

        draw_maze(screen, 0, 0, grid_size, maze)
        if finished:
            font = pygame.font.Font(None, 100)
            text = font.render(str(time), 1, YELLOW, LIGHT_BLUE)
            screen.blit(text, (120, 360))
        pygame.display.flip()





pygame.init()

screen: Surface = pygame.display.set_mode([720, 720])

finished = False
maze = Maze(8, 8)
maze.create_random_maze()
start_time = datetime.datetime.now()
game_loop(screen, maze, finished)

pygame.quit()
