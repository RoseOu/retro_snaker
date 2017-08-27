#coding:utf-8
import sys
import pygame
import random
from pygame.locals import *

ROWNUM = 20
COLNUM = 20
LEN = 20
CELLNUM = ROWNUM * COLNUM
SCREEN_SIZE = (COLNUM*LEN+5*LEN,ROWNUM*LEN)
BG_COLOR = (0,0,0)
FONT_COLOR = (255,255,255)
HEAD_COLOR = (188,50,88)
SNAKE_COLOR = (100,50,80)
FOOD_COLOR = (55,100,155)
OVER_COLOR = (55,88,211)

class Food():
    def __init__(self):
        self.pos=[random.randint(0, COLNUM-1)*LEN,random.randint(0, ROWNUM-1)*LEN]

    def draw_food(self):
        pygame.draw.rect(screen,FOOD_COLOR,(self.pos[0],self.pos[1],LEN,LEN))

    def be_eatten(self):
        self.pos=[random.randint(0, COLNUM-1)*LEN,random.randint(0, ROWNUM-1)*LEN]

class Snake():
    def __init__(self):
        self.length=4
        self.head=[random.randint(4,COLNUM-4)*LEN,random.randint(4,ROWNUM-4)*LEN]
        self.body=[
                    [self.head[0]-1*LEN,self.head[1]],
                    [self.head[0]-2*LEN,self.head[1]],
                    [self.head[0]-3*LEN,self.head[1]],
                  ]

    def draw_snake(self):
        pygame.draw.rect(screen,HEAD_COLOR,(self.head[0],self.head[1],LEN,LEN))
        for grid in self.body:
            pygame.draw.rect(screen,SNAKE_COLOR,(grid[0],grid[1],LEN,LEN))

    def insert_head_and_del_last(self,new_head):
        del self.body[-1]
        self.body.insert(0,self.head)
        self.head = new_head

    def insert_head(self,new_head):
        self.body.insert(0,self.head)
        self.head = new_head

    def turn(self,event):
        # turn left or turn right
        if self.head[0] == self.body[0][0]:
            if event.key == K_LEFT:
                new_head = [self.head[0]-LEN,self.head[1]]
                self.insert_head_and_del_last(new_head)
            if event.key == K_RIGHT:
                new_head = [self.head[0]+LEN,self.head[1]]
                self.insert_head_and_del_last(new_head)

        #turn up or turn down
        if self.head[1] == self.body[0][1]:
            if event.key == K_UP:
                new_head = [self.head[0],self.head[1]-LEN]
                self.insert_head_and_del_last(new_head)
            if event.key == K_DOWN:
                new_head = [self.head[0],self.head[1]+LEN]
                self.insert_head_and_del_last(new_head)

    def move(self):
        # move towards the left
        if self.head[0] < self.body[0][0]:
            new_head = [self.head[0]-LEN,self.head[1]]
            self.insert_head_and_del_last(new_head)

        # move towards the right
        elif self.head[0] > self.body[0][0]:
            new_head = [self.head[0]+LEN,self.head[1]]
            self.insert_head_and_del_last(new_head)

        # move upward
        elif self.head[1] < self.body[0][1]:
            new_head = [self.head[0],self.head[1]-LEN]
            self.insert_head_and_del_last(new_head)

        # move downward
        elif self.head[1] > self.body[0][1]:
            new_head = [self.head[0],self.head[1]+LEN]
            self.insert_head_and_del_last(new_head)

    def eat_food(self):
        # move towards the left
        if self.head[0] < self.body[0][0]:
            new_head = [self.head[0]-LEN,self.head[1]]
            self.insert_head(new_head)
            self.length=self.length+1

        # move towards the right
        elif self.head[0] > self.body[0][0]:
            new_head = [self.head[0]+LEN,self.head[1]]
            self.insert_head(new_head)
            self.length=self.length+1

        # move upward
        elif self.head[1] < self.body[0][1]:
            new_head = [self.head[0],self.head[1]-LEN]
            self.insert_head(new_head)
            self.length=self.length+1

        # move downward
        elif self.head[1] > self.body[0][1]:
            new_head = [self.head[0],self.head[1]+LEN]
            self.insert_head_and_del_last(new_head)
            self.length=self.length+1


def draw_screen():
    screen.fill(BG_COLOR, (0, 0, COLNUM*LEN+5*LEN, ROWNUM*LEN))
    y=0
    while y < ROWNUM:
        x=0
        while x < COLNUM:
            pygame.draw.line(screen, FONT_COLOR, (0,(y+1)*LEN), (COLNUM*LEN,(y+1)*LEN))
            pygame.draw.line(screen, FONT_COLOR, ((x+1)*LEN,0), ((x+1)*LEN,ROWNUM*LEN))
            x=x+1
            y=y+1

def draw_scores(font,scores):
    text = font.render("Scores: " + str(scores),True,FONT_COLOR)
    screen.blit(text,((COLNUM*LEN),0))

def draw_all(food,snake,font,scores):
    draw_screen()
    snake.draw_snake()
    food.draw_food()
    draw_scores(font,scores)

def game_over(font):
    text2=font.render('Game over!', True, OVER_COLOR)
    textobj=text2.get_rect()
    textobj.center = (COLNUM*LEN/2, ROWNUM*LEN/2)
    screen.blit(text2,textobj)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
    pygame.event.set_blocked(None)
    pygame.event.set_allowed((KEYDOWN,QUIT))
    pygame.display.set_caption('Retro Snaker')
    font = pygame.font.SysFont("arial",28)
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    text = font.render("Scores: " + str(snake.length-4),True,FONT_COLOR)
    text2=font.render('Game over!', True, OVER_COLOR)
    textobj=text2.get_rect()
    textobj.center = (COLNUM*LEN/2, ROWNUM*LEN/2)
    screen.blit(text,((COLNUM*LEN),0))
    draw_all(food,snake,font,snake.length-4)
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                snake.turn(event)
                if snake.head[0] == food.pos[0] and snake.head[1] == food.pos[1]:
                    food.be_eatten()
                    snake.eat_food()
        snake.move()

        if snake.head[0] == food.pos[0] and snake.head[1] == food.pos[1]:
            food.be_eatten()
            snake.eat_food()

        if snake.head[0] < 0 or snake.head[0] >= COLNUM*LEN or snake.head[1] < 0 or snake.head[1] >= ROWNUM*LEN:
            screen.blit(text2,textobj)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.quit()
                        sys.exit()
        for b in snake.body:
            if b == snake.head:
                screen.blit(text2,textobj)
                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type==QUIT:
                            pygame.quit()
                            sys.exit()
        draw_all(food,snake,font,snake.length-4)
        pygame.display.flip()
        clock.tick(5)

if __name__ == '__main__':
    main()


