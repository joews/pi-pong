import pygame
from pygame.locals import *
from pygame import *
import math


# The class for the bats on either side
class Bat(sprite.Sprite):
	
	def __init__(self, displaySize, batSize, inputHandler, player):
			
		# Initialize the sprite base class
		super(Bat, self).__init__()
		
		self.inputHandler = inputHandler		
		self.player = player
		
		width, height = batSize
		
		# Create an image for the sprite using a square
		# so we can rotate it easily
		self.image_master = pygame.Surface((100,100))
		self.image_master.fill((255,0,255))
		self.image_master.set_colorkey((255, 0, 255))
		pygame.draw.rect(self.image_master, (255, 255, 255), (44, 0, 8, 100))

		self.image = self.image_master
		self.mask = mask.from_surface(self.image, 255)
		
		# Create the sprites rectangle from the image
		self.rect = self.image.get_rect()
		
		# Set the rectangle's location depending on the player
		if player == "player1":
			# Left side
			self.rect.centerx = displaySize[0] / 20
		elif player == "player2":
			# Right side
			self.rect.centerx = displaySize[0] - displaySize[0] / 20
		
		# Center the rectangle vertically
		self.rect.centery = displaySize[1] / 2
		
		# Set a bunch of direction and moving variables
		self.moving = False
		self.direction = "none"
		#self.speed = 13

		self.roll = 0
		
	def startMove(self, direction):
		
		# Set the moving flag to true
		self.direction = direction
		self.moving = True
		
	def update(self):

		self.inputHandler.update()
		self.roll = self.inputHandler.getRoll()

		old_center = self.rect.center
		#Pygame rotates anticlockwise, so invert the wiimote input
		self.image = pygame.transform.rotate(self.image_master, -self.roll)
		self.rect = self.image.get_rect()
		self.rect.center = old_center

		self.mask = mask.from_surface(self.image);

		self.rect.centery = self.inputHandler.getY()
				
	def stopMove(self):
		self.moving = False

	#Get the angle in radians (0-2pi)
	# (we store roll in degrees)
	def get_angle(self):
		return math.radians(self.roll % 360)