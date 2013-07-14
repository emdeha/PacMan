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

	def update(self):
		self._walk()

	def move(self, newMoveState, newCollidedSprite=None):
		self.moveState = newMoveState
		self.collidedSprite = newCollidedSprite

	def deltaMove(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy

	def _walk(self):
		if self.moveState == self.MOVE_LEFT:
			if self.collidedSprite is not None:
				self.rect.left = self.collidedSprite.rect.right
			else: self.rect = self.rect.move((-self.speed, 0))
		elif self.moveState == self.MOVE_RIGHT:
			if self.collidedSprite is not None:
				self.rect.right = self.collidedSprite.rect.left
			else: self.rect = self.rect.move((self.speed, 0))
		elif self.moveState == self.MOVE_UP:
			if self.collidedSprite is not None:
				self.rect.top = self.collidedSprite.rect.bottom
			else: self.rect = self.rect.move((0, -self.speed))
		elif self.moveState == self.MOVE_DOWN:
			if self.collidedSprite is not None:
				self.rect.bottom = self.collidedSprite.rect.top
			else: self.rect = self.rect.move((0, self.speed))	
		self.moveState = self.MOVE_STILL	

class GhostEater(pygame.sprite.Sprite):
	def __init__(self, posX, posY):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('eat-coin.png', -1)
		self.pos = [posX, posY]
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY

class Level:
	def __init__(self, pathToLevel):
		self.levelArray = []
		self.levelWallGroup = pygame.sprite.Group()
		self.levelCoinGroup = pygame.sprite.Group()
		self.levelGhostEaterGroup = pygame.sprite.Group()
		self.levelGhostGroup = pygame.sprite.Group()
		self.pacmanSprite = pygame.sprite.Sprite()
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

	def movePacman(self, newMoveState):
		futurePacman = Pacman(self.pacman.pos[0], self.pacman.pos[1])
		futurePacman.move(newMoveState)
		futurePacman._walk()
		collidedSprite =\
				pygame.sprite.spritecollideany(futurePacman,\
						self.levelWallGroup)
		self.pacman.move(newMoveState, collidedSprite)

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
	pacmanLevel = Level('PacMan/data/map.txt')

	while 1:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				return	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					pacmanLevel.movePacman(Pacman.MOVE_UP)
					#pacmanLevel.movePacman(0, 25)
				elif event.key == pygame.K_DOWN:
					pacmanLevel.movePacman(Pacman.MOVE_DOWN)
					#pacmanLevel.movePacman(0, -25)
				elif event.key == pygame.K_LEFT:
					pacmanLevel.movePacman(Pacman.MOVE_LEFT)
					#pacmanLevel.movePacman(-25, 0)
				elif event.key == pygame.K_RIGHT:
					pacmanLevel.movePacman(Pacman.MOVE_RIGHT)
					#pacmanLevel.movePacman(25, 0)
			if event.type == pygame.KEYUP:
				pacmanLevel.movePacman(Pacman.MOVE_STILL)

		pacmanLevel.update()

		screen.blit(background, (0, 0))
		pacmanLevel.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()		
