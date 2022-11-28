from engi1020.arduino.api import *
import pygame as pg
import sys
import random

count = 0
x = 0
pg.init()
surflength = 1000
surfheight = 400
DISPLAYSURF = pg.display.set_mode((surflength,surfheight))
FPS = pg.time.Clock()

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0,0,0)
padwidth = 16

pad1pos = 140
pad2pos = 140
paddle1 = (0,pad1pos,16,100) #paddle rectangle values
paddle2 = (984,pad2pos,16,100)
ball_pos = [400,200] #ball starting position
paddle1_vel = 0
paddle2_vel = 0
score = [0,0]

def initial_velocity():
    """Starts the ball in a random direction"""
    x = random.randint(0,1)
    if x == 0:
        xvel = 4
    elif x == 1:
        xvel = -4
    y = random.randint(0,1)
    if y == 0:
        yvel = 4
    elif y == 1:
        yvel = -4
    return [xvel, yvel]
def ball_position():
    """Function used to change the balls position"""
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    return ball_pos
ball_vel = initial_velocity() 
GOAL = pg.USEREVENT + 1 #defines a custom user event in pygame for when a goal is scored


DISPLAYSURF.fill(white)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE)\
            or score[0] >= 3 or score[1] >= 3:
            #quits the game if escape key is pressed or a player gets to score 3
            pg.quit()
            sys.exit()
        elif event.type == GOAL:
            #when a goal is scored, the paddle positions get reset and ball gets put back into play
            ball_vel=initial_velocity()
            pad1pos = 140
            pad2pos = 140
            ball_pos = [surflength/2,200]

            ball = pg.draw.circle(DISPLAYSURF, white, ball_position(), 5)
            paddle1 = pg.Rect(0,pad1pos,16,100) #updates paddle positions
            paddle2 = pg.Rect(984,pad2pos,16,100)
            ball = pg.draw.circle(DISPLAYSURF, white, ball_position(), 5)
            pg.draw.rect(DISPLAYSURF, red, paddle1) #drawing paddles
            pg.draw.rect(DISPLAYSURF, blue, paddle2)

            print(score) 
            pg.display.update() #ran into an error where the positions did not update until the wait
            #of 1.5 seconds was over, so display update is put here
            pg.time.wait(1500) #1.5 second wait in between rounds
            #time sleep doesn't work with pygame, so pg.time.wait is used

    paddle1 = pg.Rect(0,pad1pos,16,100) #updates paddle positions
    paddle2 = pg.Rect(984,pad2pos,16,100)

    y1 = analog_read(0) #gets reading from rotary dial
    y2 = joystick_get_y() #gets reading from joystick
    #joystick testing was not necessary as the paddle speed is constant and 
    #0.35 threshold was a result of testing by printing the y2 value every frame
    #this value is subject to change for different arduinos, joysticks and computers

    keys = pg.key.get_pressed()  #checking pressed keys and changing position (obsolete for arduino)
    if y2 > 0.35 and pad2pos > 0:
        pad2pos -= 5
    if y2 < -0.35 and pad2pos < 300:
        pad2pos += 5
    if y1 > 750 and pad1pos > 0:
        pad1pos -= 5
    if y1 < 250 and pad1pos < 300:
        pad1pos += 5
    if ball_pos[1] < 0:
        ball_vel[1] *= -1
    if ball_pos[1] > surfheight:
        ball_vel[1] *= -1


    if ball_pos[0] > surflength: #checks if ball went out of screen on the right
        score[0] += 1
        pg.event.post(pg.event.Event(GOAL))
        paddle1 = pg.Rect(3000,3000,16,100) #updates paddle positions to be off the map
        paddle2 = pg.Rect(2500,3000,16,100) #for a clean round restart, otherwise 
                                            #rectangles stay on screen until the round restarts
        pg.draw.rect(DISPLAYSURF, red, paddle1)
        pg.draw.rect(DISPLAYSURF, blue, paddle2)
    if ball_pos[0] < 0: #checks if ball went out left
        score[1] +=1
        pg.event.post(pg.event.Event(GOAL))
        paddle1 = pg.Rect(3000,4000,16,100) 
        paddle2 = pg.Rect(2500,3000,16,100)
        pg.draw.rect(DISPLAYSURF, red, paddle1)
        pg.draw.rect(DISPLAYSURF, blue, paddle2)


    DISPLAYSURF.fill(black)
    pg.draw.rect(DISPLAYSURF, red, paddle1) #drawing rectangles
    pg.draw.rect(DISPLAYSURF, blue, paddle2)
    ball = pg.draw.circle(DISPLAYSURF, white, ball_position(), 5) #draws ball


    #checks if the ball is colliding 
    #with one of the paddles and reverses direction

    #ran into a problem where if the ball hits the paddle from the top, 
    #it would change directions many times and get stuck in the paddle
    #to fix, a counter is added so a collision will only happen 1 every 100 ms
    if pg.Rect.colliderect(paddle1,ball) and count < 0: 
        ball_vel[0] *= -1
        if ball_vel[0] < 8: #did some play testing to get a max speed of 7 or 8, anything higher and the 
                            # collision detection stops working and the ball flies through the paddles
            ball_vel[0] += random.uniform(.5, 1) #takes a random float as a
                                                 #constant change of speed every hit was boring
        if ball_vel[1] > 0 and ball_vel[1] < 8:
            ball_vel[1] += random.uniform(.5, 1)
        if ball_vel[1] < 0 and ball_vel[1] > -8:
            ball_vel[1] -= random.uniform(.5, 1)
        count = 100
        print(ball_vel)
    #ran into syntax and logical errors with some positive and negative values as the coordinate
    #system is different compared to traditional x,y (traditional -y is +y in pygame, ie. down is positive)
    if pg.Rect.colliderect(paddle2,ball) and count < 0:
        ball_vel[0] *= -1       
        if ball_vel[0] > -8:
            ball_vel[0] -= random.uniform(.5, 1)
        if ball_vel[1] > 0 and ball_vel[1] < 8:
            ball_vel[1] += random.uniform(.5, 1)
        if ball_vel[1] < 0 and ball_vel[1] > -8:
            ball_vel[1] -= random.uniform(.5, 1)
        count = 100
        print(ball_vel)

    count-=1

    pg.display.update()
    FPS.tick(20)