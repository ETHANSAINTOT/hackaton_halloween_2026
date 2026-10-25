##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/rules.py
## File description:
## Rules screen
##

from constants import TEXT_COLOR, RULES_TITLE, RULES_TEXT_SIZE
from ui import run_text_screen

RULES_TEXT = (
    "You control a screamer moving left and right with the LEFT and RIGHT arrow keys only.\n"
    "Press P to pause the game.\n"
    "Objects fall straight down from random positions along the top of the window.\n"
    "From level 3, ghosts start drifting side to side.\n"
    "\n"
    "• Classic pumpkin: catch as many as you can to raise your score.\n"
    "• Carved pumpkin: you lose a life.\n"
    "• Ghost: instant death, game over!\n"
    "• Candy: very rare, worth 3 points.\n"
    "• Potion: very rare, makes you invincible for a few seconds.\n"
    "\n"
    "You start with 5 lives, and the game ends when you have none left.\n"
    "If your final score is among the 5 best ever, enter your nickname to join the leaderboard!\n"
    "Any change to leaderboard.csv, other than by reaching the top 5, is strictly forbidden!"
)


# Returns True to go back to the menu, False if the window was closed
def run_rules(screen):
    lines = [(line, TEXT_COLOR) for line in RULES_TEXT.split("\n")]
    return run_text_screen(screen, RULES_TITLE, lines, RULES_TEXT_SIZE)
