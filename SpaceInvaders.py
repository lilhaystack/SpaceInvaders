# Space Invaders
# Author lil haystack
#
# Litteraly space invaders but like a clone
# 
# Planned features not yet implemented:
# - bonus dropped if strobing invader hit
# - high scores tracking using pickled data
# - explosion effects (drawn using colored pixels?)
# - more....

import math
import pygame
import random
import sys
from itertools import cycle
from datetime import datetime
from pygame import gfxdraw
from pygame.locals import *

def print_text(surface, font, text, surf_rect, x = 0, y = 0, center = False,\
               color = (255, 255, 255)):
    """
    Draws text onto a surface. If center, text is centered on screen at y
    """
    if not center:
        textimage = font.render(text, True, color)
        surface.blit(textimage, (x, y))
    else:
        textimage = font.render(text, True, color)
        text_rect = textimage.get_rect()
        x = (surf_rect.width // 2) - (text_rect.width // 2 )
        surface.blit(textimage, (x, y))

def game_is_over(surface, font, ticks):
    timer = ticks
    surf_rect = surface.get_rect()
    surf_height = surf_rect.height
    surf_width = surf_rect.width
    print_text(screen, font, "G A M E  O V E R", surf_rect, y = 260,\
               center = True)
    pygame.display.update()
    while True:
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if ticks > timer + 3000:
            break

def next_level(level):
    level += 1
    if level > 6:
        level = 6
    return level

def load_level(level):
    # create and populate(not all) lists
    invaders, colors = [], []

    start_intx, end_intx, increment_intx = 85, 725, 40 # 85, 725
    start_inty, end_inty, increment_inty = 60, 60, 30 #
    end_inty = end_inty + level * 30 # rows invaders = level number
    color_val = 256 / end_inty # ensure no color repetition
    for x in range(start_intx, end_intx, increment_intx):
        for y in range(start_inty, end_inty, increment_inty):
            invaders.append(pygame.Rect(x, y, 30, 15))
            colors.append(((x * 0.35) % 256, (y * color_val) % 256))

    return invaders, colors, len(invaders)

def draw_title_invader():
    rect = Rect(285,247,230,115)
    rect_width = 230
    a = 71
    b = 171
    pygame.draw.rect(backbuffer, (150,a, b),rect)
    # left eye
    pygame.draw.circle(backbuffer, BLACK, (rect.x+46,rect.y+30), 23)
    #right eye
    pygame.draw.circle(backbuffer, BLACK,(rect.x+rect_width-46,rect.y+30)\
                                          ,23)
    # left antennae
    pygame.draw.line(backbuffer, (150, a, b),(rect.x+115, rect.y),\
                     (rect.x+50, rect.y-55),2 )
    # right antennae
    pygame.draw.line(backbuffer,(150, a, b), (rect.x+ rect_width - 113,\
                            rect.y),(rect.x + rect_width-50, rect.y-55),2)
    # left side mouth
    pygame.draw.line(backbuffer, BLACK, (rect.x+46, rect.y+92),\
                        (rect.x + 115, rect.y + 61), 2)
    # right side mouth
    pygame.draw.line(backbuffer, BLACK, (rect.x+rect_width-46,\
                        rect.y+92), (rect.x+rect_width-115,\
                        rect.y+61), 2)

def draw_bonus_invader(i, bonus_color, bx, bonus_x):
    if i == 0:
        pygame.draw.circle(backbuffer, bonus_color,
                           (bonus_invader.x+bx,bonus_invader.y+7),2)
    if i == 1:
        pygame.draw.circle(backbuffer, bonus_color,
                           (bonus_invader.x+bx,bonus_invader.y+7),2)
    if i == 2:
        pygame.draw.circle(backbuffer, bonus_color,
                           (bonus_invader.x+bx,bonus_invader.y+7),2)
    if i == 3:
        pygame.draw.circle(backbuffer, bonus_color,
                           (bonus_invader.x+bx,bonus_invader.y+7),2)
    if i == 4:
        pygame.draw.circle(backbuffer, bonus_color,
                           (bonus_invader.x+bx,bonus_invader.y+7),2)
    if i == 5:
        pygame.draw.circle(backbuffer, bonus_color,
                           (bonus_invader.x+bx,bonus_invader.y+7),2)
        bx = next(bonus_x) # skip a color(ie it's not drawn)to move
                           # light sequence up ship


def draw_invader(backbuffer, rect, a, b, animate_invaders, ticks,\
                 animation_time):
    invader_width = 30
    # draw invader
    pygame.draw.rect(backbuffer, (150, a, b), rect)
    # left eye
    pygame.gfxdraw.filled_circle(backbuffer, rect.x + 6, rect.y + 4, 3, \
                                 BLACK)
    #right eye
    pygame.gfxdraw.filled_circle(backbuffer, rect.x + invader_width - 7,\
                                 rect.y + 4, 3, BLACK)
    # left antennae
    pygame.gfxdraw.line(backbuffer, rect.x + 14, rect.y, rect.x + 8,\
                       rect.y - 6, (150, a, b))
    # right antennae
    pygame.gfxdraw.line(backbuffer, rect.x + invader_width - 15, rect.y,\
                        rect.x + invader_width - 8, rect.y - 6, (150, a, b))

    # draw 'animation' if required
    if animate_invaders:
        pygame.gfxdraw.filled_trigon(backbuffer, rect.x+6, rect.y + 12,\
                                     rect.x + 14, rect.y + 4, rect.x +\
                                     invader_width - 7, rect.y + 12, BLACK)
    else:
        # left side mouth
        pygame.gfxdraw.line(backbuffer, rect.x + 6, rect.y + 12,\
                            rect.x + 15, rect.y + 8, BLACK)
        # right side mouth
        pygame.gfxdraw.line(backbuffer, rect.x + invader_width - 7,\
                            rect.y + 12, rect.x + invader_width - 15,\
                            rect.y + 8, BLACK)
    # ensure trigon is drawn for more than just a frame
    if ticks > animation_time + 200:
        animate_invaders = False

    return animate_invaders

##def load_sound(file):
##    return pygame.mixer.Sound(file)

pygame.init()
pygame.mixer.init() # not always called by pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
fpsclock = pygame.time.Clock()

#get screen metrics
the_screen = screen.get_rect()
screen_width = the_screen.width
screen_height = the_screen.height

backbuffer = pygame.Surface((the_screen.width, the_screen.height))

# fonts
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont("Impact", 54)
font3 = pygame.font.SysFont("Impact", 36)

### load sounds
##space_voiceover = load_sound("SpaceInvadersIntro.wav")
##missile_sound = load_sound("missile.wav")

### play voiceover on startup
##space_voiceover.play()

# User event frequencies
RELOAD_SPEED = 400
MOVE_SIDEWAYS = 1000
MOVE_DOWN = 1000
BONUS_FREQ = 10000
INV_SHOOT_FREQ = 500

# create user events
move_invaders_sideways = pygame.USEREVENT + 1
move_invaders_down = pygame.USEREVENT + 2
reload = pygame.USEREVENT + 3
invader_shoot = pygame.USEREVENT + 4
bonus = pygame.USEREVENT + 5

# event timers
pygame.time.set_timer(move_invaders_down, 0) 
pygame.time.set_timer(move_invaders_sideways, MOVE_SIDEWAYS) 
pygame.time.set_timer(reload, RELOAD_SPEED)
pygame.time.set_timer(invader_shoot, INV_SHOOT_FREQ) 
pygame.time.set_timer(bonus, BONUS_FREQ)

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
DIMGRAY = (105,105,105)

shots, invader_shots, inv_shot_colors, bonus_invaders = [], [], [], []

# create player ship        
player = Rect(380,578,42,20)
player_gun = Rect(player.x + 18,player.y - 4, 6, 4)

# make screen rect for purposes of text-centering etc
the_screen = screen.get_rect()

# invader animation variables
animation_time = 0
animate_invaders = False
invader_width = 30
invader_height = 15

# flashing text vars
the_text = cycle(["Press Enter To Play, Earthling...", ""])
insert = next(the_text)
flash_timer = 0

# flashing bonus item vars
y1,y2,y3,y4,y5,y6 = (255,255,0), (225,225,0), (195,195,0), (165,165,0),\
                    (135,135,0), (105,105,0)
bonus_colors = cycle([y1,y2,y3,y4,y5,y6])
bonus_color = next(bonus_colors)
bonus_x = cycle([4,11,18,25,32,39]) # change draw x coord
bonus_timer = 0 # used to control frequency of changes

# vars for moving invaders down
move_right, move_down, reloaded = True, True, True
vert_steps = 0
side_steps = 0
moved_down = False
invaders_paused = False

invaders = 0 # prevents error until list is created
initial_invaders = 0 # use to manage freq of inv shots as invaders removed
shoot_level = 1 # manage freq of shots

# various gameplay variables
game_over = True
score = 0
lives = 2
level = 0
playing = False

# event loop
while True:
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYUP:
            if event.key == pygame.K_1 and not game_over:
                print("Next level")

        if event.type == invader_shoot and not game_over:
            i = random.randint(0, len(invaders)-1)
            shot_from = invaders[i]
            a, b = colors[i]
            invader_fired = True
            invader_shots.append(Rect(shot_from.x, shot_from.y, 5, 7))
            inv_shot_colors.append((150, a, b))

        if event.type == reload and not game_over:
            reloaded = True
            pygame.time.set_timer(reload, 0)

        if event.type == move_invaders_sideways and not game_over:
            if move_right:
                for invader in invaders: invader.move_ip(10,0)
                side_steps += 1
            else:
                for invader in invaders: invader.move_ip(-10,0)
                side_steps -= 1
            if side_steps == 6 or side_steps == -6:
                if vert_steps <= 31: # and not moved_down
                    pygame.time.set_timer(move_invaders_sideways, 0)
                    pygame.time.set_timer(move_invaders_down, MOVE_DOWN)
                # keep invaders moving horizontally after 31 down movements    
                else: move_right = not move_right

        if event.type == move_invaders_down and not game_over:
            #for i in range(20): print("down event")
            move_right = not move_right
            animate_invaders = True
            animation_time = ticks
            # reset move_sideways timer
            pygame.time.set_timer(move_invaders_sideways, MOVE_SIDEWAYS)
            # cancel move_down timer
            pygame.time.set_timer(move_invaders_down, 0)
            for invader in invaders: invader.move_ip(0,10)
            vert_steps += 1

        if event.type == bonus and not game_over:
            #a = Rect(769,20,45,15)
            bonus_invaders.append(Rect(797,20,45,15))

    # keyboard polling
    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE]: pygame.quit(), sys.exit()
    elif pressed[K_RETURN]:
        if game_over: game_over = False
    elif pressed[K_d] or pressed[K_RIGHT]:player.move_ip((8, 0))
    #player_gun.move_ip((8,0))
    elif pressed[K_a] or pressed[K_LEFT]: player.move_ip((-8, 0))
    if pressed[K_SPACE]:
        if reloaded:
            reloaded = False
            # create timeout of RELOAD_SPEED
            pygame.time.set_timer(reload, RELOAD_SPEED)
            # shrink copy of player rect to imitate a missile
            missile = player.copy().inflate(-38, -10)
            # spawn missile higher to ensure appears missile fired from 'gun'
            # when the ship is moving horizontally
            missile.y -= 9
            shots.append(missile)
            #missile_sound.play()

    backbuffer.fill(BLACK)

    if not game_over:
        playing = True
        if level == 0:
            level = next_level(level)
            invaders, colors, initial_invaders = load_level(level)
            move_right, move_down, reloaded = True, True, True
            vert_steps = 0
            side_steps = 0
            moved_down = False
            invaders_paused = False
            pygame.time.set_timer(invader_shoot, 500)
            shoot_level = 1

        for shot in invader_shots:
            shot.move_ip((0,random.randint(5,11)))
            if not backbuffer.get_rect().contains(shot):
                i = invader_shots.index(shot)
                del invader_shots[i]
                del inv_shot_colors[i]
            if shot.colliderect(player):
                lives -= 1
                if lives < 0:
                    lives = 0
                    game_over = True
                i = invader_shots.index(shot)
                del invader_shots[i]
                del inv_shot_colors[i]

        for shot in shots:
            shot.move_ip((0, -8))
            for inv_shot in invader_shots:
                if inv_shot.colliderect(shot):
                    shots.remove(shot)
                    i = invader_shots.index(inv_shot)
                    del invader_shots[i]
                    del inv_shot_colors[i]
            for b_invader in bonus_invaders:
                if b_invader.colliderect(shot):
                    shots.remove(shot)
                    i = bonus_invaders.index(b_invader)
                    del bonus_invaders[i]
                    score += 1
            if not backbuffer.get_rect().contains(shot):
                shots.remove(shot)
            else:
                hit = False
                for invader in invaders:
                    if invader.colliderect(shot):
                        score += 1
                        hit = True
                        i = invaders.index(invader)
                        del invaders[i]
                        del colors[i]
                if hit: shots.remove(shot)

        # move bonus invader        
        for bonus_invader in bonus_invaders:
            bonus_invader.move_ip((-4,0 ))
##            if not screen.get_rect().contains(bonus_invader):
##                bonus_invaders.remove(bonus_invader)
            if bonus_invader.x < -55:
                bonus_invaders.remove(bonus_invader)

        # check if all invaders killed, if so, move to next level
        if len(invaders) == 0:
            level = next_level(level)
            invaders, colors, initial_invaders = load_level(level)
            move_right, move_down, reloaded = True, True, True
            vert_steps = 0
            side_steps = 0
            moved_down = False
            invaders_paused = False
            pygame.time.set_timer(invader_shoot, 500)
            shoot_level = 1

        # adjust shot freq when invader numbers decrease
        if len(invaders) < initial_invaders*.75 and shoot_level == 1:
            pygame.time.set_timer(invader_shoot, 750)
            shoot_level = 2
        elif len(invaders) < initial_invaders*.5 and shoot_level == 2:
            pygame.time.set_timer(invader_shoot, 1000)
            shoot_level = 3
        elif len(invaders) < initial_invaders*.25 and shoot_level == 3:
            pygame.time.set_timer(invader_shoot, 1500)
            shoot_level = 4

        # draw invaders        
        for rect, (a, b) in zip(invaders, colors):
            animate_invaders = draw_invader(backbuffer, rect, a, b,\
                                            animate_invaders, ticks, \
                                            animation_time)

        # draw bonus invaders
        if ticks > bonus_timer + 169:
                bonus_timer = ticks # change colors every 169ms approx
        for bonus_invader in bonus_invaders:
            pygame.draw.rect(backbuffer, (0,0,0,0), bonus_invader)
            pygame.draw.ellipse(backbuffer,DIMGRAY,bonus_invader)
            for i in range(6):
                bonus_color = next(bonus_colors)
                bx = next(bonus_x)
                draw_bonus_invader(i, bonus_color, bx, bonus_x)

        # draw space ship shots
        for shot in shots:
            pygame.draw.rect(backbuffer, (255,0,0), shot)
        # draw invader shots
        for shot, color in zip(invader_shots, inv_shot_colors):
            pygame.draw.rect(backbuffer, color, shot)

        #update 'gun' position and draw ship/gun
        #player_gun = Rect(player.x, player.y, 6, 4)
        player_gun.x = player.x+18
        pygame.draw.rect(backbuffer, DIMGRAY, player)
        pygame.draw.rect(backbuffer, DIMGRAY, player_gun)

        player.clamp_ip(backbuffer.get_rect())

        print_text(backbuffer, font1, "Invaders Pnwed: {}".format(score),\
                   the_screen, x=590, y=0)
        print_text(backbuffer, font1, "Lives: {}".format(lives), the_screen,\
                   x=0, y=0)
        print_text(backbuffer, font1, "Level: {}".format(level), the_screen,\
                   x=0, y=580)

    if game_over:
        if playing:
            game_is_over(backbuffer, font2, ticks)
            playing = False
            level = 0
            lives = 2
            score = 0
            shots, invader_shots, inv_shot_colors, bonus_invaders = [], [], [], []

        print_text(backbuffer, font2, "SPACE INVADERS", the_screen, y=5,\
                   center=True)
        draw_title_invader()

        if ticks > flash_timer + 800: # "press to play" flashing text
            insert = next(the_text)
            flash_timer = ticks
        print_text(backbuffer, font3, insert, the_screen, y =\
                   the_screen.height-40, center=True)

    screen.blit(backbuffer, (0,0))
    pygame.display.update()
    fpsclock.tick(30)