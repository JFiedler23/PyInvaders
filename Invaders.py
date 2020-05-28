import pygame
import sys
import main_menu

pygame.init()

#<----------BEGIN: SECTION 1---------->
#<----------PYGAME SPECIFIC OBJECTS---------->

#basic screen setup
screenSize = screenWidth, screenHeight = 640, 480
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Invaders!")

#creating font
gameFont = pygame.font.Font('Atari.ttf', 28)

#framerate clock
clock = pygame.time.Clock()

#Main menu
def MainMenu():
    startButton = pygame.Rect(190, 200, 256, 64)
    font = pygame.font.Font("SPACEBAR.ttf", 32)
    clock.tick(60)

    while True:
        mx, my = pygame.mouse.get_pos()
        titleText = font.render("INVADERS", 1, (255,255,255))
        buttonText= font.render("Start", 1, (0,0,0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if startButton.collidepoint((mx, my)):
                        game()

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (69, 180, 186), startButton, 0)
        screen.blit(titleText, (210, 20))
        screen.blit(buttonText, (250, 210))
        pygame.display.update()

#<----------BEGIN: SECTION 5---------->
#<----------GAME---------->
def game():
    #loading player image
    ssImage = pygame.image.load("Images/spaceship.png")
    pygame.display.set_icon(ssImage)
    ssImage = ssImage.convert()

    #loading laser image
    laserImg = pygame.image.load("Images/laser_bullet.png")
    laserImg = laserImg.convert()

    #loading alien Image
    alienImg = pygame.image.load("Images/alien_ship.png")
    alienImg = alienImg.convert()

    #creating reload event
    RELOAD_SPEED = 350
    RELOADED_EVENT = pygame.USEREVENT + 1
    reloaded = True
    pygame.time.set_timer(RELOADED_EVENT, RELOAD_SPEED)

    #creating alien movement event
    move_speed = 850
    ALIEN_MOVE_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(ALIEN_MOVE_EVENT, move_speed)


    #<----------BEGIN: SECTION 2---------->
    #<----------GAME OBJECT CLASSES---------->

    class Laser:
        def __init__(self, width, height, x, y):
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.velocity = 5
            self.hitbox = (self.x + 9, self.y, 8, 32)

        def draw(self, screen):
            self.hitbox = (self.x + 9, self.y, 8, 32)
            screen.blit(laserImg, (self.x, self.y))
            #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


    class Player:
        def __init__(self, width, height, x, y):
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.rightOffset = 5
            self.velocity = 2
            self.hitbox = (self.x, self.y + 32, 64, 32)

        def draw(self, screen):
            screen.blit(ssImage, (self.x, self.y))
            self.hitbox = (self.x, self.y + 32, 64, 32)
            #pygame.draw.rect(screen, (255, 0 ,0), self.hitbox, 2)

        def controller(self, screenWidth, keys):
            #checking for player input
            if keys[pygame.K_RIGHT] and self.x < (screenWidth - self.velocity - self.width + self.rightOffset):
                self.x += self.velocity
            if keys[pygame.K_LEFT] and player.x > 0:
                self.x -= self.velocity

        def shoot(self, keys):
            if keys[pygame.K_SPACE] and len(lasers) < 3:
                lasers.append(Laser(32, 32, int(self.x + self.width // 4), int(self.y + self.height // 6)))


    class Alien:
        def __init__(self, width, height, x, y):
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.moveDistance = 20
            self.hitbox = (self.x, self.y + 32, 64, 32)

        def draw(self, screen):
            self.hitbox = (self.x, self.y + 32, 64, 32)
            screen.blit(alienImg, (self.x, self.y))
            #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    #<----------BEGIN: SECTION 3---------->
    #<----------INITIALIZING GAME OBJECTS---------->

    #initializing Player
    player = Player(64, 64, (screenWidth // 2), (screenHeight - 64))

    #alien initialization variables
    aliens = []
    aliensInRow = (screenWidth // 64) - 2
    numRows = 4

    #initializing all aliens
    for i in range(aliensInRow):
        for j in range(numRows):
            aliens.append(Alien(64, 64, (70 * i+1), (64 * j)+40))


    #<----------BEGIN: SECTION 4---------->
    #<----------GAMEPLAY FUNCTIONS---------->

    #image draw
    def redrawGameWindow():
        screen.fill((0,0,0))

        scoreText = gameFont.render("Score: "+ str(score), 1, (255,255,255))
        screen.blit(scoreText, (480, 10))

        player.draw(screen)

        for alien in aliens:
            alien.draw(screen)

        for laser in lasers:
            laser.draw(screen)

        pygame.display.update()

    def playerDestory():
        #checking for alien-player collision
        for alien in aliens:
            if (player.hitbox[1] < alien.hitbox[1] + alien.hitbox[3]) and (player.hitbox[1] + player.hitbox[3] > alien.hitbox[1]):
                if (player.hitbox[0] < alien.hitbox[0] + alien.hitbox[2]) and (player.hitbox[0] + player.hitbox[2] > alien.hitbox[0]):
                    return True


    run = True
    movingRight = True #alien movement direction
    score = 0
    lasers = []
    numAliens = len(aliens)

    while run:
        largestX = 0
        smallestX = 1000
        clock.tick(60)

        #Getting all key presses
        keys = pygame.key.get_pressed()

        #Checking for custom events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #player reload event
            if event.type == RELOADED_EVENT:
                player.shoot(keys)

            #Alien movement
            if event.type == ALIEN_MOVE_EVENT:
                #Keeping track of smallest and largest x values
                for alien in aliens:
                    if alien.x > largestX:
                        largestX = alien.x

                    if alien.x < smallestX:
                        smallestX = alien.x

                #Checking boundaries
                for alien in aliens:
                    #moving right
                    if largestX+1 < (screenWidth - alien.width - alien.moveDistance) and movingRight:
                        alien.x += alien.moveDistance
                    #Moving down when right edge of screen is reached
                    elif largestX+5 == (screenWidth - alien.width - alien.moveDistance):
                        alien.y += alien.moveDistance
                    else:
                        movingRight = False

                    #moving left
                    if smallestX > alien.moveDistance and not movingRight:
                        alien.x -= alien.moveDistance
                    else:
                        movingRight = True


        if playerDestory(): run = False

        #laser manager
        for laser in lasers:
            for alien in aliens:
                if (laser.hitbox[1]) < (alien.hitbox[1] + alien.hitbox[3]) and (laser.hitbox[1] + laser.hitbox[3]) > alien.hitbox[2]:
                    if (laser.hitbox[0] - laser.hitbox[2]) < (alien.hitbox[0] + alien.hitbox[2]) and (laser.hitbox[0] + laser.hitbox[2]) > alien.hitbox[0]:
                        score += 100
                        aliens.pop(aliens.index(alien))

                        #just in case two aliens are hit at once
                        try:
                            lasers.pop(lasers.index(laser))
                        except ValueError:
                            continue

            if laser.y > 0 and laser.y < 480:
                laser.y -= laser.velocity
            else:
                lasers.pop(lasers.index(laser))

        #player controller
        player.controller(screenWidth, keys)

        redrawGameWindow()

MainMenu()
