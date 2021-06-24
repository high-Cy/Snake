import pygame
import sys
import random

pygame.init()

SNAKE = ''
APPLE = ''

size = width, height = 500, 400


grid = 24

def main():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Snake')
    icon = pygame.image.load('img/snake.png')
    pygame.display.set_icon(icon)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()
