import pygame, sys
from car import Car

from settings import *
from player import Player
from random import choice
from sprite import Sprite, Sprite2

class Sprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = pygame.math.Vector2()
		self.background = pygame.image.load('../graphics/main/map.png')

	def vykresli(self):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		display.blit(self.background, - self.offset)

		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_position = sprite.rect.topleft - self.offset
			display.blit(sprite.image, offset_position)

pygame.font.init()
#font
font = pygame.font.Font('freesansbold.ttf', 50)
text_surface = font.render("Vyhral si! ",True,"White")
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# zoznam všetkých spritov
sprites = Sprites()
#len na pozeranie collisions
obstacles = pygame.sprite.Group()

#setup
pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hihi")
clock = pygame.time.Clock()

player = Player((2062,6000),sprites,obstacles)

#hudba
hudba = pygame.mixer.Sound('../audio/music.mp3')
hudba.set_volume(20)
hudba.play(loops=-1)

#timer
timer = pygame.event.custom_type()
pygame.time.set_timer(timer, 100)

pozicie = []

for file, position in SIMPLE_OBJECTS.items():
	cesta = f'../graphics/objects/simple/{file}.png'
	surface = pygame.image.load(cesta)
	for pos in position:
		Sprite(surface,pos,[sprites,obstacles])

for file,position in LONG_OBJECTS.items():
	cesta = f'../graphics/objects/long/{file}.png'
	surface = pygame.image.load(cesta)
	for pos in position:
		Sprite2(surface,pos,[sprites,obstacles])

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == timer:
			pozicia_auta = choice(CAR_START_POSITIONS)
			if pozicia_auta not in pozicie:
				#aby sa nespawnli 2 auta na sebe/ moc pri sebe
				pozicie.append(pozicia_auta)
				Car(pozicia_auta, [sprites,obstacles])
			if len(pozicie) > 5:
				del pozicie[0]

	# deltatime
	dt = clock.tick() / 1000

	display.fill((0,0,0))

	if player.position.y >= 1000:
		#update
		sprites.update(dt)
		sprites.vykresli()
	else:
		hudba.stop()
		display.fill("teal")
		display.blit(text_surface,text_rect)

	pygame.display.update()
