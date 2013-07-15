import sys, os, random, time
import pygame
from spriteAnim import SpriteStripAnim

def load_image(name, colorKey=None):
	try:
		image = pygame.image.load(name)
	except pygame.error, message:
		print 'Cannot load image:', name 
		raise SystemExit, message
	image = image.convert()
	if colorKey is not None:
		if colorKey is -1:
		 	colorKey = image.get_at((0, 0))
		image.set_colorkey(colorKey, pygame.RLEACCEL)
	return image, image.get_rect()


class Block(pygame.sprite.Sprite):
	def __init__(self, posX, posY,
			     blockImage):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(blockImage, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY


class Coin(pygame.sprite.Sprite):
	def __init__(self, posX, posY,
				 coinImage):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(coinImage, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY 


class Pacman(pygame.sprite.Sprite):
	ORIENT_LEFT = 0
	ORIENT_RIGHT = 1
	ORIENT_UP = 2
	ORIENT_DOWN = 3

	def __init__(self, posX, posY, newSpeed,
				 pacmanImage):
		pygame.sprite.Sprite.__init__(self)
		self.anim =\
				SpriteStripAnim(pacmanImage, (0, 0, 20, 20),
						3, -1, True, 10)
		self.anim.iter()
		self.image = self.anim.next()	
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.speed = newSpeed 
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY
		self.score = 0
		self.orientation = self.ORIENT_RIGHT

	def update(self):
		self.image = self.anim.next()
		self._updateOrientation()
		self._collideWithGhosts()
		if self.score >= pacmanLevel.allCoins:
			print 'won!!!'

	def move(self, dx, dy):
		if dx == 1:
			dx = self.speed
		if dx == -1:
			dx = -self.speed
		if dy == 1:
			dy = self.speed
		if dy == -1:
			dy = -self.speed

		if dx != 0:
			self._moveSingleAxis(dx, 0)
			if dx > 0:
				self.orientation = self.ORIENT_RIGHT
			if dx < 0:
				self.orientation = self.ORIENT_LEFT
		if dy != 0:
			self._moveSingleAxis(0, dy)
			if dy > 0:
				self.orientation = self.ORIENT_DOWN
			if dy < 0:
				self.orientation = self.ORIENT_UP

	def _updateOrientation(self):
		if self.orientation == self.ORIENT_DOWN:
			self.image = pygame.transform.rotate(self.image, 90)
		elif self.orientation == self.ORIENT_UP:
			self.image = pygame.transform.rotate(self.image, -90)
		elif self.orientation == self.ORIENT_RIGHT:
			self.image = pygame.transform.rotate(self.image, 180)
		elif self.orientation == self.ORIENT_LEFT:
			self.image = pygame.transform.rotate(self.image, 0)

	def _moveSingleAxis(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy

		self._collideWithWalls(dx, dy)
		self._collideWithCoins()
		self._collideWithGhostEaters()
		
	def _collideWithWalls(self, dx, dy):
		collidedSprite =\
				pygame.sprite.spritecollideany(self,\
						pacmanLevel.levelWallGroup)
		if collidedSprite is not None:
			if dx > 0:
				self.rect.right = collidedSprite.rect.left
			if dx < 0:
				self.rect.left = collidedSprite.rect.right
			if dy > 0:
				self.rect.bottom = collidedSprite.rect.top
			if dy < 0:
				self.rect.top = collidedSprite.rect.bottom

	def _collideWithCoins(self):
		collidedSprite =\
				pygame.sprite.spritecollideany(self,\
						pacmanLevel.levelCoinGroup)
		if collidedSprite is not None:
			collidedSprite.kill()
			self.score = self.score + 1
		
	def _collideWithGhostEaters(self):
		collidedSprite =\
				pygame.sprite.spritecollideany(self,\
						pacmanLevel.levelGhostEaterGroup)
		if collidedSprite is not None:		
			for ghost in pacmanLevel.levelGhostGroup.sprites():
				ghost.isEaten = 1
				ghost.eatenClock = time.time()
			collidedSprite.kill()
	
	def _collideWithGhosts(self):
		collidedSprite =\
				pygame.sprite.spritecollideany(self,\
						pacmanLevel.levelGhostGroup)
		if collidedSprite is not None:
			if collidedSprite.isEaten == 0:
				self.kill()
			else:
				collidedSprite.isAte = 1


class Ghost(pygame.sprite.Sprite):
	MOVE_LEFT = 1
	MOVE_RIGHT = 2
	MOVE_UP = 3
	MOVE_DOWN = 4

	def __init__(self, posX, posY,\
			     regularSpritesheet, eatenSpritesheet, eyeSpritesheet):
		pygame.sprite.Sprite.__init__(self)
		self.regSpritesheet = regularSpritesheet
		self.eatSpritesheet = eatenSpritesheet
		self.eyeSpritesheet = eyeSpritesheet
		self.anim =\
				SpriteStripAnim(regularSpritesheet, (0, 0, 20, 20),
						5, -1, True, 20)
		self.anim.iter()
		self.image = self.anim.next()	
		self.rect = self.image.get_rect()
		self.pos = [posX, posY]
		self.speed = 1
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY
		self.direction = self.MOVE_UP
		self.isEaten = 0
		self.isAte = 0
		self.isSwitched = 0
		self.eatenClock = 0
		self.respawnClock = 0

	def update(self):
		if self.isAte == 1:
			self.respawnClock = time.time()
			self.anim =\
					SpriteStripAnim(self.eyeSpritesheet, (0, 0, 20, 20),
							5, -1, True, 20)
		if (time.time() - self.respawnClock) > 3 and self.isAte == 1:
			self.anim =\
					SpriteStripAnim(self.regSpritesheet, (0, 0, 20, 20),
							5, -1, True, 20)
			self.respawnClock = 0		
			self.isAte = 0
		if (time.time() - self.eatenClock) > 3 and self.isEaten == 1:
			self.isEaten = 0
			self.isSwitched = 0
		if self.isEaten == 1 and self.isSwitched == 0:
			self.anim =\
					SpriteStripAnim(self.eatSpritesheet, (0, 0, 20, 20),
							5, -1, True, 20)
			self.anim.iter()		
			self.isSwitched = 1
		elif self.isSwitched == 0:
			self.anim =\
					SpriteStripAnim(self.regSpritesheet, (0, 0, 20, 20),
							5, -1, True, 20)
			self.anim.iter()		
			self.isSwitched = 0
		self.image = self.anim.next()
		if self.direction == self.MOVE_LEFT:
			self.rect.x -= self.speed
			self._collideWithWalls(-self.speed, 0)
		if self.direction == self.MOVE_RIGHT:
			self.rect.x += self.speed
			self._collideWithWalls(self.speed, 0)
		if self.direction == self.MOVE_UP:
			self.rect.y -= self.speed
			self._collideWithWalls(0, -self.speed)
		if self.direction == self.MOVE_DOWN:
			self.rect.y += self.speed
			self._collideWithWalls(0, self.speed)

	def _collideWithWalls(self, dx, dy):
		collidedSprite =\
				pygame.sprite.spritecollideany(self,\
						pacmanLevel.levelWallGroup)
		if collidedSprite is not None:
			if dx > 0:
				self.rect.right = collidedSprite.rect.left
			if dx < 0:
				self.rect.left = collidedSprite.rect.right
			if dy > 0:
				self.rect.bottom = collidedSprite.rect.top
			if dy < 0:
				self.rect.top = collidedSprite.rect.bottom
			random.seed()
			self.direction = random.randint(self.MOVE_LEFT, self.MOVE_DOWN)


class GhostEater(pygame.sprite.Sprite):
	def __init__(self, posX, posY,
				 ghostEaterImage):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(ghostEaterImage, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY


class Level:
	def __init__(self):
		self.allCoins = 0

	def postInit(self, pathToLevel):
		self.levelWallGroup = pygame.sprite.Group()
		self.levelCoinGroup = pygame.sprite.Group()
		self.levelGhostEaterGroup = pygame.sprite.Group()
		self.levelGhostGroup = pygame.sprite.Group()
		self.pacmanSprite = pygame.sprite.Group()
		self._loadLevelFromFile(pathToLevel)

	def _loadLevelFromFile(self, pathToLevel):
		levelFile = open(pathToLevel, 'r')
		x = 0
		y = 0
		for line in levelFile:
			y = y + 25 
			x = 0
			for char in line:
				x = x + 25
				if char == '1':
					self.levelWallGroup.add(Block(x, y,
						'PacMan/data/block.png'))
				elif char == '0':
					self.levelCoinGroup.add(Coin(x, y,
						'PacMan/data/coin.png'))
					self.allCoins += 1
				elif char == 'S':
					self.pacmanSprite.add(Pacman(x, y, 2,
						'PacMan/data/pacman.png'))
				elif char == 'K':
					self.levelGhostEaterGroup.add(GhostEater(x, y,
						'PacMan/data/eat-coin.png'))
				elif char == 'G':
					self.levelGhostGroup.add(Ghost(x, y,\
						'PacMan/data/red-ghost.png', 
						'PacMan/data/eat-ghost.png',
						'PacMan/data/eye-ghost.png'))
					self.levelGhostGroup.add(Ghost(x, y,\
						'PacMan/data/orange-ghost.png', 
						'PacMan/data/eat-ghost.png',
						'PacMan/data/eye-ghost.png'))
					self.levelGhostGroup.add(Ghost(x, y,\
						'PacMan/data/blue-ghost.png',
						'PacMan/data/eat-ghost.png',
						'PacMan/data/eye-ghost.png'))
					self.levelGhostGroup.add(Ghost(x, y,\
						'PacMan/data/pink-ghost.png',
						'PacMan/data/eat-ghost.png',
						'PacMan/data/eye-ghost.png'))

	def update(self):
		self.pacmanSprite.update()
		self.levelWallGroup.update()
		self.levelCoinGroup.update()
		self.levelGhostEaterGroup.update()
		self.levelGhostGroup.update()

	def draw(self, surface):
		self.levelWallGroup.draw(surface)
		self.levelCoinGroup.draw(surface)
		self.levelGhostEaterGroup.draw(surface)
		self.levelGhostGroup.draw(surface)
		self.pacmanSprite.draw(surface)


pacmanLevel = Level()

def start():
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	pygame.display.set_caption('PacMan')
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	screen.blit(background, (0, 0))
	pygame.display.flip()

	clock = pygame.time.Clock()
	pacmanLevel.postInit('PacMan/data/map.txt')
	
	while 1:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				return	

		if bool(pacmanLevel.pacmanSprite) == 1:
			key = pygame.key.get_pressed()
			if key[pygame.K_LEFT]:
				pacmanLevel.pacmanSprite.sprites()[0].move(-1, 0)
			if key[pygame.K_RIGHT]:
				pacmanLevel.pacmanSprite.sprites()[0].move(1, 0)
			if key[pygame.K_UP]:
				pacmanLevel.pacmanSprite.sprites()[0].move(0, -1)
			if key[pygame.K_DOWN]:
				pacmanLevel.pacmanSprite.sprites()[0].move(0, 1)

		pacmanLevel.update()

		screen.blit(background, (0, 0))
		pacmanLevel.draw(screen)
		pygame.display.flip()


if __name__ == '__start__': start()		
