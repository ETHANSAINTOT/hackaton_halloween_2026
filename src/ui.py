##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/ui.py
## File description:
## Shared drawing helpers
##

import pygame
import os

from constants import WIDTH, HEIGHT, ASSETS_DIR, TEXT_FONT
from constants import TITLE_FONT, TITLE_SIZE, TITLE_Y
from constants import TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE
from constants import PANEL_COLOR, PANEL_WIDTH, PANEL_PADDING, BACK_BUTTON


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


def wrap_text(font, text, max_width):
    lines = []
    line = ""
    for word in text.split(" "):
        test = line + " " + word if line else word
        if line and font.size(test)[0] > max_width:
            lines.append(line)
            line = word
        else:
            line = test
    lines.append(line)
    return lines


# lines is a list of (text, color), each text is wrapped to fit in the panel
def load_panel(lines, text_size, top, bottom):
    font = pygame.font.Font(TEXT_FONT, text_size)
    wrapped = []
    for text, color in lines:
        for line in wrap_text(font, text, PANEL_WIDTH - 2 * PANEL_PADDING):
            wrapped.append((line, color))
    line_height = font.get_linesize()
    height = len(wrapped) * line_height + 2 * PANEL_PADDING
    panel = pygame.Surface((PANEL_WIDTH, height), pygame.SRCALPHA)
    pygame.draw.rect(panel, PANEL_COLOR, panel.get_rect(), border_radius=20)
    pygame.draw.rect(panel, TITLE_COLOR, panel.get_rect(), width=3, border_radius=20)
    # Lines are left-aligned inside a block centered in the panel
    block_width = max(font.size(line)[0] for line, color in wrapped)
    x = (PANEL_WIDTH - block_width) // 2
    for i, (line, color) in enumerate(wrapped):
        if line:
            panel.blit(font.render(line, True, color), (x, PANEL_PADDING + i * line_height))
    # Centered between the title and the back button
    rect = panel.get_rect(center=(WIDTH // 2, (top + bottom) // 2))
    return panel, rect


# Screen with a title, a text panel and a back button
# Returns True to go back to the menu, False if the window was closed
def run_text_screen(screen, title_text, lines, text_size):
    background = load_background()
    font = pygame.font.Font(TITLE_FONT, TITLE_SIZE)
    title = render_outlined_text(font, title_text, TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE)
    title_rect = title.get_rect(midtop=(WIDTH // 2, TITLE_Y))
    back_button = load_button(*BACK_BUTTON)
    _, back_image, back_rect, _ = back_button
    panel, panel_rect = load_panel(lines, text_size, title_rect.bottom, back_rect.top)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if get_clicked_button([back_button], event.pos):
                    return True
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(panel, panel_rect)
        screen.blit(back_image, back_rect)
        pygame.display.flip()
        clock.tick(60)
