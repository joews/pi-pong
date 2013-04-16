#!/usr/bin/env python

import pygame
from pygame import mask

pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)

        self.ship = ship

        self.image = pygame.Surface((10,10))
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))

        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 10, 10))

        self.rect = self.image.get_rect()
        self.rect.center = (300, 200)

        self.mask = mask.from_surface(self.image)

    def update(self):
        if self.collision():
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 10, 10))
        else:
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 10, 10))

    def collision(self):
        return pygame.sprite.collide_mask(self, self.ship)


class Ship(pygame.sprite.Sprite):
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
        self.rect.center = (320, 240)

        self.dir = 0
        self.inc = 5

    def update(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        self.mask = mask.from_surface(self.image);

    def turnLeft(self):
        self.dir += self.inc
        if self.dir > 360:
            self.dir = self.inc
    
    def turnRight(self):
        self.dir -= self.inc
        if self.dir < 0:
            self.dir = 360 - self.inc
        
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Rotate with impact masks")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    
    ship = Ship()
    shipSprites = pygame.sprite.Group(ship)

    ball = Ball(ship)
    ballSprites = pygame.sprite.Group(ball)
    
    clock = pygame.time.Clock()
    keepGoing = True

    turningLeft, turningRight = (True, True)

    while keepGoing:
        clock.tick(180)
        print clock.get_fps()

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
            ship.turnRight()
        elif turningLeft:
            ship.turnLeft()

        
        shipSprites.clear(screen, background)
        shipSprites.update()
        shipSprites.draw(screen)
        
        ballSprites.clear(screen, background)
        ballSprites.update()
        ballSprites.draw(screen)

        pygame.display.flip()
    
if __name__ == "__main__":
    main()