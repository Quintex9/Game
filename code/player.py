import pygame,sys
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self,position,groups,collisions):
        super().__init__(groups)
        self.game_over = False

        self.obrazky()
        self.index = 0
        self.poz = 'down'
        self.image = self.animations[self.poz][self.index]
        self.rect = self.image.get_rect(center = position)

        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

        #collisions
        self.collisions = collisions
        self.hitbox = self.rect.inflate(0,-self.rect.height/2)

    def hranice(self):
        if self.rect.left < 640:
            self.position.x = 640 + self.rect.width/2
            self.hitbox.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.position.x = 2560 - self.rect.width/2
            self.hitbox.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 6100:
            self.position.y = 6100 - self.rect.height/2
            self.hitbox.centery = self.rect.centery
            self.rect.bottom = 6100

    def collision(self,dir):
        if dir == 'horizontalne':
            for sprite in self.collisions.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    #najprv či existuje atribut a potom meno
                    if hasattr(sprite,'meno') and sprite.meno == 'auto':
                        self.game_over = True

                    if self.direction.x > 0:  #pohyb vpravo
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx #pri pohybe hrača do long objektu to triaslo obraz tak tu je fix
                        self.position.x = self.hitbox.centerx
                    if self.direction.x < 0:  #pohyb vlavo
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.position.x = self.hitbox.centerx
        else:
            if dir == 'vertikalne':
                for sprite in self.collisions.sprites():
                    if sprite.hitbox.colliderect(self.hitbox):
                        if hasattr(sprite,'meno') and sprite.meno == 'auto':
                            self.game_over = True

                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                            self.rect.centery = self.hitbox.centery
                            self.position.y = self.hitbox.centery
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                            self.rect.centery = self.hitbox.centery
                            self.position.y = self.hitbox.centery

    def obrazky(self):
        self.animations = {}
        for index,folder in enumerate(walk('../graphics/player')):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file in folder[2]:
                    cesta = folder[0].replace('\\','/') + '/' + file
                    surface = pygame.image.load(cesta)
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surface)



    def move(self,dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.position.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.position.x) #toto pre kolízie
        self.rect.centerx = self.hitbox.centerx # toto pre kreslenie
        self.collision('horizontalne')

        self.position.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertikalne')


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.poz = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.poz = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.poz = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.poz = 'down'
        else:
            self.direction.y = 0

    def pohyb(self,dt):
        current = self.animations[self.poz]

        if self.direction.magnitude() != 0:
            self.index += 10 * dt
            if self.index >= len(current):
                self.index = 0
        else:
            self.index = 0

        self.image = current[int(self.index)] #obrazky maju cele čísla nie floaty

    def update(self,dt):
        self.input()
        self.move(dt)
        self.pohyb(dt)
        self.hranice()

