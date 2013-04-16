from Util import *


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

	def __init__(self, displaySize):
		self.displaySize = displaySize

	def get_handler(self, type, playerId):
		#TODO!
		return NoOpInputHandler(self.displaySize)


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


#TODO
class KeyboardInputHandler(object):

	def __init(self, pitchSize, batSize, playerId):
		self.playerId = playerId
		self.y = pitchSize[1] / 2

	def handle(self, event):
		#TODO key handling code
		pass

	def update(self):
		pass

	def getY(self):
		return self.y

	def getRoll(self):
		return 0

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