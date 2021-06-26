import pygame
import sys
from random import randint
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.colour = (255, 255, 255)
        self.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.ate_food = False
        self.sfx = pygame.mixer.Sound('bite.mp3')
        self.score = 0

    def draw(self):
        for pos in self.positions:
            pos_x = int(pos.x * GRID_SIZE)
            pos_y = int(pos.y * GRID_SIZE)
            pos_rect = pygame.Rect(pos_x, pos_y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.colour, pos_rect)

    def move(self):
        if not self.ate_food:
            self.positions = self.positions[:-1]
            self.positions.insert(0, self.positions[0] + self.direction)
        else:
            self.positions = self.positions[:]
            self.positions.insert(0, self.positions[0] + self.direction)
            self.ate_food = False

    def play_sfx(self):
        self.sfx.play()


class FOOD(SNAKE):
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
                                int(self.position.y * GRID_SIZE),
                                GRID_SIZE, GRID_SIZE)
        screen.blit(self.image, food_rect)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD('img/apple.png', self.snake)

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_lose()

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def check_collision(self):
        if self.food.position == self.snake.positions[0]:
            self.snake.score += 1
            self.food.position = self.food.spawn(self.snake)
            self.snake.play_sfx()
            self.snake.ate_food = True

    def check_lose(self):
        # touch border
        if not (0 <= self.snake.positions[0].x < GRID_NUM) \
                or not (0 <= self.snake.positions[0].y < GRID_NUM):
            self.game_over()

        # head touches body
        for pos in self.snake.positions[1:]:
            if pos == self.snake.positions[0]:
                self.game_over()

    @staticmethod
    def game_over():
        pygame.quit()
        sys.exit()


pygame.init()

FOOD_PX = GRID_SIZE = 32
GRID_NUM = 20
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * GRID_NUM, GRID_SIZE * GRID_NUM

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Snake')
icon = pygame.image.load('img/snake.png').convert_alpha()
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.direction = UP
            elif event.key == pygame.K_DOWN:
                game.snake.direction = DOWN
            elif event.key == pygame.K_LEFT:
                game.snake.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                game.snake.direction = RIGHT

    screen.fill((0, 0, 0))

    game.draw()

    pygame.display.update()
    clock.tick(60)

# if __name__ == '__main__':
#     main()
