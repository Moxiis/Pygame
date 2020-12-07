import pygame
import time
import random
pygame.font.init()

# setting screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#image variables (WIDTH and HEIGHT - CONST)
LASER_WIDTH = 16
LASER_HEIGHT = 16
EXPLOSION_WIDTH = 60
EXPLOASION_HEIGHT = 60
ENEMY_WIDTH = 45
ENEMY_HEIGHT = 45
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

# setting name and icon to our pygame
pygame.display.set_caption("Space")
icon = pygame.image.load("images\ship.png")
pygame.display.set_icon(icon)

#Images
playerImage = pygame.image.load("images\ship.png")
playerlaser_image = pygame.image.load("images\laser_Player.png")
enemylaser_image = pygame.image.load("images\laser_Enemy.png")
explosion_image = [pygame.transform.scale(pygame.image.load("images\explosion1.png"), (EXPLOSION_WIDTH, EXPLOASION_HEIGHT)), pygame.transform.scale(pygame.image.load("images\explosion2.png"), (EXPLOSION_WIDTH, EXPLOASION_HEIGHT)), pygame.transform.scale(pygame.image.load("images\explosion3.png"), (EXPLOSION_WIDTH, EXPLOASION_HEIGHT)), pygame.transform.scale(pygame.image.load("images\explosion4.png"), (EXPLOSION_WIDTH, EXPLOASION_HEIGHT)), pygame.transform.scale(pygame.image.load("images\explosion5.png"), (EXPLOSION_WIDTH, EXPLOASION_HEIGHT))]
tiefighter_Image = pygame.transform.scale(pygame.image.load("images\star_Fighter.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
tiebomber_Image = pygame.transform.scale(pygame.image.load("images\star_Bomber.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
destroyer_Image = pygame.transform.scale(pygame.image.load("images\destroyer.png"), (3 * ENEMY_WIDTH, 3 * ENEMY_HEIGHT))
background = pygame.transform.scale(pygame.image.load("images\space.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# laser class(overall)
class laser:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = None

	def draw(self):
		screen.blit(self.image, (int(self.x), int(self.y)))

	def move(self,player_vel):
		self.y -= player_vel

# Ship class(overall)
class ship:
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.health = 1
		self.speed = None
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.laser_cooldown = 0

	def draw(self):
		screen.blit(self.ship_img, (int(self.x), int(self.y)))

# Explosion class
class explosion:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.image = explosion_image
		self.count = 0
		self.remove = False

	def draw(self):
		if self.count >= 25:
			self.remove = True
		else:
			screen.blit(self.image[self.count//5], (int(self.x), int(self.y)))
			self.count += 1


# player class
class player_Ship(ship):
	def __init__(self, x, y):

		super().__init__(x,y,type)
		self.health = 3
		self.speed = 5
		self.ship_img = playerImage
		self.laser_img = playerlaser_image
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.lost_life = False
		self.FLICKERING_LONG = 15
		self.FLICKERING_TIMES = 10
		self.flickering_long = self.FLICKERING_LONG
		self.flickering_times = self.FLICKERING_TIMES


	def death(self):
		global key_disabled
		if self.flickering_times <= 0:
			self.lost_life = False
			self.flickering_times = self.FLICKERING_TIMES
			self.flickering_long = self.FLICKERING_LONG
			key_disabled = False
		elif self.flickering_long <= 0:
			self.flickering_times -= 1
			self.flickering_long = self.FLICKERING_LONG
		elif self.flickering_long > 0 and self.flickering_times % 2 == 1:
			self.flickering_long -= 1
		elif self.flickering_long > 0 and self.flickering_times % 2 == 0:
			screen.blit(self.ship_img, (int(self.x), int(self.y)))
			self.flickering_long -= 1


#player laser
class player_laser(laser):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image = playerlaser_image
		self.mask = pygame.mask.from_surface(self.image)

# enemy ship class
class enemy_Ship(ship):
	ship_Type = {
		"Fighter" : tiefighter_Image,
		"Bomber" : tiebomber_Image,
		"Destroyer" : destroyer_Image
				}
	Right = True

	def __init__(self,x,y,type):
		super().__init__(x,y,type)
		self.ship_img = self.ship_Type[type]
		self.laser_img = enemylaser_image
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self,player_vel):
		if self.x >= SCREEN_WIDTH - ENEMY_WIDTH:
			self.Right = False
		if 	self.x <= 0:
			self.Right = True
		if self.type == "Fighter" and self.Right == True:
			self.y += player_vel / 2
			self.x += player_vel * 2
		elif self.type == "Fighter" and self.Right == False:
			self.y += player_vel / 2
			self.x += - player_vel * 2
		else:
			self.y += player_vel

# enemy laser
class enemy_laser:
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image = enemylaser_image
		self.mask = pygame.mask.from_surface(self.image)

def main():
	# variables
	game = True
	FPS = 60
	level = 1
	lives = 5
	enemys_Number = 5 + level * 2
	player_vel = 5
	enemies = []
	explosions = []

	clock = pygame.time.Clock()

	# initializing game font
	gamefont = pygame.font.SysFont("Bookman Old Style", 30)
	game_over_font = pygame.font.SysFont("Arial", 60)
	# initializing player
	player = player_Ship(SCREEN_WIDTH / 2 - 32, SCREEN_HEIGHT * 0.85)

	def redraw():
		screen.blit(background,(0,0))
		level_Label = gamefont.render("Level:" + str(level), 1, (255, 255, 255))
		live_Label = gamefont.render("Live:" + str(lives), 1, (255, 255, 255))
		screen.blit(level_Label,(5,5))
		screen.blit(live_Label, (SCREEN_WIDTH - level_Label.get_width() + 10, 5))
		for enemy in enemies:
			enemy.move(player_vel / 2)
			enemy.draw()
		for laser in player.lasers:
			laser.move(player_vel)
			laser.draw()
		for explo in explosions:
			if explo.remove == True:
				explosions.remove(explo)
			else:
				explo.draw()
		if player.lost_life == False:
			player.draw()
		else:
			player.death()
		pygame.display.update()

	while game:
		clock.tick(FPS)
		redraw()

		# creating enemys
		if enemies == []:
			for i in range(enemys_Number):
				enemies.append(enemy_Ship(random.randrange(0, SCREEN_WIDTH - ENEMY_WIDTH), random.randrange(- 1000, - 200), random.choice(["Fighter", "Bomber"])))


		# iterating over all events store in pygame.event.get
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game = False


		# Movement events
		keys = pygame.key.get_pressed()
		if keys[pygame.K_DOWN] and player.y <= SCREEN_HEIGHT - playerImage.get_height():
			player.y += player.speed
		if keys[pygame.K_UP] and player.y >= 0:
			player.y += -player.speed
		if keys[pygame.K_RIGHT] and player.x <= SCREEN_WIDTH - playerImage.get_width():
			player.x += player.speed
		if keys[pygame.K_LEFT] and player.x >= 0:
			player.x += -player.speed
		# Shooting
		if keys[pygame.K_SPACE] and player.laser_cooldown == 0:
			player.laser_cooldown = 10
			player.lasers.append(player_laser(player.x + PLAYER_WIDTH / 2 - 8, player.y))
		# Turbo
		if keys[pygame.K_LSHIFT]:
			player.speed = 10
		if keys[pygame.K_LSHIFT] != True:
			player.speed = 5

		# logic:
		# game over:
		if lives == 0:
			game_over_label = game_over_font.render("Game over", 1, (255,255,255))
			screen.blit(game_over_label, (SCREEN_WIDTH / 2 - game_over_label.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_label.get_height()))
			pygame.display.update()
			time.sleep(3)
			game = False
		# enemy death by falling and enemy laser detect
		for enemy in enemies:
			if player.mask.overlap(enemy.mask, (int(enemy.x) - int(player.x),int(enemy.y) - int(player.y))) != None:
				explosions.append(explosion(enemy.x, enemy.y))
				explosions.append(explosion(player.x, player.y))
				enemies.remove(enemy)
				player.health -= 1
				player.x = SCREEN_WIDTH / 2 - 32
				player.y = SCREEN_HEIGHT * 0.85
				key_disabled = True
				player.lost_life = True
			for laser in player.lasers:
				if laser.mask.overlap(enemy.mask, (int(enemy.x) - int(laser.x),int(enemy.y) - int(laser.y))) != None:
					player.lasers.remove(laser)
					explosions.append(explosion(enemy.x, enemy.y))
					enemies.remove(enemy)
				if laser.y <= 0:
					player.lasers.remove(laser)
			if enemy.y >= SCREEN_HEIGHT:
				enemies.remove(enemy)
				lives -= 1
		# laser cooldown decrease
		if player.laser_cooldown != 0:
			player.laser_cooldown -= 1
		# increase level
		if len(enemies) == 0:
			level += 1


main()
