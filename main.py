import os
import sys

import pygame

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.init()
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Крест")

    # картинки для стартового фона
    my_image = pygame.image.load("logo.png").convert_alpha()  # размер 500 на 412
    my_image_2 = pygame.image.load("start.png").convert_alpha()

    # стартовый фон
    surf_start = pygame.Surface((1000, 700))
    surf_start.fill((255, 255, 255))

    surf_start.blit(my_image, (240, 100))
    surf_start.blit(my_image_2, (405, 500))

    screen.fill((255, 255, 255))
    screen.blit(surf_start, (0, 0))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if 314 < event.pos[0] < 314 + 270 and 500 < event.pos[1] < 500 + 50:
                    levels()

        pygame.display.flip()



def levels():
    my_image_levels = pygame.image.load("levels.png").convert_alpha()

    surf_levels = pygame.Surface((1000, 700))
    surf_levels.fill((255, 255, 255))

    surf_levels.blit(my_image_levels, (100, 100))
    #screen.blit(surf_levels, (0, 0)) ?

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 314 < event.pos[0] < 314 + 270 and 500 < event.pos[1] < 500 + 50:
                    print(1)

        pygame.display.flip()



if __name__ == '__main__':
    start_screen()
    levels()




# # картинки для выбора уровней
#     my_image_levels = pygame.image.load("levels.png").convert_alpha()
#
#     # фон с уровнями
#     surf_levels = pygame.Surface((1000, 700))
#     surf_levels.fill((255, 255, 255))
#
#     surf_levels.blit(my_image_levels, (100, 100))
#
