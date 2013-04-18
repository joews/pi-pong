import pygame
from pygame.locals import *
from pygame import *
import random
from math import sin, cos, pi, atan2, hypot, sqrt, radians, degrees
import pymunk
from Util import *

TWO_PI = 2 * pi


class Ball(sprite.Sprite):
	
	def __init__(self, space, displaySize, bat1, bat2):
			
		# Initialize the sprite base class
		super(Ball, self).__init__()

		self.bat1 = bat1
		self.bat2 = bat2
		
		self.displaySize = displaySize
		
		width = 20
		height = 16

		#Initialise physics
		self.mass = 1
		self.radius = 8
		self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
		self.body = pymunk.Body(self.mass, self.inertia)
		self.shape = pymunk.Circle(self.body, self.radius)
		space.add(self.body, self.shape)
		self.shape.elasticity = 0.99 #perfect bounce

		#Initialise graphics		
		self.image = pygame.Surface((10,10))
		self.image.fill((255, 0, 255))
		self.image.set_colorkey((255, 0, 255))

		#Initial position of the ball is set by reset
		pygame.draw.circle(self.image, (255, 255, 255), (0, 0), self.radius, 2)
		self.rect = self.image.get_rect()
			
		# Work out a speed (pick a value that works for pymunk)
		self.speed = 500
	
		# Reset the ball
		self.reset()
	
	def reset(self):
		
		position = (self.displaySize[0] / 2, self.displaySize[1] / 2)

		#Reset physics
		self.body.position = position
		self.body.velocity = (-self.speed, 0) #for now, always go left

		#Reset graphics
		self.rect.center = to_pygame_tuple(position)

	def update(self):
		#Physics update themselves
		#update graphics
		position = to_pygame(self.body.position)
		self.rect.center = position


	
