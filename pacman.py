import sys, os, pygame

def load_image(name, colorKey=None):
	fullName = os.path.join('PacMan/data', name)
	try:
		image = pygame.image.load(fullName)
	except pygame.error, message:
		print 'Cannot load image:', fullName
		raise SystemExit, message
	image = image.convert()
	if colorKey is not None:
		if colorKey is -1:
		 	colorKey = image.get_at((0, 0))
		image.set_colorkey(colorKey, pygame.RLEACCEL)
	return image, image.get_rect()


class Block(pygame.sprite.Sprite):
	def __init__(self, posX, posY):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('block.jpg', -1)
		self.pos = [posX, posY]
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY


class Coin(pygame.sprite.Sprite):
	def __init__(self, posX, posY):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('coin.png', -1)
		self.pos = [posX, posY]
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY 


class Pacman(pygame.sprite.Sprite):
	MOVE_STILL = 0
	MOVE_LEFT = 1
	MOVE_RIGHT = -1
	MOVE_UP = 2
	MOVE_DOWN = -2

	def __init__(self, posX, posY):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('pacman-open.png', -1)
		self.pos = [posX, posY]
		screen = pygame.display.get_surface()
		self.speed = 5 
		self.moveState = self.MOVE_STILL
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY
		self.collidedSprite = None
		self.score = 0

	def update(self):
		self._walk()
		if self.score >= pacmanLevel.allCoins:
			print 'won!!!'

	def move(self, dx, dy):
		if dx != 0:
			self.moveSingleAxis(dx, 0)
		if dy != 0:
			self.moveSingleAxis(0, dy)

	def moveSingleAxis(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy

		self._collideWithWalls(dx, dy)
		self._collideWithCoins()
		self._collideWithGhostEaters()
		
	def _walk(self):
		dummy = 0

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
		dummy = 0


class GhostEater(pygame.sprite.Sprite):
	def __init__(self, posX, posY):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('eat-coin.png', -1)
		self.pos = [posX, posY]
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY


class Level:
	def __init__(self):
		self.levelArray = []
		
	def postInit(self, pathToLevel):
		self.levelWallGroup = pygame.sprite.Group()
		self.levelCoinGroup = pygame.sprite.Group()
		self.levelGhostEaterGroup = pygame.sprite.Group()
		self.levelGhostGroup = pygame.sprite.Group()
		self.pacmanSprite = pygame.sprite.Sprite()
		self.allCoins = 0
		self._loadLevelFromFile(pathToLevel)

	def _loadLevelFromFile(self, pathToLevel):
		levelFile = open(pathToLevel, 'r')
		x = 0
		y = 0
		for line in levelFile:
			newLine = []
			y = y + 27 
			x = 0
			for char in line:
				x = x + 26
				if char == '1':
					self.levelWallGroup.add(Block(x, y))
				if char == '0':
					self.levelCoinGroup.add(Coin(x, y))
					self.allCoins += 1
				if char == 'S':
					self.pacman = Pacman(x, y)
				if char == 'K':
					self.levelGhostEaterGroup.add(GhostEater(x, y))
	
	def update(self):
		self.pacman.update()
		self.levelWallGroup.update()
		self.levelCoinGroup.update()
		self.levelGhostEaterGroup.update()
		self.levelGhostGroup.update()

	def draw(self, surface):
		self.levelWallGroup.draw(surface)
		self.levelCoinGroup.draw(surface)
		self.levelGhostEaterGroup.draw(surface)
		self.levelGhostGroup.draw(surface)
		pacmanToDraw = pygame.sprite.RenderPlain((self.pacman))
		pacmanToDraw.draw(surface)


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

		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			pacmanLevel.pacman.move(-2, 0)
		if key[pygame.K_RIGHT]:
			pacmanLevel.pacman.move(2, 0)
		if key[pygame.K_UP]:
			pacmanLevel.pacman.move(0, -2)
		if key[pygame.K_DOWN]:
			pacmanLevel.pacman.move(0, 2)

		pacmanLevel.update()

		screen.blit(background, (0, 0))
		pacmanLevel.draw(screen)
		pygame.display.flip()


if __name__ == '__start__': start()		
