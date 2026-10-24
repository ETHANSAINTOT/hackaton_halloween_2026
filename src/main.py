##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton-haloween - src/main.py
## File description:
## Open the main window
##

import pygame
import os

WIDTH = 1280
HEIGHT = 720
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hackaton Halloween 2026")
    background = pygame.image.load(os.path.join(ASSETS_DIR, "background.jpg")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
