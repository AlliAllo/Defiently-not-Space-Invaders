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
bossShots = []

width = 1200
height = int(width * 9/16) + 100
background = (0, 0, 0)

playerShooting = True
Running = True
bossSpawned = False
dead = False
paused = False
pause = False
shoot = False
WIN = False

resizeScreen = 0
resizeSCREEN = False


Display = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pygame.display.set_caption('Definitely not Space Invaders')

playerPNG = [pygame.image.load(os.path.join("jet1.png")), pygame.image.load(os.path.join("jet2.png")),
             pygame.image.load(os.path.join("jet3.png"))]

explo = pygame.image.load(os.path.join("explo.png")).convert_alpha()
healthBar = pygame.image.load(os.path.join("healthBar.png")).convert_alpha()
bossBar = pygame.image.load(os.path.join("bossBar.png")).convert_alpha()

shot1 = "bullet.png"


npcshot1 = "npcBullet.png"
npcshot2 = "redcircle.png"

npcGraphicRes2 = [25,25]

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
bossCounter = 0
shotTimer = 0
bossTimer = 0

jetWidth = 115
jetHeight = 115

pygame.init()


# "stats" for the Player
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.damage = 5
        self.health = 100
        self.velocity = 25
        self.critical = 10
        self.maxCount = 0
        self.shootingRate = 2.5

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
        global playerShooting
        if self.spawned:
            self.y += 1
            self.bossTimer += 1
            playerShooting = False
            if self.bossTimer >= npcGraphicRes3[1] / 2 + npcGraphicRes3[1]:
                self.spawned = False
                self.bossrapidFire = True
                playerShooting = True


class Projectile():
    def __init__(self, x, y, speed, graphicPath,verspeed):
        self.x = x
        self.y = y
        self.speed = speed
        self.graphicPath = graphicPath
        self.shotGraphic = pygame.image.load(os.path.join(graphicPath)).convert_alpha()
        self.shootingRate = shootingRate
        self.exponential = self.speed ** 2 - self.speed * 5  # FIX THIS NUMBER
        self.verspeed = verspeed

    def draw(self, screen):
        self.screen = screen
        # Delete bullet if it's out of screen, otherwise move it up.
        self.y -= self.exponential
        if self.y < -200:
            shots.pop(shots.index(shots[0]))
        self.screen.blit(self.shotGraphic, (self.x, self.y))

    def npcDraw(self,screen):
        self.screen = screen
        if not self.y > height - 100 + jetHeight:
            self.y += self.exponential
            self.x += self.verspeed
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
        if self.y > height - 100:
            powerups.pop(powerups.index(powerups[0]))

        self.screen.blit(self.powerPath, (self.x, self.y))


#Update all object visuals into the display

def update():
    Display.fill(background)
    if not dead:
        # Make NPC move, and come down from "space"
        if bossSpawned and not WIN:
            # HEALTH BAR FOR THE BOSS
            Display.blit(bossBar, (100, 0))
            pygame.draw.rect(Display, (255, 0, 0), (102, 2, npcs[0].HP * 10 - 4, 56))

        player.draw(Display)

        for npc in npcs:
            npc.draw(Display)

        for shot in shots:
            shot.draw(Display)

        for npcShot in npcShots:
            npcShot.npcDraw(Display)

        for powerup in powerups:
            powerup.draw(Display)

        if WIN:
            winFont = pygame.font.Font("pepega.ttf", 40)
            winText = winFont.render("You beat the game with a score of " + str(SCORE) + "!", True, (0, 0, 0),
                                     (0, 255, 0))
            winRect = winText.get_rect()
            winRect.center = (width / 2 - 50, height / 2)
            Display.blit(winText, winRect)


        #BOTTOM SIDEBAR FOR STATS
        pygame.draw.rect(Display,(100,100,100),(0,height-100,width,height))

        #SCORE FONT
        scoreFont = pygame.font.Font("pepega.ttf", 20)
        scoreText = scoreFont.render("Score: " + str(SCORE), True, (255,255,255), (100,100,100))
        scoreRect = scoreText.get_rect()
        scoreRect.center = (width / 2 + 200, height-85)
        Display.blit(scoreText,scoreRect)

        dmgFont = pygame.font.Font("pepega.ttf", 15)
        dmgText = dmgFont.render("Damage: " + str(player.damage), True, (255, 255, 255), (100, 100, 100))
        dmgRect = dmgText.get_rect()
        dmgRect.center = (width / 2 - 50, height - 86)
        Display.blit(dmgText, dmgRect)

        speedFont = pygame.font.Font("pepega.ttf", 15)
        speedText = speedFont.render("Speed: " + str(player.speed), True, (255, 255, 255), (100, 100, 100))
        speedRect = speedText.get_rect()
        speedRect.center = (width / 2 - 50, height - 65)
        Display.blit(speedText, speedRect)

        aspeedFont = pygame.font.Font("pepega.ttf", 15)
        aspeedText = aspeedFont.render("Attack speed: " + str(player.shootingRate), True, (255, 255, 255), (100, 100, 100))
        aspeedRect = aspeedText.get_rect()
        aspeedRect.center = (width / 2 - 50, height - 45)
        Display.blit(aspeedText, aspeedRect)

        critFont = pygame.font.Font("pepega.ttf", 15)
        critText = critFont.render("Critical chance: " + str(player.critical) + " %", True, (255, 255, 255), (100, 100, 100))
        critRect = critText.get_rect()
        critRect.center = (width / 2 - 50, height - 25)
        Display.blit(critText, critRect)


        Display.blit(healthBar,(0, height-80))
        # MAN GANGER LIVET MED 4 DA LÆNGDEN AF BARREN ER 400 PIXELS OG MAN STARTER MED HUNDRED LIV
        pygame.draw.rect(Display,(255,0,0),(40,height-78,player.health*4,56))
        pygame.display.flip()

    if dead:
        # DEATH MENU
        pygame.draw.rect(Display,(125,125,125),(1/4*width,1/4*height,(2/4)*width,(2/4)*height))

        deathFont = pygame.font.Font("pepega.ttf", 120)
        deathText = deathFont.render("You died!", True, (255, 255, 255),(125, 125, 125))
        deathRect = deathText.get_rect()
        deathRect.center = (width / 2, height / 2 - 100)
        Display.blit(deathText, deathRect)

        retryFont = pygame.font.Font("pepega.ttf", 80)
        retryText = retryFont.render("Retry", True, (255, 255, 255), (125, 125, 125))
        retryRect = retryText.get_rect()
        retryRect.center = (width / 2, height / 2 + 60)
        Display.blit(retryText, retryRect)
        if pygame.mouse.get_pos()[0] >= 510 and pygame.mouse.get_pos()[0] <= 690 and pygame.mouse.get_pos()[1] >= 415 and pygame.mouse.get_pos()[1] <= 462:
            if pygame.mouse.get_pressed()[0]:
                print("hehe")

        pygame.display.flip()




# Starter player and npc
player = Player(width / 2, height -100 - jetHeight * 1.5)

npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight-npcGraphicRes1[1])), 3, 12, 6, 1, 6, 1, npcGraphicRes1[0],
                npcGraphicRes1[1], "alien1.png",0,True))

pygame.mixer.music.load("song.mp3")

pygame.mixer.music.play(-1)

def collision():
    for npc in npcs:
        global Running, dead
        # COLLISION BETWEEN NPC AND PLAYER
        if Collision().collision(player.x, player.y,npc.x, npc.y,jetWidth-30,jetHeight - 30, npc.npcWidth, npc.npcHeight):
            dead = True

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
                # Did npc die? Then randomly spawn a random powerup
                if npc.HP <= 0:
                    # POWERUP CRATE SPAWNES
                    chance = random.randint(1, 30)
                    if 0 <= chance <= 5:
                        #ATTACK BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0 , 0,0,2,0, "attack.png"))
                    if 5 < chance <= 10:
                        #HEALTH BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0, 0, 20, 0, 0, "health.png"))
                    if 10 < chance <= 15:
                        #ATTACKRATE BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0, 0, 0 ,0, 0.5, "attackSpeed.png"))
                    if 15 < chance <= 20:
                        #SPEED BOOST
                        powerups.append(powerUps(random.randint(0, width - 120), 0, 2, 0 ,0,0, "speed.png"))

                    #REMOVE NPC FROM SCREEN AND THEN SUMMON A NEW ONE
                    npcs.pop(npcs.index(npc))
                    global SCORE
                    if npc.number == 0:
                        SCORE += 1
                        if npc.spawnNew:
                            npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 4, 20, 7, 1.7, 7, 1.5,npcGraphicRes1[0], npcGraphicRes1[1], "alien2.png",1,True))
                    if npc.number == 1:
                        SCORE += 3
                        if npc.spawnNew:
                            npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 7, 40, 6.5,1.2, 7, 1,npcGraphicRes1[0], npcGraphicRes1[1], "alien4.png",2,True))
                    if npc.number == 2:
                        SCORE += 10
                        if npc.spawnNew:
                            npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 13, 75, 6.2,1.4, 5, 1,npcGraphicRes2[0], npcGraphicRes2[1], "alien3.png",3,True))
                    if npc.number == 3:
                        SCORE += 30
                    if npc.number == 4:
                        global WIN
                        SCORE += 100
                        WIN = True

               # BUG FIX FOR WHEN SHOT COLLIDES WITH TWO NPCS AT ONCE
                try:
                    shots.pop(shots.index(shot))
                except:
                    pass
    #COLLISION BETWEEN PLAYER SHOTS AND NPC SHOTS
    for npcshot in npcShots:
        for shot in shots:
            if Collision().collision(npcshot.x, npcshot.y, shot.x, shot.y, shotGraphicRes1[0], shotGraphicRes1[1],
                                     shotGraphicRes1[0], shotGraphicRes1[1]):
                npcShots.pop(npcShots.index(npcshot))
                shots.pop(shots.index(shot))

    #COLLISION BETWEEN NPC SHOTS AND PLAYER
    for npcshot in npcShots:
        # COLLISION BETWEEN NPC SHOTS AND PLAYER
        # SHOT1 IS THE RESOLUTION OF ALL SHOTS, PROBLEM IS THAT THE RED CIRCLES FROM THE BOSS HAVE A DIFFERENT RESOLUTION
        shot1 = [50, 50]
        if len(npcs) >= 1:
            if bossSpawned and npcs[0].bossrapidFire:
                # IF THE BOSS IS DOING HIS FIRE ANIMATION THE SHOTS SHOULD HAVE A RESOLUTION OF 25x25 PIXELS
                shot1 = [25,25]

        if Collision().collision(npcshot.x, npcshot.y, player.x, player.y, shot1[0],shot1[1],jetWidth,jetHeight - 15):
            if len(npcs) >= 1:
                player.health -= npcs[0].dmg
            if player.health <= 0:
                dead = True
                #MAKE A DEATH SCREEN WITH RETRY BUTTON
            npcShots.pop(npcShots.index(npcshot))

    # COLLISION BETWEEN PLAYER AND POWERUP
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

    if press[pygame.K_p] and not pause:

        pauseFont = pygame.font.Font("pepega.ttf", 40)
        pauseText = pauseFont.render("Paused, press P to resume", True, (255, 0, 255), (0, 0, 0))
        pauseRect = pauseText.get_rect()
        pauseRect.center = (width / 2, height / 2 - 50)
        Display.blit(pauseText, pauseRect)
        pygame.display.flip()

        paused = not paused
        pause = True

    if not press[pygame.K_p]:
        pause = False


    if press[pygame.K_ESCAPE]:
        Running = False

    if not paused:
        # Movement and wall collisions
        if (press[pygame.K_RIGHT] or press[pygame.K_d]) and not player.x > width - jetWidth - player.speed + 10:
            player.x += player.speed

        if (press[pygame.K_LEFT] or press[pygame.K_a]) and not player.x < 0 + player.speed - 10:
            player.x -= player.speed

        if (press[pygame.K_UP] or press[pygame.K_w]) and not player.y < 0 + player.speed:
            player.y -= player.speed

        if (press[pygame.K_DOWN] or press[pygame.K_s]) and not player.y > height - 100 - jetHeight - player.speed:
            player.y += player.speed

        #LIMIT HOW OFTEN PLAYER CAN SHOOT
        if shootingRate >= 50:
            if press[pygame.K_SPACE] and playerShooting and not shoot:
                shots.append(Projectile(player.x + jetWidth / 2 - shotGraphicRes1[0] / 2, player.y - shotGraphicRes1[1] / 2, 7, shot1, 0))
                shootingRate = 0
                shoot = True
            if not press[pygame.K_SPACE]:
                shoot = False

        if npcshootingRate >= 35:
            # IF THERE'S AN NPC THEN SHOOT
            if len(npcs) >= 1:
                for npc in npcs:
                    if not npc.spawned and not npc.bossrapidFire and npc.number == 4:
                        npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - shotGraphicRes1[0] / 2, npc.y + shotGraphicRes1[1], npc.vel, npcshot1, 0))
                    if not npc.number == 4:
                        npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - shotGraphicRes1[0] / 2, npc.y + shotGraphicRes1[1], npc.vel, npcshot1, 0))
            npcshootingRate = 0


        for npc in npcs:
            #BOSS ANIMATION
            if npc.bossrapidFire and shotTimer >= 15:
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, 1))
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, 10))
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, 20))
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, 50))

                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, -1))
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, -10))
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, -20))
                npcShots.append(Projectile(npc.x + npc.npcWidth / 2 - 25 / 2, npc.y + 25 + 50, 7, npcshot2, -50))

                bossTimer += 1
                if bossTimer >= 40:
                    npc.bossrapidFire = False

                shotTimer = 0
            shotTimer += 1

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

        #SPAWN BOSS IF ALL NPC's ARE DEAD AND WHEN TIMER IS SET
        if bossCounter > 2000 and not bossSpawned and len(npcs) == 0:
            npcs.append(NPC(width / 2 - 64, -npcGraphicRes3[0] * 1.5, 10, 100, 8, 2, 6.5, 1.2, npcGraphicRes3[0], npcGraphicRes3[1], "alien5.png", 4, False))
            bossSpawned = True

        if npcSpawn >= 400 and not bossCounter > 1999 and not WIN:
            chance = random.randint(1,100)
            if chance <= 90:
                npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 3, 12, 6, 1, 6, 1,
                            npcGraphicRes1[0],npcGraphicRes1[1], "alien1.png", 0,False))
            if chance >= 90:
                npcs.append(NPC((random.randint(0, (width - npcGraphicRes1[0]))), (random.randint(0, maxHeight - npcGraphicRes1[1])), 3, 12, 6, 1, 6, 1,
                                npcGraphicRes1[0], npcGraphicRes1[1], "alien1.png", 0, True))
            npcSpawn = 0


        shootingRate += player.shootingRate

        npcshootingRate += npc.attackRate


        npcSpawn += 1
        timer.tick(FPS)
        bossCounter += 0.5

        update()
        collision()



#NPCS SHOOTING AT THE EXACT SAME TIME BUG

#MAKE BOSS FIGHT MOVEMENT AND SHOOTING

#COLLIDIIING WITH TWO DIFFERENT NPC's AT ONCE

# MAKING SHOOTING ROCKETS/MISSLES

# MAKE STARS WITH A "FORWARD ANIMATION"

# HOW TO PERMANANTLY DELETE A OBJECT -- AND COORDS

# RESTART BUTTON

#  BAR FOR BOSS

#Obstacles?

# GAME ICON

#MAYBE MAKE STARS IN PYGAME, AS CIRCLES - IDEA

