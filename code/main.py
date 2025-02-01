import pygame, sys
from car import Car
from settings import *
from player import Player
from random import choice
from sprite import Sprite, Sprite2

pygame.font.init()

class Sprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.background = pygame.image.load('../graphics/main/map.png')

    def vykresli(self):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        display.blit(self.background, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            display.blit(sprite.image, offset_position)

# Koniec hry
loading_screen = pygame.image.load('../graphics/main/over.jpg')
restart_font = pygame.font.Font('freesansbold.ttf', 40)
restart_text = restart_font.render("Stlač [R] pre reštart", True, "White")
restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))

# Font
font = pygame.font.Font('freesansbold.ttf', 50)
text_surface = font.render("Vyhral si! ", True, "White")
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# Zoznam všetkých spritov
sprites = Sprites()
obstacles = pygame.sprite.Group()

# Setup
pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hihi")
clock = pygame.time.Clock()

player = Player((2062, 2200), sprites, obstacles)

# Hudba
#hudba = pygame.mixer.Sound('../audio/music.mp3')
#hudba.set_volume(0.5)
#hudba.play(loops=-1)

# Timer
timer = pygame.event.custom_type()
pygame.time.set_timer(timer, 20)

pozicie = []

# Pridanie objektov
for file, position in SIMPLE_OBJECTS.items():
    cesta = f'../graphics/objects/simple/{file}.png'
    surface = pygame.image.load(cesta)
    for pos in position:
        Sprite(surface, pos, [sprites, obstacles])

for file, position in LONG_OBJECTS.items():
    cesta = f'../graphics/objects/long/{file}.png'
    surface = pygame.image.load(cesta)
    for pos in position:
        Sprite2(surface, pos, [sprites, obstacles])

# Pridanie koncového objektu
end_image = pygame.image.load('../graphics/main/vlajka.png')
end_image = pygame.transform.scale(end_image, (150, 150))
end_sprite = pygame.sprite.Sprite()
end_sprite.image = end_image
end_sprite.rect = end_image.get_rect(topleft=(1550, 1050))
end_sprite.rect.width /= 2 ; end_sprite.rect.height /= 2
sprites.add(end_sprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == timer:
            pozicia_auta = choice(CAR_START_POSITIONS)
            if pozicia_auta not in pozicie:
                pozicie.append(pozicia_auta)
                Car(pozicia_auta, [sprites, obstacles])
            if len(pozicie) > 15:
                del pozicie[0]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and player.game_over:
                player.game_over = False
                player.position = pygame.math.Vector2(2062, 6000)
                player.direction = pygame.math.Vector2()
                #hudba.play(loops=-1)
                pozicie.clear()
                for sprite in sprites.sprites():
                    if hasattr(sprite, 'meno') and sprite.meno == 'auto':
                        sprite.kill()

    # deltatime
    dt = clock.tick() / 1000

    if not player.game_over:
        display.fill((0, 0, 0))
        sprites.update(dt)
        sprites.vykresli()

        # Kontrola kolízie s end_sprite
        if player.rect.colliderect(end_sprite.rect):
            player.game_over = True
        if player.position.y <= 900:
            player.position.y = 900

    else:
        #hudba.stop()
        display.blit(loading_screen, (0, 0))
        display.blit(restart_text, restart_text_rect)

    pygame.display.update()