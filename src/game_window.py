##
## EPITECH PROJECT, 2026
## B-INN-00 : hackaton halloween - src/game_window.py
## File description :
## Game window
##

import pygame
import random
import os

from constants import WIDTH, HEIGHT, ASSETS_DIR, GROUND_Y
from constants import SCREAMER_SIZE, SCREAMER_SPEED, OBJECT_SIZE, FALLING_OBJECTS, SCREAMER_HEALTH
from constants import SPAWN_DELAY_MIN, SPAWN_DELAY_MAX, FALL_SPEED_MIN, FALL_SPEED_MAX
from constants import GAME_QUIT_BUTTON, TOOLTIP_TEXT_SIZE, GAME_MUSIC, SCREAM_SOUND, GAME_OVER_PLAY_BUTTON
from ui import load_background, Button, ButtonGroup, render_tooltip, play_music, play_sound

QUIT_WARNING = "You will go back to the main menu and lose all your progress!"


def load_sprite(filename, size, smooth):
    image = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()
    if smooth:
        return pygame.transform.smoothscale(image, size)
    # Pixel art: no smoothing to keep the pixels sharp
    return pygame.transform.scale(image, size)


class Screamer:
    def __init__(self):
        self.health = SCREAMER_HEALTH
        self.image = load_sprite("screamer.png", SCREAMER_SIZE, True)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, GROUND_Y))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.score = 0

    def update(self, dt, objs):
        keys = pygame.key.get_pressed()
        direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.x += direction * SCREAMER_SPEED * dt
        self.x = max(0, min(self.x, WIDTH - self.rect.width))
        self.rect.x = round(self.x)
        for obj in objs:
            self.touch_objcet(obj)
    
    def touch_objcet(self, obj):
        if self.rect.colliderect(obj.rect):
            obj.set_destroy()
            damage = obj.get_damage()
            if (damage == 0):
                self.score += 1
            else:
                self.health = max(0, self.health - damage)
                if self.health == 0:
                    play_sound(SCREAM_SOUND)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class FallingObject:
    def __init__(self, kind, image, damage):
        self.destroyed = False
        self.kind = kind
        self.damage = damage
        self.image = image
        # Starts just above the top edge of the window
        self.x = random.randint(0, WIDTH - OBJECT_SIZE)
        self.rect = image.get_rect(bottomleft=(self.x, 0))
        self.y = float(self.rect.y)
        self.speed = random.uniform(FALL_SPEED_MIN, FALL_SPEED_MAX)
    def get_damage(self):
        return self.damage
    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = round(self.y)
    def set_destroy(self):
        self.destroyed = True
    def on_destroy(self):
        return self.destroyed
    def on_ground(self):
        return self.rect.bottom >= GROUND_Y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def spawn_object(sprites):
    kind, filename, weight, damage = random.choices(
        FALLING_OBJECTS,
        weights=[weight for kind, filename, weight, damage in FALLING_OBJECTS],
        k=1
    )[0]
    return FallingObject(kind, sprites[kind], damage)

def draw_stats(screen, screamer):
    font = pygame.font.Font(None, 32)

    health_text = font.render(
        f"Health : {screamer.health}",
        True,
        (255, 255, 255)
    )
    score_text = font.render(
        f"Score : {screamer.score}",
        True,
        (255, 255, 255)
    )

    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 45))

def show_game_over(screen):
    image = load_sprite("true_screamer.png", (1920, 1080), True)
    image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))

    play_button = Button(*GAME_OVER_PLAY_BUTTON)
    buttons = ButtonGroup([play_button])

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if buttons.handle_event(event):
                return True

        screen.fill((0, 0, 0))
        screen.blit(image, image_rect)
        buttons.draw(screen)
        pygame.display.flip()

# Returns True to go back to the menu (Escape or quit button), False if the window was closed
def run_game(screen):
    while True:
        background = load_background()
        screamer = Screamer()
        sprites = {}
        for kind, filename, weight, damage in FALLING_OBJECTS:
            sprites[kind] = load_sprite(
                filename,
                (OBJECT_SIZE, OBJECT_SIZE),
                False
            )
        objects = []
        spawn_timer = random.uniform(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)
        quit_button = Button(*GAME_QUIT_BUTTON)
        buttons = ButtonGroup([quit_button])
        tooltip = render_tooltip(QUIT_WARNING, TOOLTIP_TEXT_SIZE)
        tooltip_rect = tooltip.get_rect(
            topright=(quit_button.rect.right, quit_button.rect.bottom + 8)
        )
        play_music(GAME_MUSIC)
        clock = pygame.time.Clock()
        while screamer.health > 0:
            dt = min(clock.tick(60) / 1000, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True
                if buttons.handle_event(event):
                    return True
            screamer.update(dt, objects)
            spawn_timer -= dt
            if spawn_timer <= 0:
                objects.append(spawn_object(sprites))
                spawn_timer += random.uniform(
                    SPAWN_DELAY_MIN,
                    SPAWN_DELAY_MAX
                )
            for obj in objects:
                obj.update(dt)
            objects = [
                obj for obj in objects
                if not obj.on_ground() and not obj.on_destroy()
            ]
            screen.blit(background, (0, 0))
            screamer.draw(screen)
            for obj in objects:
                obj.draw(screen)
            buttons.draw(screen)
            draw_stats(screen, screamer)
            if buttons.get_button_at(pygame.mouse.get_pos()):
                screen.blit(tooltip, tooltip_rect)
            pygame.display.flip()
        result = show_game_over(screen)
        if result is True:
            continue  # Nouvelle partie : tout est réinitialisé.
        if result is False:
            return False
        return True  # Retour au menu.
