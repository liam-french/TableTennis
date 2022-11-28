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
paddle1 = (0,pad1pos,16,100)
paddle2 = (984,pad2pos,16,100)
ball_pos = [surflength/2,200]
paddle1_vel = 0
paddle2_vel = 0
score = [0,0]


def initial_velocity():
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
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    return ball_pos
ball_vel = initial_velocity()
GOAL = pg.USEREVENT + 1
# def paddle_position():
#     paddle1_

DISPLAYSURF.fill(white)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.type == GOAL:
            ball_vel=initial_velocity()
            pad1pos = 140
            pad2pos = 140
            ball_pos = [surflength/2,200]
            ball = pg.draw.circle(DISPLAYSURF, white, ball_position(), 5)
            paddle1 = pg.Rect(0,pad1pos,16,100) #updates paddle positions
            paddle2 = pg.Rect(984,pad2pos,16,100)
            pg.draw.rect(DISPLAYSURF, red, paddle1) #drawing rectangles
            pg.draw.rect(DISPLAYSURF, blue, paddle2)
            print(score)
            pg.display.update()
            pg.time.wait(1500)
    paddle1 = pg.Rect(0,pad1pos,16,100) #updates paddle positions
    paddle2 = pg.Rect(984,pad2pos,16,100)
    # ball = pg.
    keys = pg.key.get_pressed()  #checking pressed keys and changing position
    if keys[pg.K_o] and pad2pos > 0:
        pad2pos -= 5
    if keys[pg.K_l] and pad2pos < 300:
        pad2pos += 5
    if keys[pg.K_w] and pad1pos > 0:
        pad1pos -= 5
    if keys[pg.K_s] and pad1pos < 300:
        pad1pos += 5
    if ball_pos[1] < 0:
        ball_vel[1] *= -1
    if ball_pos[1] > surfheight:
        ball_vel[1] *= -1

    
    if ball_pos[0] > surflength:
        score[0] += 1
        pg.event.post(pg.event.Event(GOAL))
        paddle1 = pg.Rect(3000,3000,16,100) #updates paddle positions to be off the map for clean
        paddle2 = pg.Rect(2500,3000,16,100) #round restart
        pg.draw.rect(DISPLAYSURF, red, paddle1)
        pg.draw.rect(DISPLAYSURF, blue, paddle2)
    if ball_pos[0] < 0:
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
    if pg.Rect.colliderect(paddle1,ball) and count < 0: 
        ball_vel[0] *= -1
        if ball_vel[0] < 8:
            ball_vel[0] += random.uniform(.5, 1)
        if ball_vel[1] > 0 and ball_vel[1] < 8:
            ball_vel[1] += random.uniform(.5, 1)
        if ball_vel[1] < 0 and ball_vel[1] > -8:
            ball_vel[1] -= random.uniform(.5, 1)
        count = 100
        print(ball_vel)
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
    FPS.tick(60)