##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/constants.py
## File description:
## Constsants storage
##

import os

WIDTH = 1280
HEIGHT = 720
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# (name, x, y, width, height) in the 1280x720 window
BUTTONS = [
    ("play", 290, 165, 701, 280),
    ("rules", 36, 496, 359, 171),
    ("leaderboard", 442, 512, 396, 155),
    ("quit", 896, 521, 347, 148),
]

TITLE = "Pumpkin Scream"
TITLE_FONT = os.path.join(ASSETS_DIR, "font", "bloody_ghost.otf")
TITLE_SIZE = 110
TITLE_Y = 25
TITLE_COLOR = (255, 140, 0)
TITLE_OUTLINE_COLOR = (30, 10, 20)
TITLE_OUTLINE = 4

TEXT_FONT = os.path.join(ASSETS_DIR, "font", "ARIAL.TTF")

# Rules screen
RULES_TITLE = "Rules"
RULES_TEXT_SIZE = 26
RULES_TEXT_COLOR = (240, 240, 240)
RULES_PANEL_COLOR = (20, 10, 25, 190)
RULES_PANEL_WIDTH = 1100
RULES_PANEL_PADDING = 30
RULES_QUIT_BUTTON = ("quit", 467, 540, 347, 148)
