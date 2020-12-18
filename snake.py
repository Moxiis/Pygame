import pygame
import time
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.3
        self.change_y = 0
        self.change_x = 0

class tail:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class food:
    def __init__(self, x, y):
        self.x = x
        self.y = y    
    
def main():
    run = True
    clock = pygame.time.Clock()
    food = []
    clock.tick(FPS)
    player = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def draw():
        screen.fill((0,0,0))
        pygame.draw.rect(screen,(255,255,255), (player.x, player.y, 20, 20))
        pygame.draw.rect(screen, (155,155,155), (food.x, food.y, 20, 20))
        for tail in player.tail:
            pygame.draw.rect(screen,(255,255,255),(tail.x, tail.y, 20, 20))
        pygame.display.update()
    
    def spawn_food():
        if food == []:
            food.append(food(random.randrage(20, SCREEN_WIDTH - 20),random.randrage(20, SCREEN_HEIGHT + 20)))
        
    
    while run:
        draw()
        spawn_food()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 

        event = pygame.key.get_pressed()
        if event[pygame.K_UP]:
            player.change_y = - player.speed
            player.change_x = 0
        elif event[pygame.K_DOWN]:
            player.change_y = player.speed
            player.change_x = 0
        elif event[pygame.K_RIGHT]:
            player.change_x = player.speed
            player.change_y = 0
        elif event[pygame.K_LEFT]:
            player.change_x = - player.speed
            player.change_y = 0
            
        player.y += player.change_y    
        player.x += player.change_x

        if player.y + 20 >= SCREEN_HEIGHT:
            player.y = SCREEN_HEIGHT - 20
        if player.y <= 0:
            player.y = 0
        if player.x + 20 >= SCREEN_WIDTH:
            player.x = SCREEN_WIDTH - 20
        if player.x <= 0:
            player.x = 0


            
        
main()    
