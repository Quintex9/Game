import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self,surface,position,groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-self.rect.height/2) #zmena rozmerov

class Sprite2(pygame.sprite.Sprite):
    def __init__(self,surface,position,groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.8,-self.rect.height / 2)
        self.hitbox.bottom = self.rect.bottom - 10