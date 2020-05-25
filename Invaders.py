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

#loading laser image
laserImg = pygame.image.load("Images/laser_bullet.png")
laserImg = laserImg.convert()

class Laser(object):
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.velocity = 5

    def draw(self, screen):
        screen.blit(laserImg, (self.x, self.y))


class Player(object):
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rightOffset = 5
        self.velocity = 5

    def draw(self, screen):
        screen.blit(ssImage, (self.x, self.y))


#framerate clock
clock = pygame.time.Clock()

#initializing Player
spaceship = Player(64, 64, int(screenWidth / 2), int(screenHeight - 64))

#image draw
def redrawGameWindow():
    screen.fill((0,0,0))
    spaceship.draw(screen)

    for laser in lasers:
        laser.draw(screen)

    pygame.display.update()

lasers = []

#creating reload event
RELOAD_SPEED = 450
reloaded_event = pygame.USEREVENT + 1
reloaded = True

#main loop
run = True
while run:
    clock.tick(60)

    #Checking if game window has been closed
    if pygame.event.get(pygame.QUIT): run = False

    #Checking if reload event has occured
    for event in pygame.event.get():
        if event.type == reloaded_event:
            reloaded = True
            pygame.time.set_timer(reloaded_event, 0)

    #laser manager
    for laser in lasers:
        if laser.y > 0 and laser.y < 480:
            laser.y -= laser.velocity
        else:
            lasers.pop(lasers.index(laser))

    #Getting all key presses
    keys = pygame.key.get_pressed()

    #checking for player input
    if keys[pygame.K_RIGHT] and spaceship.x < (screenWidth -spaceship.velocity - spaceship.width + spaceship.rightOffset):
        spaceship.x += spaceship.velocity
    if keys[pygame.K_LEFT] and spaceship.x > 0:
        spaceship.x -= spaceship.velocity
    if keys[pygame.K_SPACE]:
        if reloaded:
            lasers.append(Laser(32, 32, int(spaceship.x + spaceship.width // 4), int(spaceship.y + spaceship.height // 6)))
            reloaded = False
            pygame.time.set_timer(reloaded_event, RELOAD_SPEED)

    redrawGameWindow()

pygame.quit()
