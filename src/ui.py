##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/ui.py
## File description:
## Shared drawing helpers
##

import pygame
import os

from constants import WIDTH, HEIGHT, ASSETS_DIR, TEXT_FONT, TEXT_COLOR
from constants import TITLE_FONT, TITLE_SIZE, TITLE_Y
from constants import TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE
from constants import PANEL_COLOR, PANEL_WIDTH, PANEL_PADDING, BACK_BUTTON
from constants import HOVER_SCALE, HOVER_BRIGHTEN, PRESSED_SCALE, PRESSED_DARKEN
from constants import MUSIC_VOLUME

current_cursor = None


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


# Replaces the current music and plays it in loop, the game still works without sound
def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    except pygame.error as error:
        print(f"Cannot play the music: {error}")

def play_sound(path):
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(MUSIC_VOLUME)
        sound.play()
    except pygame.error as error:
        print(f"Cannot play the sound effect: {error}")


# Only change the cursor when needed, it is shared by every screen
def set_cursor(cursor):
    global current_cursor
    if cursor != current_cursor:
        pygame.mouse.set_cursor(cursor)
        current_cursor = cursor


def scale_and_tint(image, w, h, color, flag):
    result = pygame.transform.smoothscale(image, (round(w), round(h)))
    result.fill(color, special_flags=flag)
    return result


class Button:
    def __init__(self, name, x, y, w, h):
        original = pygame.image.load(os.path.join(ASSETS_DIR, "buttons", name + ".png")).convert_alpha()
        self.name = name
        self.image = pygame.transform.smoothscale(original, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        # Effects are scaled from the original image to stay sharp
        self.hover_image = scale_and_tint(original, w * HOVER_SCALE, h * HOVER_SCALE,
                                          HOVER_BRIGHTEN, pygame.BLEND_RGB_ADD)
        self.pressed_image = scale_and_tint(original, w * PRESSED_SCALE, h * PRESSED_SCALE,
                                            PRESSED_DARKEN, pygame.BLEND_RGB_MULT)

    # Pixel perfect: the transparent parts of the image are not part of the button
    def collide(self, pos):
        if not self.rect.collidepoint(pos):
            return False
        return self.mask.get_at((pos[0] - self.rect.x, pos[1] - self.rect.y))

    def draw(self, screen, hovered, pressed):
        if pressed:
            image = self.pressed_image
        elif hovered:
            image = self.hover_image
        else:
            image = self.image
        screen.blit(image, image.get_rect(center=self.rect.center))


class ButtonGroup:
    def __init__(self, buttons):
        self.buttons = buttons
        self.pressed = None

    def get_button_at(self, pos):
        for button in self.buttons:
            if button.collide(pos):
                return button.name
        return None

    # A click counts when the mouse is pressed and released on the same button
    # Returns the name of the clicked button, or None
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.get_button_at(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = self.pressed if self.get_button_at(event.pos) == self.pressed else None
            self.pressed = None
            return clicked
        return None

    def draw(self, screen):
        hovered = self.get_button_at(pygame.mouse.get_pos())
        set_cursor(pygame.SYSTEM_CURSOR_HAND if hovered else pygame.SYSTEM_CURSOR_ARROW)
        for button in self.buttons:
            is_hovered = button.name == hovered
            button.draw(screen, is_hovered, is_hovered and button.name == self.pressed)


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


# Small text box with the same look as the panels
def render_tooltip(text, text_size):
    font = pygame.font.Font(TEXT_FONT, text_size)
    label = font.render(text, True, TEXT_COLOR)
    padding = text_size // 2
    size = (label.get_width() + 2 * padding, label.get_height() + 2 * padding)
    tooltip = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(tooltip, PANEL_COLOR, tooltip.get_rect(), border_radius=10)
    pygame.draw.rect(tooltip, TITLE_COLOR, tooltip.get_rect(), width=2, border_radius=10)
    tooltip.blit(label, (padding, padding))
    return tooltip


# Screen with a title, a text panel and a back button
# Returns True to go back to the menu, False if the window was closed
def run_text_screen(screen, title_text, lines, text_size):
    background = load_background()
    font = pygame.font.Font(TITLE_FONT, TITLE_SIZE)
    title = render_outlined_text(font, title_text, TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE)
    title_rect = title.get_rect(midtop=(WIDTH // 2, TITLE_Y))
    back_button = Button(*BACK_BUTTON)
    buttons = ButtonGroup([back_button])
    panel, panel_rect = load_panel(lines, text_size, title_rect.bottom, back_button.rect.top)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if buttons.handle_event(event):
                return True
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(panel, panel_rect)
        buttons.draw(screen)
        pygame.display.flip()
        clock.tick(60)
