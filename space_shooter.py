import pygame
import random
import math
from pygame import mixer

#initiliaze the game
pygame.init()

#initialize the window
window = pygame.display.set_mode((800,600))

#logo
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

#background
background = pygame.image.load("background.jpg")
#Background music
mixer.music.load("background_misic.wav")
mixer.music.play(-1)

#the spaceship
space_ship = pygame.image.load("spaceship.png")
space_shipX = 370
space_shipY = 500
pos_x_change = 0

#enemy
enemy = []
enemy_x = []
enemy_y = []
enemy_pos_change_x = []
enemy_pos_change_y = [0.5,0.3,0.55,0.4,0.35,0.45]
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy.append(pygame.image.load("asteroid.png"))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(-50,-30))
    enemy_pos_change_x.append(1)

#bullet
bullet = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 500
bullet_pos_change_x = 0
bullet_pos_change_y = 7
bullet_visible = False

score = 0
text_x = 10
text_y = 10
font = pygame.font.Font("freesansbold.ttf",32)


def show_score(x,y):
    score_value = font.render("Score:"+str(score),True,(255,255,255))
    window.blit(score_value,(x,y))
def game_over(x,y):
    over_text = font.render("Game Over",True,(255,255,255))
    window.blit(over_text,(x,y))

def enemy_draw(x,y,i):
    window.blit(enemy[i],(x,y))

def space_ship_draw(x,y):
    window.blit(space_ship,(x,y))

def space_bullet(x,y):
    global bullet_visible
    bullet_visible = True
    window.blit(bullet,(x+20,y+10))

def detect_collision(x1,y1,x2,y2):
    distance = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    if distance<30:
        return True
    return False

def spaceship_collision(x1,y1,x2,y2):
    distance = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    if distance<50:
        return True
    return False

run = True
flag = False
live = 5

while run:
    window.fill((0,0,0))
    window.blit(background,(0,0))
    if flag:
        game_over(300,200)
        mixer.music.stop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if flag==False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pos_x_change = -3
                if event.key == pygame.K_RIGHT:
                    pos_x_change = 3
                if event.key == pygame.K_SPACE:
                    if bullet_visible is False:
                        bullet_x = space_shipX
                        space_bullet(bullet_x,bullet_y)
                        bullet_sound = mixer.Sound("bullet_music.wav")
                        bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pos_x_change = 0
    space_shipX+=pos_x_change
    if space_shipX<=0:
        space_shipX = 0
    elif space_shipX>=736:
        space_shipX = 736
    for i in range(num_of_enemies):
        space_collision = spaceship_collision(space_shipX, space_shipY, enemy_x[i], enemy_y[i])
        if space_collision:
            explosion_sound = mixer.Sound("explosion_music.wav")
            explosion_sound.play()
            space_shipY = 1000
            flag = True

        if flag:
            for x in range(num_of_enemies):
                enemy_y[x] = 2000
            break
        enemy_y[i] += enemy_pos_change_y[i]
        # if enemy_x[i]<=0:
        #     enemy_pos_change_x[i] = 1
        #     enemy_y[i] += enemy_pos_change_y[i]
        # elif enemy_x[i] >=736:
        #     enemy_pos_change_x[i] = -1
        #     enemy_y[i] += enemy_pos_change_y[i]
        if enemy_y[i]>=600:
            score-=1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = -34

        bullet_collision = detect_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if bullet_collision:
            explosion_sound = mixer.Sound("explosion_music.wav")
            explosion_sound.play()
            bullet_y = space_shipY
            bullet_visible = False
            score += 1
            enemy_x[i] = random.randint(0,735)
            enemy_y[i] = -34

        enemy_draw(enemy_x[i], enemy_y[i],i)

    space_ship_draw(space_shipX,space_shipY)

    if bullet_visible is True:
        space_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_pos_change_y
    if bullet_y<0:
        bullet_y = space_shipY
        bullet_visible = False
    show_score(text_x,text_y)
    pygame.display.update()