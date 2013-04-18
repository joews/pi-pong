import pygame
from pygame.locals import *
from pygame import *
import math
import pymunk


# The class for the bats on either side
class Bat(sprite.Sprite):
	
	def __init__(self, space, displaySize, batSize, inputHandler, player):
			
		# Initialize the sprite base class
		super(Bat, self).__init__()
		
		self.inputHandler = inputHandler		
		self.player = player
		
		width, height = batSize

		#Initial position
		if player == "player1":
			x = displaySize[0] / 20
		elif player == "player2":
			x displaySize[0] - displaySize[0] / 20

		y = displaySize[1] / 2
		position = (x, y)

		#Initialise physics
		self.mass = pymunk.inf #don't move when the ball hits
		self.inertia = pymunk.inf #don't rotate when the ball hits
		self.body = pymunk.Body(mass, inertia)
		self.body.position = position
		self.shape = pymunk.Poly.create_box(body, (width, height))
		self.space.add(body, shape)
		self.shape.elasticity = 0.99 #perfect bounce
		self.shape.friction = 0


		#Initialise graphics
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
		self.rect.center = to_pygame_tuple(position)
		
		# Set a bunch of direction and moving variables
		self.moving = False
		self.direction = "none"
		self.roll = 0
		
	def startMove(self, direction):
		
		# Set the moving flag to true
		self.direction = direction
		self.moving = True
		
	def update(self):

		#Get new input
		self.inputHandler.update()
		self.roll = self.inputHandler.getRoll()
		newY = self.inputHandler.getY()

		#Invert roll to account for anticlockwise rotation
		degrees = -self.roll	
		radians = radians(degrees)	

		#Rotate
		# - physics
		body.angle = radians

		# - graphics
		old_center = self.rect.center
		self.image = pygame.transform.rotate(self.image_master, degrees)
		self.rect = self.image.get_rect()
		self.rect.center = old_center

		self.mask = mask.from_surface(self.image);

		#Move
		# - physics
		position = (self.x, newY)
		body.position = position
		# - graphics
		self.rect.center = to_pygame_tuple(newY)
		
				
	def stopMove(self):
		self.moving = False

	#Get the angle in radians (0-2pi)
	# (we store roll in degrees)
	def get_angle(self):
		return math.radians(self.roll % 360)