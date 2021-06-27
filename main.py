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
        self.sfx = pygame.mixer.Sound('sfx/bite.mp3')
        self.score = 0

    def draw_snake(self):
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

    def reset(self):
        self.positions = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.score = 0


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

    def draw_food(self):
        food_rect = pygame.Rect(int(self.position.x * GRID_SIZE),
                                int(self.position.y * GRID_SIZE),
                                GRID_SIZE, GRID_SIZE)
        screen.blit(self.image, food_rect)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD('img/apple.png', self.snake)
        self.lose = False

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_lose()

    def draw(self):
        self.snake.draw_snake()
        self.food.draw_food()
        self.display_score()

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

    def game_over(self):
        self.lose = True

    @staticmethod
    def game_over_menu():
        lose_font = pygame.font.Font(None, 60)
        lose_surface = lose_font.render('GAME OVER!', True, (250, 250, 250))
        lose_x = int(SCREEN_WIDTH / 2)
        lose_y = int(SCREEN_HEIGHT / 2 - 2 * GRID_SIZE)
        lose_rect = lose_surface.get_rect(center=(lose_x, lose_y))

        restart_font = pygame.font.Font(None, 32)
        restart_surface = restart_font.render('Restart with Spacebar', True,
                                              (250, 250, 250))
        restart_x = lose_x
        restart_y = lose_y + 2 * GRID_SIZE
        restart_rect = restart_surface.get_rect(center=(restart_x, restart_y))

        bg_rect = pygame.Rect(restart_rect.left - 5, restart_rect.top - 5,
                              restart_rect.width + 10, restart_rect.height + 5)

        pygame.draw.rect(screen, (93, 93, 93), bg_rect)
        screen.blit(restart_surface, restart_rect)
        screen.blit(lose_surface, lose_rect)

    def display_score(self):
        score_font = pygame.font.Font(None, 30)

        score = f'Score: {str(self.snake.score)}'
        score_surface = score_font.render(score, True, (250, 250, 250))
        score_x = int(SCREEN_WIDTH - 60)
        score_y = int(SCREEN_HEIGHT - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        screen.blit(score_surface, score_rect)


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

        if not game.lose and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = UP

            if event.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = DOWN

            if event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = LEFT

            if event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = RIGHT

        if game.lose:
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE:
                    game.lose = False
                    game.snake.reset()

    screen.fill((0, 0, 0))

    game.draw()

    if game.lose:
        game.game_over_menu()

    pygame.display.update()
    clock.tick(60)

# if __name__ == '__main__':
#     main()
