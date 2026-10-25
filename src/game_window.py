##
## EPITECH PROJECT, 2026
## B-INN-00 : hackaton halloween - src/game_window.py
## File description :
## Game window
##

import pygame
import random
import math
import os

from constants import WIDTH, HEIGHT, ASSETS_DIR, GROUND_Y, GOOD_SOUND, PAIN_SOUND
from constants import SCREAMER_SIZE, SCREAMER_SPEED, OBJECT_SIZE, FALLING_OBJECTS, SCREAMER_HEALTH
from constants import SPAWN_DELAY_MIN, SPAWN_DELAY_MAX, FALL_SPEED_MIN, FALL_SPEED_MAX
from constants import SCORE_PER_LEVEL, MAX_LEVEL, SPAWN_DELAY_STEP, FALL_SPEED_STEP
from constants import POTION_DURATION
from constants import SWAY_LEVEL, SWAY_AMPLITUDE, SWAY_SPEED
from constants import GAME_QUIT_BUTTON, TOOLTIP_TEXT_SIZE, GAME_MUSIC, SCREAM_SOUND, GAME_OVER_PLAY_BUTTON
from constants import TEXT_FONT, TEXT_COLOR, PANEL_COLOR, TITLE_COLOR, TITLE_OUTLINE_COLOR
from ui import load_background, Button, ButtonGroup, render_tooltip, render_outlined_text, play_music, play_sound
from leaderboard_window import qualifies, save_score

QUIT_WARNING = "You will go back to the main menu and lose all your progress!"


def current_level(score):
    return min(score // SCORE_PER_LEVEL + 1, MAX_LEVEL)


def spawn_delay(level):
    factor = max(0.3, 1 - SPAWN_DELAY_STEP * (level - 1))
    return random.uniform(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX) * factor


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
        # Blue tinted copy drawn while the potion effect is active
        self.shield_image = self.image.copy()
        self.shield_image.fill((90, 170, 255), special_flags=pygame.BLEND_RGB_ADD)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, GROUND_Y))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.score = 0
        self.shield_time = 0.0

    def update(self, dt, objs):
        keys = pygame.key.get_pressed()
        direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.x += direction * SCREAMER_SPEED * dt
        self.x = max(0, min(self.x, WIDTH - self.rect.width))
        self.rect.x = round(self.x)
        if self.shield_time > 0:
            self.shield_time = max(0.0, self.shield_time - dt)
        for obj in objs:
            self.touch_objcet(obj)
    
    def touch_objcet(self, obj):
        if self.rect.colliderect(obj.rect):
            obj.set_destroy()
            damage = obj.get_damage()
            if (damage == 0):
                self.score += obj.get_score()
                play_sound(GOOD_SOUND)
                if obj.kind == "potion":
                    self.shield_time = POTION_DURATION
            elif self.shield_time > 0:
                return
            else:
                self.health = max(0, self.health - damage)
                if self.health == 0:
                    play_sound(SCREAM_SOUND)
                else:
                    play_sound(PAIN_SOUND)
    
    def draw(self, screen):
        image = self.shield_image if self.shield_time > 0 else self.image
        screen.blit(image, self.rect)


class FallingObject:
    def __init__(self, kind, image, damage, score, level):
        self.destroyed = False
        self.kind = kind
        self.damage = damage
        self.score = score
        self.image = image
        # Starts just above the top edge of the window
        self.x = random.randint(0, WIDTH - OBJECT_SIZE)
        self.rect = image.get_rect(bottomleft=(self.x, 0))
        self.y = float(self.rect.y)
        self.speed = random.uniform(
            FALL_SPEED_MIN + FALL_SPEED_STEP * (level - 1),
            FALL_SPEED_MAX + FALL_SPEED_STEP * (level - 1)
        )
        # From SWAY_LEVEL on, ghosts drift side to side in a sine wave
        self.sway_amplitude = SWAY_AMPLITUDE if (kind == "boo" and level >= SWAY_LEVEL) else 0
        self.sway_phase = 0.0
    def get_damage(self):
        return self.damage
    def get_score(self):
        return self.score
    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = round(self.y)
        if self.sway_amplitude > 0:
            self.sway_phase += SWAY_SPEED * dt
            self.rect.x = max(
                0,
                min(
                    self.x + int(self.sway_amplitude * math.sin(self.sway_phase)),
                    WIDTH - OBJECT_SIZE
                )
            )
    def set_destroy(self):
        self.destroyed = True
    def on_destroy(self):
        return self.destroyed
    def on_ground(self):
        return self.rect.bottom >= GROUND_Y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def spawn_object(sprites, level):
    weights = [
        random.randint(weight[0], weight[1])
        for kind, filename, weight, damage, score in FALLING_OBJECTS
    ]
    kind, filename, weight, damage, score = random.choices(
        FALLING_OBJECTS,
        weights=weights,
        k=1
    )[0]
    return FallingObject(kind, sprites[kind], damage, score, level)

def draw_stats(screen, screamer, level):
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
    level_text = font.render(
        f"Level : {level}",
        True,
        (255, 255, 255)
    )

    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 45))
    screen.blit(level_text, (10, 80))

# End of the game: shows the final score, and asks for a nickname
# when the score makes the top 5
# Returns True for a new game, None for the menu, False if the window was closed
def show_game_over(screen, score):
    image = load_sprite("true_screamer.png", (1920, 1080), True)
    image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))

    play_button = Button(*GAME_OVER_PLAY_BUTTON)
    buttons = ButtonGroup([play_button])
    clock = pygame.time.Clock()

    score_font = pygame.font.Font(TEXT_FONT, 44)
    # Outlined so it stays readable over the light part of the image
    score_label = render_outlined_text(
        score_font, f"Score : {score}", TEXT_COLOR, TITLE_OUTLINE_COLOR, 3
    )
    score_rect = score_label.get_rect(midtop=(WIDTH // 2, 40))

    entering = qualifies(score)
    nickname = ""
    nick_font = pygame.font.Font(TEXT_FONT, 32)
    box_rect = pygame.Rect(0, 0, 420, 48)
    box_rect.midbottom = (WIDTH // 2, 520)
    prompt = pygame.font.Font(TEXT_FONT, 28).render(
        "You made the top 5 ! Enter your nickname :",
        True,
        (255, 215, 0)
    )
    prompt_rect = prompt.get_rect(midbottom=(box_rect.x, box_rect.top - 10))
    hint = pygame.font.Font(TEXT_FONT, 20).render(
        "Enter to save - Escape for the menu",
        True,
        TEXT_COLOR
    )
    hint_rect = hint.get_rect(midtop=(WIDTH // 2, box_rect.bottom + 8))

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if buttons.handle_event(event):
                return True
            if entering and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = nickname.strip()
                    if name:
                        save_score(name, score)
                    return None
                if event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                elif event.unicode and event.unicode.isprintable() and len(nickname) < 16:
                    nickname += event.unicode

        screen.fill((0, 0, 0))
        screen.blit(image, image_rect)
        screen.blit(score_label, score_rect)
        if entering:
            screen.blit(prompt, prompt_rect)
            pygame.draw.rect(screen, PANEL_COLOR, box_rect, border_radius=10)
            pygame.draw.rect(screen, TITLE_COLOR, box_rect, width=2, border_radius=10)
            cursor = ">" if (pygame.time.get_ticks() // 400) % 2 == 0 else ""
            label = nick_font.render(nickname + cursor, True, TEXT_COLOR)
            screen.blit(label, (box_rect.x + 12, box_rect.y + 8))
            screen.blit(hint, hint_rect)
        buttons.draw(screen)
        pygame.display.flip()

# Returns True to go back to the menu (Escape or quit button), False if the window was closed
def run_game(screen):
    while True:
        background = load_background()
        screamer = Screamer()
        sprites = {}
        for kind, filename, weight, damage, score in FALLING_OBJECTS:
            sprites[kind] = load_sprite(
                filename,
                (OBJECT_SIZE, OBJECT_SIZE),
                False
            )
        objects = []
        spawn_timer = spawn_delay(1)
        quit_button = Button(*GAME_QUIT_BUTTON)
        buttons = ButtonGroup([quit_button])
        tooltip = render_tooltip(QUIT_WARNING, TOOLTIP_TEXT_SIZE)
        tooltip_rect = tooltip.get_rect(
            topright=(quit_button.rect.right, quit_button.rect.bottom + 8)
        )
        play_music(GAME_MUSIC)
        clock = pygame.time.Clock()
        paused = False
        pause_label = render_outlined_text(
            pygame.font.Font(TEXT_FONT, 60),
            "Paused",
            TEXT_COLOR,
            TITLE_OUTLINE_COLOR,
            4
        )
        pause_hint = pygame.font.Font(TEXT_FONT, 24).render(
            "Press P to resume",
            True,
            TEXT_COLOR
        )
        while screamer.health > 0:
            dt = min(clock.tick(60) / 1000, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True
                if buttons.handle_event(event):
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = not paused
            level = current_level(screamer.score)
            if not paused:
                screamer.update(dt, objects)
                spawn_timer -= dt
                if spawn_timer <= 0:
                    objects.append(spawn_object(sprites, level))
                    spawn_timer += spawn_delay(level)
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
            draw_stats(screen, screamer, level)
            if buttons.get_button_at(pygame.mouse.get_pos()):
                screen.blit(tooltip, tooltip_rect)
            if paused:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 130))
                screen.blit(overlay, (0, 0))
                screen.blit(
                    pause_label,
                    pause_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
                )
                screen.blit(
                    pause_hint,
                    pause_hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
                )
            pygame.display.flip()
        result = show_game_over(screen, screamer.score)
        if result is True:
            continue  # Nouvelle partie : tout est réinitialisé.
        if result is False:
            return False
        return True  # Retour au menu.
