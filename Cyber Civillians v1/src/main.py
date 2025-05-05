#import all libraries
import pygame
from pygame.locals import *
from pygame import mixer

#import all files

#make the game
pygame.init()
pygame.mixer.pre_init(buffer = 1024)
game_width = 1000
game_heigh = 600
screen = pygame.display.set_mode((game_width, game_heigh))
clock = pygame.time.Clock()
running = True
game_started = False

#start the game
def startGame():
    pass

#==================================================================#
#============================LOOP LAND=============================#
#==================================================================#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    #screen.blit(background_image, (0, 0))
    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                startGame()
                break
    
    #game functions
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("Cyber Civillians fps: " + str(clock.get_fps))