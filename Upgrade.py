'''
Created on Aug 6, 2018

@author: justo
'''
import os
from time import sleep
import pygame
import Player
from Controls import GetKey
Directory = os.getcwd()
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
inMenu = True
aspect_ratio = 0
screen_width = 0
screen_height = 0
arrow0 = pygame.image.load(Directory+'\Images\Arrow0.png')
arrow1 = pygame.image.load(Directory+'\Images\Arrow1.png')
Cursor0 = pygame.image.load(Directory+'/Images/Cursor0.png') #Loads the arrow cursor
Cursor1 = pygame.image.load(Directory+'/Images/Cursor1.png') #Loads the pointer cursor
Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25))) #Sets cursor to arrow
Controls = None


class Button():
    def __init__(self,screen,y,value,increment,index,maximum):
        self.screen = screen
        self.x = .6
        self.y = y
        self.value = value
        self.increment = increment
        self.index = index
        self.min = value
        self.max = maximum
    def update(self):
        global Points, Cursor, Cursor1
        mouse = pygame.mouse.get_pos()
        img = pygame.transform.scale(arrow0, (int(screen_height*.1),int(screen_height*.1)))
        if self.value > self.min:
            if screen_width*.6 < mouse[0] < screen_width*.6+img.get_width() and screen_height*self.y < mouse[1] < screen_height*self.y+img.get_height():
                Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                self.screen.blit(img,(screen_width*.6,screen_height*self.y))
                for event in pygame.event.get():
                    if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                        self.value -= self.increment
                        Points += 1
            else:
                img = pygame.transform.scale(arrow1, (int(screen_height*.1),int(screen_height*.1)))
                self.screen.blit(img,(screen_width*.6,screen_height*self.y)) 
        fontsize = 35-(len(format(self.value,','))*3)
        valuefont = pygame.font.SysFont('Arial Black', int(fontsize*(screen_height/600)),True)
        text = valuefont.render(format(self.value,','), False, (0,255,255))
        self.screen.blit(text,((screen_width*.6)+(((screen_width*.725)-(screen_width*.6)+img.get_width())/2)-(text.get_width()/2),(screen_height*self.y)+(img.get_height()/2)-(text.get_height()/2)))
        if self.value < self.max and Points > 0:
            img = pygame.transform.scale(arrow0, (int(screen_height*.1),int(screen_height*.1)))
            img = pygame.transform.flip(img, True, False)
            if screen_width*.725 < mouse[0] < screen_width*.725+img.get_width() and screen_height*self.y < mouse[1] < screen_height*self.y+img.get_height():
                self.screen.blit(img,(screen_width*.725,screen_height*self.y)) 
                Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                for event in pygame.event.get():
                    if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                        self.value += self.increment
                        Points -= 1
            else:
                img = pygame.transform.scale(arrow1, (int(screen_height*.1),int(screen_height*.1)))
                img = pygame.transform.flip(img, True, False)
                self.screen.blit(img,(screen_width*.725,screen_height*self.y)) 
                
class ColorButton():
    def __init__(self,screen,y,value,MechImg,Mech_Img,MechBackImg):
        global Colors
        self.colorindex = Colors.index(value)
        self.index = 'Color'
        self.screen = screen
        self.x = .6
        self.y = y
        self.value = value
        self.MechImg = MechImg
        self.Mech_Img = Mech_Img
        self.MechBackImg = MechBackImg
    def update(self):
        global Colors, Cursor, Cursor1
        mouse = pygame.mouse.get_pos()
        img = pygame.transform.scale(arrow0, (int(screen_height*.1),int(screen_height*.1)))
        if screen_width*.6 < mouse[0] < screen_width*.6+img.get_width() and screen_height*self.y < mouse[1] < screen_height*self.y+img.get_height():
            self.screen.blit(img,(screen_width*.6,screen_height*self.y))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    if self.colorindex > 0:
                        self.colorindex -= 1
                        self.value = Colors[self.colorindex]
                        self.Mech_Img = Colorize(self.MechBackImg, self.value)
                    else:
                        self.colorindex = len(Colors)-1
                        self.value = Colors[self.colorindex]
                        self.Mech_Img = Colorize(self.MechBackImg, self.value)
        else:
            img = pygame.transform.scale(arrow1, (int(screen_height*.1),int(screen_height*.1)))
            self.screen.blit(img,(screen_width*.6,screen_height*self.y)) 
        pygame.draw.rect(self.screen, self.value, [(screen_width*.6)+(((screen_width*.725)-(screen_width*.6)+img.get_width())/2)-(img.get_width()/2),screen_height*self.y,img.get_width(),img.get_height()])
        self.Mech_Img = pygame.transform.scale(self.Mech_Img, (int(screen_height/4), int(screen_height/4)))
        self.MechImg = pygame.transform.scale(self.MechImg, (int(screen_height/4), int(screen_height/4)))
        self.screen.blit(self.Mech_Img,(0,screen_height*.66))
        self.screen.blit(self.MechImg,(0,screen_height*.66))
        img = pygame.transform.scale(arrow0, (int(screen_height*.1),int(screen_height*.1)))
        img = pygame.transform.flip(img, True, False)
        if screen_width*.725 < mouse[0] < screen_width*.725+img.get_width() and screen_height*self.y < mouse[1] < screen_height*self.y+img.get_height():
            self.screen.blit(img,(screen_width*.725,screen_height*self.y))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25))) 
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    if self.colorindex < len(Colors)-1:
                        self.colorindex += 1
                        self.value = Colors[self.colorindex]
                        self.Mech_Img = Colorize(self.MechBackImg, self.value)
                    else:
                        self.colorindex = 0
                        self.value = Colors[self.colorindex]
                        self.Mech_Img = Colorize(self.MechBackImg, self.value)
        else:
            img = pygame.transform.scale(arrow1, (int(screen_height*.1),int(screen_height*.1)))
            img = pygame.transform.flip(img, True, False)
            self.screen.blit(img,(screen_width*.725,screen_height*self.y)) 

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
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
    
def Colorize(image, color):
    m = pygame.mask.from_surface(image, 0)
    shader = pygame.Surface((image.get_size()), masks=m).convert_alpha()
    shader.fill(color)
    copied = image.copy()
    copied.blit(shader, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return copied    
    
def Delete(Screen,PlayerName):
    choosing = True
    global Cursor, Cursor0, Cursor1
    while choosing:
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        Screen.fill(Black)    
        optionfont = pygame.font.SysFont('Arial Black', int(40*(screen_height/600)),True)
        surefont = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True)
        sure1 = surefont.render("Are you sure you want", False, Cyan)
        sure2 = surefont.render("to delete {}".format(PlayerName), False, Cyan)
        sure3 = surefont.render("for good?", False, Cyan)
        yes = optionfont.render("Yes", False, Red, Black)
        no = optionfont.render("No", False, Cyan, Black)
        Screen.blit(sure1,(screen_width*.5-(sure1.get_width()//2),screen_height*.15))
        Screen.blit(sure2,(screen_width*.5-(sure2.get_width()//2),screen_height*.15+sure1.get_height()))
        Screen.blit(sure3,(screen_width*.5-(sure3.get_width()//2),screen_height*.15+sure1.get_height()+sure3.get_height()))
        y = .8
        mouse = pygame.mouse.get_pos()
        if screen_width*.4-yes.get_width() < mouse[0] < screen_width*.4 and screen_height*y < mouse[1] < screen_height*y+yes.get_height():
            yes = optionfont.render("Yes", False, Red, DarkRed)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    Player.DeletePlayer(PlayerName)
                    choosing = False
                    global inMenu
                    inMenu = False
        if screen_width*.55 < mouse[0] < screen_width*.55+yes.get_width() and screen_height*y < mouse[1] < screen_height*y+no.get_height():
            no = optionfont.render("No", False, Cyan, Blue)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    choosing = False
        Screen.blit(yes,(screen_width*.4-yes.get_width(),screen_height*y))
        Screen.blit(no,(screen_width*.55,screen_height*y))
        Screen.blit(Cursor,pygame.mouse.get_pos())
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if GetKey(event) and GetKey(event).items() >= Controls['Back'].items():
                choosing = False
 
def Resize(Size):
    global Screen, screen_width, screen_height, aspect_ratio
    w,h = Size
    if w < 400: #If the screens width is less than 800
        w = 400 #Set it to 800
    if h < 300: #If the screens height is less than 600
        h = 300 #Set it to 600
    while w != int(h*aspect_ratio): #While the window is not in its original aspect ratio
        if w < int(h*aspect_ratio): #If the width is too small
            w += 1 #Increase it
        elif w > int(h*aspect_ratio): #If the width is too big
            w -= 1 #Decrease it
        if w < int(h*aspect_ratio): #If the width is too small
            h -= 1 #Decrease the height
        elif w > int(h*aspect_ratio): #If the width is too big
            h += 1 #Increase the height
    screen_width = w
    screen_height = h
    Screen = pygame.display.set_mode((int(screen_width), int(screen_height)),pygame.RESIZABLE) #Resize the game window

def ControllerHelp(keybind):
    try:
        joystick = pygame.joystick.Joystick(keybind['joystick'])
        if not joystick.get_init(): joystick.init()
        xaxis, yaxis = keybind['axi']
        x = joystick.get_axis(xaxis)
        y = joystick.get_axis(yaxis)
        if round(x,1) != 0:
            pygame.mouse.set_pos(pygame.mouse.get_pos()[0]+(25*x),pygame.mouse.get_pos()[1])
        if round(y,1) != 0:
            pygame.mouse.set_pos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+(25*y))
    except:
        return
        
def Main(Screen,PlayerName,MechImg,Mech_Img,a,w,h,controls):
    Data = Player.LoadPlayer(PlayerName)
    global Points, aspect_ratio, screen_width, screen_height, inMenu, Cursor, Cursor0, Controls
    Controls = controls
    aspect_ratio = a
    screen_width = w
    screen_height = h
    Points = Data['Points']
    Buttons = []
    MechBackImg = pygame.transform.scale(pygame.image.load(Directory+'\Images\Mech_.png'), (MechImg.get_width(), MechImg.get_height()))
    Buttons.append(ColorButton(Screen,.7,Data['Color'],MechImg,Mech_Img,MechBackImg))
    Buttons.append(Button(Screen,.075,Data['Health'],10,'Health',Data['Level']**2))
    Buttons.append(Button(Screen,.2,Data['Damage'],1,'Damage',Data['Level']/4))
    Buttons.append(Button(Screen,.325,Data['FireSpeed'],1,'FireSpeed',Data['Level']/5))
    Buttons.append(Button(Screen,.45,Data['MoveSpeed'],1,'MoveSpeed',Data['Level']/10))
    Buttons.append(Button(Screen,.575,Data['BlastSpeed'],1,'BlastSpeed',Data['Level']/10))
    inMenu = True
    while inMenu:
        if Controls['Mouse']['type'] == 'joystick':
            ControllerHelp(Controls['Mouse'])
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        Screen.fill((0,0,0))
        for button in Buttons:
            button.update()
        optionfont = pygame.font.SysFont('Arial Black', int(30*(screen_height/600)),True) #Set a font to arial black size 30 and bold
        health = optionfont.render("Health", False, (0,255,255))
        damage = optionfont.render("Damage", False, (0,255,255))
        fire = optionfont.render("Fire Rate", False, (0,255,255))
        move = optionfont.render("Move Speed", False, (0,255,255))
        blast = optionfont.render("Blast Speed", False, (0,255,255))
        color = optionfont.render("Color", False, (0,255,255))
        p = optionfont.render("Points:{}".format(format(Points,',')),False,Cyan)
        if Data['Level'] == 100:
            xp = optionfont.render("XP: Max",False,Cyan)
        else:
            xp = optionfont.render("XP:{}/{}".format(format(Data['XP'],','),format(Data['Level']**2,',')),False,Cyan)
        l = optionfont.render("Level:{}".format(str(Data['Level'])),False,Cyan)
        Screen.blit(health,(screen_width*.25,screen_height*.075))
        Screen.blit(damage,(screen_width*.25,screen_height*.2))
        Screen.blit(fire,(screen_width*.25,screen_height*.325))
        Screen.blit(move,(screen_width*.25,screen_height*.45))
        Screen.blit(blast,(screen_width*.25,screen_height*.575))
        Screen.blit(color,(screen_width*.25,screen_height*.7))
        Screen.blit(p,(screen_width*.05,0))
        Screen.blit(xp,(screen_width*.5-(xp.get_width()//2),0))
        Screen.blit(l,(screen_width*.75,0))
        myfont = pygame.font.SysFont('Arial Black', int(25*(screen_height/600)),True)
        save = myfont.render('Save', False, DarkOrange, Black)
        delete = myfont.render('Delete', False, DarkOrange, Black)
        back = myfont.render('Back', False, DarkOrange, Black)
        mouse = pygame.mouse.get_pos()
        if screen_width*.75 <= mouse[0] <= screen_width*.75+save.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+save.get_height():
            save = myfont.render('Save', False, DarkOrange, Orange)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    for button in Buttons:
                        Data[button.index] = button.value
                    Data['Points'] = Points
                    Player.SavePlayer(Data)
                    inMenu = False
                    Mech_Img = Colorize(MechBackImg, Data['Color'])
                    wait(0.5)
                    Main(Screen,Data['Name'],MechImg,Mech_Img,aspect_ratio,screen_width,screen_height,controls)
        if screen_width*.5 <= mouse[0] <= screen_width*.5+save.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+save.get_height():
            delete = myfont.render('Delete', False, DarkOrange, Orange)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    Delete(Screen,PlayerName)
        if screen_width*.25 <= mouse[0] <= screen_width*.25+save.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+save.get_height():
            back = myfont.render('Back', False, DarkOrange, Orange)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    inMenu = False
        Screen.blit(save,(screen_width*.75,screen_height*.9))
        Screen.blit(delete,(screen_width*.5,screen_height*.9))
        Screen.blit(back,(screen_width*.25,screen_height*.9))
        Screen.blit(Cursor,pygame.mouse.get_pos())
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if GetKey(event) and GetKey(event).items() >= Controls['Back'].items(): #If the back button is pressed
                Screen.fill(Black)
                inMenu = False
        Clock.tick(30)
    return screen_width, screen_height