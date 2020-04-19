import pygame
import time
from pygame.locals import *
from copy import deepcopy
import os
import random

shootingRate = 0
npcshootingRate = 0
AFK = 0

shots = []
npcs = []
powerups = []
npcShots = []

width = 1200
height = int(width * 9/16)
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
healthIcon = pygame.image.load(os.path.join("healthIcon.png")).convert_alpha()

shot1 = "bullet.png"

npcshot1 = "npcBullet.png"
npcshot1Res = [50,50]

shotGraphicRes1 = [50, 50]
powerupWidth,powerupHeight = 60,60

npcGraphicRes1 = [180, 180]
npcGraphicRes2 = [240, 240]
npcGraphicRes3 = [128, 128]

FPS = 45
timer = pygame.time.Clock()
maxHeight = int(height/3)
SCORE = 0
npcSpawn = 0

jetWidth = 115
jetHeight = 115


# "stats" for the Player
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 6
        self.damage = 50  #NORMAL ER 2
        self.health = 100
        self.velocity = 25
        self.critical = 10
        self.maxCount = 0
        self.shootingRate = 3

        self.critDMG = 2

    def draw(self, screen):
        self.screen = screen

        self.screen.blit(playerPNG[self.maxCount], (self.x, self.y))
        self.maxCount += 1
        if self.maxCount >= 3:
            self.maxCount = 0


# NPC stats
class NPC():
    def __init__(self, x, y, dmg, HP, vel,attackRate, xspeed, yspeed, npcWidth, npcHeight, graphicPath,number,spawnNew):
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
        self.attackRate = attackRate
        self.number = number
        self.speed2 = [xspeed * 2, yspeed*2]
        self.speed3 = [xspeed * 0.8, yspeed*0.8]
        self.speed4 = [xspeed * 0.4, yspeed*0.4]
        self.speed5 = [xspeed * 3, yspeed * 3]
        self.spawnNew = spawnNew

        self.right = True
        self.down = True

        self.bossrapidFire = False
        self.spawned = True
        self.bossTimer = 0

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
            if self.y > maxHeight - self.npcHeight:
                self.down = False
        if not self.down:
            self.y -= self.speed[1]
            if self.y <= 0:
                self.down = True

    def npcMovement2(self):
        # x posision
        if self.right:
            self.x += self.speed2[0]
            if self.x > width - self.npcWidth:
                self.right = False
        if not self.right:
            self.x -= self.speed2[0]
            if self.x <= 0:
                self.right = True
        # y posision
        if self.down:
            self.y += self.speed2[1]
            if self.y > maxHeight - self.npcHeight:
                self.down = False
        if not self.down:
            self.y -= self.speed2[1]
            if self.y <= 0:
                self.down = True


    def npcMovement3(self):
        # x posision
        if self.right:
            self.x += self.speed3[0]
            if self.x > width - self.npcWidth:
                self.right = False
        if not self.right:
            self.x -= self.speed3[0]
            if self.x <= 0:
                self.right = True
        # y posision
        if self.down:
            self.y += self.speed3[1]
            if self.y > maxHeight - self.npcHeight:
                self.down = False
        if not self.down:
            self.y -= self.speed3[1]
            if self.y <= 0:
                self.down = True

    def npcMovement4(self):
        # x posision
        if self.right:
            self.x += self.speed4[0]
            if self.x > width - self.npcWidth:
                self.right = False
        if not self.right:
            self.x -= self.speed4[0]
            if self.x <= 0:
                self.right = True
        # y posision
        if self.down:
            self.y += self.speed4[1]
            if self.y > maxHeight - self.npcHeight:
                self.down = False
        if not self.down:
            self.y -= self.speed4[1]
            if self.y <= 0:
                self.down = True

    def npcMovement5(self):
        #COOL BOSS MOVEMENT
        if not self.spawned and not self.bossrapidFire:
            # x posision
            if self.right:
                self.x += self.speed5[0]
                if self.x > width - self.npcWidth:
                    self.right = False
            if not self.right:
                self.x -= self.speed5[0]
                if self.x <= 0:
                    self.right = True
            # y posision
            if self.down:
                self.y += self.speed5[1]
                if self.y > maxHeight - self.npcHeight:
                    self.down = False
            if not self.down:
                self.y -= self.speed5[1]
                if self.y <= 0:
                    self.down = True
        if self.spawned:
            self.y += 1
            self.bossTimer += 1
            if self.bossTimer >= npcGraphicRes3[1] / 2 + npcGraphicRes3[1]:
                self.spawned = False
                self.bossrapidFire = True


class Projectile():
    def __init__(self, x, y, speed, graphicPath):
        self.x = x
        self.y = y
        self.speed = speed
        self.graphicPath = graphicPath
        self.shotGraphic = pygame.image.load(os.path.join(graphicPath)).convert_alpha()
        self.shootingRate = shootingRate
        self.exponential = self.speed ** 2 - self.speed * 5  # FIX THIS NUMBER

    def draw(self, screen):
        self.screen = screen
        # Delete bullet if it's out of screen, otherwise move it up.
        self.y -= self.exponential
        if self.y < -200:
            shots.pop(shots.index(shots[0]))
        self.screen.blit(self.shotGraphic, (self.x, self.y))


    def npcDraw(self,screen):
        self.screen = screen
        if not self.y > height + jetHeight:
            self.y += self.exponential
        else:
            npcShots.pop(npcShots.index(npcShots[0]))

        self.screen.blit(self.shotGraphic, (self.x, self.y))




# I hope you know what this is...
class Collision:
    def collision(self, x1, y1, x2, y2, sizeX, sizeY,size2X,size2Y):
        if x1 >= x2 and x1 <= x2 + size2X or x2 >= x1 and x2 <= x1 + sizeX:
            if y1 >= y2 and y1 <= y2 + size2Y or y2 >= y1 and y2 <= y1 + sizeY:
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


class healthBars:
    def __init__(self):
        self.x = 0
        self.y = height - 200
        self.color = color


class powerUps:
    def __init__(self, x, y, speed, hp, dmg,attackRate, powerGraphic):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.dmg = dmg
        self.powerGraphic = powerGraphic
        self.attackRate = attackRate
        self.powerPath = pygame.image.load(os.path.join(powerGraphic)).convert_alpha()

    def draw(self, screen):
        self.screen = screen
        self.y += 4
        if self.y > height + 200:
            powerups.pop(powerups.index(powerups[0]))

        self.screen.blit(self.powerPath, (self.x, self.y))



def update():
    # Make NPC move, and come down from "space"
    Display.fill(background)

    player.draw(Display)

    for npc in npcs:
        npc.draw(Display)

    for shot in shots:
        shot.draw(Display)

    for npcShot in npcShots:
        npcShot.npcDraw(Display)

    for powerup in powerups:
        powerup.draw(Display)



    #Display.blit(healthIcon,(0, height-200))

    pygame.display.flip()


# Starter player and npc
player = Player(width / 2, height - jetHeight * 1.5)
npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight-npcGraphicRes1[1])), 3, 10, 10,1, 5, 1, npcGraphicRes1[0],
                npcGraphicRes1[1], "alien1.png",0,True))


def collision():
    for npc in npcs:
        global Running
        # COLLISION BETWEEN NPC AND PLAYER
        if Collision().collision(player.x, player.y,npc.x, npc.y,jetWidth,jetHeight - 15, npc.npcWidth, npc.npcHeight):
            print("You died")
            #FIX COLLISION - SOMETHING IS VERY WUNG

    for shot in shots:
        for npc in npcs:
            #COLLISION BETWEEN NPC AND PLAYER SHOTS
            if Collision().collision(shot.x, shot.y, npc.x, npc.y,shotGraphicRes1[0],shotGraphicRes1[1], npc.npcWidth, npc.npcHeight):
                chance = (random.randint(1, 100))
                npc.HP -= player.damage
                # CRIT CHANCE
                if chance <= player.critical:
                    # CRIT ANIMATION
                    npc.HP -= player.damage * player.critDMG
                    print("you qwuit")

                # Did npc die?
                if npc.HP <= 0:
                    # POWERUP CRATE SPAWNES
                    chance = random.randint(1, 20)
                    if 0 <= chance <= 5:
                        #ATTACK BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0 , 0,0,1,0, "attack.png"))
                    if 5 < chance <= 10:
                        #HEALTH BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0, 0, 10, 0, 0, "health.png"))
                    if 10 < chance <= 15:
                        #ATTACKRATE BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0, 0, 0 ,0, 3, "attackSpeed.png"))
                    if 15 < chance <= 20:
                        #SPEED BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0, 1.2, 0 ,0,0, "speed.png"))

                    #REMOVE NPC FROM SCREEN AND THEN SUMMON A NEW ONE
                    npcs.pop(npcs.index(npc))
                    if npc.number == 0 and npc.spawnNew:
                        npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 6, 20, 10,1, 5, 1,npcGraphicRes1[0], npcGraphicRes1[1], "alien2.png",1,True))
                    if npc.number == 1 and npc.spawnNew:
                        npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 6, 50, 10,1, 5, 1,npcGraphicRes1[0], npcGraphicRes1[1], "alien4.png",2,True))
                    if npc.number == 2 and npc.spawnNew:
                        npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 6, 50, 10,1, 5, 1,npcGraphicRes2[0], npcGraphicRes2[1], "alien3.png",3,True))
                    if npc.number == 3 and npc.spawnNew:
                        npcs.append(NPC(width / 2 - 64, -npcGraphicRes3[0] * 1.5 , 6, 50, 10,1, 5, 1,npcGraphicRes3[0], npcGraphicRes3[1], "alien5.png",4,False))


               # BUG FIX FOR WHEN SHOT COLLIDES WITH TWO NPCS AT ONCE
                try:
                    shots.pop(shots.index(shot))
                except:
                    pass

    for npcshot in npcShots:
        for shot in shots:
            if Collision().collision(npcshot.x, npcshot.y, shot.x, shot.y, shotGraphicRes1[0], shotGraphicRes1[1],
                                     npcshot1Res[1], npcshot1Res[1]):

                npcShots.pop(npcShots.index(npcshot))
                shots.pop(shots.index(shot))


    for npcshot in npcShots:
        # COLLISION BETWEEN NPC SHOTS AND PLAYER
        if Collision().collision(npcshot.x, npcshot.y, player.x, player.y, shotGraphicRes1[0],shotGraphicRes1[1],jetWidth,jetHeight - 15):
            if len(npcs) >= 1:
                for npc in npcs:
                    player.health -= npc.dmg
                if player.health <= 0:
                    print("You died")
                    #MAKE A DEATH SCREEN WITH RETRY BUTTON
                npcShots.pop(npcShots.index(npcshot))


    for powerup in powerups:
        #COLLISION BETWEEN PLAYER AND POWERUP
        if Collision().collision(powerup.x, powerup.y, player.x, player.y, powerupWidth,powerupHeight,jetWidth,jetHeight - 15):
            #POWER PLAYER UP

            player.speed += powerup.speed
            player.health += powerup.hp
            #MAKE SURE PLAYER DOESN'T EXCEED 100 HP
            if player.health > 100:
                player.health = 100
            player.damage += powerup.dmg
            player.shootingRate += powerup.attackRate
            #REMOVE THE POWERUP AFTER COLLISION
            powerups.pop(powerups.index(powerup))







# Main Loop
while Running:
    press = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False



        #HOW TO MAKE WINDOWED FULLSCREEN, AND MAKE SMALLER THE RIGHT WAY

    if event.type == pygame.VIDEORESIZE:
        width = 1200
        height = int(width * 9/16)
        newDisplay = pygame.display.set_mode((width, height), FULLSCREEN)
        Display = newDisplay

    if press[pygame.K_p] and not PAUSED:
        PAUSE = True
        PAUSE = not PAUSE

    if press[pygame.K_ESCAPE]:
        Running = False


    if not PAUSE:
        # Movement and wall collisions
        if (press[pygame.K_RIGHT] or press[pygame.K_d]) and not player.x > width - jetWidth - player.speed + 10:
            player.x += player.speed

        if (press[pygame.K_LEFT] or press[pygame.K_a]) and not player.x < 0 + player.speed - 10:
            player.x -= player.speed

        if (press[pygame.K_UP] or press[pygame.K_w]) and not player.y < 0 + player.speed:
            player.y -= player.speed

        if (press[pygame.K_DOWN] or press[pygame.K_s]) and not player.y > height - jetHeight - player.speed:
            player.y += player.speed

        #LIMIT HOW OFTEN PLAYER CAN SHOOT
        if shootingRate >= 50:
            if press[pygame.K_SPACE]:
                shots.append(Projectile(player.x + jetWidth / 2 - shotGraphicRes1[0] / 2, player.y - shotGraphicRes1[1] / 2, 7, shot1))
                shootingRate = 0

        if npcshootingRate >= 35:
            if len(npcs) >= 1:
                for npc in npcs:
                    if not npc.spawned and not npc.bossrapidFire and npc.number == 4:
                        print("pew pew")
                    if not npc.number == 4:
                        npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - shotGraphicRes1[0] / 2, npc.y + shotGraphicRes1[1], 7, npcshot1))
            npcshootingRate = 0

        for npc in npcs:
            if npc.bossrapidFire:
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - shotGraphicRes1[0] / 2, npc.y + shotGraphicRes1[1], 7, npcshot1))

        for npc in npcs:
            if npc.number == 0:
                npc.npcMovement()
            if npc.number == 1:
                npc.npcMovement2()
            if npc.number == 2:
                npc.npcMovement3()
            if npc.number == 3:
                npc.npcMovement4()
            if npc.number == 4:
                npc.npcMovement5()

        if len(npcs) == 0 and SCORE >= 100:
            print("SPawn")

        update()
        collision()

        if npcSpawn >= 200:
            chance = random.randint(1,100)
            if chance <= 85:
                npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 3, 10, 10, 1, 5, 1,
                            npcGraphicRes1[0],npcGraphicRes1[1], "alien1.png", 0,False))
            if chance >= 85:
                npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 3, 10, 10, 1, 5, 1,
                                npcGraphicRes1[0], npcGraphicRes1[1], "alien1.png", 0, True))
            npcSpawn = 0


        shootingRate += player.shootingRate
        npcshootingRate += npc.attackRate

        npcSpawn += 1
        timer.tick(FPS)


#NPCS SHOOTING AT THE EXACT SAME TIME BUG

#MAKE BOSS FIGHT MOVEMENT AND SHOOTING

#SKAL MAN GENTAGE COLLISION CHECK FOR npc IN npcs.

# IF YOU KILL NPC AND THEY SHOO

#COLLIDIIING WITH TWO DIFFERENT NPC's AT ONCE

# MAKING SHOOTING ROCKETS/MISSLES

# MAKE STARS WITH A "FORWARD ANIMATION"

# HOW TO PERMANANTLY DELETE A OBJECT -- AND COORDS

# RESTART BUTTON

# ADD MUSIC AND SOUND EFFECTS

#  BAR FOR BOSS

#Obstacles?

# GAME ICON

#MAYBE MAKE STARS IN PYGAME, AS CIRCLES - IDEA

# HOW TO DISGUANGE BETWEEN NPCS - OBJECTS

# SET CODE TOGETHER LAST THING

