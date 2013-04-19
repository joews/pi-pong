from Util import *
from pygame.locals import *

#offser Wiichuck Y so horizontal Nunchuk yields zero
WIICHUCK_ZERO_Y = 0;

#Control sensitivity of input
WIICHUCK_Y_SENSITIVITY = 40;
WIICHUCK_ROLL_SENSITIVITY = 1.9;

#The limits of the Wiichuck input
#Actually slightly within limits so we don't have to strain
# to reach the extremes
WIICHUCK_MIN_Y = -180 + WIICHUCK_Y_SENSITIVITY;
WIICHUCK_MAX_Y = 240 - WIICHUCK_Y_SENSITIVITY;

#Factory class: get the player InputHandlers
#TODO
class InputHandlers(object):

	def __init__(self, displaySize, batSize):
		self.displaySize = displaySize
		self.batSize = batSize

	def get_handler(self, type, playerId):
		if type == "none":
			return NoOpInputHandler(self.displaySize)
		elif type == "keyboard":
			return KeyboardInputHandler(self.displaySize, self.batSize, playerId)

		return None


#An input handler that doesn't move the bat
# - for testing
class NoOpInputHandler(object):
	
	def __init__(self, pitchSize):
		self.y = pitchSize[1] / 2

	def handle(self, event):
		pass

	def update(self):
		pass

	def getY(self):
		return self.y

	def getRoll(self):
		return 0


class KeyboardInputHandler(object):

	def __init__(self, pitchSize, batSize, playerId):
		self.playerId = playerId
		self.y = pitchSize[1] / 2

		#Map keys to players
		#Invert up/down because of pygame's inverted y axis
		self.upKey = (playerId == 1) and K_DOWN or K_s
		self.downKey = (playerId == 1) and K_UP or K_w
		self.leftKey = (playerId == 1) and K_LEFT or K_a
		self.rightKey = (playerId == 1) and K_RIGHT or K_d

		#From original PiPong
		self.moving = False
		self.direction = "none"
		self.speed = 13

		#Direction of rotation (degrees, negative allowed)
		self.dir = 0

		#Speed of rotation (#degrees to turn for each frame)
		self.inc = 5
		self.rolling = False
		self.rollDirection = "none"

	def handle(self, event):
		if event.type == KEYDOWN:
			if event.key == self.downKey:
				self.startMove("down")
			elif event.key == self.upKey:
				self.startMove("up")

			if event.key == self.leftKey:
				self.startRoll("left")
			elif event.key == self.rightKey:
				self.startRoll("right")
		
		if event.type == KEYUP:
			if event.key == self.upKey or event.key == self.downKey:
				self.stopMove()
			if event.key == self.rightKey or event.key == self.leftKey:
				self.stopRoll()


	#TODO constrain y and roll
	def update(self):
		#Y
		if self.moving:
			# Move the bat up or down if moving
			if self.direction == "up":
				self.y -= self.speed
			elif self.direction == "down":
				self.y += self.speed

		#roll
		if self.rolling:
			if self.rollDirection == "left":
				self.dir -= self.inc
			elif self.rollDirection == "right":
				self.dir += self.inc

	def startMove(self, direction):
		self.direction = direction
		self.moving = True

	def stopMove(self):
		self.moving = False

	def startRoll(self, direction):
		self.rollDirection = direction
		self.rolling = True

	def stopRoll(self):
		self.rolling = False

	def getY(self):
		return self.y

	def getRoll(self):
		return self.dir



#The default input handler
class WiimoteInputHandler(object):

	def __init__(self, serial, pitchSize, batSize, playerId):
		self.serial = serial
		self.batHeight = batSize[1]
		self.pitchHeight = pitchSize[1]
		self.playerId = playerId

		#Min/Max Y coordinates for the centre of the bat
		self.minY = self.batHeight / 2
		self.maxY = self.pitchHeight = self.minY

	def handle(self, event):
		pass

	def update(self):
		self._handleSerialInput()
		#print self.y, self.roll

	def getY(self):
		return self.y

	def getRoll(self):
		return self.roll

	def _readSerial(self):
		#Read raw values from the serial port
		self.serial.flush()
		line = ""
		y, roll = (0, 0)

		while "," not in line:
			line = self.serial.readline()
			try	:	
				#All players are reported on the same line
				players = line.strip().split("|")

				#Use playerId to find the right tuple
				if len(players) >= self.playerId + 1:
					myPlayer = players[self.playerId]
					(serialRoll, serialY) = myPlayer.split(",")
					roll, y = (int(serialRoll), int(serialY))
				else:
					line = ""
					continue
			except ValueError, IndexError:
				line = ""
				continue

		return roll, y


	def _handleSerialInput(self):
		(rawRoll, rawY) = self._readSerial()

		compensatedY = rawY - WIICHUCK_ZERO_Y
		constrainedY = constrain(rawY, WIICHUCK_MIN_Y, WIICHUCK_MAX_Y)
		
		self.y = map(constrainedY, WIICHUCK_MIN_Y, WIICHUCK_MAX_Y, 40, 440)
		
		compensatedRoll = rawRoll * WIICHUCK_ROLL_SENSITIVITY
		self.roll = constrain(compensatedRoll, -90, 90)
		#self.roll = map(compensatedRoll, -255, 255, -90, 90)