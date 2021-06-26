import pygame
import sys
from random import randint
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.colour = (255, 255, 255)
        self.length = 3
        self.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
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


class Food(Snake):
    def __init__(self, pic_path, snake_class):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.position = self.spawn(snake_class)

    @staticmethod
    def spawn(snake_class):
        """ Ensures food spawn won't collide with snake """

        exclude_x = exclude_y = []
        for pos in snake_class.positions:
            exclude_x.append(pos.x)
            exclude_y.append(pos.y)

        x = randint(0, GRID_NUM - 1)
        y = randint(0, GRID_NUM - 1)
        while x in exclude_x or y in exclude_y:
            if x in exclude_x:
                x = randint(0, GRID_NUM - 1)
            if y in exclude_y:
                y = randint(0, GRID_NUM - 1)

        return Vector2(x, y)

    def draw(self):
        food_rect = pygame.Rect(int(self.position.x * GRID_SIZE),
                                int(self.position.y * GRID_SIZE), GRID_SIZE,
                                GRID_SIZE)
        screen.blit(self.image, food_rect)


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

    food.draw()

    pygame.display.update()
    clock.tick(60)

# if __name__ == '__main__':
#     main()
