import pygame

# from pygame.math import Vector2


class Snake(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.rect = self.image.get_rect(x_pos, y_pos)

    def update(self, direction):
        pass

    def grow(self):
        pass


class Morsel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
