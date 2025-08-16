import pygame
import random
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fly Killer")
icon = pygame.image.load("img/flykiller.png")
pygame.display.set_icon(icon)

background_color = (144, 238, 144)

target_img = pygame.image.load("img/flykiller_target.png")
targer_width = 50
targer_height = 50

target_x = random.randint(0, SCREEN_WIDTH - targer_width)
target_y = random.randint(0, SCREEN_HEIGHT - targer_height)



running = True
while running:
    pass

pygame.quit()


