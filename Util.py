import math

piOver180 = math.pi/ 180

#Global utility functions (for Processing compatibility)
def constrain(x, min, max):
	if x > max:
		return max
	elif x < min: 
		return min
	return x

def map(x, minIn, maxIn, minOut, maxOut):
	return minOut + (maxOut - minOut) * (x - minIn) / (maxIn - minIn)

def radians(degrees):
	return degrees * piOver180