import pygame
import sys
import os
import random
import game_data
from player import *
from laser import *
from alien import *

pygame.init()
my_path = os.path.abspath(os.path.dirname(__file__))

#<----------PYGAME SPECIFIC OBJECTS---------->

#basic screen setup
screenSize = screenWidth, screenHeight = 640, 480
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Invaders!")

#creating font
game_font_path = os.path.join(my_path, '../Fonts/Atari.ttf')
gameFont = pygame.font.Font(game_font_path, 28)

title_font_path = os.path.join(my_path, "../Fonts/SPACEBAR.ttf")
title_font = pygame.font.Font(title_font_path, 32)

#framerate clock
clock = pygame.time.Clock()

#game data object
data = game_data.GameData(0, 1, 850, 40)

#<----------Main Menu---------->
def MainMenu():
    icon_path = os.path.join(my_path, '../Images/icon.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    startButton = pygame.Rect(190, 140, 256, 64)
    high_score_button = pygame.Rect(190, 224, 256, 64)

    while True:
        clock.tick(56)
        mx, my = pygame.mouse.get_pos()

        title_text = title_font.render("INVADERS", 1, (255,255,255))
        startButtonText = title_font.render("Start", 1, (0,0,0))
        high_score_button_text = title_font.render("Scores", 1, (0,0,0))

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
                        game(data)
                    elif high_score_button.collidepoint((mx, my)):
                        DisplayHighScores()

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (69, 180, 186), startButton, 0)
        pygame.draw.rect(screen, (69, 180, 186), high_score_button, 0)
        screen.blit(title_text, (210, 20))
        screen.blit(startButtonText, (250, 150))
        screen.blit(high_score_button_text, (235, 235))
        pygame.display.update()

#<----------GAME OVER SCREEN---------->
def GameOver():
    SaveHighScores(data.score)

    game_over_sound_path = os.path.join(my_path, "../Sounds/Game_Over.wav")
    game_over_sound = pygame.mixer.Sound(game_over_sound_path)

    game_over_sound.play()

    while True:
        clock.tick(60)

        gameOverText = title_font.render("GAME OVER", 1, (255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()

        screen.fill((0,0,0))
        screen.blit(gameOverText, (210, 20))
        pygame.display.update()

#<----------CHECKING/SAVING HIGH SCORES---------->
def SaveHighScores(score):
    high_scores = []
    index = -1

    #Getting current high scores list
    with open("high_scores.txt", "r") as f:
        high_scores_data = f.readlines()

    #splitting entries between name and high score
    for item in high_scores_data:
        high_scores.append(item.split())

    #Checking if player set a new high score
    for i in high_scores:
        #if so grabbing index of beaten high score
        if score >= int(i[1]):
            index = high_scores.index(i)
            break

    #if we have new high score
    if index > -1:
        name = GetPlayerName()
        high_scores.pop()
        new_entry = [name, str(score)]

        #scores before and after index
        top = high_scores[:index]
        top.append(new_entry)
        bottom = high_scores[index:]

        #Creating new high scores list
        new_high_scores = top + bottom

        #writing new high scores to file
        with open("high_scores.txt", "w") as f:
            for i in new_high_scores:
                entry = i[0] + " " + i[1] + "\n"
                f.write(entry)

        DisplayHighScores()

#<----------HIGH SCORE SCREEN---------->
def DisplayHighScores():
    x, y = 225, 70
    yIncrease = 0

    title_text = title_font.render("High Scores", 0, ((255,255,255)))

    #Getting current high scores list
    with open("high_scores.txt", "r") as f:
        high_scores_data = f.readlines()

    while True:
        clock.tick(56)
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()

        for entry in high_scores_data:
            score_text = gameFont.render(entry[:-1], 0, ((255,255,255)))
            screen.blit(score_text, (x, y+yIncrease))
            yIncrease += 40

        yIncrease = 0

        screen.blit(title_text, (170, 20))
        pygame.display.update()

def GetPlayerName():
    name = ""
    #input_field = pygame.Rect(190, 140, 256, 64)
    title_text = title_font.render("New High Score!", 0, (255,255,255))
    input_header = gameFont.render("Enter your name: ", 0, (255,255,255))

    #Getting player name
    while True:
        name_text = gameFont.render(name, 0, (255,255,255))
        clock.tick(56)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((0,0,0))
        #pygame.draw.rect(screen, (69, 180, 186), input_field, 2)
        screen.blit(title_text, (140, 20))
        screen.blit(input_header, (170, 150))
        screen.blit(name_text, (395, 150))
        pygame.display.update()

#<----------GAME---------->
def game(data):
    #Creating sound objects
    laser_sound_path = os.path.join(my_path, "../Sounds/Laser_1.wav")
    laser_sound = pygame.mixer.Sound(laser_sound_path)

    explosion_sound_path = os.path.join(my_path, "../Sounds/Explosion.wav")
    explosion_sound = pygame.mixer.Sound(explosion_sound_path)

    #loading player image
    spaceship_path = os.path.join(my_path, "../Images/spaceship.png")
    ssImage = pygame.image.load(spaceship_path)
    ssImage = ssImage.convert()

    #loading laser image
    laser_path = os.path.join(my_path, "../Images/laser_bullet.png")
    laserImg = pygame.image.load(laser_path)
    laserImg = laserImg.convert()

    #loading alien Image
    alien_path = os.path.join(my_path, "../Images/alien_ship.png")
    alienImg = pygame.image.load(alien_path)
    alienImg = alienImg.convert()

    explosionImg = [pygame.image.load(os.path.join(my_path, "../Images/explosion_1.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_2.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_3.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_4.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_5.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_6.png")), \
                    pygame.image.load(os.path.join(my_path, "../Images/explosion_7.png"))]

    #creating player shoot event
    RELOAD_SPEED = 350
    RELOADED_EVENT = pygame.USEREVENT + 1
    reloaded = True
    pygame.time.set_timer(RELOADED_EVENT, RELOAD_SPEED)

    #creating alien movement event
    move_speed = data.alien_speed
    ALIEN_MOVE_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(ALIEN_MOVE_EVENT, move_speed)

    #creating alien shoot event
    ALIEN_SHOOT_SPEED = 900
    ALIEN_SHOOT_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(ALIEN_SHOOT_EVENT, ALIEN_SHOOT_SPEED)

    #explosion event
    EXPLOSION_SPEED = 200
    EXPLOSION_EVENT = pygame.USEREVENT + 4
    pygame.time.set_timer(EXPLOSION_EVENT, EXPLOSION_SPEED)

    #<----------INITIALIZING GAME OBJECTS---------->

    #initializing Player
    mainPlayer = Player(64, 64, (screenWidth // 2), (screenHeight - 64))

    #alien initialization variables
    aliens = []
    aliensInRow = (screenWidth // 64) - 2
    numRows = 4

    #initializing all aliens
    for i in range(aliensInRow):
        for j in range(numRows):
            aliens.append(Alien(64, 64, (70 * i+1), (64 * j)+data.alien_y))


    #<----------GAMEPLAY FUNCTIONS---------->
    #image draw
    def redrawGameWindow():
        scoreText = gameFont.render("Score: "+ str(data.score), 1, (255,255,255))
        levelText = gameFont.render("Level: "+ str(data.curr_level), 1, (255, 255, 255))

        screen.blit(scoreText, (480, 10))
        screen.blit(levelText, (10, 10))

        mainPlayer.draw(screen, ssImage)

        for alien in aliens:
            alien.draw(screen, alienImg)

        for laser in playerLasers:
            laser.draw(screen, laserImg)

        for laser in alienLasers:
            laser.draw(screen, laserImg)


    def playerDestory():
        #checking for alien-player collision
        for alien in aliens:
            if (mainPlayer.hitbox[1] < alien.hitbox[1] + alien.hitbox[3]) and (mainPlayer.hitbox[1] + mainPlayer.hitbox[3] > alien.hitbox[1]):
                if (mainPlayer.hitbox[0] < alien.hitbox[0] + alien.hitbox[2]) and (mainPlayer.hitbox[0] + mainPlayer.hitbox[2] > alien.hitbox[0]):
                    return True


    #<----------GAMEPLAY VARIABLES---------->
    run = True
    movingRight = True #alien movement direction
    animCount = 0
    explosion = False
    playerLasers = []
    alienLasers = []
    numAliens = len(aliens)

    #<----------GAME LOOP---------->
    while run:
        screen.fill((0,0,0))

        largestX = 0
        smallestX = 1000
        clock.tick(56)

        #Getting all key presses
        keys = pygame.key.get_pressed()

        #Checking for custom events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #player reload event
            if event.type == RELOADED_EVENT:
                mainPlayer.shoot(keys, playerLasers, laser_sound)

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
                    if largestX < (screenWidth - alien.width - alien.moveDistance) and movingRight:
                        alien.x += alien.moveDistance
                    #Moving down when right edge of screen is reached
                    elif largestX+5 == (screenWidth - alien.width - alien.moveDistance):
                        alien.y += alien.moveDistance
                    else:
                        movingRight = False

                    #moving left
                    if smallestX >= alien.moveDistance and not movingRight:
                        alien.x -= alien.moveDistance
                    else:
                        movingRight = True

            #Alien shooting
            if event.type == ALIEN_SHOOT_EVENT:
                if len(aliens) > 0:
                    choice = random.randint(0, len(aliens)-1)
                    aliens[choice].shoot(alienLasers, laser_sound)

        if playerDestory():
            explosion_sound.play()
            run = False
            GameOver()

        #Player laser manager
        for laser in playerLasers:
            #Checking if an alien has been hit
            for alien in aliens:
                if (laser.hitbox[1]) < (alien.hitbox[1] + alien.hitbox[3]) and (laser.hitbox[1] + laser.hitbox[3]) > alien.hitbox[1]:
                    if (laser.hitbox[0] - laser.hitbox[2]) < (alien.hitbox[0] + alien.hitbox[2]) and (laser.hitbox[0] + laser.hitbox[2]) > alien.hitbox[0]:
                        explosion_sound.play()
                        data.score += 100
                        tempX, tempY = alien.x, alien.y
                        aliens.pop(aliens.index(alien))

                        explosion = True
                        #just in case two aliens are hit at once
                        try:
                            playerLasers.pop(playerLasers.index(laser))
                        except ValueError:
                            continue

            if laser.y > 0 and laser.y < screenHeight:
                laser.y -= laser.velocity
            else:
                playerLasers.pop(playerLasers.index(laser))

        #Alien laser manager
        for laser in alienLasers:
            #checking if player has been hit
            if (laser.hitbox[1] < mainPlayer.hitbox[1] + mainPlayer.hitbox[3]) and (laser.hitbox[1] + laser.hitbox[3] > mainPlayer.hitbox[1]):
                if (laser.hitbox[0] - laser.hitbox[2] < mainPlayer.hitbox[0] + mainPlayer.hitbox[2]) and (laser.hitbox[0] + laser.hitbox[2] > mainPlayer.hitbox[0]):
                    explosion_sound.play()
                    run = False
                    GameOver()

            if laser.y < screenHeight and laser.y > 0:
                laser.y += laser.velocity
            else:
                alienLasers.pop(alienLasers.index(laser))

        #player controller
        mainPlayer.controller(screenWidth, keys)

        #explosion animation
        if animCount + 1 >= 56:
            animCount = 0
            explosion = False

        if explosion:
            screen.blit(explosionImg[animCount//8], (tempX, tempY))
            animCount += 1

        #player wins level, start new level.
        if len(aliens) <= 0 and data.curr_level <= 10:
            data.curr_level += 1
            data.alien_y += 5
            data.alien_speed -= 5
            game(data)


        redrawGameWindow()

        pygame.display.update()

MainMenu()
