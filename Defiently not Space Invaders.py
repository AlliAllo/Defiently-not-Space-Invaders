import pygame
import time
from pygame.locals import *
from copy import deepcopy
import os
import random

AFK = 0

shots = []
npcs = []
powerups = []

width, height = 980,600
background = (0, 0, 0)


PAUSED = False
PAUSE = False
Running = True

resizeScreen = 0
resizeSCREEN = False


Display = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pygame.display.set_caption('Definitely not Space Invaders')

playerPNG = [pygame.image.load(os.path.join("jet1.png")), pygame.image.load(os.path.join("jet2.png")),
             pygame.image.load(os.path.join("jet3.png"))]

explo = pygame.image.load(os.path.join("explo.png")).convert_alpha()

shot1 = "bullet.png"

shotGraphicRes1 = [50, 50]

npcGraphicRes1 = [120, 120]  # SQUARE PNG

FPS = 60
timer = pygame.time.Clock()
maxHeight = 300

jetWidth = 128
jetHeight = 128


# "stats" for the Player
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 9
        self.damage = 2
        self.health = 100
        self.velocity = 25
        self.critical = 10
        self.maxCount = 0

        self.critDMG = 2

    def draw(self, screen):
        self.screen = screen

        self.screen.blit(playerPNG[self.maxCount], (self.x, self.y))
        self.maxCount += 1
        if self.maxCount >= 3:
            self.maxCount = 0


# NPC stats
class NPC():
    def __init__(self, x, y, dmg, HP, vel, xspeed, yspeed, npcWidth, npcHeight, graphicPath):
        self.x = x
        self.y = y
        self.speed = [xspeed, yspeed]
        self.vel = vel
        self.NPCWidth = width
        self.NPCHeight = height
        self.HP = HP
        self.dmg = dmg
        self.npcWidth = npcWidth
        self.npcHeight = npcHeight

        self.right = True
        self.down = True

        self.npcGraphic = pygame.image.load(os.path.join(graphicPath)).convert_alpha()

    def draw(self, screen):
        screen.blit(self.npcGraphic, (self.x, self.y))

    def npcMovement(self):
        # x posision
        if self.right:
            self.x += self.speed[0]
            if self.x > width - self.npcWidth:
                self.right = False
        if not self.right:
            self.x -= self.speed[0]
            if self.x <= 0:
                self.right = True
        # y posision
        if self.down:
            self.y += self.speed[1]
            if self.y > height / 2 - self.npcHeight:
                self.down = False
        if not self.down:
            self.y -= self.speed[1]
            if self.y <= 0:
                self.down = True


class Projectile():
    def __init__(self, x, y, speed, graphicPath):
        self.x = x
        self.y = y
        self.speed = speed
        self.graphicPath = graphicPath
        self.shotGraphic = pygame.image.load(os.path.join(graphicPath)).convert_alpha()
        self.exponential = self.speed ** 2 - self.speed * 5  # FIX THIS NUMBER

    def draw(self, screen):
        self.screen = screen
        # Delete bullet if it's out of screen, otherwise move it up.
        if not self.y > height + jetHeight and not self.y < -200:
            self.y -= self.exponential
        else:
            shots.pop(shots.index(shots[0]))
        self.screen.blit(self.shotGraphic, (self.x, self.y))


# I hope you know what this is...
class Collision:
    def collision(self, x1, y1, x2, y2, sizeX, sizeY):
        if x1 >= x2 and x1 <= x2 + sizeX:
            if y1 >= y2 and y1 <= y2 + sizeY:
                return True
        return False


class Font():
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self):
        # Health score
        self.healthFont = pygame.font.Font("pepega.ttf", self.size)
        self.healthText = self.healthFont.render("HEALTH:" + str(self.player.health), True, self.color, background)
        self.healthRect = self.healthText.get_rect()
        self.healthRect.center = (self.x, self.y)

        # scoreboard
        self.scoreFont = pygame.font.Font("pepega.ttf", self.size)
        self.scoreText = self.scoreFont.render("SCORE:" + str(SCORE), True, self.color, background)
        self.scoreRect = self.scoreText.get_rect()
        self.scoreRect.center = (self.x, self.y)


class powerUps:
    def __init__(self, x, y, speed, hp, dmg, powerGraphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.dmg = dmg
        self.powerGraphic = powerGraphic
        self.powerPath = pygame.image.load(os.path.join(powerGraphic)).convert_alpha()

    def draw(self, screen):
        self.screen = screen

        self.y += 5
        if self.y > height + 300:
            powerups.pop(powerups.index(powerups[0]))

        self.screen.blit(self.powerPath, (self.x, self.y))

    def powerUp(self):
        # HOW TO MAKE PLAYER STRONGER
        pass


def update():
    # Make NPC move, and come down from "space"
    Display.fill(background)

    player.draw(Display)

    for npc in npcs:
        npc.draw(Display)

    for shot in shots:
        shot.draw(Display)

    for powerup in powerups:
        powerup.draw(Display)

    pygame.display.flip()


# Starter player and npc
player = Player(width / 2, height - jetHeight * 1.5)
npcs.append(NPC((random.randint(0, (width - 120))), (random.randint(0, maxHeight)), 2, 10, 10, 5, 2, npcGraphicRes1[0],
                npcGraphicRes1[1], "babyYoda.png"))


def collision():
    for npc in npcs:
        global Running
        if Collision().collision(player.x, player.y,npc.x, npc.y, jetWidth, jetHeight):
            Running = False
            print("You died")
            #FIX COLLISION - SOMETHING IS VERY WUNG

    for shot in shots:
        for npc in npcs:
            if Collision().collision(shot.x, shot.y, npc.x, npc.y, npc.npcWidth - shotGraphicRes1[0],
                                   npc.npcHeight - shotGraphicRes1[1]):
                chance = (random.randint(1, 100))
                npcs[0].HP -= player.damage
                # CRIT CHANCE
                if chance <= player.critical:
                    # CRIT ANIMATION
                    npc.HP -= player.damage * player.critDMG

                # Did player die?
                if npcs[0].HP <= 0:
                    npcs.pop(npcs.index(npc))
                    npcs.append(
                        NPC((random.randint(0, (width - 120))), (random.randint(0, maxHeight)), 2, 100, 10, 5, 2,
                            npcGraphicRes1[0], npcGraphicRes1[1], "babyYoda.png"))
                shots.pop(shots.index(shot))

                print("You hit")

            # SHOULD COLLISION BE HERE OR IN OBJECTS? IF HERE SHOULD I REMOVE HP HERE THING


# Main Loop
while Running:
    press = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    if event.type == pygame.VIDEORESIZE and width >= 1920:
        width, height = 980, 600
        Display = pygame.display.set_mode((width, height), RESIZABLE)
        Display = Display
        #HOW TO MAKE WINDOWED FULLSCREEN, AND MAKE SMALLER THE RIGHT WAY

    if event.type == pygame.VIDEORESIZE:
        del Display
        width, height = 1920, 1080
        newDisplay = pygame.display.set_mode((width, height), RESIZABLE)
        Display = newDisplay







    if press[pygame.K_p] and not PAUSED:
        PAUSE = True
        PAUSE = not PAUSE

    if press[pygame.K_ESCAPE]:
        Running = False

        # ADD PAUSE FUNCTION + SIMON THINGY

    if not PAUSE:
        # Movement and wall collisions
        if (press[pygame.K_RIGHT] or press[pygame.K_d]) and not player.x > width - jetWidth:
            player.x += player.speed

        if (press[pygame.K_LEFT] or press[pygame.K_a]) and not player.x < 0:
            player.x -= player.speed

        if (press[pygame.K_UP] or press[pygame.K_w]) and not player.y < 5:
            player.y -= player.speed

        if (press[pygame.K_DOWN] or press[pygame.K_s]) and not player.y > height - jetHeight - 10:
            player.y += player.speed

        if press[pygame.K_SPACE]:
            if len(shots) < 1000:
                shots.append(
                    Projectile(player.x + jetWidth / 2 - shotGraphicRes1[0] / 2, player.y - shotGraphicRes1[1] / 2, 7, shot1))

        if press[pygame.K_r]:
            powerups.append(powerUps(random.randint(0, (width - 120)), (random.randint(0, 350)), 1, 1, 1, "square.png"))

        for npc in npcs:
            npc.npcMovement()
        update()
        collision()
        PAUSED = False
        timer.tick(FPS)


# MAKING SHOOTING ROCKETS/MISSLES

# MAKE STARS WITH A "FORWARD ANIMATION"

# HOW TO PERMANANTLY DELETE A OBJECT -- AND COORDS

# RESTART BUTTON

# HEALTH BAR FOR BOSS

# GAME ICON 

#MAYBE MAKE STARS IN PYGAME, AS CIRCLES - IDEA


