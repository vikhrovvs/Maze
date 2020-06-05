import datetime
from itertools import product
from queue import Queue
from random import randint, choice

import pygame
from pygame import Surface

from .consts import *
from .maze import Maze


def relax_loop(screen: Surface):
    n, m = 24, 24
    maze = Maze(n, m)
    maze.create_random_maze()
    maze.walkthrough[0][0] = NOT_VISITED
    maze.walkthrough[n - 1][m - 1] = NOT_VISITED
    grid_size = screen.get_size()[0] // max(n, m)
    color = choice((LIGHT_BLUE, GREEN, YELLOW, PINK))
    x_start, y_start = randint(n / 4, 3 * n / 4), randint(n / 4, 3 * n / 4)
    maze.walkthrough[x_start][y_start] = VISITED
    queue = Queue()
    queue.put((x_start, y_start))
    while not queue.empty():
        x, y = queue.get()
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            wall = maze.get_wall_number(x, y, x + i, y + j)
            if wall is not None and not maze.walls[wall]:
                if not maze.walkthrough[x + i][y + j] == VISITED:
                    maze.walkthrough[x + i][y + j] = VISITED
                    queue.put((x + i, y + j))
                    draw_maze(screen, 0, 0, grid_size, maze, n, m, color)
                    pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    maze.create_random_maze()
                    return False
    relax_loop(screen)


def correct_size(maze_size: int):
    result = 6
    for size in POSSIBLE_SIZE:
        if maze_size >= size:
            result = size
    return result


def blit_text(screen: Surface, text: str):
    font = pygame.font.Font(None, 100)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        screen.blit(font.render(line, 1, YELLOW, LIGHT_BLUE), (120, 240 + 69 * i))


def get_result_text(score, time, hints, excess_turns):
    return 'Time:' + str(time) + '\nHints used: ' + str(hints) + '\nExcess turns: ' + str(
        excess_turns) + '\nScore: ' + str(score)


def draw_maze(screen: Surface, pos_x: int, pos_y: int, elem_size: int, maze: Maze, n: int, m: int,
              visited_color=LIGHT_BLUE):
    for y, x in product(range(m), range(n)):
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        color = WHITE
        if maze.walkthrough[x][y] == START:
            color = YELLOW
        if maze.walkthrough[x][y] == FINISH:
            color = RED
        if maze.walkthrough[x][y] == VISITED:
            color = visited_color
        if maze.walkthrough[x][y] == HINT:
            color = PINK
        pygame.draw.rect(screen, color, position)
        if maze.get_wall_number(x, y, x, y - 1) is None or maze.walls[maze.get_wall_number(x, y, x, y - 1)]:
            position_top = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size / 10
            pygame.draw.rect(screen, BLACK, position_top)
        if maze.get_wall_number(x, y, x - 1, y) is None or maze.walls[maze.get_wall_number(x, y, x - 1, y)]:
            position_left = pos_x + x * elem_size, pos_y + y * elem_size, elem_size / 10, elem_size
            pygame.draw.rect(screen, BLACK, position_left)
        if y == m - 1:
            position_bottom = pos_x + x * elem_size, pos_y + y * elem_size + elem_size * 9 / 10, elem_size, elem_size / 10
            pygame.draw.rect(screen, BLACK, position_bottom)
        if x == n - 1:
            position_right = pos_x + x * elem_size + elem_size * 9 / 10, pos_y + y * elem_size, elem_size / 10, elem_size
            pygame.draw.rect(screen, BLACK, position_right)


def game_loop(screen: Surface):
    n, m = 8, 8
    maze = Maze(n, m)
    maze.create_random_maze()
    start_time = datetime.datetime.now()
    read_n = False
    read_m = False
    new_n = 0
    new_m = 0
    show_highscore = False
    finished = False
    grid_size = screen.get_size()[0] // max(n, m)
    screen.fill(WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if not finished:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    x, y = [p // grid_size for p in event.pos]
                    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        wall = maze.get_wall_number(x, y, x + i, y + j)
                        if wall is not None and not maze.walls[wall] and maze.walkthrough[x + i][y + j] > 0:
                            if maze.walkthrough[x][y] in (NOT_VISITED, HINT):
                                maze.turns += 1
                                maze.walkthrough[x][y] = VISITED
                            if maze.walkthrough[x][y] == FINISH:
                                finished = True
                                time = datetime.datetime.now() - start_time
                                excess_turns = maze.turns - len(maze.path)
                                score = 4 * len(maze.path) - int(time.total_seconds()) - 10 * maze.hints - excess_turns
                                leaderboard_filename = 'leaderboard' + str(n) + 'x' + str(m)
                                leaderboard = open('./leaderboard/' + leaderboard_filename, 'a')
                                leaderboard.write(str(score) + ', ' + str(time) + ', ' + str(maze.hints) + ', ' + str(
                                    excess_turns) + '\n')
                                leaderboard.close()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    x, y = [p // grid_size for p in event.pos]
                    if maze.walkthrough[x][y] == VISITED:
                        neighbours = 0
                        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            wall = maze.get_wall_number(x, y, x + i, y + j)
                            if wall is not None and not maze.walls[wall] and maze.walkthrough[x + i][y + j] > 0:
                                neighbours += 1
                        if neighbours == 1:
                            maze.turns -= 1
                            maze.walkthrough[x][y] = NOT_VISITED
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        maze.get_next_move()

            # finished == false section end
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restart
                    finished = False
                    start_time = datetime.datetime.now()
                    maze.create_random_maze()
                if event.key == pygame.K_s:  # set size
                    read_n = True
                    new_n = 0
                if pygame.K_0 <= event.key <= pygame.K_9:
                    if read_n:
                        new_n = new_n * 10 + event.key - pygame.K_0
                    if read_m:
                        new_m = new_m * 10 + event.key - pygame.K_0
                if event.key == pygame.K_RETURN:
                    if read_n:
                        read_n = False
                        read_m = True
                        new_m = 0
                    elif read_m:
                        n, m = correct_size(new_n), correct_size(new_m)
                        maze = Maze(n, m)
                        read_m = False
                        finished = False
                        start_time = datetime.datetime.now()
                        maze.create_random_maze()
                        grid_size = screen.get_size()[0] // max(n, m)
                        screen.fill(WHITE)
                        draw_maze(screen, 0, 0, grid_size, maze, n, m)
                if event.key == pygame.K_x:  # relax
                    if relax_loop(screen):  # if ended with QUIT
                        return
                    finished = False
                    start_time = datetime.datetime.now()
                    maze.create_random_maze()
                if event.key == pygame.K_l:  # show best result
                    show_highscore ^= 1
                    if finished and show_highscore:
                        highscore = 0
                        leaderboard_filename = 'leaderboard' + str(n) + 'x' + str(m)
                        leaderboard = open('./leaderboard/' + leaderboard_filename, 'r')
                        for line in leaderboard:
                            l_score, l_time, l_hints, l_excess_turns = line.split(',')
                            if int(l_score) > int(highscore):
                                highscore = l_score
                                h_time, h_hints, h_excess_turns = l_time, l_hints, l_excess_turns
                        leaderboard.close()
                        draw_maze(screen, 0, 0, grid_size, maze, n, m)
                        blit_text(screen,
                                  'Highscore for ' + str(n) + 'x' + str(m) + ':\n' + get_result_text(highscore, h_time,
                                                                                        h_hints, int(h_excess_turns)))
                        pygame.display.flip()

        draw_maze(screen, 0, 0, grid_size, maze, n, m)
        if finished and not show_highscore:
            blit_text(screen, get_result_text(score, time, maze.hints, excess_turns))
        if not show_highscore:
            pygame.display.flip()
