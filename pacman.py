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
		self.area = screen.get_rect()
		self.rect.topleft = posX, posY

class GhostCoin(pygame.sprite.Sprite):
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
		self.levelSpriteGroup = pygame.sprite.Group()
		self.loadLevelFromFile(pathToLevel)

	def loadLevelFromFile(self, pathToLevel):
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
					self.levelSpriteGroup.add(Block(x, y))
				if char == '0':
					self.levelSpriteGroup.add(Coin(x, y))
				if char == 'S':
					self.levelSpriteGroup.add(Pacman(x, y))
				if char == 'K':
					self.levelSpriteGroup.add(GhostCoin(x, y))
	
	def update(self):
		self.levelSpriteGroup.update()

	def draw(self, surface):
		self.levelSpriteGroup.draw(surface)

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
	#sampleBlock = Block(50, 50)
	#allSprites = pygame.sprite.RenderPlain((sampleBlock))

	while 1:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				return	
		
		pacmanLevel.update()

		screen.blit(background, (0, 0))
		pacmanLevel.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()		
