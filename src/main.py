##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton-haloween - src/main.py
## File description:
## Open the main window
##

import pygame

from constants import WIDTH, HEIGHT, BUTTONS
from constants import TITLE, TITLE_FONT, TITLE_SIZE, TITLE_Y
from constants import TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE
from ui import load_background, render_outlined_text, load_button, get_clicked_button
from rules import run_rules


def load_title():
    font = pygame.font.Font(TITLE_FONT, TITLE_SIZE)
    title = render_outlined_text(font, TITLE, TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE)
    rect = title.get_rect(midtop=(WIDTH // 2, TITLE_Y))
    return title, rect


def load_buttons():
    return [load_button(*button) for button in BUTTONS]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    background = load_background()
    title, title_rect = load_title()
    buttons = load_buttons()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                name = get_clicked_button(buttons, event.pos)
                if name:
                    print(f"button {name} clicked")
                if name == "quit":
                    running = False
                elif name == "rules":
                    running = run_rules(screen)
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)
        for name, image, rect, mask in buttons:
            screen.blit(image, rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
