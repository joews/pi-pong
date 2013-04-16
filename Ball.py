import pygame
from pygame.locals import *
from pygame import *
import random
from math import sin, cos, pi, atan2, hypot, sqrt, radians, degrees

TWO_PI = 2 * pi


class Ball(sprite.Sprite):
	
	def __init__(self, displaySize, bat1, bat2):
			
		# Initialize the sprite base class
		super(Ball, self).__init__()

		self.bat1 = bat1
		self.bat2 = bat2
		
		# Get the display size for working out collisions later
		self.displaySize = displaySize
		
		# Get a width and height values proportionate to the display size
		width = displaySize[0] / 30
		height = displaySize[1] / 30
		
		self.image = pygame.Surface((10,10))
		self.image.fill((255, 0, 255))
		self.image.set_colorkey((255, 0, 255))

		pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 10, 10))
		self.rect = self.image.get_rect()
			
		# Work out a speed
		self.speed = 5
	
		# Reset the ball
		self.reset()
	
	def reset(self):
		
		# Start the ball directly in the centre of the screen
		self.rect.centerx = self.displaySize[0] / 2
		self.rect.centery = self.displaySize[1] / 2
		
		# Start the ball moving to the left or right (pick randomly)
		# Vector(x, y)
		if random.randrange(1, 3) == 1:
			# move to left
			self.vector = (-self.speed, 0)
		else:
			# move to right
			self.vector = (self.speed, 0)

		self.mask = mask.from_surface(self.image)
		self.colliding = False

	def get_angle(self):
		dx, dy = self.vector
		return atan2(-dy, dx) % TWO_PI

	def update(self):
		dx, dy = self.vector

		#Calculate collisions before actually moving
		newrect = self.rect
		newrect.centerx += dx
		newrect.centery += dy

		#Use a colliding flag so we don't get the ball trapped "inside"
		# the edges
		bat = self.bat_collision()
		if bat:
			if not self.colliding:
				self.colliding = True   

				#Angle of ball to 0 radians (3 o'clock)
				#Pygame y axis is "upside down", so invert dy  
				angleBallIn = self.get_angle()

				#Angle off ball to bat
				angleBat = bat.get_angle()
				angleBallToBat = (angleBallIn - angleBat) % TWO_PI

				#Head-on collision: reverse both dx, dy
				if angleBallToBat == 0 or abs(angleBallToBat) == pi:
					self.invert()
				else:
					#Angle of reflection from bat
					angleBallFromBat = ((2 * pi) - angleBallToBat) % TWO_PI

					#Angle of reflection to 0 radians
					angleBallOut = (angleBallFromBat + angleBat) % TWO_PI

					dxOut = self.speed * cos(angleBallOut)
					dyOut = self.speed * sin(angleBallOut)

					#TODO: Invert vectors based on angle
					self.vector = [dxOut, dyOut]
					self.invert()

			else:
				pass
		else:
			#CARTESIAN UPDATES
			if not self.colliding:
				#Hit top or bottom
				if newrect.top <= 0 or newrect.bottom >= 480:
					self.invertY()
					self.colliding = True

					if newrect.top <= 0:
						self.rect.top = 5
					else:
						self.rect.bottom = 475

				#Hit left or right
				if newrect.right >= 640 or newrect.left <= 0:
					self.invertX()
					self.colliding = True

					if newrect.left <= 0:
						self.rect.left = 5
					else: 
						self.rect.right = 635

			#Hit nothing: update position
			else:
				#print "No collision, moving"
				self.rect = newrect
				if self.colliding:
					self.colliding = False

	def invertX(self):
		dx, dy = self.vector
		self.vector = [-dx, dy]

	def invertY(self):
		dx, dy = self.vector
		self.vector = [dx, -dy]

	def invert(self):
		dx, dy = self.vector
		self.vector = [-dx, -dy]

	#Update direction following a collision with a bat,
	# passing in the new angle the ball should face
	def updateDirection(self, newAngle):
		x = self.speed * cos(newAngle)
		y = self.speed * sin(newAngle)
		self.vector = [x, y]
	
	def reflectVector(self):
		
		# Gets the current angle of the ball and reflects it, for bouncing
		# off walls
		deltaX = self.vector[0]
		deltaY = - self.vector[1]
		self.vector = (deltaX, deltaY)

	#If the ball is colliding with either bat, return it
	def bat_collision(self):
		if pygame.sprite.collide_mask(self, self.bat1):
			return self.bat1
		elif pygame.sprite.collide_mask(self, self.bat2):
			return self.bat2
		else:
			return None