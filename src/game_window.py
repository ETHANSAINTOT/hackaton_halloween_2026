##
## EPITECH PROJECT, 2026
## B-INN-00 : hackaton halloween - src/game_window.py
## File description :
## Game window
##

import pygame
import random
import os

from constants import WIDTH, ASSETS_DIR, GROUND_Y
from constants import SCREAMER_SIZE, SCREAMER_SPEED, OBJECT_SIZE, FALLING_OBJECTS
from constants import SPAWN_DELAY_MIN, SPAWN_DELAY_MAX, FALL_SPEED_MIN, FALL_SPEED_MAX
from ui import load_background, set_cursor


def load_sprite(filename, size, smooth):
    image = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()
    if smooth:
        return pygame.transform.smoothscale(image, size)
    # Pixel art: no smoothing to keep the pixels sharp
    return pygame.transform.scale(image, size)


class Screamer:
    def __init__(self):
        self.image = load_sprite("screamer.png", SCREAMER_SIZE, True)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, GROUND_Y))
        self.x = float(self.rect.x)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.x += direction * SCREAMER_SPEED * dt
        self.x = max(0, min(self.x, WIDTH - self.rect.width))
        self.rect.x = round(self.x)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class FallingObject:
    def __init__(self, kind, image):
        self.kind = kind
        self.image = image
        # Starts just above the top edge of the window
        x = random.randint(0, WIDTH - OBJECT_SIZE)
        self.rect = image.get_rect(bottomleft=(x, 0))
        self.y = float(self.rect.y)
        self.speed = random.uniform(FALL_SPEED_MIN, FALL_SPEED_MAX)

    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = round(self.y)

    def on_ground(self):
        return self.rect.bottom >= GROUND_Y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def spawn_object(sprites):
    kinds = [kind for kind, filename, weight in FALLING_OBJECTS]
    weights = [weight for kind, filename, weight in FALLING_OBJECTS]
    kind = random.choices(kinds, weights)[0]
    return FallingObject(kind, sprites[kind])


# Returns True to go back to the menu (Escape), False if the window was closed
def run_game(screen):
    background = load_background()
    screamer = Screamer()
    sprites = {}
    for kind, filename, weight in FALLING_OBJECTS:
        sprites[kind] = load_sprite(filename, (OBJECT_SIZE, OBJECT_SIZE), False)
    objects = []
    spawn_timer = random.uniform(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)
    set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    clock = pygame.time.Clock()

    while True:
        # Time since the last frame in seconds, capped to avoid big jumps
        dt = min(clock.tick(60) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        screamer.update(dt)
        spawn_timer -= dt
        if spawn_timer <= 0:
            objects.append(spawn_object(sprites))
            spawn_timer += random.uniform(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)
        for obj in objects:
            obj.update(dt)
        objects = [obj for obj in objects if not obj.on_ground()]
        screen.blit(background, (0, 0))
        screamer.draw(screen)
        for obj in objects:
            obj.draw(screen)
        pygame.display.flip()
