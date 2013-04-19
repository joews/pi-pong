#!/usr/bin/env python

# PiPong - A remake of the classic Pong game using PyGame. Written by
# Liam Fraser - 28/07/2012 for the Linux User & Developer magazine.

# Updated by Joe Whitfield-Seed to work with Wiimotes and physics and stuff

import pygame # Provides what we need to make a game
import sys # Gives us the sys.exit function to close our program
import random # Can generate random positions for the pong ball

from pygame.locals import *
from pygame import *

import pymunk


from InputHandler import *
from PymunkBall import Ball
from PymunkBat import Bat
from Text import Text

from Util import *
from Border import Border

FRAME_RATE = 180



# Our main game class
class PiPong:
	
	def __init__(self):

		#TODO config
		self.debug = True

		self.displaySize = (640, 480)
		self.batSize = (8, 80)
		
		# Initialize pygame
		pygame.init()		
		self.clock = pygame.time.Clock()
		self.frameCount = 0
		self.fps = ""
		display.set_caption("Pi Pong")
		self.display = display.set_mode(self.displaySize)

		# Initialise physics
		self.space = pymunk.Space()
		self.space.gravity = (0.0, 0)

		#Initialise sprites 			
		self.background = Background(self.space, self.displaySize)
	
		#Input handlers for the bats
		#TODO config!
		inputType1 = "nunchuk"
		inputType2 = "none"

		inputHandlers = InputHandlers(self.displaySize, self.batSize)
		input1 = inputHandlers.get_handler(inputType1, 0)
		input2 = inputHandlers.get_handler(inputType2, 1)

		# Create two bats, a ball and add them to a sprite group
		self.player1Bat = Bat(self.space, self.displaySize, self.batSize, input1, "player1")
		self.player2Bat = Bat(self.space, self.displaySize, self.batSize, input2, "player2")
		self.ball = Ball(self.space, self.displaySize, self.player1Bat, self.player2Bat)

		self.bat_sprites = sprite.Group(self.player1Bat, self.player2Bat)
		self.ball_sprites = sprite.Group(self.ball)

		# Debugging sprites
		self.fps_text = Text(30, 10)
		self.debug_sprites = sprite.Group(self.fps_text)

	
	def run(self):
		# Runs the game loop
		
		while True:
			self.frameCount += 1
			self.handleEvents()

			# Draw the background
			self.background.draw(self.display)

			self.bat_sprites.clear(self.display, self.background.image)
			self.bat_sprites.update()
			self.bat_sprites.draw(self.display)

			self.ball_sprites.clear(self.display, self.background.image)
			self.ball_sprites.update()
			self.ball_sprites.draw(self.display)

			if self.debug:
				self.debug_update()
				self.debug_sprites.clear(self.display, self.background.image)
				self.debug_sprites.update()
				self.debug_sprites.draw(self.display)


			#tick physics
			self.space.step(1/50.0)

			#tick graphics
			pygame.display.flip()
			self.clock.tick(FRAME_RATE)


	def debug_update(self):
		#Update FPS display every 30 frames
		if(self.frameCount % 30 == 0):
			self.fps = "%.0f fps" % (self.clock.get_fps())
			self.fps_text.rerender(self.fps)

		


	def handleEvents(self):
		
		# Handle events, starting with the quit event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			self.player1Bat.inputHandler.handle(event)
			self.player2Bat.inputHandler.handle(event)
				
# The class for the background
class Background:
	
	def __init__(self, space, displaySize):
		
		self.space = space
		# Set our image to a new surface, the size of the screen rectangle
		self.image = Surface(displaySize)
		
		# Fill the image with a green colour (specified as R,G,B)
		self.image.fill((27, 210, 57))
		
		# Get width proportionate to display size
		lineWidth = displaySize[0] / 80
		
		# Create a rectangle to make the white line
		lineRect = Rect(0, 0, lineWidth, displaySize[1])
		lineRect.centerx  = displaySize[0] / 2
		draw.rect(self.image, (255, 255, 255), lineRect)

		#Create invisible top and bottom static objects so the ball bounces
		Border(space, self.image, displaySize, 0)
		Border(space, self.image, displaySize, displaySize[1])

	def build_top(self):
		body = pymunk.Body() # static 
		body.position = (0, 470)
		line = pymunk.Segment(body, (0, 0), (640, 0), 1) 

		#Make the walls perfectly bouncy
		line.elasticity = 0.99

		#Static shapes, so only add the Segments, not the body
		self.space.add(line)
		#self.draw_line(line, (255,0 ,0))

	def build_bottom(self):
		body = pymunk.Body() # static 
		body.position = (0, 0)
		line = pymunk.Segment(body, (0, 10), (640, 10), 1) 

		#Make the walls perfectly bouncy
		line.elasticity = 0.99

		#Static shapes, so only add the Segments, not the body
		self.space.add(line)
		#self.draw_line(line, (0, 0 ,255))

	#Debug
	def draw_line(self, line, color):
		body = line.body
		pv1 = body.position + line.a.rotated(body.angle) # 1
		pv2 = body.position + line.b.rotated(body.angle)
		p1 = to_pygame(pv1) # 2
		p2 = to_pygame(pv2)
		pygame.draw.lines(self.image, color, False, [p1,p2])
		
	def draw(self, display):
			
		# Draw the background to the display that has been passed in
		display.blit(self.image, (0,0))
		
if __name__ == '__main__':
	game = PiPong()
	game.run()
