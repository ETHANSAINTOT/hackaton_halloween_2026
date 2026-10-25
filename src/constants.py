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

# Menu music is played on the main menu, rules and leaderboard, game music during the game
MENU_MUSIC = os.path.join(ASSETS_DIR, "music", "spooky_halloween.mp3")
GAME_MUSIC = os.path.join(ASSETS_DIR, "music", "spooky_scary_skeleton.mp3")
# Between 0.0 (mute) and 1.0 (max)
MUSIC_VOLUME = 0.5

TEXT_FONT = os.path.join(ASSETS_DIR, "font", "ARIAL.TTF")
TEXT_COLOR = (240, 240, 240)

# Button effects: hovered buttons grow and get brighter, pressed ones shrink and get darker
HOVER_SCALE = 1.06
HOVER_BRIGHTEN = (40, 40, 40)
PRESSED_SCALE = 0.96
PRESSED_DARKEN = (200, 200, 200)

# Text screens (rules, leaderboard)
PANEL_COLOR = (20, 10, 25, 190)
PANEL_WIDTH = 1100
PANEL_PADDING = 30
BACK_BUTTON = ("quit", 467, 540, 347, 148)

# Rules screen
RULES_TITLE = "Rules"
RULES_TEXT_SIZE = 26

# Leaderboard screen
LEADERBOARD_TITLE = "Leaderboard"
LEADERBOARD_TEXT_SIZE = 40
LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.csv")
LEADERBOARD_SIZE = 5
# Gold, silver, bronze
PODIUM_COLORS = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]

# Game screen
GROUND_Y = HEIGHT - 20
SCREAMER_SIZE = (120, 180)
# Speeds are in pixels per second, delays in seconds
SCREAMER_SPEED = 600
OBJECT_SIZE = 64
# (kind, image, weight): the bigger the weight, the more often the object falls
FALLING_OBJECTS = [
    ("pumpkin", "pumpkin.png", 6),
    ("pumpkin_carved", "pumpkin_carved.png", 3),
    ("boo", "boo.png", 1),
]
SPAWN_DELAY_MIN = 0.5
SPAWN_DELAY_MAX = 1.5
FALL_SPEED_MIN = 150
FALL_SPEED_MAX = 400
# Same ratio as the image (453x193), in the top right corner
GAME_QUIT_BUTTON = ("quit", 1085, 15, 180, 77)
TOOLTIP_TEXT_SIZE = 20
