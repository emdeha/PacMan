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
		self.rect.topleft = posX + 5, posY + 5 

class Pacman(pygame.sprite.Sprite):
	def __init__(self, posX, posY):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('pacman-open.png', -1)
		self.pos = [posX, posY]
		screen = pygame.display.get_surface()
		self.move = 3 
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY

	def update(self):
		self._walk()

	def deltaMove(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy

	def posMove(self, newPosX, newPosY):
		self.rect.right = newPosX
		self.rect.bottom = newPosY

	def _walk(self):
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

	def movePacman(self, dx, dy):
		futurePacman = Pacman(self.pacman.pos[0], self.pacman.pos[1])
		futurePacman.deltaMove(dx, dy)
		collidedSprite =\
				pygame.sprite.spritecollideany(futurePacman, self.levelWallGroup)
		if collidedSprite is not None:		
			self.pacman.posMove(collidedSprite.rect.top,\
					collidedSprite.rect.left)
		else:
			self.pacman.deltaMove(dx, dy)

def main():
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
					pacmanLevel.movePacman(0, 25)
				elif event.key == pygame.K_DOWN:
					pacmanLevel.movePacman(0, -25)
				elif event.key == pygame.K_LEFT:
					pacmanLevel.movePacman(-25, 0)
				elif event.key == pygame.K_RIGHT:
					pacmanLevel.movePacman(25, 0)
			if event.type == pygame.KEYUP:
				pacmanLevel.movePacman(0, 0)

		pacmanLevel.update()

		screen.blit(background, (0, 0))
		pacmanLevel.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()		
