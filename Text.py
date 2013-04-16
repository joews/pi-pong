import pygame
from pygame.locals import *
from pygame import *
import math

class Text(pygame.sprite.Sprite):
	def __init__(self, x, y, text=None):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font(None, 14)
		self.color = (255, 255, 255)

		self.text = text

		self.image = self.font.render(self.text, True, self.color)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def rerender(self, text):
		oldCenter = self.rect.center
		self.image = self.font.render(text, True, self.color)
		self.rect = self.image.get_rect()
		self.rect.center = oldCenter