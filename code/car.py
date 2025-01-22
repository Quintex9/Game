import pygame
from os import walk
from random import choice

class Car(pygame.sprite.Sprite):
    def __init__(self, position,groups):
        super().__init__(groups)

        self.meno = 'auto'

        for folder, sub_folder, image in walk('../graphics/cars'):
            car = choice(image)

        self.image = pygame.image.load('../graphics/cars/' + car)
        self.rect = self.image.get_rect(center=position)

        self.position = pygame.math.Vector2(self.rect.center)

        if position[0] < 200:
            self.direction = pygame.math.Vector2(1,0)
        else:
            self.direction = pygame.math.Vector2(-1,0)
            self.image = pygame.transform.flip(self.image, True, False)

        self.speed = 200

        self.hitbox = self.rect.inflate(0,-self.rect.height/2)

    def update(self,dt):
        self.position += self.direction * self.speed * dt
        self.hitbox.center = (round(self.position.x), round(self.position.y))
        self.rect.center = self.hitbox.center

        if not -200 < self.rect.x < 3400:
            self.kill()