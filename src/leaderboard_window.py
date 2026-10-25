##
## EPITECH PROJECT, 2026
## B-INN-000 : hackaton halloween - src/leaderboard_window.py
## File description:
## Leaderboard screen
##

import csv

from constants import TEXT_COLOR, LEADERBOARD_TITLE, LEADERBOARD_TEXT_SIZE
from constants import LEADERBOARD_FILE, LEADERBOARD_SIZE, PODIUM_COLORS
from ui import run_text_screen


# The file is sorted from the best score to the worst
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, newline="", encoding="utf-8") as file:
            return [(row["nickname"], row["score"]) for row in csv.DictReader(file, delimiter=";")]
    except FileNotFoundError:
        return []


# Returns True if the score would get into the top 5
def qualifies(score):
    scores = [
        int(points)
        for _, points in load_leaderboard()
        if points.isdigit()
    ]
    if len(scores) < LEADERBOARD_SIZE:
        return True
    return score > min(scores)


# Adds the new entry, keeps only the top 5, and rewrites the file
def save_score(nickname, score):
    entries = [
        (name, int(points))
        for name, points in load_leaderboard()
        if points.isdigit()
    ]
    entries.append((nickname, int(score)))
    entries.sort(key=lambda entry: entry[1], reverse=True)
    with open(LEADERBOARD_FILE, "w", newline="", encoding="utf-8") as file:
        file.write("nickname;score\n")
        for name, points in entries[:LEADERBOARD_SIZE]:
            file.write(f"{name};{points}\n")


# Returns True to go back to the menu, False if the window was closed
def run_leaderboard(screen):
    entries = load_leaderboard()
    lines = []
    for i in range(LEADERBOARD_SIZE):
        nickname, score = entries[i] if i < len(entries) else ("---", "---")
        color = PODIUM_COLORS[i] if i < len(PODIUM_COLORS) else TEXT_COLOR
        lines.append((f"{i + 1}. {nickname} : {score}", color))
    return run_text_screen(screen, LEADERBOARD_TITLE, lines, LEADERBOARD_TEXT_SIZE)
