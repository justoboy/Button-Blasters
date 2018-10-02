'''
Created on Jul 7, 2018

@author: justo
'''
import os
import random
from random import randint
from time import sleep
import pickle
import math
import Player
import pyautogui as pygui
import ctypes
user32 = ctypes.WinDLL('user32')
import pygame
import Upgrade
import Multiplayer
#import Controllers

Directory = os.getcwd() #Gets the directory this script is in
pygame.init()
pygame.font.init()
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
Icon = pygame.image.load(Directory+'\Images\Icon.png') #Loads the icon for the game window
pygame.display.set_icon(Icon) #Sets the game window icon
BlastImg = pygame.image.load(Directory+'\Images\Blast.png') #Loads the player's energy blast image
EBlastImg = pygame.image.load(Directory+'\Images\EBlast.png') #Loads the enemy's energy blast image
Explosion1 = [] #List of explosion frames
Explosion2 = [] #List of explosion frames
for i in range(32): #Loads explosion images(frames) into Explosion1
    Explosion1.append(pygame.image.load(Directory+'\Images\Explosion1\\frame_{}.png'.format(i)))
for i in range(16):#Loads explosion images(frames) into Explosion2
    Explosion2.append(pygame.image.load(Directory+'\Images\Explosion2\\frame_{}.png'.format(i)))
    Explosion2.append(pygame.image.load(Directory+'\Images\Explosion2\\frame_{}.png'.format(i)))
ding = pygame.mixer.Sound(Directory+'\Sounds\Menu\Ding.wav')
wrong = pygame.mixer.Sound(Directory+'\Sounds\Menu\Wrong.wav')
unlocked = pygame.mixer.Sound(Directory+'\Sounds\Menu\\Unlocked.wav')
lazer = pygame.mixer.Sound(Directory+'\Sounds\Effects\\151022__bubaproducer__laser-shot-silenced.wav') #Loads the lazer sound effect
pygame.mixer.Sound.set_volume(ding,0.025)
pygame.mixer.Sound.set_volume(wrong,0.1)
pygame.mixer.Sound.set_volume(unlocked,0.5)
screen_width,screen_height = pygui.size() #The size of the computer screen
screen_height //= 2
screen_height = int(screen_height)
screen_width //= 2
screen_width = int(screen_width)
Screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE) #Create the game window
user32.ShowWindow(user32.GetForegroundWindow(), 3) #Maximizes the window
for event in pygame.event.get(): #Sets the new screen size
    if event.type == pygame.VIDEORESIZE:
        screen_width, screen_height = event.size
Screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)
aspect_ratio = screen_width/screen_height
pygame.display.update()
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
Cursor0 = pygame.image.load(Directory+'/Images/Cursor0.png') #Loads the arrow cursor
Cursor1 = pygame.image.load(Directory+'/Images/Cursor1.png') #Loads the pointer cursor
Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25))) #Sets cursor to arrow
pygame.display.set_caption('Button Blasters') #Set the windows display name
Clock = pygame.time.Clock()
Close = False
Blasts = [] #List of player blasts on the screen
EBlasts = [] #List of computer blasts on the screen
Explosions = [] #List of explosions on the screen
Music = [] #List of music for the game
for filename in os.listdir(Directory+'\Sounds\Music'): #Searches the music folder for music and puts it in the music list
    if filename.endswith(".wav"): 
        Music.append(Directory+'\Sounds\Music\\'+filename)
Reloading = False #If the player's mech is reloading
ComputerReloading = False #If the computer's mech is reloading
SettingsFile = open(Directory+'\Data\Settings.dat','rb')
Settings = pickle.load(SettingsFile)
SettingsFile.close()
EnemyColor = Red #The background color of the computers mech
ComputerLevel = 1 #The difficulty of the computer
ComputerHealth = 10 #The health of the computer
ComputerDmg = 1 #The damage the computer deals
ComputerFireSpeed = 1 #How many times the computer can shoot per second
ComputerBlastSpeed = 1 #The speed of the computers blasts
ComputerMoveSpeed = 1 #How fast the computer can move up and down
ComputerPosition = 0.6 #The current position of the computer
PlayerPosition = 0.6 #The current position of the player
PlayerData = {'Color':Blue} #The stats of the loaded player
PlayerHealth = 10 #The current health of the player
pygame.mouse.set_visible(False)

def Colorize(image, color):
    m = pygame.mask.from_surface(image, 0)
    shader = pygame.Surface((image.get_size()), masks=m).convert_alpha()
    shader.fill(color)
    copied = image.copy()
    copied.blit(shader, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return copied

image = Colorize(pygame.transform.scale(Mech_Img, (int(screen_height/4), int(screen_height/4))),PlayerData['Color'])
Mech_Img = pygame.Surface((int(screen_height/4),int(screen_height/4))).convert()
Mech_Img.blit(image, (0,0))
image = Colorize(pygame.transform.scale(EMech_Img, (int(screen_height/4), int(screen_height/4))),EnemyColor)
EMech_Img = pygame.Surface((int(screen_height/4),int(screen_height/4))).convert()
EMech_Img.blit(image, (0,0))

#Debug mode stuff
Debug = False #If debug mode is enabled
ShootLock = False #If the player constantly shoots
Regen = False #If the player regenerates health
Follow = False #If the player automatically follows the computer
LevelSelect = False #If the player can choose any level
CheatCodeIndex = 0
Controls = ["mouse",pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_SPACE,pygame.K_ESCAPE,pygame.K_b,pygame.K_a,pygame.K_y,pygame.K_RETURN,"click"]
DebugCheatCode = [1,1,2,2,3,4,3,4,7,8,10]
LevelSelectCheatCode = [1,2,3,4,9,10]

class Blast: #The class for the player's energy blasts
    def __init__(self,speed,dmg,img):
        global PlayerPosition, screen_height
        self.speed = speed #How fast the blast travels
        self.dmg = dmg #How much dmg it deals
        self.size = int(1+(self.dmg/25)) #Calculates the size of the blast based on its damage
        self.x = (screen_height*.1875)/screen_width #The x position of the blast
        self.y = PlayerPosition+.1275 #The y position of the blast
        self.bmp = img
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.05*self.size),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def __del__(self): #When the blast is deleted make an explosion at the blast's position
        Explosions.append(Boom(self.x,self.y,self.size))
    def img_update(self):
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.05*self.size),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def update(self): #Draws the blast on the screen and runs its logic
        self.x += math.sqrt(self.speed)/1000
        global ComputerPosition
        if screen_width*self.x > screen_width-(((screen_height/4)*.77)+(screen_height*.05*self.size)) and (screen_height*self.y)+(screen_height*.0125*self.size) >= screen_height*ComputerPosition >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.7): #If the blast hits the computers mech make it explode and deal damage to the computer
            global ComputerHealth
            ComputerHealth -= self.dmg
            Blasts.remove(self)
        elif screen_width*self.x > screen_width-(((screen_height/4)*.22)+(screen_height*.05*self.size)) and screen_height*self.y+(screen_height*.0125*self.size) >= screen_height*ComputerPosition >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.9):
            ComputerHealth -= self.dmg
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
        self.y = ComputerPosition+.1275 #The y position of the blast
        self.bmp = img
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.025*self.size*2),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def __del__(self): #When the blast is deleted make an explosion at the blast's position
        Explosions.append(Boom(self.x-(self.size*.025),self.y,self.size))
    def img_update(self):
        self.img = pygame.transform.scale(self.bmp,(int(screen_height*.025*self.size*2),int(screen_height*.025*self.size))) #Sets the size of the image of the blast
    def update(self): #Draws the blast on the screen and runs its logic
        self.x -= math.sqrt(self.speed)/1000
        if screen_width*self.x < (screen_height/4)*.77 and screen_height*self.y+(screen_height*.0125*self.size) >= screen_height*PlayerPosition >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.7): #If the blast hits the players mech make it explode and deal dmg to the player
            global PlayerHealth
            PlayerHealth -= self.dmg
            EBlasts.remove(self)
        elif screen_width*self.x < (screen_height/4)*.22 and screen_height*self.y+(screen_height*.0125*self.size) >= screen_height*PlayerPosition >= screen_height*self.y+(screen_height*.0125*self.size)-((screen_height/4)*.9):
            PlayerHealth -= self.dmg
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
            
class LevelButton():
    def __init__(self,row,column,unlocked):
        self.row = row
        self.column = column
        self.level = (column+1)+(10*row)
        self.unlocked = (unlocked>=self.level)
    def update(self,events):
        global LevelSelect
        mouse = pygame.mouse.get_pos()
        myfont = pygame.font.SysFont('Arial Black', int(25*(screen_height/600)),True) #Set a font to arial black size 75 and bold
        if self.unlocked or LevelSelect:
            textsurface = myfont.render(str(self.level), False, Cyan, Black) #Make a text 'Button' using that font with the color Cyan and a black background
        else:
            textsurface = myfont.render(str(self.level), False, Red) #Make a text 'Button' using that font with the color Red
        if (screen_width*.27)+(screen_width*.04*self.column) <= mouse[0] <= (screen_width*.27)+(screen_width*.04*self.column)+textsurface.get_width() and screen_width*.04*self.row <= mouse[1] <= (screen_width*.04*self.row)+textsurface.get_height() and (self.unlocked or LevelSelect):
            textsurface = myfont.render(str(self.level), False, Cyan, Red) #Make a text 'Button' using that font with the color Cyan and a red background
            global Cursor, Cursor1
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    global ComputerLevel
                    ComputerLevel = self.level #Set the computers level to the same as the button's
                    GameLoop() #Start the game
        Screen.blit(textsurface,((screen_width*.27)+(screen_width*.04*self.column),screen_width*.04*self.row)) #Draw the texts on the screen
                
class PlayerButton():
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
    def update(self):
        myfont = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True) #Set a font to arial black size 50 and bold
        player = myfont.render(self.name, False, DarkOrange, Black) #Show a button with the text of the player's name
        mouse = pygame.mouse.get_pos()
        if screen_width*self.x <= mouse[0] <= (screen_width*self.x)+player.get_width() and screen_height*self.y <= mouse[1] <= (screen_height*self.y)+player.get_height(): #If the user is hovering over this button
            player = myfont.render(self.name, False, DarkOrange, Orange) #Add an orange background to the button
            global Cursor, Cursor1
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    global PlayerData
                    PlayerData = Player.LoadPlayer(self.name) #Load the player data of the name of this button
                    ChooseLevel() #Open the choose level menu
        Screen.blit(player,(screen_width*self.x,screen_height*self.y))
                
class NewPlayer(): #A button that creates a new player
    def update(self):
        myfont = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True) #Set a font to arial black size 50 and bold
        text = myfont.render("New Player", False, DarkOrange, Black)
        mouse = pygame.mouse.get_pos()
        if screen_width*.5-(text.get_width()/2) <= mouse[0] <= screen_width*.5-(text.get_width()/2)+text.get_width() and screen_height*.8 <= mouse[1] <= screen_height*.8+text.get_height(): #If the mouse is hovering over the button
            text = myfont.render("New Player", False, DarkOrange, Orange) #Give it an orange background
            global Cursor, Cursor1
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    typing = True
                    newname = "" #The name of the new player
                    while typing:
                        Screen.fill(Black) #Makes the screen blank
                        pygame.draw.line(Screen, White, (screen_width*.1,screen_height*.5), (screen_width*.9,screen_height*.5), 1) #Draws a white line across the screen
                        text = myfont.render(newname, False, White) #Renders a text that displays the name of the new player
                        Screen.blit(text,(screen_width*.5-(text.get_width()//2),screen_height*.5-(text.get_height()*.8))) #Draws that text on the white line
                        pygame.display.update() #Refreshes the screen
                        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
                            if event.type == pygame.QUIT: #If the user clicked the close button
                                kill() #Close the window and stop the program
                            if event.type == pygame.VIDEORESIZE:
                                Resize(event.size)
                            if event.type == pygame.KEYDOWN: #If a key is being pressed
                                if event.key == pygame.K_ESCAPE: #If the player presses the escape key
                                    ChoosePlayer() #Go back to the choose player menu
                                elif event.key == pygame.K_BACKSPACE: #If the player pressed the backspace key
                                    newname = newname[:-1] #Delete the last character in the newname
                                elif event.key == pygame.K_RETURN: #If the player presses the enter key
                                    if newname not in Player.GetPlayers() and len(newname) > 0: #If there is not a player with the entered name already and the name is not blank
                                        Player.CreatePlayer(newname) #Create a player with the name entered
                                        global PlayerData
                                        PlayerData = Player.LoadPlayer(newname) #Load that new player's data
                                        ChooseLevel() #Open the choose level menu
                                else:
                                    if len(newname) < 15: #If the length of the name is less than 15
                                        newname += event.unicode #Add whatever key the user just pressed to the name
                                    
                        Clock.tick(50)
        Screen.blit(text,(screen_width*.5-(text.get_width()/2),screen_height*.8))
        
class TextButton(): #Exits to the main menu from the choose level screen
    def __init__(self,x,y,text,function):
        self.x = x
        self.y = y
        self.text = text
        self.function = function
    def update(self,events):
        myfont = pygame.font.SysFont('Arial Black', int(33*(screen_height/600)),True) #Set a font to arial black size 25 and bold
        player = myfont.render(self.text, False, DarkOrange, Black) #Show a button with the text of the player's name
        mouse = pygame.mouse.get_pos()
        if screen_width*self.x <= mouse[0] <= screen_width*self.x+player.get_width() and screen_height*self.y <= mouse[1] <= screen_height*self.y+player.get_height(): #If the user is hovering over this button
            player = myfont.render(self.text, False, DarkOrange, Orange) #Add an orange background to the button
            global Cursor, Cursor1
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.function() #Trigger the button's function
        Screen.blit(player,(screen_width*self.x,screen_height*self.y))
        
def Resize(Size):
    global Screen, screen_width, screen_height, aspect_ratio, MechImg, EMechImg, Mech_Img, EMech_Img, Blasts, EBlasts, M_Img, MImg, EM_Img, EMImg, Cursor, Cursor0
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
    image = Colorize(pygame.transform.scale(M_Img, (int(screen_height/4), int(screen_height/4))),PlayerData['Color'])
    Mech_Img = pygame.Surface((int(screen_height/4),int(screen_height/4))).convert()
    Mech_Img.blit(image, (0,0))
    image = Colorize(pygame.transform.scale(EM_Img, (int(screen_height/4), int(screen_height/4))),EnemyColor)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #If the player hits space return false so that the intro will be skipped
                    return False
                    t = 0
    return True
  
def change_volume(start,change):
    start *= 10
    start += change
    if start > 10:
        start = 10
    elif start < 0:
        start = 0
    start = int(start)/10
    wait(0.25)
    return start
    
def update_volume():
    pygame.mixer.music.set_volume(Settings['Master']*Settings['Music']) #Set the volume of the music to the master volume times the music volume
    pygame.mixer.Sound.set_volume(lazer,Settings['Master']*Settings['Effects']) #Set the volume of the lazer sound to the master volume times the sound effect volume 
    SettingsFile = open(Directory+'\Data\Settings.dat','wb') #Open the settings file
    pickle.dump(Settings,SettingsFile) #Save the new settings in the file
    SettingsFile.close()

def Intro(): #The intro animation
    pygame.mixer.music.load(Directory+'\Sounds\Menu\intro.wav') #Load the intro music
    pygame.mixer.music.play(loops=0, start=0_0) #Play the intro music
    playing = wait(0.01)
    while playing and pygame.mixer.music.get_pos() < 3900:
        playing = wait(1/60)
    while playing and pygame.mixer.music.get_pos() < 11250:
        playing = wait(1/60)
        MechSize = int(screen_height/4)
        MechPos = int(screen_height*.6)
        Screen.blit(Mech_Img,(0,MechPos))
        Screen.blit(MechImg,(0,MechPos)) #Draw a blue mech
        pygame.display.update()
    while playing and pygame.mixer.music.get_pos() < 15550:
        playing = wait(1/60)
        MechSize = int(screen_height/4)
        MechPos = int(screen_height*.6)
        Screen.blit(Mech_Img,(0,MechPos)) #Draw a blue mech
        Screen.blit(MechImg,(0,MechPos))
        Screen.blit(EMech_Img,(screen_width-MechSize,MechPos)) #Draw a red mech
        Screen.blit(EMechImg,(screen_width-MechSize,MechPos))
        pygame.display.update() 
    while playing and pygame.mixer.music.get_pos() < 19250:
        playing = wait(1/60)
        MechSize = int(screen_height/4)
        MechPos = int(screen_height*.6)
        Screen.blit(Mech_Img,(0,MechPos)) #Draw a blue mech
        Screen.blit(MechImg,(0,MechPos))
        Screen.blit(EMech_Img,(screen_width-EMechImg.get_width(),MechPos)) #Draw a red mech
        Screen.blit(EMechImg,(screen_width-EMechImg.get_width(),MechPos))
        Img =  pygame.transform.scale(BlastImg, (int(MechSize/10)*2, int(MechSize/10))) #Draw a blue blast 
        Screen.blit(Img,(int(screen_width/3.5),MechPos+int(MechSize/2)))
        Img =  pygame.transform.scale(EBlastImg, (int(MechSize/10)*2, int(MechSize/10)))  #Draw a red blast
        Screen.blit(Img,(screen_width-int(screen_width/3),MechPos+int(MechSize/2)))
        Img = pygame.transform.scale(Explosion1[25],(int(MechSize/10)*2,int(MechSize/10)*2)) #Draw an explosion
        Screen.blit(Img,(int(screen_width/1.97),MechPos+int(MechSize/2.2)))
        Img = pygame.transform.scale(Explosion1[24],(int(MechSize/10)*2,int(MechSize/10)*2)) #Draw an explosion
        Screen.blit(Img,(int(screen_width/2.03),MechPos+int(MechSize/2.2)))
        pygame.display.update() 
    while playing and pygame.mixer.music.get_pos() < 30500:
        playing = wait(1/60)
        MechSize = int(screen_height/4)
        MechPos = int(screen_height*.6)
        Screen.blit(Mech_Img,(0,MechPos)) #Draw a blue mech
        Screen.blit(MechImg,(0,MechPos))
        Screen.blit(EMech_Img,(screen_width-EMechImg.get_width(),MechPos)) #Draw a red mech
        Screen.blit(EMechImg,(screen_width-EMechImg.get_width(),MechPos))
        Img =  pygame.transform.scale(BlastImg, (int(MechSize/10)*2, int(MechSize/10))) #Draw a blue blast 
        Screen.blit(Img,(int(screen_width/3.5),MechPos+int(MechSize/2)))
        Img =  pygame.transform.scale(EBlastImg, (int(MechSize/10)*2, int(MechSize/10)))  #Draw a red blast
        Screen.blit(Img,(screen_width-int(screen_width/3),MechPos+int(MechSize/2)))
        Img = pygame.transform.scale(Explosion1[25],(int(MechSize/10)*2,int(MechSize/10)*2)) #Draw an explosion
        Screen.blit(Img,(int(screen_width/1.97),MechPos+int(MechSize/2.2)))
        Img = pygame.transform.scale(Explosion1[24],(int(MechSize/10)*2,int(MechSize/10)*2)) #Draw an explosion
        Screen.blit(Img,(int(screen_width/2.03),MechPos+int(MechSize/2.2)))
        myfont = pygame.font.SysFont('Arial Black', int(75*(screen_height/600)),True) #Set a font to arial black size 75 and bold
        textsurface1 = myfont.render('Button ', False, Cyan) #Make a text 'Button ' using that font with the color Cyan
        textsurface2 = myfont.render('Blasters', False, Red) #Make a text 'Blasters' using that font with the color Red
        Screen.blit(textsurface1,(int(screen_width/2)-textsurface1.get_width(),int(screen_height/25))) #Draw the texts on the screen
        Screen.blit(textsurface2,(int(screen_width/2),int(screen_height/25)))
        pygame.display.update() 
    while playing and pygame.mixer.music.get_busy():
        playing = wait(1/60)
        Screen.fill(Black) #Make the screen black
        pygame.display.update()
    pygame.mixer.music.stop() #Stop the intro music
    
class MenuButton():
    def __init__(self,y,text,function):
        self.y = y
        self.text = text
        self.function = function
    def update(self):
        global screen_height, screen_width
        mouse = pygame.mouse.get_pos()
        optionfont = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True) #Set a font to arial black size 50 and bold
        back = optionfont.render(self.text, False, Red)
        front = optionfont.render(self.text, False, Cyan)
        if screen_width/3.5 < mouse[0] < (screen_width/3.5)+front.get_width() and screen_height*self.y < mouse[1] < screen_height*self.y+front.get_height(): #If the mouse is hovering over this button switch its colors else draw it normally
            back = optionfont.render(self.text, False, Cyan)
            front = optionfont.render(self.text, False, Red)
            global Cursor, Cursor1
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.function()
        Screen.blit(back,(screen_width/3.5+screen_width*0.004,screen_height*self.y+screen_height*.004))
        Screen.blit(front,(screen_width/3.5,screen_height*self.y))
        
def ControllerHelp(joystick):
    joystick.init()
    y = joystick.get_axis(0)
    x = joystick.get_axis(1)
    if round(x) == 1:
        pygame.mouse.set_pos(pygame.mouse.get_pos()[0]-10,pygame.mouse.get_pos()[1])
    elif round(x) == -1:
        pygame.mouse.set_pos(pygame.mouse.get_pos()[0]+10,pygame.mouse.get_pos()[1])
    if round(y) == 1:
        pygame.mouse.set_pos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+10)
    elif round(y) == -1:
        pygame.mouse.set_pos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-10)
    joystick.quit()
        
def StartMultiplayer():
    global Screen, aspect_ratio, screen_width, screen_height
    Resize(Multiplayer.ChoosePlayers(Screen,aspect_ratio,screen_width,screen_height))
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    
def MenuLoop(): #The function that runs the main menu
    global CheatCodeIndex, Cursor, Cursor0
    CheatCodeIndex = 0
    inMenu = True #If it should stay in the menu
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    Buttons = []
    Buttons.append(MenuButton(.35,"singleplayer",ChoosePlayer))
    Buttons.append(MenuButton(.48,"multiplayer",StartMultiplayer))
    Buttons.append(MenuButton(.6,"settings",SettingsLoop))
    Buttons.append(MenuButton(.73,"exit",kill))
    while inMenu:
        Screen.fill(Black) #Blacks out the screen
        titlefont = pygame.font.SysFont('Arial Black', int(75*(screen_height/600)),True) #Set a font to arial black size 75 and bold
        title1 = titlefont.render('Button ', False, Cyan) #Make a text 'Button ' using that font with the color Cyan
        title2 = titlefont.render('Blasters', False, Red) #Make a text 'Blasters' using that font with the color Red
        Screen.blit(title1,(int(screen_width/2)-title1.get_width(),int(screen_height/25))) #Draw the texts on the screen
        Screen.blit(title2,(int(screen_width/2),int(screen_height/25)))
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        for button in Buttons:
            button.update()
        Screen.blit(Cursor, pygame.mouse.get_pos())
        pygame.display.update() 
        if Controls[0] != "mouse":
            ControllerHelp(Controls[0])
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            global Debug
            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_TAB:
                    #Controls[0] = Controllers.GetController()
                global DebugCheatCode
                if event.key == Controls[DebugCheatCode[CheatCodeIndex]]:
                    CheatCodeIndex +=1
                    pygame.mixer.Sound.play(ding)
                    if CheatCodeIndex == len(DebugCheatCode):
                        Debug = not Debug
                        CheatCodeIndex = 0
                        pygame.mixer.Sound.play(unlocked)
                else:
                    if CheatCodeIndex > 0:
                        CheatCodeIndex = 0
                        pygame.mixer.Sound.play(wrong)
        Clock.tick(30)
        
def ChoosePlayer():
    Players = Player.GetPlayers() #Gets a list of saved players
    Buttons = [] #A list of buttons on the screens
    i = 1
    for p in Players: #Creates a player button for every saved player and adds it to the list of buttons
        Buttons.append(PlayerButton(.4,i/7.5,p))
        i += 1
    if len(Buttons) < 5: #If there are less than 5 saved players
        Buttons.append(NewPlayer()) #Add a new player button to the list of buttons
    choosing = True
    global Cursor, Cursor0
    while choosing:
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        Screen.fill(Black) #Blanks the screen
        for button in Buttons: #Have all of the buttons run their update method
            button.update()
        Screen.blit(Cursor, pygame.mouse.get_pos())
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE: #If the escape key is being pressed
                    MenuLoop() #Go back to the main menu
        Clock.tick(30)
        
def UpgradeMenu():        
    global PlayerData
    Size = Upgrade.Main(Screen,PlayerData['Name'],MechImg,Mech_Img,aspect_ratio,screen_width,screen_height)
    try:
        PlayerData = Player.LoadPlayer(PlayerData['Name'])
        Resize(Size)
    except:
        print("WARNING:",PlayerData['Name'],"deleted!")
        Resize(Size)
        wait(.25)
        MenuLoop()
    
def ChooseLevel():
    global CheatCodeIndex, Cursor, Cursor0
    CheatCodeIndex = 0
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    Screen.fill(Black)
    Levels = []
    for row in range(10): #For each of 10 rows
        for column in range(10): #For each of 10 columns
            pygame.display.update()
            Levels.append(LevelButton(row,column,PlayerData['Unlocked'])) #Add a level button to the list of levels with the current row, column, and highest level the player has unlocked
    Levels.append(TextButton(.25,.85,"Main Menu",MenuLoop))
    Levels.append(TextButton(.5,.85,"Upgrades",UpgradeMenu))
    choosing = True
    while choosing:
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        Screen.fill(Black)
        events = []
        for event in pygame.event.get():
            events.append(event)
        for button in Levels: #Has all of the level buttons run their update method
            button.update(events)
        for event in events: #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            global LevelSelect
            if event.type == pygame.KEYDOWN:
                global LevelSelectCheatCode
                if event.key == Controls[LevelSelectCheatCode[CheatCodeIndex]]:
                    CheatCodeIndex +=1
                    pygame.mixer.Sound.play(ding)
                    if CheatCodeIndex == len(LevelSelectCheatCode):
                        LevelSelect = not LevelSelect
                        CheatCodeIndex = 0
                        pygame.mixer.Sound.play(unlocked)
                else:
                    if CheatCodeIndex > 0:
                        CheatCodeIndex = 0
                        pygame.mixer.Sound.play(wrong)
        Screen.blit(Cursor, pygame.mouse.get_pos())
        pygame.display.update()
        Clock.tick(30)

def GameLoop(): #The function that runs the game
    ReloadCounter = 0
    ComputerReloadCounter = 0
    #Tells the function to use the following global variables instead of making new variables
    global Reloading
    global ComputerReloading
    global EnemyColor
    global ComputerFireSpeed
    global ComputerHealth
    global ComputerBlastSpeed
    global ComputerDmg
    global ComputerMoveSpeed
    global ComputerPosition
    global PlayerPosition
    global PlayerData
    global PlayerHealth
    global ComputerLevel
    global ShootLock
    global Regen
    global Follow
    #Reset the computer's stats
    ComputerHealth = 10
    ComputerDmg = 1
    ComputerFireSpeed = 1
    ComputerBlastSpeed = 1
    ComputerMoveSpeed = 1
    #Reset the player's health
    PlayerHealth = PlayerData['Health']
    #Reset mech positions
    ComputerPosition = .6
    PlayerPosition = .6
    pygame.mixer.music.load(Music[random.randint(0,len(Music)-1)]) #Load a random song from the music list
    #pygame.mixer.music.set_volume(Settings['Master']*Settings['Music'])
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the song 
    EnemyColor = Colors[random.randint(0,(len(Colors)-1))]
    Resize((screen_width,screen_height)) #Reload screen so that new enemy color is loaded
    ComputerReloadTime = 100/(ComputerFireSpeed*(random.randint(75,100)/100)) #The amount of time needed for the computer to reload
    Aggressive = randint(1,2) #Whether the computer is aggressive or not
    stats = 0
    for i in range(1,ComputerLevel):
        stats += i//5
    while stats > 0: #Gives the computer random stats based on its level
        rand = random.randint(1,int(5+(ComputerLevel/2)))
        if ComputerBlastSpeed < ComputerLevel/10: #If the computer's blast's speed is below the level cap
            if rand ==  1: #If the random number is four
                ComputerBlastSpeed += 1 #Increase its speed by one
                stats -= 1 #And subtract a stat point
        if ComputerDmg < ComputerLevel/4: #If the computer's damage is below the level cap
            if rand == 2:
                ComputerDmg += 1 #Increase its damage by one
                stats -= 1 #Use up a stat point
        if ComputerFireSpeed < ComputerLevel/5: #If the computer's shooting speed is below the level cap
            if rand == 3:
                ComputerFireSpeed += 1 #Increase its shooting speed by one
                stats -= 1
        if ComputerMoveSpeed < ComputerLevel/10:
            if rand == 4:
                ComputerMoveSpeed += 1
                stats -= 1
        if ComputerHealth < ComputerLevel**2: #If the computer's health is below the level cap
            if rand >= 5:
                ComputerHealth += 10 #Increase it by 10
                stats -= 1
        if not ComputerBlastSpeed < ComputerLevel/10 and not ComputerDmg < ComputerLevel/4 and not ComputerFireSpeed < ComputerLevel/5 and not ComputerMoveSpeed < ComputerLevel/10 and not ComputerHealth < ComputerLevel**2:
            break #If the computer has hit all level caps break the loop
    while not Close:
        if PlayerHealth < PlayerData['Health'] and Regen: #If Debug Regen is enable and the player has less than max health
            PlayerHealth += math.sqrt(PlayerData['Health'])/100 #Heal the player
        if ReloadCounter >= 100/PlayerData['FireSpeed']: #If the reload counter is more than the time needed to reload
            Reloading = False #Set reloading to false
            ReloadCounter = 0 #Reset the reload counter to 0
        elif Reloading == True: #Else as long as it is reloading
            ReloadCounter += 1 #Add 1 to the reload counter
        if ComputerReloadCounter >= ComputerReloadTime: #If the reload counter is more than the time needed to reload
            ComputerReloadCounter = 0 #Reset the reload counter to 0
            ComputerReloadTime = 100/(ComputerFireSpeed*(random.randint(75,100)/100)) #Reset reload time
            EBlasts.append(EBlast(ComputerBlastSpeed,ComputerDmg,EBlastImg)) #Create a blast with the speed of BlastSpeed dmg and size of BlastDmg and with the image of BlastImg
            pygame.mixer.Sound.play(lazer) #Play the lazer blast sound effect
        else: #Else as long as it is reloading
            ComputerReloadCounter += 1 #Add 1 to the reload counter
        rand = randint(1,25)
        if Aggressive == 1: #If the computer is aggressive
            if rand == 1: #If rand is 1 then move towards the player
                if PlayerPosition > ComputerPosition < .8:
                    ComputerPosition += ComputerMoveSpeed/1000
                elif PlayerPosition < ComputerPosition > .1:
                    ComputerPosition -= ComputerMoveSpeed/1000
        else:
            if rand == 1: #If rand is 1 then move away from the player
                if PlayerPosition > ComputerPosition > .1:
                    ComputerPosition -= ComputerMoveSpeed/1000
                elif PlayerPosition < ComputerPosition < .8:
                    ComputerPosition += ComputerMoveSpeed/1000
                else:
                    newrand = randint(1,2)
                    if newrand == 1 and ComputerPosition > .1:
                        ComputerPosition -= ComputerMoveSpeed/1000
                    elif newrand == 2 and ComputerPosition < .8:
                        ComputerPosition += ComputerMoveSpeed/1000
        if Follow: #If debug Follow is enabled
            if rand == 1: #If rand is 1 then move towards the computer
                if ComputerPosition > PlayerPosition < .8:
                    PlayerPosition += PlayerData['MoveSpeed']/1000
                elif ComputerPosition < PlayerPosition > .1:
                    PlayerPosition -= PlayerData['MoveSpeed']/1000
        rand = randint(ComputerLevel,250) #The computer's level determines the chance of gaining/dropping its aggressiveness
        if rand == 250: #If rand is 1000
            Aggressive = randint(1,2) #Possibly change the computer's strategy
        GameEventHandler() #Run the game event handler function
        DrawScreen() #Run the draw screen function
        if PlayerHealth < 1: #If the player's health is less than 1
            Blasts.clear() #Destroy all player blasts
            EBlasts.clear() #Destroy all enemy blasts
            Explosions.clear() #Destroy all explosions
            Lose()
        elif ComputerHealth < 1: #If the computer's health is less than 1
            Blasts.clear() #Destroy all player blasts
            EBlasts.clear() #Destroy all enemy blasts
            Explosions.clear() #Destroy all explosions
            Win()
        Clock.tick(100) #How many times this function will run per second
        
def GameEventHandler(): #Handles the events during the game
    global Reloading
    global PlayerPosition
    global PlayerData
    global ShootLock
    if ShootLock and not Reloading: #If Debug ShootLock is enabled and the player is not reloading
        Blasts.append(Blast(PlayerData['BlastSpeed'],PlayerData['Damage'],BlastImg)) #Create a blast with the speed of BlastSpeed dmg and size of BlastDmg and with the image of BlastImg
        pygame.mixer.Sound.play(lazer) #Play the lazer blast sound effect
        Reloading = True #Set reloading to true
    for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
        if event.type == pygame.QUIT: #If the user clicked the close button
            kill() #Close the window and stop the program
        if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
        if event.type == pygame.KEYDOWN: #If a key is being pressed
            if event.key == pygame.K_SPACE: #If that key is space
                if not Reloading: #If the mech is not reloading
                    Blasts.append(Blast(PlayerData['BlastSpeed'],PlayerData['Damage'],BlastImg)) #Create a blast with the speed of BlastSpeed dmg and size of BlastDmg and with the image of BlastImg
                    pygame.mixer.Sound.play(lazer) #Play the lazer blast sound effect
                    Reloading = True #Set reloading to true
            elif event.key == pygame.K_ESCAPE: #If the player presses escape
                Pause() #Pause the game
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and PlayerPosition > .1: #If the player presses the up arrow and their mech is not at the top
                PlayerPosition -= PlayerData['MoveSpeed']/1000 #Move their mech upward at their move speed
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and PlayerPosition < .8: #If the player presses the down arrow and their mech is not at the bottom
                PlayerPosition += PlayerData['MoveSpeed']/1000 #Move their mech downward at their move speed
            global Debug
            if Debug:
                if event.key == pygame.K_1:
                    ShootLock = not ShootLock
                elif event.key == pygame.K_2:
                    global Regen
                    Regen = not Regen
                elif event.key == pygame.K_3:
                    global Follow
                    Follow = not Follow
                    
def DrawScreen(): #Draws the screen
    Screen.fill(Black) #Resets the screen to black
    Screen.blit(Mech_Img,(0,screen_height*PlayerPosition))
    Screen.blit(EMech_Img,(screen_width-EMech_Img.get_width(),screen_height*ComputerPosition))
    for Blast in Blasts: #Draws all of the player blasts on the screen
        Blast.update()
    for Blast in EBlasts: #Draws all of the computer blasts on the screen
        Blast.update()
    Screen.blit(MechImg,(0,screen_height*PlayerPosition))
    Screen.blit(EMechImg,(screen_width-EMechImg.get_width(),screen_height*ComputerPosition))
    for Boom in Explosions: #Draws all of the explosions on the screen
        Boom.update()
    chealth = ComputerHealth
    hindex = 0
    while chealth > 0: #Draws the computer's health bar
        if chealth >= 500:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [screen_width,screen_height*.02,-screen_width*.3,screen_height*.05])
            chealth -= 500
        else:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [screen_width,screen_height*.02,-(((screen_width*.3)/500)*chealth),screen_height*.05])
            chealth -= chealth
        hindex += 1
    phealth = PlayerHealth
    hindex = 0
    while phealth > 0: #Draws the player's health bar
        if phealth >= 500:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [0,screen_height*.02,screen_width*.3,screen_height*.05])
            phealth -= 500
        else:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [0,screen_height*.02,((screen_width*.3)/500)*phealth,screen_height*.05])
            phealth -= phealth
        hindex += 1
    pygame.display.update() #Updates the screen so the user can see the new screen
    
def Pause():
    paused = True
    s = Screen.copy()
    global Cursor, Cursor0, Cursor1
    while paused:
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        si = pygame.transform.scale(s, (screen_width, screen_height))
        Screen.blit(si,(0,0))
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
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    #Return to the choose level menu
                    Blasts.clear()
                    EBlasts.clear()
                    Explosions.clear()
                    ChooseLevel()
        Screen.blit(back,(screen_width/2-back.get_width()/2,screen_height/2-back.get_height()))
        Screen.blit(menu,(screen_width/2-menu.get_width()/2,screen_height/2))
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE: #If that key is escape
                    paused = False #Unpause the game
        Screen.blit(Cursor,mouse)
        pygame.display.update()
        Clock.tick(30)
        
def Win(): #Displays the win screen
    s = Screen.copy()
    global PlayerData, ComputerLevel
    XP = randint(ComputerLevel//2,ComputerLevel) #The amount of xp gained
    if PlayerData['XP'] < 9801:
        PlayerData['XP'] += XP #Add the gained xp to the player's xp
    bonuschance = randint(ComputerLevel//PlayerData['Level'],100) #The chance the player will get points
    bonus = 0 #The amount of points gained
    while PlayerData['XP'] >= PlayerData['Level']**2 and PlayerData['Level'] < 100: #If the player can level up
        PlayerData['XP'] -= PlayerData['Level']**2 #Subtract the needed xp for the level up
        PlayerData['Level'] += 1 #Level up
        bonus += int(math.sqrt(PlayerData['Level'])) #Give points for leveling up
    if bonuschance == 100: #If the bonus chance is 100
        bonus += randint(1,PlayerData['Level']) #Add bonus points
    PlayerData['Points'] += bonus #Add the points to the player's
    if ComputerLevel == PlayerData['Unlocked']:
        PlayerData['Unlocked'] += 1
    Player.SavePlayer(PlayerData) #Save the player's stats
    waiting = True
    while waiting:
        si = pygame.transform.scale(s, (screen_width, screen_height))
        Screen.blit(si,(0,0))
        mainfont = pygame.font.SysFont('Arial Black', int(75*(screen_height/600)),True)
        text = mainfont.render('YOU WON!', False, Cyan) #Render the text 'YOU WON!' in Cyan
        Screen.blit(text,(screen_width//2-(text.get_width()//2),screen_height//2-(text.get_height()//2))) #Display the text
        statsfont = pygame.font.SysFont('Arial Black', int(60*(screen_height/600)),False)
        xptext = statsfont.render('+{} {}/{} Level:{}'.format(XP,PlayerData['XP'],PlayerData['Level']**2,PlayerData['Level']), False, Blue) #Display the amount of xp gained, the player's total xp, the amount of xp needed to level up, and the player's current level
        Screen.blit(xptext,(screen_width//2-(xptext.get_width()//2),screen_height//2+(text.get_height()//2)))
        if bonus > 0: #If the player got points
            pointstext = statsfont.render('Points +'+str(bonus),False,Blue) #Render the amount of points gained
            Screen.blit(pointstext,(screen_width//2-(pointstext.get_width()//2),screen_height//2+(text.get_height()//2)+xptext.get_height())) #Display how many points they gained
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE:
                    ChooseLevel() #Returns to the choose level menu
        Clock.tick(10)
    
def Lose(): #Displays the game over screen
    s = Screen.copy()
    global PlayerData, ComputerLevel
    XP = randint(0,ComputerLevel//10) #The amount of xp gained
    PlayerData['XP'] += XP #Add the gained xp to the player's xp
    bonuschance = randint(ComputerLevel//PlayerData['Level'],1000) #The chance the player will get points
    bonus = 0 #The amount of points gained
    while PlayerData['XP'] >= PlayerData['Level']**2 and PlayerData['Level'] < 100: #If the player can level up
        PlayerData['XP'] -= PlayerData['Level']**2 #Subtract the needed xp for the level up
        PlayerData['Level'] += 1 #Level up
        bonus += int(math.sqrt(PlayerData['Level'])) #Give points for leveling up
    if bonuschance == 1000: #If the bonus chance is 1000
        bonus += randint(1,PlayerData['Level']) #Add bonus points
    PlayerData['Points'] += bonus #Add the points to the player's
    Player.SavePlayer(PlayerData) #Save the player's stats
    waiting = True
    while waiting:
        si = pygame.transform.scale(s, (screen_width, screen_height))
        Screen.blit(si,(0,0))
        mainfont = pygame.font.SysFont('Arial Black', int(75*(screen_height/600)),True)
        text = mainfont.render('GAME OVER', False, Red) #Render the text 'GAME OVER' in Red
        Screen.blit(text,(screen_width//2-(text.get_width()//2),screen_height//2-(text.get_height()//2))) #Display the text
        statsfont = pygame.font.SysFont('Arial Black', int(60*(screen_height/600)),False)
        xptext = statsfont.render('+{} {}/{} Level:{}'.format(XP,PlayerData['XP'],PlayerData['Level']**2,PlayerData['Level']), False, Blue) #Display the amount of xp gained, the player's total xp, the amount of xp needed to level up, and the player's current level
        Screen.blit(xptext,(screen_width//2-(xptext.get_width()//2),screen_height//2+(text.get_height()//2)))
        if bonus > 0: #If the player got points
            pointstext = statsfont.render('Points +'+str(bonus),False,Blue) #Render the amount of points gained
            Screen.blit(pointstext,(screen_width//2-(pointstext.get_width()//2),screen_height//2+(text.get_height()//2)+xptext.get_height())) #Display how many points they gained
        pygame.display.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE:
                    ChooseLevel() #Returns to the choose level menu
        Clock.tick(10)
        
def SettingsLoop():
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    inSettings = True
    arrow0 = pygame.image.load(Directory+'\Images\Arrow0.png')
    arrow1 = pygame.image.load(Directory+'\Images\Arrow1.png')
    while inSettings:
        global screen_height, screen_width, Cursor, Cursor0, Cursor1
        Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25)))
        mouse = pygame.mouse.get_pos()
        Screen.fill(Black) #Blacks out the screen
        optionfont = pygame.font.SysFont('Arial Black', int(30*(screen_height/600)),True) #Set a font to arial black size 30 and bold
        masterfront = optionfont.render("Master Volume", False, Cyan)
        musicfront = optionfont.render("Music Volume", False, Cyan)
        effectfront = optionfont.render("Effect Volume", False, Cyan)
        backback = optionfont.render("Back", False, Red)
        backfront = optionfont.render("Back", False, Cyan)
        numberfont = pygame.font.SysFont('Arial Black', int(50*(screen_height/600)),True) #Set a font to arial black size 50 and bold
        masternumber = numberfont.render(str(Settings['Master']),False,Cyan)
        musicnumber = numberfont.render(str(Settings['Music']),False,Cyan)
        effectnumber = numberfont.render(str(Settings['Effects']),False,Cyan)
        #If the mouse is hovering over a button switch its colors else draw it normally and check if it is being pressed
        #Volume downs
        if screen_width*.6 < mouse[0] < screen_width*.7 and screen_height*.2 < mouse[1] < screen_height*.3:
            img = arrow1
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.6,screen_height*.2))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    Settings['Master'] = change_volume(Settings['Master'], -1)
                    update_volume()
        else:
            img = arrow0
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.6,screen_height*.2))
        if screen_width*.8 < mouse[0] < screen_width*.9 and screen_height*.2 < mouse[1] < screen_height*.3:
            img = arrow1
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.8,screen_height*.2))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    Settings['Master'] = change_volume(Settings['Master'], +1)
                    update_volume()
        else:
            img = arrow0
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.8,screen_height*.2)) 
        if screen_width*.6 < mouse[0] < screen_width*.7 and screen_height*.3 < mouse[1] < screen_height*.4:
            img = arrow1
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.6,screen_height*.3))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    Settings['Music'] = change_volume(Settings['Music'], -1)
                    update_volume()
        else:
            img = arrow0
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.6,screen_height*.3))
        if screen_width*.8 < mouse[0] < screen_width*.9 and screen_height*.3 < mouse[1] < screen_height*.4:
            img = arrow1
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.8,screen_height*.3))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    Settings['Music'] = change_volume(Settings['Music'], +1)
                    update_volume()
        else:
            img = arrow0
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.8,screen_height*.3)) 
        if screen_width*.6 < mouse[0] < screen_width*.7 and screen_height*.4 < mouse[1] < screen_height*.5:
            img = arrow1
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.6,screen_height*.4))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    Settings['Effects'] = change_volume(Settings['Effects'], -1)
                    update_volume()
        else:
            img = arrow0
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.6,screen_height*.4))
        if screen_width*.8 < mouse[0] < screen_width*.9 and screen_height*.4 < mouse[1] < screen_height*.5:
            img = arrow1
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.8,screen_height*.4))
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    Settings['Effects'] = change_volume(Settings['Effects'], 1)
                    update_volume()
        else:
            img = arrow0
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (int(screen_height*.1),int(screen_height*.1)))
            Screen.blit(img,(screen_width*.8,screen_height*.4)) 
        if screen_width/10 < mouse[0] < (screen_width/10)+backfront.get_width() and screen_height*.9 < mouse[1] < screen_height*.9+backfront.get_height(): #If the mouse is hovering over this button switch its colors else draw it normally
            backback = optionfont.render("Back", False, Cyan)
            backfront = optionfont.render("Back", False, Red)
            Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    MenuLoop()
        Screen.blit(backback,(screen_width*.1+screen_width*.004,screen_height*.9+screen_height*.004))
        Screen.blit(backfront,(screen_width*.1,screen_height*.9))
        Screen.blit(masterfront,(screen_width*.2,screen_height*.2))
        Screen.blit(musicfront,(screen_width*.2,screen_height*.3))
        Screen.blit(effectfront,(screen_width*.2,screen_height*.4))
        Screen.blit(masternumber,(screen_width*.68,screen_height*.2))
        Screen.blit(musicnumber,(screen_width*.68,screen_height*.3))
        Screen.blit(effectnumber,(screen_width*.68,screen_height*.4))
        Screen.blit(Cursor, pygame.mouse.get_pos())
        pygame.display.update() 
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.VIDEORESIZE:
                Resize(event.size)
        Clock.tick(25)
    
update_volume()
Intro()
MenuLoop()
