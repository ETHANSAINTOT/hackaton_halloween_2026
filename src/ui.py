##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/ui.py
## File description:
## Shared drawing helpers
##

import pygame
import os

from constants import WIDTH, HEIGHT, ASSETS_DIR


def load_background():
    background = pygame.image.load(os.path.join(ASSETS_DIR, "background.jpg")).convert()
    return pygame.transform.scale(background, (WIDTH, HEIGHT))


def render_outlined_text(font, text, color, outline_color, outline):
    front = font.render(text, True, color)
    back = font.render(text, True, outline_color)
    o = outline
    surface = pygame.Surface((front.get_width() + 2 * o, front.get_height() + 2 * o), pygame.SRCALPHA)
    for dx in range(-o, o + 1):
        for dy in range(-o, o + 1):
            if dx * dx + dy * dy <= o * o:
                surface.blit(back, (o + dx, o + dy))
    surface.blit(front, (o, o))
    # Crop the empty space around the letters so the centering is exact
    return surface.subsurface(surface.get_bounding_rect()).copy()


def load_button(name, x, y, w, h):
    image = pygame.image.load(os.path.join(ASSETS_DIR, "buttons", name + ".png")).convert_alpha()
    image = pygame.transform.smoothscale(image, (w, h))
    rect = image.get_rect(topleft=(x, y))
    mask = pygame.mask.from_surface(image)
    return name, image, rect, mask


def get_clicked_button(buttons, pos):
    for name, image, rect, mask in buttons:
        if rect.collidepoint(pos) and mask.get_at((pos[0] - rect.x, pos[1] - rect.y)):
            return name
    return None
