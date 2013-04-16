#!/usr/bin/env python

import pygame
pygame.init()

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.topX, self.topY = (50, 10)
        self.bottomX, self.bottomY = (50, 90)

        #self.imageMaster = pygame.image.load("raspberry_pi_logo.png")
        #self.imageMaster = self.imageMaster.convert()

        self.imageMaster = pygame.Surface((100,100))
        self.image = self.imageMaster

        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.dir = 0

        self.inc = 5

    def update(self):
        # oldCenter = self.rect.center
        # self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        # self.rect = self.image.get_rect()
        # self.rect.center = oldCenter
        self.image.fill((0, 0, 0))
        pygame.draw.line(self.image, (255, 255, 255), (self.topX, self.topY), (self.bottomX, self.bottomY), 5)

    #TODO trig!
    #TODO impact
    def turnLeft(self):
        self.topX -= 5;
        self.bottomX += 5;
    
    def turnRight(self):
        self.topX += 5;
        self.bottomX -= 5;
        
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Rotate a sprite")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    
    ship = Ship()
    allSprites = pygame.sprite.Group(ship)
    
    clock = pygame.time.Clock()
    keepGoing = True

    turningLeft, turningRight = (True, True)

    while keepGoing:
        clock.tick(60)
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

        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
if __name__ == "__main__":
    main()