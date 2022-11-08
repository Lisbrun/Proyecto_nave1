
import pygame, random, time

from sympy import true

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
MORADO= (128,0,128)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


def draw_text(surface, text, size, x, y,color):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.velocidad=5

		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -self.velocidad
		if keystate[pygame.K_RIGHT]:
			self.speed_x = self.velocidad
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

class poder(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("rayo3.png").convert() 
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x= random.randrange(700)
		self.rect.y= random.randrange(20)
		self.speed_y = 3


	def update(self):
		self.rect.y += self.speed_y

def crearpoder():
	for i in range(1):
		habilidad= poder()
		all_sprites.add(habilidad)
		sprite_list_poderes.add(habilidad)

class corazon(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load("corazon.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x= random.randrange(700)
		self.rect.y= random.randrange(20)
		self.speed_y = 3

	def update(self):
		self.rect.y += self.speed_y

def crearcorazon():
	for i in range(1):
		corazonpoder= corazon()
		all_sprites.add(corazonpoder)
		sprite_corazon.add(corazonpoder)
	
def generarpoderes():
	z= random.randrange(2)
	if z==0:
		crearpoder()
	elif z==1:
		crearcorazon()


class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22 :
			self.rect.x = random.randrange(WIDTH - self.rect.width)

			#Change this variable
			self.rect.y = random.randrange(-150, -100)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill() # if we get to the end of the animation we don't keep going.
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


def show_go_screen():
	screen.blit(background, [0, 0])
	draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT / 4, WHITE)
	draw_text(screen, "(Instructions)", 27, WIDTH // 2, HEIGHT // 2, WHITE)
	draw_text(screen, "Press key to begin", 17, WIDTH // 2, HEIGHT * 3/4, WHITE)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())

## --------------- CARGAR IMAGENES EXPLOSIÓN -------------------------- ##
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)



background = pygame.image.load("assets/background.png").convert()


laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.1)

inicial=time.time()

tiempojuego=time.time()
choque= 0
colision_hecha=0
game_over = True
running = True
while running:
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		habilidad= poder()
		player = Player()
		all_sprites.add(player)
		sprite_list_poderes=pygame.sprite.Group()
		sprite_corazon= pygame.sprite.Group()
		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)

	
		score = 0

	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
		
	tiempo=time.time()-inicial
	z=round(tiempo,0)
	print(z)
	if z==10:
		generarpoderes()
		inicial= time.time()
	colision = pygame.sprite.spritecollide(player,sprite_corazon,True)
	for coli in colision:
		colision_hecha +=1
	if colision_hecha==1:
		player.shield=100
		colision_hecha=0

	hits = pygame.sprite.spritecollide(player,sprite_list_poderes,True)
	for hit in hits:
		choque+=1
		actual=time.time()
	if choque==1:
		if time.time()-actual<6:
			player.velocidad=10

		else:
			player.velocidad=5
			actual=0
			choque=0



		
		


	all_sprites.update()

	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 1
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

		



	hits = pygame.sprite.spritecollide(player, meteor_list, True) # Change here
	for hit in hits:
		player.shield -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			#running = False


			game_over = True


	screen.blit(background, [0, 0])
	all_sprites.draw(screen)

	tiempodejuego=time.time()-tiempojuego
	timellevado=round(tiempodejuego,0)

	draw_text(screen, str(score), 25, WIDTH // 2, 10, BLACK)
	draw_text(screen, str(timellevado), 25, 750, 30, MORADO)		



	draw_shield_bar(screen, 5, 5, player.shield)


	pygame.display.flip()

pygame.quit()
