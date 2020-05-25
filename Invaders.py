import pygame

pygame.init()

#basic screen setup
screenSize = screenWidth, screenHeight = 640, 480
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Invaders!")

#loading spaceship image
ssImage = pygame.image.load("Images/spaceship.png")
pygame.display.set_icon(ssImage)
ssImage = ssImage.convert()

class Player(object):
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rightOffset = 5
        self.velocity = 5

    def controller(self, screenWidth):
        #Getting all key presses
        keys = pygame.key.get_pressed()

        #checking for player input
        if keys[pygame.K_RIGHT] and self.x < (screenWidth - self.velocity - self.width + self.rightOffset):
            self.x += self.velocity
        if keys[pygame.K_LEFT] and spaceship.x > 0:
            self.x -= self.velocity
        if keys[pygame.K_SPACE]:
            print("Fire!")

#framerate clock
clock = pygame.time.Clock()

#image draw
def redrawGameWindow():
    screen.fill((0,0,0))
    screen.blit(ssImage, (spaceship.x,spaceship.y))
    pygame.display.update()

#initializing Player
spaceship = Player(64, 64, int(screenWidth / 2), int(screenHeight - 64))

#main loop
run = True
while run:
    clock.tick(60)

    #Checking if game window has been closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    spaceship.controller(screenWidth)

    redrawGameWindow()

pygame.quit()
