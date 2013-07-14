import pygame

class Spritesheet(object):
	def __init__(self, fileName):
		try:
			self.sheet = pygame.image.load(fileName).convert()
		except pygame.error, message:
			print 'Unable to load spritesheet image: ', fileName
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


class SpriteStripAnim(object):
	def __init__(self, fileName, rect, count,\
			     colorKey = None, loop = False, frames = 1):
		self.fileName = fileName
		ss = Spritesheet(fileName)
		self.images = ss.loadImageStrip(rect, count, colorKey)
		self.i = 0
		self.loop = loop
		self.frames = frames
		self.f = frames

	def iter(self):
		self.i = 0
		self.f = self.frames
		return self

	def next(self):
		if self.i >= len(self.images):
			if not self.loop:
				raise StopIteration
			else:
				self.i = 0
		image = self.images[self.i]
		self.f -= 1
		if self.f == 0:
			self.i += 1
			self.f = self.frames
		return image	
	
	def __add__(self, ss):
		self.images.extend(ss.images)
		return self
