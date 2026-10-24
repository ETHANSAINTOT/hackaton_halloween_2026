##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton-haloween - src/main.py
## File description:
## Open the main window
##

import pygame
import os

from constants import WIDTH, HEIGHT, ASSETS_DIR, BUTTONS
from constants import TITLE, TITLE_FONT, TITLE_SIZE, TITLE_Y
from constants import TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE


def load_title():
    font = pygame.font.Font(TITLE_FONT, TITLE_SIZE)
    text = font.render(TITLE, True, TITLE_COLOR)
    outline = font.render(TITLE, True, TITLE_OUTLINE_COLOR)
    o = TITLE_OUTLINE
    title = pygame.Surface((text.get_width() + 2 * o, text.get_height() + 2 * o), pygame.SRCALPHA)
    for dx in range(-o, o + 1):
        for dy in range(-o, o + 1):
            if dx * dx + dy * dy <= o * o:
                title.blit(outline, (o + dx, o + dy))
    title.blit(text, (o, o))
    # Crop the empty space around the letters so the centering is exact
    title = title.subsurface(title.get_bounding_rect()).copy()
    rect = title.get_rect(midtop=(WIDTH // 2, TITLE_Y))
    return title, rect


def load_buttons():
    buttons = []
    for name, x, y, w, h in BUTTONS:
        image = pygame.image.load(os.path.join(ASSETS_DIR, "buttons", name + ".png")).convert_alpha()
        image = pygame.transform.smoothscale(image, (w, h))
        rect = image.get_rect(topleft=(x, y))
        mask = pygame.mask.from_surface(image)
        buttons.append((name, image, rect, mask))
    return buttons


def get_clicked_button(buttons, pos):
    for name, image, rect, mask in buttons:
        if rect.collidepoint(pos) and mask.get_at((pos[0] - rect.x, pos[1] - rect.y)):
            return name
    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    background = pygame.image.load(os.path.join(ASSETS_DIR, "background.jpg")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
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
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)
        for name, image, rect, mask in buttons:
            screen.blit(image, rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
