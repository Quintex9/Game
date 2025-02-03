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

# umrtie
loading_screen = pygame.image.load('../graphics/main/over.jpg')
restart_font = pygame.font.Font('freesansbold.ttf', 40)
restart_text = restart_font.render("Stlač [R] pre reštart", True, "White")
restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))

#vyhra
victory = pygame.image.load('../graphics/main/victory.jpg')
victory = pygame.transform.scale(victory, (WINDOW_WIDTH, WINDOW_HEIGHT))
victory_font = pygame.font.Font('freesansbold.ttf', 40)
victory_text = restart_font.render("Stlač [R] ak chceš ísť ešte raz", True, "White")
victory_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH / 2 -50, WINDOW_HEIGHT / 2 + 250))


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

player = Player((1700, 12500), sprites, obstacles)

# Hudba
hudba = pygame.mixer.Sound('../audio/music.mp3')
hudba.set_volume(0.5)
hudba.play(loops=-1)

# Timer
timer = pygame.event.custom_type()
pygame.time.set_timer(timer, 25)

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

# časovač na štart
start_timer = pygame.time.get_ticks()
move_allowed = False
game_started = False
last_countdown_update = 0  # Pomocná premenná na update raz za sekundu

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == timer:
            pozicia_auta = choice(CAR_START_POSITIONS)
            if pozicia_auta not in pozicie:
                pozicie.append(pozicia_auta)
                Car(pozicia_auta, [sprites, obstacles])
            if len(pozicie) > 12:
                del pozicie[0]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and player.game_over:
                player.game_over = False
                player.position = pygame.math.Vector2(1700, 12500)
                player.direction = pygame.math.Vector2()
                pozicie.clear()
                hudba.play(loops=-1)
                for sprite in sprites.sprites():
                    if hasattr(sprite, 'meno') and sprite.meno == 'auto':
                        sprite.kill()

                game_started = False
                move_allowed = False
                start_timer = pygame.time.get_ticks()

    # deltatime
    dt = clock.tick(60) / 1000

    display.fill((0, 0, 0))
    sprites.update(dt)
    sprites.vykresli()

    if not game_started:
        elapsed_time = current_time - start_timer
        countdown = max(0, (7000 - elapsed_time) // 1000 + 1)

        if countdown > 0:
            if current_time - last_countdown_update >= 1000:
                last_countdown_update = current_time  # Aktualizácia každú sekundu

            countdown_text = font.render(f"{countdown}", True, "White")
            text_rect = countdown_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            display.blit(countdown_text, text_rect)
            player.position.x = 1700 ; player.position.y = 12500
        else:
            game_started = True
            move_allowed = True

    elif not player.game_over:
        # Kontrola kolízie s end_sprite
        if player.rect.colliderect(end_sprite.rect):
            player.game_over = True
            player.won = True
        if player.position.y <= 900:
            player.position.y = 900

    elif player.game_over:
        hudba.stop()
        if player.won:
            display.blit(victory, (0, 0))
            display.blit(victory_text, victory_text_rect)
        else:
            display.blit(loading_screen, (0, 0))
            display.blit(restart_text, restart_text_rect)
    pygame.display.update()
