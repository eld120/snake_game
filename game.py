import random

import pygame
from pygame.math import Vector2


class Snake(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        super().__init__()

        self.direction = Vector2(0, 0)
        self.head = Vector2(5, 10)
        self.tail = Vector2(3, 10)
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.new_segment = False

        self.head_vertical = pygame.image.load("assets/body_vert.png").convert_alpha()
        self.head_horizontal = pygame.image.load("assets/body_horiz.png").convert_alpha()
        self.tail_vertical = pygame.image.load("assets/body_vert.png").convert_alpha()
        self.tail_horizontal = pygame.image.load("assets/body_horiz.png").convert_alpha()
        self.body_vertical = pygame.image.load("assets/body_vert.png").convert_alpha()
        self.body_horizontal = pygame.image.load("assets/body_horiz.png").convert_alpha()

    def update(self, direction):
        self.direction.x += direction

    def grow(self):
        pass

    def render_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, segment in enumerate(self.body):
            # breakpoint()
            x_pos = int(segment.x * cell_size)
            y_pos = int(segment.y * cell_size)
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else:
                prev = self.body[index + 1] - segment
                next = self.body[index - 1] - segment
                if prev.x == next.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif prev.y == next.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    pass
                    # contains rendering of smooth turns that I don't have graphics for
                    # if prev.x == -1 and next.y == -1 or prev.y == -1 and next.x == -1:
                    #     screen.blit(self.body)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_horizontal
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_horizontal
        elif head_relation == Vector2(0, 1):
            self.head = self.head_vertical
        elif head_relation == Vector2(0, -1):
            self.head = self.head_vertical

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_horizontal
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_horizontal
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_vertical
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_vertical

    def move(self):
        if self.new_segment:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_segment = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_segment(self):
        self.new_segment = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Morsel(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.random_fruit_spreader()

    def draw_morsel(self):
        morsel_rect = pygame.Rect(
            int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size
        )
        pygame.draw.rect(screen, (126, 166, 114), morsel_rect)

    def random_fruit_spreader(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x)


class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18

    def update(self):
        self.walk()

    def walk(self):
        new_position = self.rect.move((self.move, 0))
        if not self.area.contains(new_position):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                new_position = self.rect.move((self.move, 0))


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.morsel = Morsel()

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()

    def draw_stuff(self):
        self.morsel.draw_morsel()
        self.snake.render_snake()
        # self.draw_score()

    def check_collision(self):
        if self.morsel.position == self.snake.body[0]:
            self.morsel.random_fruit_spreader()
            self.snake.add_segment()

        for block in self.snake.body[1:]:
            if block == self.morsel.position:
                self.morsel.random_fruit_spreader()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()


pygame.init()
# screen = pygame.display.set_mode((1280, 720))

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

clock = pygame.time.Clock()
running = True

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()


if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)

        # screen.fill("black")

        screen.fill((175, 215, 70))
        main_game.draw_stuff()
        pygame.display.update()

        # pygame.display.flip()

        clock.tick(60)

    pygame.quit()
