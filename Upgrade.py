'''
Created on Aug 6, 2018

@author: justo
'''
from time import sleep
import pygame
import Player
Clock = pygame.time.Clock()
Points = 0
Black = (0,0,0) #A bunch of colors
White = (255,255,255)
Red = (255,0,0)
DarkRed = (150,0,0)
Green = (0,255,0)
DarkGreen = (0,150,0)
LightGreen = (170,255,0)
GreenBlue = (0,170,85)
BlueGreen = (0,85,170)
Blue = (0,0,255)
DarkBlue = (0,0,150)
BluePurple = (85,170,255)
LightBlue = (0,170,255)
Cyan = (0,255,255)
BabyBlue = (170,255,255)
Indigo = (85,0,255)
Purple = (170,0,255)
HotPink = (255,85,255)
Pink = (255,0,255)
DarkOrange = (255,85,0)
Orange = (255,170,0)
Yellow = (255,255,0)
Colors = [Black,White,Red,DarkRed,Green,DarkGreen,LightGreen,GreenBlue,BlueGreen,Blue,DarkBlue,BluePurple,LightBlue,Cyan,BabyBlue,Indigo,Purple,Pink,HotPink,DarkOrange,Orange,Yellow] #A list of all those colors

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
                pygame.draw.polygon(self.screen, Cyan, ((495,self.y+25),(553,self.y-5),(553,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, Red, ((500,self.y+25),(550,self.y),(550,self.y+50)), 0) 
                if click[0] == 1:
                    self.value -= self.increment
                    Points += 1
            else:
                pygame.draw.polygon(self.screen, Red, ((495,self.y+25),(553,self.y-5),(553,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, Cyan, ((500,self.y+25),(550,self.y),(550,self.y+50)), 0) 
        fontsize = 30-len(format(self.value,','))
        valuefont = pygame.font.SysFont('Arial Black', fontsize,True)
        text = valuefont.render(format(self.value,','), False, (0,255,255))
        self.screen.blit(text,(600-((30-fontsize)*6),self.y+(30-fontsize)))
        if self.value < self.max and Points > 0:
            if 675 < mouse[0] < 725 and self.y < mouse[1] < self.y+50:
                pygame.draw.polygon(self.screen, Cyan, ((725,self.y+25),(675,self.y-5),(675,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, Red, ((720,self.y+25),(678,self.y),(678,self.y+50)), 0) 
                if click[0] == 1:
                    self.value += self.increment
                    Points -= 1
            else:
                pygame.draw.polygon(self.screen, Red, ((725,self.y+25),(675,self.y-5),(675,self.y+55)), 0) 
                pygame.draw.polygon(self.screen, Cyan, ((720,self.y+25),(678,self.y),(678,self.y+50)), 0)
                
class ColorButton():
    def __init__(self,screen,y,value,MechImg):
        global Colors
        self.colorindex = Colors.index(value)
        self.index = 'Color'
        self.screen = screen
        self.x = 500
        self.y = y
        self.value = value
        self.MechImg = MechImg
    def update(self):
        global Colors
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 500 < mouse[0] < 550 and self.y < mouse[1] < self.y+50:
            pygame.draw.polygon(self.screen, Cyan, ((495,self.y+25),(553,self.y-5),(553,self.y+55)), 0) 
            pygame.draw.polygon(self.screen, Red, ((500,self.y+25),(550,self.y),(550,self.y+50)), 0) 
            if click[0] == 1:
                if self.colorindex > 0:
                    self.colorindex -= 1
                    self.value = Colors[self.colorindex]
                else:
                    self.colorindex = len(Colors)-1
                    self.value = Colors[self.colorindex]
        else:
            pygame.draw.polygon(self.screen, Red, ((495,self.y+25),(553,self.y-5),(553,self.y+55)), 0) 
            pygame.draw.polygon(self.screen, Cyan, ((500,self.y+25),(550,self.y),(550,self.y+50)), 0) 
        pygame.draw.rect(self.screen, self.value, [575,self.y-15,75,75])
        pygame.draw.rect(self.screen, self.value, [0,425,100,70]) #Draws the player's mech
        pygame.draw.polygon(self.screen, self.value, ((0,490),(50,490),(30,510),(0,510)))
        self.screen.blit(self.MechImg,(0,400))
        if 675 < mouse[0] < 725 and self.y < mouse[1] < self.y+50:
            pygame.draw.polygon(self.screen, Cyan, ((725,self.y+25),(675,self.y-5),(675,self.y+55)), 0) 
            pygame.draw.polygon(self.screen, Red, ((720,self.y+25),(678,self.y),(678,self.y+50)), 0) 
            if click[0] == 1:
                if self.colorindex < len(Colors)-1:
                    self.colorindex += 1
                    self.value = Colors[self.colorindex]
                else:
                    self.colorindex = 0
                    self.value = Colors[self.colorindex]
        else:
            pygame.draw.polygon(self.screen, Red, ((725,self.y+25),(675,self.y-5),(675,self.y+55)), 0) 
            pygame.draw.polygon(self.screen, Cyan, ((720,self.y+25),(678,self.y),(678,self.y+50)), 0)

def kill(): #Kills the program
    pygame.quit()
    quit()
    
def wait(t): #A function that makes the program sleep while still allowing the user to close the program
    while t > 0:
        sleep(0.01)
        t -= 0.01
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #If the player hits space return false so that the intro will be skipped
                    return False
                    t = 0
    return True
    
def Main(Screen,PlayerName,MechImg):
    optionfont = pygame.font.SysFont('Arial Black', 30,True) #Set a font to arial black size 30 and bold
    Data = Player.LoadPlayer(PlayerName)
    global Points
    Points = Data['Points']
    Buttons = []
    Buttons.append(Button(Screen,75,Data['Health'],10,'Health',Data['Level']**2))
    Buttons.append(Button(Screen,150,Data['Damage'],1,'Damage',Data['Level']/4))
    Buttons.append(Button(Screen,225,Data['FireSpeed'],1,'FireSpeed',Data['Level']/5))
    Buttons.append(Button(Screen,300,Data['MoveSpeed'],1,'MoveSpeed',Data['Level']/10))
    Buttons.append(Button(Screen,375,Data['BlastSpeed'],1,'BlastSpeed',Data['Level']/10))
    Buttons.append(ColorButton(Screen,450,Data['Color'],MechImg))
    inMenu = True
    while inMenu:
        Screen.fill((0,0,0))
        health = optionfont.render("Health", False, (0,255,255))
        damage = optionfont.render("Damage", False, (0,255,255))
        fire = optionfont.render("Fire Rate", False, (0,255,255))
        move = optionfont.render("Move Speed", False, (0,255,255))
        blast = optionfont.render("Blast Speed", False, (0,255,255))
        color = optionfont.render("Color", False, (0,255,255))
        p = optionfont.render("Points:{}".format(format(Points,',')),False,Cyan)
        xp = optionfont.render("XP:{}/{}".format(format(Data['XP'],','),format(Data['Level']**2,',')),False,Cyan)
        l = optionfont.render("Level:{}".format(str(Data['Level'])),False,Cyan)
        Screen.blit(health,(200,75))
        Screen.blit(damage,(200,150))
        Screen.blit(fire,(200,225))
        Screen.blit(move,(200,300))
        Screen.blit(blast,(200,375))
        Screen.blit(color,(200,450))
        Screen.blit(p,(50,0))
        Screen.blit(xp,(350,0))
        Screen.blit(l,(600,0))
        for button in Buttons:
            button.update()
        myfont = pygame.font.SysFont('Arial Black', 25,True)
        save = myfont.render('Save', False, DarkOrange, Black)
        back = myfont.render('Back', False, DarkOrange, Black)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 600 <= mouse[0] <= 600+save.get_width() and 550 <= mouse[1] <= 550+save.get_height():
            save = myfont.render('Save', False, DarkOrange, Orange)
            if click[0] == 1:
                for button in Buttons:
                    Data[button.index] = button.value
                Data['Points'] = Points
                Player.SavePlayer(Data)
                inMenu = False
                wait(0.5)
                Main(Screen,Data['Name'],MechImg)
        if 200 <= mouse[0] <= 200+save.get_width() and 550 <= mouse[1] <= 550+save.get_height():
            back = myfont.render('Back', False, DarkOrange, Orange)
            if click[0] == 1:
                inMenu = False
        Screen.blit(save,(600,550))
        Screen.blit(back,(200,550))
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN: #If a button gets pressed
                if event.key == pygame.K_ESCAPE: #If that button is the escape key
                    Screen.fill(Black)
                    inMenu = False
        Clock.tick(10)