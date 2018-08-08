'''
Created on Aug 6, 2018

@author: justo
'''
import pygame
import Player
Clock = pygame.time.Clock()
Points = 0

class Button():
    def __init__(self,screen,y,value,increment,index,maximum):
        self.screen = screen
        self.x = 500
        self.y = y
        self.value = value
        self.increment = increment
        self.index = index
        self.min = value
        self.max = maximum
    def update(self):
        global Points
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.value > self.min:
            if 500 < mouse[0] < 550 and self.y < mouse[1] < self.y+50:
                pygame.draw.polygon(self.screen, (0,255,255), ((495,self.y+25),(553,self.y-5),(553,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, (255,0,0), ((500,self.y+25),(550,self.y),(550,self.y+50)), 0) 
                if click[0] == 1:
                    self.value -= self.increment
                    Points += 1
            else:
                pygame.draw.polygon(self.screen, (255,0,0), ((495,self.y+25),(553,self.y-5),(553,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, (0,255,255), ((500,self.y+25),(550,self.y),(550,self.y+50)), 0) 
        fontsize = 30-len(format(self.value,','))
        valuefont = pygame.font.SysFont('Arial Black', fontsize,True)
        text = valuefont.render(format(self.value,','), False, (0,255,255))
        self.screen.blit(text,(600-((30-fontsize)*6),self.y+(30-fontsize)))
        if self.value < self.max and Points > 0:
            if 675 < mouse[0] < 725 and self.y < mouse[1] < self.y+50:
                pygame.draw.polygon(self.screen, (0,255,255), ((725,self.y+25),(675,self.y-5),(675,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, (255,0,0), ((720,self.y+25),(678,self.y),(678,self.y+50)), 0) 
                if click[0] == 1:
                    self.value += self.increment
                    Points -= 1
            else:
                pygame.draw.polygon(self.screen, (255,0,0), ((725,self.y+25),(675,self.y-5),(675,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, (0,255,255), ((720,self.y+25),(678,self.y),(678,self.y+50)), 0)

def kill(): #Kills the program
    pygame.quit()
    quit()
    
def Main(Screen,PlayerData,MechImg):
    optionfont = pygame.font.SysFont('Arial Black', 30,True) #Set a font to arial black size 30 and bold
    Data = Player.LoadPlayer(PlayerData)
    global Points
    Points = Data['Points']
    Buttons = []
    Buttons.append(Button(Screen,75,Data['Health'],50,'Health',Data['Level']**2))
    inMenu = True
    while inMenu:
        Screen.fill((0,0,0))
        health = optionfont.render("Health", False, (0,255,255))
        damage = optionfont.render("Damage", False, (0,255,255))
        fire = optionfont.render("Fire Rate", False, (0,255,255))
        move = optionfont.render("Move Speed", False, (0,255,255))
        blast = optionfont.render("Blast Speed", False, (0,255,255))
        color = optionfont.render("Color", False, (0,255,255))
        p = optionfont.render("Points:{}".format(format(Points,',')),False,(0,255,255))
        Screen.blit(health,(200,75))
        Screen.blit(damage,(200,150))
        Screen.blit(fire,(200,225))
        Screen.blit(move,(200,300))
        Screen.blit(blast,(200,375))
        Screen.blit(color,(200,450))
        Screen.blit(p,(50,0))
        pygame.draw.rect(Screen, Data['Color'], [0,425,100,70]) #Draws the player's mech
        pygame.draw.polygon(Screen, Data['Color'], ((0,490),(50,490),(30,510),(0,510)))
        Screen.blit(MechImg,(0,400))
        for button in Buttons:
            button.update()
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN: #If a button gets pressed
                if event.key == pygame.K_ESCAPE: #If that button is the escape key
                    Screen.fill((0,0,0))
                    inMenu = False
        Clock.tick(10)