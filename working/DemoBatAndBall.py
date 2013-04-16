#!/usr/bin/env python

import pygame
from pygame import mask
from math import sin, cos, pi, atan2, hypot, sqrt, radians, degrees
import random
import sys

TWO_PI = 2 * pi

pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self, Bat):
        pygame.sprite.Sprite.__init__(self)

        self.bat = Bat

        self.image = pygame.Surface((10,10))
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))

        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 10, 10))
        self.rect = self.image.get_rect()

        self.randomStart = False

        self.reset()

    def reset(self):

        #Polar coordinates
        #self.speed = 3
        #self.angle = 1.5 * pi

        #Cartesian coordinates - more performant
        # (we don't have to do trigonometry on every frame)

        #Set the speed we want the ball to move at
        # (i.e. the hypotenuse of the triangle formed with dx, dy)
        self.speed = 5

        if self.randomStart:
            t2 = self.speed ** 2
            x2 = random.uniform(0.5, t2)
            x = sqrt(x2)
            y = sqrt(t2 - x2)
            self.vector = [x, y]
        else:
            self.vector = [-self.speed, 0]


        self.rect.center = (620, 240)
        self.mask = mask.from_surface(self.image)
        self.colliding = False

    #Translate polar coordinates to x,y vector
    #def get_vector(self):
    #    deltaX = self.speed * sin(self.angle)
    #    deltaY = self.speed * cos(self.angle)
    #    return (deltaX, deltaY)

    def get_angle(self):
        dx, dy = self.vector
        return atan2(-dy, dx) % TWO_PI

    def update(self):
        #vector = self.get_vector()
        dx, dy = self.vector

        #Calculate collisions before actually moving
        newrect = self.rect
        newrect.centerx += dx
        newrect.centery += dy

        #Use a colliding flag so we don't get the ball trapped "inside"
        # the edges
        if self.collision():
            if not self.colliding:
                #pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 10, 10)
                self.colliding = True   

                #Angle of ball to 0 radians (3 o'clock)
                #Pygame y axis is "upside down", so invert dy  
                angleBallIn = self.get_angle()

                #Angle off ball to bat
                angleBat = self.bat.get_angle()
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
                #print "Collided, not updating"            

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

            #POLAR UPDATES
            # #Hit top or bottom
            # if self.rect.top < 0:
            #     self.rect.top = 5
            #     self.angle = 2 * pi - self.angle
            # elif self.rect.bottom > 480:
            #     self.rect.bottom = 475
            #     self.angle = 2 * pi - self.angle


            # #Hit right
            # elif self.rect.right > 640:
            #     self.angle = 2 * pi - self.angle
            #     self.rect.right = 635

            # #Hit left: reset
            # elif self.rect.left < 0:
            #     self.reset()

    def collision(self):
        return pygame.sprite.collide_mask(self, self.bat)

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


class Bat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #Can't get the mask to work with mask! never seems to be set
        #self.imageMaster = pygame.image.load("square_bat.png")
        #self.imageMaster = self.imageMaster.convert_alpha()

        #Draw and rotate a rect in a square transparent surface
        # - mask works fine here
        self.imageMaster = pygame.Surface((100,100))
        self.imageMaster.fill((255,0,255))
        self.imageMaster.set_colorkey((255, 0, 255))
        pygame.draw.rect(self.imageMaster, (255, 255, 255), (44, 0, 8, 100))


        self.image = self.imageMaster
        self.mask = mask.from_surface(self.image, 255);

        self.rect = self.image.get_rect()
        self.rect.center = (80, 240)

        #Direction of rotation (degrees, negative allowed)
        self.dir = 0

        #Speed of rotation (#degrees to turn for each frame)
        self.inc = 5

    def update(self):
        oldCenter = self.rect.center
        #Pygame rotates ANTICLOCKWISE, so invert our direction
        self.image = pygame.transform.rotate(self.imageMaster, -self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        self.mask = mask.from_surface(self.image);

    #Rotation is constrained to +- 90 degrees
    def turnLeft(self):
        if self.dir > -90:
            self.dir -= self.inc
    
    def turnRight(self):
        if self.dir < 90:
            self.dir += self.inc

    #Get the angle in radians (0-2pi)
    # (we store dir in degrees)
    def get_angle(self):
        return radians(self.dir % 360)

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text=None):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 14)
        self.color = (255, 255, 255)

        self.text = text

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def rerender(self, text):
        oldCenter = self.rect.center
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter


def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Rotate with impact masks")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    
    bat = Bat()
    batSprites = pygame.sprite.Group(bat)

    ball = Ball(bat)
    ballSprites = pygame.sprite.Group(ball)
    
    clock = pygame.time.Clock()
    keepGoing = True

    turningLeft, turningRight = (False, False)

    batAngleText = Text(10, 10)
    ballAngleText = Text(10, 30)
    dxText = Text(10, 50)
    dyText = Text(10, 70)
    textSprites = pygame.sprite.Group(batAngleText, ballAngleText, dxText, dyText)

    while keepGoing:
        clock.tick(180)
        #print clock.get_fps()

        background.fill((0, 0, 0))

        ### DEBUG ###
        batAngle = "%.0f" % (degrees(bat.get_angle()))
        batAngleText.rerender(batAngle)

        ballAngle = "%.0f" % (degrees(ball.get_angle()))
        ballAngleText.rerender(ballAngle)

        dx = "%.2f" % (ball.vector[0])
        dy = "%.2f" % (ball.vector[1])
        dxText.rerender(dx)
        dyText.rerender(dy)
        #############

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    turningLeft = True
                elif event.key == pygame.K_RIGHT:
                    turningRight = True
            elif event.type == pygame.KEYUP:
                turningLeft = False
                turningRight = False

        if turningRight:
            bat.turnRight()
        elif turningLeft:
            bat.turnLeft()

        
        batSprites.clear(screen, background)
        batSprites.update()
        batSprites.draw(screen)
        
        ballSprites.clear(screen, background)
        ballSprites.update()
        ballSprites.draw(screen)

        textSprites.clear(screen, background)
        textSprites.update()
        textSprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()