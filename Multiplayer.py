'''
Created on Aug 9, 2018

@author: justo
'''
import os
import math
from time import sleep
import random
import pickle
import pygame
import Player
from Controls import GetKey
from Controls import Convert
from Controls import DeConvert
from Controls import ControllerHelp
from Controls import GetInput
from Controls import GetKeyName
from Controls import CheckForJoystick

Directory = os.getcwd() #Gets the directory this script is in
pygame.init()
screen_width = 800 #The width of the game window
screen_height = 600 #The height of the game window
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
HealthBarColors = [Red,DarkOrange,Orange,Yellow,LightGreen,Green,GreenBlue,DarkGreen,DarkBlue,BlueGreen,Blue,Indigo,Purple,Pink,HotPink,BluePurple,LightBlue,Cyan,BabyBlue,White] #A list of the colors of the health bars
MImg = pygame.image.load(Directory+'\Images\Mech.png') #Loads the players mech image
M_Img = pygame.image.load(Directory+'\Images\Mech_.png') #Loads the players mech image
EMImg = pygame.image.load(Directory+'\Images\EMech.png') #Loads the enemy's mech image
EM_Img = pygame.image.load(Directory+'\Images\EMech_.png') #Loads the enemy's mech image
MechImg = MImg
Mech_Img = M_Img
EMechImg = EMImg
EMech_Img = EM_Img
MechImg = pygame.transform.scale(MechImg, (int(screen_height/4), int(screen_height/4))) #Changes the image's size
EMechImg = pygame.transform.scale(EMechImg, (int(screen_height/4), int(screen_height/4))) #Changes its size
BlastImg = pygame.image.load(Directory+'\Images\Blast.png') #Loads the player's energy blast image
EBlastImg = pygame.image.load(Directory+'\Images\EBlast.png') #Loads the enemy's energy blast image
Explosion1 = [] #List of explosion frames
Explosion2 = [] #List of explosion frames
for i in range(32): #Loads explosion images(frames) into Explosion1
    Explosion1.append(pygame.image.load(Directory+'\Images\Explosion1\\frame_{}.png'.format(i)))
for i in range(16):#Loads explosion images(frames) into Explosion2
    Explosion2.append(pygame.image.load(Directory+'\Images\Explosion2\\frame_{}.png'.format(i)))
    Explosion2.append(pygame.image.load(Directory+'\Images\Explosion2\\frame_{}.png'.format(i)))
Cursor0 = pygame.image.load(Directory+'/Images/Cursor0.png') #Loads the arrow cursor
Cursor1 = pygame.image.load(Directory+'/Images/Cursor1.png') #Loads the pointer cursor
Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25))) #Sets cursor to arrow
lazer = pygame.mixer.Sound(Directory+'\Sounds\Effects\\151022__bubaproducer__laser-shot-silenced.wav') #Loads the lazer sound effect
wrong = pygame.mixer.Sound(Directory+'\Sounds\Menu\Wrong.wav') #Loads the wrong sound effect
Clock = pygame.time.Clock()
Screen = None
Blasts = [] #List of player blasts on the screen
EBlasts = [] #List of computer blasts on the screen
Explosions = [] #List of explosions on the screen
Music = [] #List of music for the game
for filename in os.listdir(Directory+'\Sounds\Music'): #Searches the music folder for music and puts it in the music list
    if filename.endswith(".wav"): 
        Music.append(Directory+'\Sounds\Music\\'+filename)
Reloading1 = False #If the player1's mech is reloading
Reloading2 = False #If the player2's mech is reloading
SettingsFile = open(Directory+'\Data\Settings.dat','rb')
Settings = pickle.load(SettingsFile)
SettingsFile.close()
Player1Position = 0.6 #The current position of player1
Player1Data = {} #The stats of player1
Player1Health = 10 #The current health of player1
Player2Position = 0.6 #The current position of player2
Player2Data = {} #The stats of player2
Player2Health = 10 #The current health of player2
choosing = True
Close = False
aspect_ratio = 0
ControlsFile = open(Directory+'\Data\Controls.dat','rb')
Controls = pickle.load(ControlsFile)
ControlsFile.close()
Controls = Convert(Controls)
ControlsFile2 = open(Directory+'\Data\Controls2.dat','rb')
Controls2 = pickle.load(ControlsFile2)
ControlsFile2.close()
Controls2 = Convert(Controls2)
controls2 = Controls2
Keybinds = []
DefaultKeybinds = [{'name':'Shoot1','keybind':{'type': 'key', 'value': 32}},{'name':'Up1','keybind':{'type': 'key', 'value': 119}},{'name':'Down1','keybind':{'type': 'key', 'value': 115}},{'name':'Shoot2','keybind':{'type': 'key', 'value': 13}},{'name':'Up2','keybind':{'type': 'key', 'value': 273}},{'name':'Down2','keybind':{'type': 'key', 'value': 274}}]


class Blast: #The class for the Player1's energy blasts
    def __init__(self,speed,dmg,img):
        global Player1Position, screen_height
        self.speed = speed #How fast the blast travels
        self.dmg = dmg #How much dmg it deals
        self.size = int(1+(self.dmg/25)) #Calculates the size of the blast based on its damage
        self.x = (screen_height*.1875)/screen_width #The x position of the blast
        self.y = Player1Position+.1275 #The y position of the blast
        self.bmp = img
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.05*self.size),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def __del__(self): #When the blast is deleted make an explosion at the blast's position
        Explosions.append(Boom(self.x,self.y,self.size))
    def img_update(self):
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.05*self.size),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def update(self): #Draws the blast on the screen and runs its logic
        self.x += math.sqrt(self.speed)/1000
        global Player2Position
        if screen_width*self.x > screen_width-(((screen_height/4)*.77)+(screen_height*.05*self.size)) and (screen_height*self.y)+(screen_height*.0125*self.size) >= screen_height*Player2Position >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.7): #If the blast hits the Player2s mech make it explode and deal damage to the Player2
            global Player2Health
            Player2Health -= self.dmg
            Blasts.remove(self)
        elif screen_width*self.x > screen_width-(((screen_height/4)*.22)+(screen_height*.05*self.size)) and screen_height*self.y+(screen_height*.0125*self.size) >= screen_height*Player2Position >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.9):
            Player2Health -= self.dmg
            Blasts.remove(self)
        elif screen_width*self.x > screen_width: #Else if the blast is off the screen destroy it
            Blasts.remove(self) 
        for blast in EBlasts: #Iterate over all of the enemy blasts
            if screen_width*self.x+(screen_height*.05*self.size) >= screen_width*blast.x and screen_height*self.y+(screen_height*.0125*self.size) >= (screen_height*blast.y)-(screen_height*.0125*blast.size) >= screen_height*self.y-(screen_height*.025*blast.size): #If the blast is touching an enemy blast
                if blast.dmg > 0 and self.dmg > 0: #If both blasts have more than 0 dmg left
                    mydmg = self.dmg
                    yourdmg = blast.dmg
                    self.dmg -= yourdmg #Decrease their dmg by each other's dmg
                    blast.dmg -= mydmg
                    if blast.dmg > 0: #If the enemy blast's dmg is more than 0 update its image size
                        blast.size = int(1+(blast.dmg/25))
                        blast.img_update()
                    else: #Otherwise destroy it
                        EBlasts.remove(blast)
                    if self.dmg > 0: #If this blast's dmg is more than 0 update its image size
                        self.size = int(1+(self.dmg/25))
                        self.img_update()
                    else: #Otherwise destroy it
                        if self in Blasts:
                            Blasts.remove(self)
        Screen.blit(self.img,(int(screen_width*self.x),int(screen_height*self.y-(screen_height*.0125*self.size)))) #Draw the blast 
        
class EBlast: #The class for the player's energy blasts
    def __init__(self,speed,dmg,img):
        self.speed = speed #How fast the blast travels
        self.dmg = dmg #How much dmg it deals
        self.size = int(1+(self.dmg/25)) #The base size of the blasts is 25 and is bigger the more dmg it deals
        self.x = 1-(((screen_height*.1875)+((screen_height*.025*self.size*2)))/screen_width) #The x position of the blast
        self.y = Player2Position+.1275 #The y position of the blast
        self.bmp = img
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.025*self.size*2),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def __del__(self): #When the blast is deleted make an explosion at the blast's position
        Explosions.append(Boom(self.x-(self.size*.025),self.y,self.size))
    def img_update(self):
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.025*self.size*2),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def update(self): #Draws the blast on the screen and runs its logic
        self.x -= math.sqrt(self.speed)/1000
        if screen_width*self.x < (screen_height/4)*.77 and screen_height*self.y+(screen_height*.0125*self.size) >= screen_height*Player1Position >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.7): #If the blast hits the Player1s mech make it explode and deal dmg to the player
            global Player1Health
            Player1Health -= self.dmg
            EBlasts.remove(self)
        elif screen_width*self.x < (screen_height/4)*.22 and screen_height*self.y+(screen_height*.0125*self.size) >= screen_height*Player1Position >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.9):
            Player1Health -= self.dmg
            EBlasts.remove(self)
        elif screen_width*self.x < 0-(screen_height*.05*self.size): #Else if the blast is off the screen destroy it
            if self in EBlasts:
                EBlasts.remove(self)
        Screen.blit(self.img,(int(screen_width*self.x),int(screen_height*self.y-(screen_height*.0125*self.size)))) #Draw the blast
    
class Boom(): #The class for explosions
    def __init__(self,x,y,size):
        if random.randint(1,2) == 1: #Picks a random image list for the explosion so that explosions don't all look the same
            self.explosion = Explosion1
        else:
            self.explosion = Explosion2
        self.frame = 0 #Which frame the explosion is on
        self.size = int(size*2) #The size of the explosion
        self.x = x #The x position of the explosion
        self.y = y #The y position of the explosion
    def update(self): #Draws the explosion on the screen and deletes it when its animation completes
        img = pygame.transform.scale(self.explosion[int(self.frame)], (int(screen_height*.025*self.size), int(screen_height*.025*self.size))) #Changes the explosion frame image size to the size of the explosion 
        Screen.blit(img,(screen_width*self.x+(screen_height*.0125*self.size),screen_height*self.y-(screen_height*.0125*self.size))) #Draws the explosion
        self.frame += 0.5 #Skips to the next frame once every other run of this function
        if self.frame > 30: #If it has reached the end of the animation then delete this explosion
            Explosions.pop(0)
                    
class PlayerButton():
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.activating = False
        self.active = False
    def update(self):
        global Cursor, Cursor1
        myfont = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True) #Set a font to arial black size 50 and bold
        player = myfont.render(self.name, False, DarkOrange, Black) #Show a button with the text of the player's name
        mouse = pygame.mouse.get_pos()
        if screen_width*self.x <= mouse[0] <= (screen_width*self.x)+player.get_width() and screen_height*self.y <= mouse[1] <= (screen_height*self.y)+player.get_height(): #If the user is hovering over this button
            player = myfont.render(self.name, False, DarkOrange, Orange) #Add an orange background to the button
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    self.activating = True
        elif self.active:
            player = myfont.render(self.name, False, DarkOrange, Orange) #Add an orange background to the button
        Screen.blit(player,(screen_width*self.x,screen_height*self.y))
        
class TextButton(): #Exits to the main menu from the choose level screen
    def __init__(self,x,y,text,function):
        self.x = x
        self.y = y
        self.text = text
        self.function = function
    def update(self):
        global Cursor, Cursor1
        myfont = pygame.font.SysFont('Arial Black', int(33*(screen_height/600)),True) #Set a font to arial black size 25 and bold
        player = myfont.render(self.text, False, DarkOrange, Black) #Show a button with the text of the player's name
        mouse = pygame.mouse.get_pos()
        if screen_width*self.x <= mouse[0] <= screen_width*self.x+player.get_width() and screen_height*self.y <= mouse[1] <= screen_height*self.y+player.get_height(): #If the user is hovering over this button
            player = myfont.render(self.text, False, DarkOrange, Orange) #Add an orange background to the button
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    self.function() #Trigger the button's function
        Screen.blit(player,(screen_width*self.x,screen_height*self.y))
        
class Keybind():
    def __init__(self,name,keybind):
        self.name = name
        self.keybind = keybind
    def new_keybind(self):
        self.keybind = GetInput(self.name)
        global controls
        controls[self.name] = self.keybind
    def get_name(self):
        return self.name
        
def Colorize(image, color):
    m = pygame.mask.from_surface(image, 0)
    shader = pygame.Surface((image.get_size()), masks=m).convert_alpha()
    shader.fill(color)
    copied = image.copy()
    copied.blit(shader, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return copied
        
def Resize(Size):
    global Screen, screen_width, screen_height, aspect_ratio, MechImg, EMechImg, Mech_Img, EMech_Img, Blasts, EBlasts, M_Img, MImg, EM_Img, EMImg
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
    #Resize images to match
    MechImg = pygame.transform.scale(MImg, (int(screen_height/4), int(screen_height/4)))
    EMechImg = pygame.transform.scale(EMImg, (int(screen_height/4), int(screen_height/4)))
    image = Colorize(pygame.transform.scale(M_Img, (int(screen_height/4), int(screen_height/4))),Player1Data['Color'])
    Mech_Img = pygame.Surface((int(screen_height/4),int(screen_height/4))).convert()
    Mech_Img.blit(image, (0,0))
    image = Colorize(pygame.transform.scale(EM_Img, (int(screen_height/4), int(screen_height/4))),Player2Data['Color'])
    EMech_Img = pygame.Surface((int(screen_height/4),int(screen_height/4))).convert()
    EMech_Img.blit(image, (0,0))
    for blast in Blasts:
        blast.img_update()
    for blast in EBlasts:
        blast.img_update()
      
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
                
def StartGame(p1,p2):
    global Player1Data
    global Player2Data
    Player1Data = Player.LoadPlayer(p1)
    Player2Data = Player.LoadPlayer(p2)
    global Close
    Close = False
    GameLoop()
    
def Back():
    global choosing
    choosing = False    
    
def GetPlayer(players):
    for player in players:
        if player.active:
            return player.name
        
def ControlsMenu():
    global screen_height, screen_width, aspect_ratio, Screen, Controls, Controls2, Keybinds, Clock
    for keybind in DeConvert(Controls2):
        Keybinds.append(Keybind(keybind['name'],keybind['keybind']))
    done = False
    pygame.joystick.quit()
    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        if not joystick.get_init(): joystick.init()
    while not done:
        global Screen, screen_height, screen_width, Cursor
        Screen.fill(Black)
        events = []
        for event in pygame.event.get():
            events.append(event)
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        font = pygame.font.SysFont('Arial Black', int(25*(screen_height/600)),True)
        mouse = pygame.mouse.get_pos()
        for i in range(len(Keybinds)):
            name = font.render(Keybinds[i].name, False, Cyan)
            for event in events:
                if GetKey(event) and GetKey(event).items() >= Keybinds[i].keybind.items():
                    name = font.render(Keybinds[i].name, False, Cyan, Red)
            value = font.render(GetKeyName(Keybinds[i].keybind), False, Red,Cyan)
            if i <= 10:
                Screen.blit(name,(0,screen_height*(i/15)))
                if screen_width*.1 <= mouse[0] <= screen_width*.1+value.get_width() and screen_height*(i/15) <= mouse[1] <= screen_height*(i/15)+value.get_height():
                    Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                    value = font.render(GetKeyName(Keybinds[i].keybind), False, Cyan,Red)
                    for event in events:
                        if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                            Keybinds[i].new_keybind()
                        elif Keybinds[i].get_name() == 'Click' and Controls['Click']['type'] != 'click' and Controls['Click']['type'] != 'key' and not CheckForJoystick() and event.type == pygame.MOUSEBUTTONDOWN: #If this is the click keybind and the click button is on a controller that is disconnected and the player clicks the mouse
                            Keybinds[i].new_keybind()
                Screen.blit(value,(screen_width*.1,screen_height*(i/15)))
            elif i <= 21:
                Screen.blit(name,(screen_width*.375,screen_height*((i-11)/15)))
                if screen_width*.475 <= mouse[0] <= screen_width*.475+value.get_width() and screen_height*((i-11)/15) <= mouse[1] <= screen_height*((i-11)/15)+value.get_height():
                    Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                    value = font.render(GetKeyName(Keybinds[i].keybind), False, Cyan,Red)
                    for event in events:
                        if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                            Keybinds[i].new_keybind()
                Screen.blit(value,(screen_width*.475,screen_height*((i-11)/15)))
            elif i <= 32:
                Screen.blit(name,(screen_width*.75,screen_height*((i-22)/15)))
                if screen_width*.85 <= mouse[0] <= screen_width*.85+value.get_width() and screen_height*((i-22)/15) <= mouse[1] <= screen_height*((i-22)/15)+value.get_height():
                    Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                    value = font.render(GetKeyName(Keybinds[i].keybind), False, Cyan,Red)
                    for event in events:
                        if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                            Keybinds[i].new_keybind()
                Screen.blit(value,(screen_width*.85,screen_height*((i-22)/15)))
        back = font.render('Back', False, DarkOrange)
        reset = font.render('Reset', False, DarkOrange)
        save = font.render('Save', False, DarkOrange)
        if screen_width*.1 <= mouse[0] <= screen_width*.1+back.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+back.get_height():
            back = font.render('Back', False, DarkOrange, Orange)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in events:
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    done = True
        if screen_width*.4 <= mouse[0] <= screen_width*.4+reset.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+reset.get_height():
            reset = font.render('Reset', False, DarkOrange, Orange)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in events:
                if GetKey(event) and (GetKey(event).items() >= Controls['Click'].items() or GetKey(event).items() >= {'type':'click','value':1}.items()):
                    Reset()
                    done = True
        if screen_width*.7 <= mouse[0] <= screen_width*.7+save.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+save.get_height():
            save = font.render('Save', False, DarkOrange, Orange)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in events:
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    Save()
                    save = font.render('Saved', False, Orange, DarkOrange)
        Screen.blit(back,(screen_width*.1,screen_height*.9))
        Screen.blit(reset,(screen_width*.4,screen_height*.9))
        Screen.blit(save,(screen_width*.7,screen_height*.9))
        Screen.blit(Cursor,mouse)
        pygame.display.update()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            elif event.type == pygame.VIDEORESIZE:
                Resize(event.size)
        if Controls['Mouse']['type'] == 'joystick':
            ControllerHelp(Controls['Mouse'])
        Clock.tick(30)
    Keybinds.clear()
    
def Reset():
    global DefaultKeybinds, Controls2, controls2, Screen, aspect_ratio, screen_width, screen_height
    ControlsFile = open(Directory+'\Data\Controls2.dat', 'wb')
    pickle.dump(DefaultKeybinds, ControlsFile)
    Controls2 = DefaultKeybinds
    controls2 = Convert(Controls2)
    Keybinds.clear()
    ControlsMenu()
    
def Save():
    global Controls2, controls2
    Controls2 = DeConvert(controls2)
    ControlsFile = open(Directory+'\Data\Controls2.dat', 'wb')
    pickle.dump(Controls2, ControlsFile)
    ControlsFile.close()
                
def ChoosePlayers(s,a,w,h):
    global Screen, aspect_ratio, screen_width, screen_height, Cursor, Cursor0
    Screen = s
    aspect_ratio = a
    screen_width = w
    screen_height = h
    Screen.fill(Black) #Blanks the screen
    pygame.display.update()
    Players = Player.GetPlayers() #Gets a list of saved players
    Buttons1 = [] #A list of players for player1
    Buttons2 = [] #A list of players for player2
    i = 1
    for p in Players: #Creates a player button for every saved player and adds it to the list of buttons
        Buttons1.append(PlayerButton(.2,.125*i,p))
        Buttons2.append(PlayerButton(.6,.125*i,p))
        i += 1
    backbutton = TextButton(.2,.9,"Back",Back)
    playbutton = TextButton(.4,.9,"Play",lambda: StartGame(GetPlayer(Buttons1), GetPlayer(Buttons2)) if GetPlayer(Buttons1) and GetPlayer(Buttons2) else pygame.mixer.Sound.play(wrong))
    controlsbutton = TextButton(.6,.9,"Controls",ControlsMenu)
    global choosing
    choosing = True
    while choosing:
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        Screen.fill(Black) #Blanks the screen
        for button in Buttons1: #Have all of the buttons1 run their update method
            button.update()
            if button.activating:
                for b in Buttons1:
                    b.active = False
                button.active = True
                button.activating = False
        for button in Buttons2: #Have all of the buttons2 run their update method
            button.update()
            if button.activating:
                for b in Buttons2:
                    b.active = False
                button.active = True
                button.activating = False
        backbutton.update()
        playbutton.update()
        controlsbutton.update()
        Screen.blit(Cursor,pygame.mouse.get_pos())
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if GetKey(event) and GetKey(event).items() >= Controls['Back'].items(): #If the back button is being pressed
                choosing = False
        Clock.tick(30)
    return screen_width, screen_height
        
def GameLoop(): #The function that runs the game
    Resize((screen_width,screen_height))
    ReloadCounter1 = 0
    ReloadCounter2 = 0
    #Tells the function to use the following global variables instead of making new variables
    global Reloading1
    global Reloading2
    global Player1Position
    global Player1Data
    global Player1Health
    global Player2Position
    global Player2Data
    global Player2Health
    #Reset the players' health
    Player1Health = Player1Data['Health']
    Player2Health = Player2Data['Health']
    #Reset mech positions
    Player1Position = 0.6
    Player2Position = 0.6
    pygame.mixer.music.load(Music[random.randint(0,len(Music)-1)]) #Load a random song from the music list
    #pygame.mixer.music.set_volume(Settings['Master']*Settings['Music'])
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the song 
    while not Close:
        if ReloadCounter1 >= 100/Player1Data['FireSpeed']: #If the reload counter is more than the time needed to reload
            Reloading1 = False #Set reloading to false
            ReloadCounter1 = 0 #Reset the reload counter to 0
        elif Reloading1 == True: #Else as long as it is reloading
            ReloadCounter1 += 1 #Add 1 to the reload counter
        if ReloadCounter2 >= 100/Player2Data['FireSpeed']: #If the reload counter is more than the time needed to reload
            Reloading2 = False #Set reloading to false
            ReloadCounter2 = 0 #Reset the reload counter to 0
        elif Reloading2 == True: #Else as long as it is reloading
            ReloadCounter2 += 1 #Add 1 to the reload counter
        GameEventHandler() #Run the game event handler function
        DrawScreen() #Run the draw screen function
        if Player1Health < 1: #If the player's health is less than 1
            Blasts.clear() #Destroy all player blasts
            EBlasts.clear() #Destroy all enemy blasts
            Explosions.clear() #Destroy all explosions
            GameOver(Player2Data['Name'])
        elif Player2Health < 1: #If the computer's health is less than 1
            Blasts.clear() #Destroy all player blasts
            EBlasts.clear() #Destroy all enemy blasts
            Explosions.clear() #Destroy all explosions
            GameOver(Player1Data['Name'])
        Clock.tick(100) #How many times this function will run per second
        
def GameEventHandler(): #Handles the events during the game
    global Reloading1
    global Player1Position
    global Player1Data
    global Reloading2
    global Player2Position
    global Player2Data
    for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
        if event.type == pygame.QUIT: #If the user clicked the close button
            kill() #Close the window and stop the program
        if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
        if GetKey(event) and GetKey(event).items() >= Controls2['Shoot1'].items(): #If player1 presses their shoot button
            if not Reloading1: #If their mech is not reloading
                Blasts.append(Blast(Player1Data['BlastSpeed'],Player1Data['Damage'],BlastImg)) #Create a blast with player1's speed and dmg and with the image of BlastImg
                pygame.mixer.Sound.play(lazer) #Play the lazer blast sound effect
                Reloading1 = True #Set their mech reloading to true
        if GetKey(event) and GetKey(event).items() >= Controls2['Up1'].items() and Player1Position > .1: #If player1 presses their up button and their mech is not at the top
            Player1Position -= Player1Data['MoveSpeed']/1000 #Move their mech upward at their move speed
        if GetKey(event) and GetKey(event).items() >= Controls2['Down1'].items() and Player1Position < .8: #If player1 presses their down button and their mech is not at the top
            Player1Position += Player1Data['MoveSpeed']/1000 #Move their mech downward at their move speed
        if GetKey(event) and GetKey(event).items() >= Controls2['Shoot2'].items(): #If player2 presses their shoot button
            if not Reloading2: #If the mech is not reloading
                EBlasts.append(EBlast(Player2Data['BlastSpeed'],Player2Data['Damage'],EBlastImg)) #Create a blast with the speed of BlastSpeed dmg and size of BlastDmg and with the image of BlastImg
                pygame.mixer.Sound.play(lazer) #Play the lazer blast sound effect
                Reloading2 = True #Set reloading to true
        if GetKey(event) and GetKey(event).items() >= Controls2['Up2'].items() and Player2Position > .1: #If player2 presses their up button and their mech is not at the top
            Player2Position -= Player2Data['MoveSpeed']/1000 #Move their mech upward at their move speed
        if GetKey(event) and GetKey(event).items() >= Controls2['Down2'].items() and Player2Position < .8: #If player2 presses their down button and their mech is not at the top
            Player2Position += Player2Data['MoveSpeed']/1000 #Move their mech downward at their move speed
        elif GetKey(event) and GetKey(event).items() >= Controls['Back'].items(): #If the players press back button
            Pause() #Pause the game
                    
def DrawScreen(): #Draws the screen
    Screen.fill(Black) #Resets the screen to black
    Screen.blit(Mech_Img,(0,screen_height*Player1Position))
    Screen.blit(EMech_Img,(screen_width-EMech_Img.get_width(),screen_height*Player2Position))
    for Blast in Blasts: #Draws all of the player blasts on the screen
        Blast.update()
    for Blast in EBlasts: #Draws all of the computer blasts on the screen
        Blast.update()
    Screen.blit(MechImg,(0,screen_height*Player1Position))
    Screen.blit(EMechImg,(screen_width-EMechImg.get_width(),screen_height*Player2Position))
    for Boom in Explosions: #Draws all of the explosions on the screen
        Boom.update()
    p2health = Player2Health
    hindex = 0
    while p2health > 0: #Draws player2's health bar
        if p2health >= 500:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [screen_width,screen_height*.02,-screen_width*.3,screen_height*.05])
            p2health -= 500
        else:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [screen_width,screen_height*.02,-(((screen_width*.3)/500)*p2health),screen_height*.05])
            p2health -= p2health
        hindex += 1
    p1health = Player1Health
    hindex = 0
    while p1health > 0: #Draws player1's health bar
        if p1health >= 500:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [0,screen_height*.02,screen_width*.3,screen_height*.05])
            p1health -= 500
        else:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [0,screen_height*.02,((screen_width*.3)/500)*p1health,screen_height*.05])
            p1health -= p1health
        hindex += 1
    pygame.display.update() #Updates the screen so the user can see the new screen
    
def Pause():
    paused = True
    global Cursor, Cursor0, Cursor1
    s = Screen.copy()
    while paused:
        si = pygame.transform.scale(s,(screen_width,screen_height))
        Screen.blit(si,(0,0))
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        font = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True) #Set a font to arial black size 50 and bold
        back = font.render("Back To Game", False, DarkOrange)
        menu = font.render("Exit To Menu", False, DarkOrange)
        mouse = pygame.mouse.get_pos()
        if screen_width/2-back.get_width()/2 < mouse[0] < screen_width/2+back.get_width()/2 and screen_height/2-back.get_height() < mouse[1] < screen_height/2: #If the mouse is hovering over the back to game button
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            back = font.render("Back To Game", False, DarkOrange, Orange)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    paused = False #Unpause the game
        if screen_width/2-menu.get_width()/2 < mouse[0] < screen_width/2+menu.get_width()/2 and screen_height/2 < mouse[1] < screen_height/2+menu.get_height(): #If the mouse is hovering over the menu button
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            menu = font.render("Exit To Menu", False, DarkOrange, Orange)
            for event in pygame.event.get():
                if GetKey(event) and GetKey(event).items() >= Controls['Click'].items():
                    #Return to the choose players menu
                    Blasts.clear()
                    EBlasts.clear()
                    Explosions.clear()
                    wait(.25)
                    global Close
                    Close = True
                    paused = False
                    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
                    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
        Screen.blit(back,(screen_width/2-back.get_width()/2,screen_height/2-back.get_height()))
        Screen.blit(menu,(screen_width/2-menu.get_width()/2,screen_height/2))
        Screen.blit(Cursor, mouse)
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if GetKey(event) and GetKey(event).items() >= Controls['Back'].items(): #If the back button is pressed
                paused = False #Unpause the game
        Clock.tick(30)
        
def GameOver(Winner): #Displays the game over screen
    global Cursor, Cursor0, Cursor1
    s = Screen.copy()
    waiting = True
    while waiting:
        si = pygame.transform.scale(s,(screen_width,screen_height))
        Screen.blit(si,(0,0))
        mainfont = pygame.font.SysFont('Arial Black', int(75*(screen_height/600)),True)
        text = mainfont.render('GAME OVER', False, Red) #Render the text 'GAME OVER' in Red
        Screen.blit(text,(screen_width//2-(text.get_width()//2),screen_height//2-(text.get_height()//2))) #Display the text
        playerfont = pygame.font.SysFont('Arial Black', int(60*(screen_height/600)),False)
        winnertext = playerfont.render('{} Wins!'.format(Winner), False, Blue) #Display the amount of xp gained, the player's total xp, the amount of xp needed to level up, and the player's current level
        Screen.blit(winnertext,(screen_width//2-(winnertext.get_width()//2),screen_height//2+(text.get_height()//2)))
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if GetKey(event) and GetKey(event).items() >= Controls['Back'].items(): #If the back button is pressed
                global Close
                Close = True
                waiting = False
                pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
                pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
        Clock.tick(10)