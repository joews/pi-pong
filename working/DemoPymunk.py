import sys
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk #1
import random
import math

def to_pygame(p):
	"""Small hack to convert pymunk to pygame coordinates"""
	return int(p.x), int(-p.y+600)

def to_pygame_tuple(p):
	"""Small hack to convert pymunk to pygame coordinates"""
	return int(p[0]), int(-p[1]+600)

def add_ball(space):
	mass = 1
	radius = 14
	inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
	body = pymunk.Body(mass, inertia) # 2
	x = random.randint(120,380)
	body.position = x, 300 # 3

	#Make the ball move
	body.apply_impulse((-250, 0), (0,0))
	shape = pymunk.Circle(body, radius) # 4
	space.add(body, shape) # 5

	#make the ball perfectly bouncy
	shape.elasticity = 1.0
	shape.friction = 0
	return shape


def draw_ball(screen, ball):
	p = int(ball.body.position.x), 600-int(ball.body.position.y)
	pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)

def add_box(space):
	body = pymunk.Body() # static 
	body.position = (300, 300)
	top = pymunk.Segment(body, (290, 290), (-290, 290), 1) 
	left = pymunk.Segment(body, (-290, -290), (-290, 290), 1) 
	bottom = pymunk.Segment(body, (-290, -290), (290, -290), 1) 
	right = pymunk.Segment(body, (290, 290), (290, -290), 1) 

	#Make the walls perfectly bouncy
	top.elasticity = 0.99
	bottom.elasticity = 0.99
	right.elasticity = 0.99
	left.elasticity = 0.99

	#Static shapes, so only add the Segments, not the body
	space.add(top, left, bottom, right)
	return (top, left, bottom, right)

def draw_box(screen, lines):
	for line in lines:
		body = line.body
		pv1 = body.position + line.a.rotated(body.angle) # 1
		pv2 = body.position + line.b.rotated(body.angle)
		p1 = to_pygame(pv1) # 2
		p2 = to_pygame(pv2)
		pygame.draw.lines(screen, THECOLORS["black"], False, [p1,p2])

#My custom code - add a bat object that can rotate
def add_bat(space):
	mass = pymunk.inf
	width = 8
	height = 80
	inertia = pymunk.inf #we don't want rotation
	#pymunk.moment_for_box(mass, width, height)
	body = pymunk.Body(mass, inertia)
	body.position = (50, 300)

	shape = pymunk.Poly.create_box(body, (width, height))
	space.add(body, shape)

	shape.elasticity = 0.99
	shape.friction = 0

	return shape

def draw_bat(screen, shape):
	body = shape.body

	position = to_pygame_tuple((body.position[0], body.position[1]))

	image = pygame.Surface((80, 80))
	image.fill((255,0,255))
	image.set_colorkey((255, 0, 255))

	pygame.draw.rect(image, (0, 0, 0), (36, 0, 8, 80))

	degrees = math.degrees(body.angle)

	rect = image.get_rect()
	rect.center = position

	oldCenter = rect.center
	image = pygame.transform.rotate(image, degrees)
	rect = image.get_rect()
	rect.center = oldCenter

	screen.blit(image, rect.topleft)



def main():
	pygame.init()
	screen = pygame.display.set_mode((600, 600))
	pygame.display.set_caption("Joints. Just wait and the L will tip over")
	clock = pygame.time.Clock()
	running = True
	
	space = pymunk.Space()
	space.gravity = (0.0, 0)
	
	balls = []

	ball_shape = add_ball(space)
	balls.append(ball_shape)

	box = add_box(space)
	bat = add_bat(space)
	
	ticks_to_rotate = 20
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False


		
		ticks_to_rotate -= 1
		if ticks_to_rotate <= 0:
			ticks_to_rotate = 20

			#Rotation is anticlockwise
			bat.body.angle -= math.pi / 10

			#Debug: print fps every few frames
			print clock.get_fps()

		screen.fill(THECOLORS["white"])
		
		for ball in balls:
			draw_ball(screen, ball)

		draw_box(screen, box)
		draw_bat(screen, bat)
		
		space.step(1/100.0)
		
		pygame.display.update()
		#pygame.display.flip()
		clock.tick(100)


		
if __name__ == '__main__':
	sys.exit(main())
		
if __name__ == '__main__':
	sys.exit(main())