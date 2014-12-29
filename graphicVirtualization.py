#graphic module to show the location
import sys
import pygame
import main

def draw():
    pygame.init()
    screen=pygame.display.set_mode((500,500),0,32)
    pygame.display.set_caption('Position Tracking')
    background=pygame.image.load("/Users/BboyKellen/Documents/LiClipse Workspace/MENG/PH2.jpg").convert()
    #mouse_c=pygame.image.load("/Users/BboyKellen/Documents/LiClipse Workspace/MENG/PH2.jpg").convert_alpha()
    position=[300,176]  
    color=[255,0,0]  
    color_cross=[0,0,255]
    radius=(6)
    minus=True
    clock=pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(background,(0,0))   
        x,y=pygame.mouse.get_pos()        
        if minus==True:
            radius -=1
            if radius==0:
                minus=False
        else:
            radius+=1
            if radius==6:
                minus=True  
        position[0]= main.xGraphic  
        position[1]= main.yGraphic       
        screen.lock()
        'draw positions'  
        pygame.draw.circle(screen,color, position,radius)
        pygame.draw.line(screen,color_cross,(x-10,y),(x+10,y),1)
        pygame.draw.line(screen,color_cross,(x,y+10),(x,y-10),1)         
        'release the canvas'
        screen.unlock()
        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)
        
