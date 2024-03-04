#BẢN THỨ 2 (ACTIVE)
from email.mime import image
import pipes
import random
import sys
from cmath import pi
from distutils.spawn import spawn
from hashlib import new
from lib2to3.pytree import convert
from pickle import TRUE
from tkinter import CENTER
from venv import create

import pygame
from this import d

#tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
    screen.blit(floor,(floor_x_pos+864,650))
    screen.blit(floor,(floor_x_pos+1200,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (1280,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (1280,random_pipe_pos-730))
    return bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            hit_sound.play()
            return False
    return True
def rotate_bird(bird01):
    new_bird = pygame.transform.rotozoom(bird01,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (610, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_suface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_suface.get_rect(center = (630,100))
        screen.blit(score_suface,score_rect)
    if game_state == 'game_over':
        score_suface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_suface.get_rect(center = (630,100))
        screen.blit(score_suface,score_rect)

        high_score_suface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = score_suface.get_rect(center = (600,630))
        screen.blit(high_score_suface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def create_fakepipe(): ############################
    #fakepipe_surface = game_font.render(image,True,(0,0,0,0))
    fakepipe = fakepipe_surface.get_rect(midtop = (1360,40))
    #top_fakepipe = fakepipe_surface.get_rect(midtop = (1360,-340))
    return fakepipe
def move_fakepipe(fake_pipes):###########################
    for piped in fake_pipes:
        piped.centerx -= 3
    return fake_pipes
def draw_fakepipe(fake_pipes):######################
    for piped in fake_pipes:
        screen.blit(fakepipe_surface,piped)
def check_score_point(fake_pipes):#####################
    for piped in fake_pipes:
        if bird_rect.colliderect(piped):
            return True

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

#tạo các biến cho trò chơi
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
high_score = 0

#chèn background
bg = pygame.image.load('assets/city1-night.jpg').convert()
bg = pygame.transform.scale2x(bg)

#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png')).convert_alpha()
bird_list = [bird_down,bird_mid,bird_up] # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (610,384))

#tạo thời gian chim đập cánh
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
fakepipe_surface = pygame.image.load('assets/pipe-black.png').convert_alpha()############
fakepipe_surface = pygame.transform.scale2x(fakepipe_surface)#############
#fakepipe_surface = pygame.mask.from_surface(fakepipe_surface)
pipe_list_1 = [] #########
pipe_list_2 = [] #########

#tạo thời gian ống xuất hiện
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1800)
pipe_height = [250,350,450]

#tạo màn hình hết thúc
game_over_suface = pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect = game_over_suface.get_rect(center = (632,384))

#chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_nope.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_coldown = 47

#while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -7 
                flap_sound.play()   
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list_1.clear()
                pipe_list_2.clear()
                bird_rect.center = (600,384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list_1.extend(create_pipe())
            pipe_list_2.append(create_fakepipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg,(-550,-200))
    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list_1)
        if check_score_point(pipe_list_2) == True:###################
            score +=0.02040816327
            score_sound_coldown -= 1
            if score_sound_coldown == 0:
                score_sound.play()
                score_sound_coldown = 47
        #ống
        pipe_list_1 = move_pipe(pipe_list_1)#########
        pipe_list_2 = move_fakepipe(pipe_list_2)########
        #cộng điểm
        draw_pipe(pipe_list_1)#########
        #draw_fakepipe(pipe_list_2)#########
        
        # score += 0.01

        score_display('main game')
        #score_sound_coldown -= 1
        #if score_sound_coldown <= 0:
            #score_sound.play()
            #score_sound_coldown = 100
    else:
        screen.blit(game_over_suface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #sàn
    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()  
    clock.tick(120)
