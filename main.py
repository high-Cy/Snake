import pygame
import sys
from random import randint


class Snake:
    def __init__(self):
        self.colour = (255, 255, 255)
        self.length = 1
        self.score = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour,
                         (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, GRID, GRID))

    @staticmethod
    def get_keys():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass


class Food(pygame.sprite.Sprite):
    def __init__(self, pic_path):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()
        self.position = self.rect.center = self.spawn()

    @staticmethod
    def spawn():
        """ Ensures initial spawn won't collide with snake in the middle """
        exclude_x = [i for i in
                     range(SCREEN_WIDTH // 2 - GRID, SCREEN_WIDTH // 2 + GRID)]
        exclude_y = [i for i in
                     range(SCREEN_HEIGHT // 2 - GRID,
                           SCREEN_HEIGHT // 2 + GRID)]

        x = randint(FOOD_PX, SCREEN_WIDTH - FOOD_PX)
        y = randint(FOOD_PX, SCREEN_HEIGHT - FOOD_PX)
        while x in exclude_x or y in exclude_y:
            if x in exclude_x:
                x = randint(FOOD_PX, SCREEN_WIDTH - FOOD_PX)
            if y in exclude_y:
                y = randint(FOOD_PX, SCREEN_HEIGHT - FOOD_PX)

        return x, y

    def respawn(self):
        pass


SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400

FOOD_PX = GRID = 24
GRID_WIDTH = SCREEN_WIDTH / GRID
GRID_HEIGHT = SCREEN_HEIGHT / GRID

food = Food('img/apple24px.png')
food_group = pygame.sprite.Group()
food_group.add(food)

snake = Snake()


def main():
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Snake')
    icon = pygame.image.load('img/snake.png')
    pygame.display.set_icon(icon)

    '''
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    '''
    while True:
        pygame.display.flip()

        Snake.get_keys()

        snake.draw(screen)
        food_group.draw(screen)


if __name__ == '__main__':
    main()
