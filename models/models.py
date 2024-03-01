import pygame
from pygame.math import Vector2


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


class Lazer(pygame.sprite.Sprite):
    def __init__(self, position, speed, height) -> None:
        super().__init__()
        self.image = pygame.Surface((6,30))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.height_y_constraint = height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()