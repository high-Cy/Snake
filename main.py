import pygame
import sys
from random import randint
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.colour = (255, 255, 255)
        self.length = 3
        self.positions = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(0, 0)
        self.score = 0

    def draw(self):
        for pos in self.positions:
            pos_x = int(pos.x * GRID_SIZE)
            pos_y = int(pos.y * GRID_SIZE)
            pos_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.colour, pos_rect)

    def move(self):
        pos_copy = self.positions[:-1]
        pos_copy.insert(0, pos_copy[0] + self.direction)
        self.positions = pos_copy[:]
        while len(self.positions) > self.length:
            del self.positions[-1]


class Food(pygame.sprite.Sprite, Snake):
    def __init__(self, pic_path, snake_class):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()
        self.position = self.rect.center = self.spawn(snake_class)

    @staticmethod
    def spawn(snake_class):
        """ Ensures spawn won't collide with snake """

        snake_x = snake_y = []
        for pos in snake_class.positions:
            snake_x.append(pos.x)
            snake_y.append(pos.y)

        exclude_x = exclude_y = []
        for i in snake_x:  # , snake_y:
            exclude_x.append(range(int(i) - GRID_SIZE, int(i) + GRID_SIZE))
            # exclude_y.append(range(int(j) - GRID_SIZE, int(j) + GRID_SIZE))

        x = randint(FOOD_PX, SCREEN_WIDTH - FOOD_PX)
        y = randint(FOOD_PX, SCREEN_HEIGHT - FOOD_PX)
        while x in exclude_x or y in exclude_y:
            if x in exclude_x:
                x = randint(FOOD_PX, SCREEN_WIDTH - FOOD_PX)
            if y in exclude_y:
                y = randint(FOOD_PX, SCREEN_HEIGHT - FOOD_PX)

        return x, y


pygame.init()

FOOD_PX = GRID_SIZE = 32
GRID_NUM = 20
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * GRID_NUM, GRID_SIZE * GRID_NUM

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

snake = Snake()

food = Food('img/apple.png', snake)
food_group = pygame.sprite.Group()
food_group.add(food)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Snake')
icon = pygame.image.load('img/snake.png').convert_alpha()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            snake.move()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = UP
            elif event.key == pygame.K_DOWN:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.direction = RIGHT

    screen.fill((0, 0, 0))

    snake.draw()

    food_group.draw(screen)

    pygame.display.update()
    clock.tick(60)

# if __name__ == '__main__':
#     main()
