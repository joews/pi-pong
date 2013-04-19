import pymunk
import pygame
from Util import *

#A border to bounce the ball at the top or bottom
#pymunk won't create two lines on the pi! use rects instead
class Border(object):

	def __init__(self, space, image, displaySize, y):
		self.body = pymunk.Body(pymunk.inf, pymunk.inf)

		self.image = image
		self.y = y

		self.width = displaySize[0]

		self.body.position = (self.width/2, y)
		self.line = pymunk.Poly.create_box(self.body, (self.width, 1))

		self.rect = (0, y, self.width, 1)

		self.line.elasticity = 0.99
		space.add(self.body, self.line)
		self.draw_box() #debug

	def draw_box(self, color=(255,255,255)):
		pygame.draw.rect(self.image, color, self.rect)
		




