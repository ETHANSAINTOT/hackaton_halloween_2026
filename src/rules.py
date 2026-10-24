##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/rules.py
## File description:
## Rules screen
##

import pygame

from constants import WIDTH, TITLE_FONT, TITLE_SIZE, TITLE_Y
from constants import TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE, TEXT_FONT
from constants import RULES_TITLE, RULES_TEXT_SIZE, RULES_TEXT_COLOR
from constants import RULES_PANEL_COLOR, RULES_PANEL_WIDTH, RULES_PANEL_PADDING
from constants import RULES_QUIT_BUTTON
from ui import load_background, render_outlined_text, load_button, get_clicked_button

RULES_TEXT = (
    "You control a screamer moving left and right with the LEFT and RIGHT arrow keys only.\n"
    "Objects always fall straight down from random positions along the top of the window.\n"
    "\n"
    "• Classic pumpkin: catch as many as you can to raise your score.\n"
    "• Carved pumpkin: you lose a life.\n"
    "• Ghost: instant death, game over!\n"
    "\n"
    "You start with 5 lives, and the game ends when you have none left.\n"
    "If your final score is among the 5 best ever, enter your nickname to join the leaderboard!"
)


def wrap_text(font, text, max_width):
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split(" "):
            test = line + " " + word if line else word
            if line and font.size(test)[0] > max_width:
                lines.append(line)
                line = word
            else:
                line = test
        lines.append(line)
    return lines


def load_panel(top, bottom):
    font = pygame.font.Font(TEXT_FONT, RULES_TEXT_SIZE)
    lines = wrap_text(font, RULES_TEXT, RULES_PANEL_WIDTH - 2 * RULES_PANEL_PADDING)
    line_height = font.get_linesize()
    height = len(lines) * line_height + 2 * RULES_PANEL_PADDING
    panel = pygame.Surface((RULES_PANEL_WIDTH, height), pygame.SRCALPHA)
    pygame.draw.rect(panel, RULES_PANEL_COLOR, panel.get_rect(), border_radius=20)
    pygame.draw.rect(panel, TITLE_COLOR, panel.get_rect(), width=3, border_radius=20)
    for i, line in enumerate(lines):
        if line:
            text = font.render(line, True, RULES_TEXT_COLOR)
            panel.blit(text, (RULES_PANEL_PADDING, RULES_PANEL_PADDING + i * line_height))
    # Centered between the title and the quit button
    rect = panel.get_rect(center=(WIDTH // 2, (top + bottom) // 2))
    return panel, rect


# Returns True to go back to the menu, False if the window was closed
def run_rules(screen):
    background = load_background()
    font = pygame.font.Font(TITLE_FONT, TITLE_SIZE)
    title = render_outlined_text(font, RULES_TITLE, TITLE_COLOR, TITLE_OUTLINE_COLOR, TITLE_OUTLINE)
    title_rect = title.get_rect(midtop=(WIDTH // 2, TITLE_Y))
    quit_button = load_button(*RULES_QUIT_BUTTON)
    _, quit_image, quit_rect, _ = quit_button
    panel, panel_rect = load_panel(title_rect.bottom, quit_rect.top)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if get_clicked_button([quit_button], event.pos):
                    return True
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)
        screen.blit(panel, panel_rect)
        screen.blit(quit_image, quit_rect)
        pygame.display.flip()
        clock.tick(60)
