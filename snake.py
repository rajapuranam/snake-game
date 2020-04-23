import pygame
import sys
import random
import time
import tkinter as tk
from tkinter import messagebox

# Snake Object
class Snake():

    # constructor
    def __init__(self):
        self.position = [100,50]
        self.body = [[100,50], [90,50]]
        self.direction = 'RIGHT'
        self.changeDirection = self.direction

    # change direction method
    def changeDir(self, dir):
        if dir is 'RIGHT' and self.direction is not 'LEFT':
            self.direction = "RIGHT"
        if dir is 'LEFT' and self.direction is not 'RIGHT':
            self.direction = "LEFT"
        if dir is 'UP' and self.direction is not 'DOWN':
            self.direction = "UP"
        if dir is 'DOWN' and self.direction is not 'UP':
            self.direction = "DOWN"

    # to move snake on screen
    def moveSnake(self, food):
        if self.direction is 'RIGHT':
            self.position[0] += 10
        elif self.direction is 'LEFT':
            self.position[0] -= 10
        elif self.direction is 'UP':
            self.position[1] -= 10
        elif self.direction is 'DOWN':
            self.position[1] += 10
        
        self.body.insert(0,self.position[:])
        if self.position == food:
            return 1
        else:
            self.body.pop()
            return 0

    # check for any collisions 
    def isCollision(self):
        if self.position[0] > 490 or self.position[0] < 0 or self.position[1] > 490 or self.position[1] < 0:
            return 1 
        
        for i in self.body[1:]:
            if self.position == i:
                return 1
        return 0

    # returns a list of snake body
    def getBody(self):
        return self.body

class Food():
    def __init__(self):
        self.food_pos = [random.randrange(1,50)*10, random.randrange(1,50)*10]
        self.isFood = True

    # placing food on screen at random positions
    def keepFood(self):
        if not self.isFood:
            self.food_pos = [random.randrange(1,50)*10, random.randrange(1,50)*10]
            self.isFood = True
        return self.food_pos

    def setFood(self,b):
        self.isFood = b

window = pygame.display.set_mode((500,500))
pygame.display.set_caption('Snake Game')
score, speed = 0, 10

snake = Snake()
food = Food()

# displaying message box when game is over
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# when collision occurs - game over
def gameOver(score):
    msg = 'Your score is :' + str(score)
    message_box('Game Over!', msg)
    pygame.quit()
    sys.exit()

# making grid on screen
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (100,100,100), (x,0),(x,w))
        pygame.draw.line(surface, (100,100,100), (0,y),(w,y))

clock = pygame.time.Clock()

while True:
    pygame.time.delay(40)
    clock.tick(speed)

    # getting user click events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver(score)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.changeDir('RIGHT')
            elif event.key == pygame.K_LEFT:
                snake.changeDir('LEFT')
            elif event.key == pygame.K_UP:
                snake.changeDir('UP')
            else:
                snake.changeDir('DOWN')

    # placing food
    foodP = food.keepFood()
    if snake.moveSnake(foodP) == 1:
        score += 1
        if speed != 50:
            speed += 3
        food.setFood(False)

    window.fill(pygame.Color(255,255,255))
    drawGrid(500,50, window)

    # drawing snake
    for pos in snake.getBody():
        pygame.draw.rect(window,pygame.Color(0,255,0), pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(window,pygame.Color(255,0,0), pygame.Rect(foodP[0], foodP[1], 10, 10))

    if(snake.isCollision() == 1):
        gameOver(score)

    pygame.display.set_caption("Snake Game | Score : " + str(score))

    pygame.display.flip()