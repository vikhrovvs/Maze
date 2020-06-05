import pygame
from src.gui import game_loop

if __name__ == '__main__':
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode([960, 960])
    game_loop(screen)
    pygame.quit()
