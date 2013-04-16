#!/usr/bin/env python

# PiPong - A remake of the classic Pong game using PyGame. Written by
# Liam Fraser - 28/07/2012 for the Linux User & Developer magazine.

# Updated by Joe Whitfield-Seed to work with Wiimotes 

import pygame # Provides what we need to make a game
import sys # Gives us the sys.exit function to close our program
import random # Can generate random positions for the pong ball

from pygame.locals import *
from pygame import *

from serial import Serial

from InputHandler import *
from Ball import Ball
from Bat import Bat
from Text import Text

from Util import *

FRAME_RATE = 180



# Our main game class
class PiPong:
	
	def __init__(self):

		self.debug = True

		# Make the display size a member of the class
		self.displaySize = (640, 480)
		self.batSize = (8, 80)
		
		# Initialize pygame
		pygame.init()
		
		# Create a clock to manage time
		self.clock = pygame.time.Clock()
		self.frameCount = 0
		self.fps = ""
		
		# Set the window title
		display.set_caption("PiChuk Pong")
		
		# Create the window
		self.display = display.set_mode(self.displaySize)
			
		# Create the background, passing through the display size
		self.background = Background(self.displaySize)
	
		#Input handlers for the bats
		#TODO: AI, keyboard
		#TODO factory to get the right input handler
		#serial = Serial("/dev/ttyACM0", 115200)
		#input1 = WiimoteInputHandler(serial, self.displaySize, self.batSize, 0);
		#input1 = WiimoteInputHandler(serial, self.displaySize, self.batSize, 1);

		#Do we see an increase in frame rate when not listening to Serial?
		#Yes! up to 80fps on Xubuntu VM! need to investigate
		#input1 = NoOpInputHandler(self.displaySize)
		#input2 = NoOpInputHandler(self.displaySize)

		#TODO config!
		inputType1 = "none"
		inputType2 = "none"

		inputHandlers = InputHandlers(self.displaySize)
		input1 = inputHandlers.get_handler(inputType1, 0)
		input2 = inputHandlers.get_handler(inputType2, 1)

		# Create two bats, a ball and add them to a sprite group
		self.player1Bat = Bat(self.displaySize, self.batSize, input1, "player1")
		self.player2Bat = Bat(self.displaySize, self.batSize, input2, "player2")
		self.ball = Ball(self.displaySize, self.player1Bat, self.player2Bat)

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
			
			if event.type == KEYDOWN:
				# Find which key was pressed and start moving appropriate bat
				if event.key == K_s:
					# Start moving bat
					self.player1Bat.startMove("down")
				elif event.key == K_w:
					self.player1Bat.startMove("up")
				if event.key == K_DOWN:
					self.player2Bat.startMove("down")
				elif event.key == K_UP:
					self.player2Bat.startMove("up")
			
			if event.type == KEYUP:
				if event.key == K_s or event.key == K_w:
					self.player1Bat.stopMove()
				elif event.key == K_DOWN or event.key == K_UP:
					self.player2Bat.stopMove()
				
# The class for the background
class Background:
	
	def __init__(self, displaySize):
		
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
		
	def draw(self, display):
			
		# Draw the background to the display that has been passed in
		display.blit(self.image, (0,0))
		
if __name__ == '__main__':
	game = PiPong()
	game.run()
