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
    ("play", 213, 85, 847, 338),
    ("rules", 36, 486, 359, 171),
    ("leaderboard", 442, 502, 396, 155),
    ("quit", 896, 511, 347, 148),
]
