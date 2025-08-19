import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fly Killer")

ROUND_TIME_MS = 30_000   # длительность раунда
MOVE_INTERVAL_MS = 1_000 # как часто муха меняет позицию
TARGET_SIZE = (40, 40)
SWATTER_SIZE = (50, 80)

HIGHSCORE_FILE = "highscore.txt"

def load_highscore(path=HIGHSCORE_FILE):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return int(f.read().strip() or 0)
    except Exception:
        pass
    return 0

def save_highscore(score, path=HIGHSCORE_FILE):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(score))
    except Exception:
        pass

highscore = load_highscore()

icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

background_img = pygame.image.load("img/background.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

target_img = pygame.image.load("img/target.png").convert_alpha()
target_img = pygame.transform.smoothscale(target_img, TARGET_SIZE)
target_rect = target_img.get_rect()

swatter_img = pygame.image.load("img/swatter.png").convert_alpha()
swatter_img = pygame.transform.smoothscale(swatter_img, SWATTER_SIZE)
swatter_rect = swatter_img.get_rect()

hit_img = pygame.image.load("img/hit.png").convert_alpha()
hit_img = pygame.transform.smoothscale(hit_img, TARGET_SIZE)

hit_sound = pygame.mixer.Sound("sound/hit.wav")

pygame.mouse.set_visible(False)

# Таймер для прыжков мухи
MOVE_FLY = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_FLY, MOVE_INTERVAL_MS)

clock = pygame.time.Clock()
score = 0
show_hit = False
game_over = False
round_start_ms = pygame.time.get_ticks()

# Кнопка Restart
font_button = pygame.font.SysFont(None, 48)
restart_text = font_button.render("Restart", True, (0, 0, 0))
restart_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 60)

def random_target_pos():
    target_rect.x = random.randint(0, SCREEN_WIDTH - TARGET_SIZE[0])
    target_rect.y = random.randint(0, SCREEN_HEIGHT - TARGET_SIZE[1])

random_target_pos()

# Полупрозрачная плашка для финиша
def draw_finish_overlay(final_score, best_score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))  # затемнение

    font_big = pygame.font.SysFont(None, 96)
    font_mid = pygame.font.SysFont(None, 56)
    font_small = pygame.font.SysFont(None, 40)

    text1 = font_big.render("Finish!", True, (255, 255, 255))
    text2 = font_mid.render(f"Score: {final_score}", True, (255, 255, 255))
    text3 = font_small.render(f"High Score: {best_score}", True, (255, 255, 255))

    t1_rect = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110))
    t2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    t3_rect = text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 15))

    overlay.blit(text1, t1_rect)
    overlay.blit(text2, t2_rect)
    overlay.blit(text3, t3_rect)

    # Кнопка Restart
    pygame.draw.rect(overlay, (200, 200, 200), restart_rect)
    pygame.draw.rect(overlay, (50, 50, 50), restart_rect, 3)
    txt_rect = restart_text.get_rect(center=restart_rect.center)
    overlay.blit(restart_text, txt_rect)

    screen.blit(overlay, (0, 0))

# Отображение таймера и рекорда
def draw_hud(ms_left, best_score):
    seconds_left = max(0, ms_left // 1000)
    font_timer = pygame.font.SysFont(None, 48)
    timer_text = font_timer.render(f"Time: {seconds_left}", True, (255, 255, 255))
    timer_rect = timer_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(timer_text, timer_rect)

running = True
while running:
    dt = clock.tick(60)

    # Время раунда
    if not game_over:
        elapsed = pygame.time.get_ticks() - round_start_ms
        time_left = max(0, ROUND_TIME_MS - elapsed)
        if time_left <= 0:
            game_over = True
            pygame.time.set_timer(MOVE_FLY, 0)

            if score > highscore:
                highscore = score
                save_highscore(highscore)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            if score > highscore:
                highscore = score
                save_highscore(highscore)
            running = False

        if not game_over:
            if event.type == MOVE_FLY and not show_hit:
                random_target_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if target_rect.collidepoint(event.pos):
                    score += 1
                    show_hit = True
                    hit_sound.play()

        else:  # экран финиша
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):

                    score = 0
                    show_hit = False
                    game_over = False
                    round_start_ms = pygame.time.get_ticks()
                    pygame.time.set_timer(MOVE_FLY, MOVE_INTERVAL_MS)
                    random_target_pos()

    # Рендер
    screen.blit(background_img, (0, 0))

    if not game_over:
        if show_hit:
            screen.blit(hit_img, target_rect.topleft)
            random_target_pos()
            show_hit = False
        else:
            screen.blit(target_img, target_rect.topleft)

        draw_hud(ROUND_TIME_MS - (pygame.time.get_ticks() - round_start_ms), highscore)
    else:
        draw_finish_overlay(score, highscore)

    # Мухобойка
    mouse_x, mouse_y = pygame.mouse.get_pos()
    swatter_rect.center = (mouse_x, mouse_y)
    screen.blit(swatter_img, swatter_rect.topleft)

    pygame.display.flip()

pygame.quit()
print("Score:", score, "| High Score:", highscore)



