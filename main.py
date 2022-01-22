import os
import sys

import pygame


def main():
    pygame.init()
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Крест")

    # картинки для стартового фона
    my_image = pygame.image.load("logo.png").convert_alpha()  # размер 500 на 412
    my_image_2 = pygame.image.load("start.png").convert_alpha()

    # картинки для выбора уровней
    my_image_levels = pygame.image.load("levels.png").convert_alpha()

    # стартовый фон
    surf_start = pygame.Surface((1000, 700))
    surf_start.fill((255, 255, 255))

    surf_start.blit(my_image, (240, 100))
    surf_start.blit(my_image_2, (405, 500))


    # фон с уровнями
    surf_levels = pygame.Surface((1000, 700))
    surf_levels.fill((255, 255, 255))

    surf_levels.blit(my_image_levels, (100, 100))


    screen.fill((255, 255, 255))
    screen.blit(surf_start, (0, 0))


    running = True
    x, y = 314, 500

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if x < event.pos[0] < x + 270 and y < event.pos[1] < y + 50:
                     screen.blit(surf_levels, (0, 0))





        pygame.display.flip()


if __name__ == '__main__':
    main()
