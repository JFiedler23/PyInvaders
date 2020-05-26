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

#loading alien Image
alienImg = pygame.image.load("Images/alien_ship.png")
alienImg = alienImg.convert()


class Laser:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.velocity = 5

    def draw(self, screen):
        screen.blit(laserImg, (self.x, self.y))


class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rightOffset = 5
        self.velocity = 5

    def draw(self, screen):
        screen.blit(ssImage, (self.x, self.y))

    def controller(self, screenWidth, reloaded):
        #Getting all key presses
        keys = pygame.key.get_pressed()

        #checking for player input
        if keys[pygame.K_RIGHT] and self.x < (screenWidth - self.velocity - self.width + self.rightOffset):
            self.x += self.velocity
        if keys[pygame.K_LEFT] and spaceship.x > 0:
            self.x -= self.velocity
        if keys[pygame.K_SPACE]:
            if reloaded:
                lasers.append(Laser(32, 32, int(self.x + self.width // 4), int(self.y + self.height // 6)))
                reloaded = False
                pygame.time.set_timer(RELOADED_EVENT, RELOAD_SPEED)

class Alien:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.moveDistance = 10

    def draw(self, screen):
        screen.blit(alienImg, (self.x, self.y))


#framerate clock
clock = pygame.time.Clock()

#initializing Player
spaceship = Player(64, 64, (screenWidth // 2), (screenHeight - 64))

#initializing aliens
aliens = []
aliensInRow = (screenWidth // 64) - 2
numRows = 4

#alien movement variables
movingLeft = False
movingRight = True

#initializing all aliens
for i in range(aliensInRow):
    for j in range(numRows):
        aliens.append(Alien(64, 64, (64 * i+1), (64 * j)))

lasers = []

#creating reload event
RELOAD_SPEED = 450
RELOADED_EVENT = pygame.USEREVENT + 1
reloaded = True

#creating alien movement event
MOVE_SPEED = 850
ALIEN_MOVE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ALIEN_MOVE_EVENT, MOVE_SPEED)

#image draw
def redrawGameWindow():
    screen.fill((0,0,0))
    spaceship.draw(screen)

    for alien in aliens:
        alien.draw(screen)

    for laser in lasers:
        laser.draw(screen)

    pygame.display.update()


#main loop
run = True
while run:
    largestX = 0
    smallestX = 1000
    clock.tick(60)

    #Checking if game window has been closed
    if pygame.event.get(pygame.QUIT): run = False

    #Checking for custom events
    for event in pygame.event.get():
        if event.type == RELOADED_EVENT:
            reloaded = True
            pygame.time.set_timer(RELOADED_EVENT, 0)
        if event.type == ALIEN_MOVE_EVENT:
            for alien in aliens:
                if alien.x > largestX:
                    largestX = alien.x

                if alien.x < smallestX:
                    smallestX = alien.x

            for alien in aliens:
                #moving right
                if largestX+1 < (screenWidth - alien.width - alien.moveDistance) and movingRight:
                    alien.x += alien.moveDistance
                else:
                    movingLeft = True
                    movingRight = False

                #moving left
                if smallestX > alien.moveDistance and movingLeft:
                    alien.x -= alien.moveDistance
                else:
                    movingLeft = False
                    movingRight = True

    #laser manager
    for laser in lasers:
        if laser.y > 0 and laser.y < 480:
            laser.y -= laser.velocity
        else:
            lasers.pop(lasers.index(laser))



    spaceship.controller(screenWidth, reloaded)

    redrawGameWindow()

pygame.quit()
