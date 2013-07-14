import pygame

class Spritesheet(object):
	def __init__(self, fileName):
		try:
			self.sheet = pygame.image.load(fileName).convert()
		except:
			print 'Unable to load spritesheet imae: ', fileName
			raise SystemExit, message
	
	# Load a specific image from a specific rectangle
	def loadImageAt(self, rectangle, colorKey = None):
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorKey is not None:
			if colorKey is -1:
				colorKey = image.get_at((0, 0))
			image.set_colorkey(colorKey, pygame.RLEACCEL)
		return image	

	# Load a list of images
	def loadListOfImagesAt(self, rects, colorKey = None):
		return [self.loadImageAt(rect, colorKey) for rect in rects]

	# Load a strip of images
	def loadImageStrip(self, rect, imageCount, colorKey = None):
		tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
				for x in range(imageCount)]
		return self.loadListOfImagesAt(tups, colorKey)
