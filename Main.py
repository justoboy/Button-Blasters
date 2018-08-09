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
try:
    import pygame
except ModuleNotFoundError:
    try:
        from pip._internal import main
        main(['install','pygame'])
        import pygame
    except:
        print("Could not install the required pygame module!")
        print("You must install pygame before you can play this game")
import Upgrade
import Multiplayer

Directory = os.getcwd() #Gets the directory this script is in
pygame.init()
pygame.font.init()
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
Icon = pygame.image.load(Directory+'\Images\Icon.png') #Loads the icon for the game window
pygame.display.set_icon(Icon) #Sets the game window icon
MechImg = pygame.image.load(Directory+'\Images\Mech.png') #Loads the players mech image
MechImg = pygame.transform.scale(MechImg, (150, 150)) #Changes the image's size
EMechImg = pygame.image.load(Directory+'\Images\EMech.png') #Loads the enemy's mech image
EMechImg = pygame.transform.scale(EMechImg, (150, 150)) #Changes its size
BlastImg = pygame.image.load(Directory+'\Images\Blast.png') #Loads the player's energy blast image
EBlastImg = pygame.image.load(Directory+'\Images\EBlast.png') #Loads the enemy's energy blast image
Explosion1 = [] #List of explosion frames
Explosion2 = [] #List of explosion frames
for i in range(32): #Loads explosion images(frames) into Explosion1
    Explosion1.append(pygame.image.load(Directory+'\Images\Explosion1\\frame_{}.png'.format(i)))
for i in range(16):#Loads explosion images(frames) into Explosion2
    Explosion2.append(pygame.image.load(Directory+'\Images\Explosion2\\frame_{}.png'.format(i)))
    Explosion2.append(pygame.image.load(Directory+'\Images\Explosion2\\frame_{}.png'.format(i)))
lazer = pygame.mixer.Sound(Directory+'\Sounds\Effects\\151022__bubaproducer__laser-shot-silenced.wav') #Loads the lazer sound effect
Screen = pygame.display.set_mode((screen_width, screen_height)) #Create the game window
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
EnemyColor = Black #The background color of the computers mech
ComputerLevel = 1 #The difficulty of the computer
ComputerHealth = 10 #The health of the computer
ComputerDmg = 1 #The damage the computer deals
ComputerFireSpeed = 1 #How many times the computer can shoot per second
ComputerBlastSpeed = 1 #The speed of the computers blasts
ComputerMoveSpeed = 1 #How fast the computer can move up and down
ComputerPosition = 400 #The current position of the computer
PlayerPosition = 400 #The current position of the player
PlayerData = {} #The stats of the loaded player
PlayerHealth = 10 #The current health of the player


class Blast: #The class for the player's energy blasts
    def __init__(self,speed,dmg,img):
        global PlayerPosition
        self.speed = speed #How fast the blast travels
        self.dmg = dmg #How much dmg it deals
        self.size = int(15*(1+(self.dmg/25))) #Calculates the size of the blast based on its damage
        self.x = 125-(self.size) #The x position of the blast
        self.y = (PlayerPosition+80)-(self.size/2) #The y position of the blast
        self.bmp = img
        self.img = pygame.transform.scale(self.bmp,(self.size*2,self.size)) #Sets the size of the image of the blast
    def __del__(self): #When the blast is deleted make an explosion at the blast's position
        Explosions.append(Boom((self.x+self.size),self.y,self.size))
    def update(self): #Draws the blast on the screen and runs its logic
        self.x += math.sqrt(self.speed)
        global ComputerPosition
        if self.x > screen_width-(100+(self.size*2)) and self.y+self.size >= ComputerPosition+15 >= (self.y-80): #If the blast hits the computers mech make it explode and deal damage to the computer
            global ComputerHealth
            ComputerHealth -= self.dmg
            Blasts.remove(self)
        elif self.x > screen_width-(35+(self.size*2)) and self.y+self.size >= ComputerPosition+15 >= (self.y-100):
            ComputerHealth -= self.dmg
            Blasts.remove(self)
        elif self.x > screen_width: #Else if the blast is off the screen destroy it
            Blasts.remove(self) 
        for blast in EBlasts: #Iterate over all of the enemy blasts
            if self.x+(self.size*2) >= blast.x and self.y+self.size >= blast.y >= (self.y-blast.size): #If the blast is touching an enemy blast
                if blast.dmg > 0 and self.dmg > 0: #If both blasts have more than 0 dmg left
                    mydmg = self.dmg
                    yourdmg = blast.dmg
                    self.dmg -= yourdmg #Decrease their dmg by each other's dmg
                    blast.dmg -= mydmg
                    if blast.dmg > 0: #If the enemy blast's dmg is more than 0 update its image size
                        blast.size = int(15*(1+(blast.dmg/25)))
                        blast.img_update()
                    else: #Otherwise destroy it
                        EBlasts.remove(blast)
                    if self.dmg > 0: #If this blast's dmg is more than 0 update its image size
                        self.size = int(15*(1+(self.dmg/25)))
                        self.img = pygame.transform.scale(self.bmp,(self.size*2,self.size))
                    else: #Otherwise destroy it
                        if self in Blasts:
                            Blasts.remove(self)
        Screen.blit(self.img,(int(self.x),self.y)) #Draw the blast 
        
class EBlast: #The class for the player's energy blasts
    def __init__(self,speed,dmg,img):
        self.speed = speed #How fast the blast travels
        self.dmg = dmg #How much dmg it deals
        self.size = int(15*(1+(self.dmg/25))) #The base size of the blasts is 25 and is bigger the more dmg it deals
        self.x = (screen_width-125)+(self.size) #The x position of the blast
        self.y = (ComputerPosition+80)-(self.size/2) #The y position of the blast
        self.bmp = img
        self.img = pygame.transform.scale(self.bmp,(self.size*2,self.size)) #Sets the size of the image of the blast
    def __del__(self): #When the blast is deleted make an explosion at the blast's position
        Explosions.append(Boom(self.x,self.y,self.size))
    def img_update(self):
        self.img = pygame.transform.scale(self.bmp,(self.size*2,self.size)) #Sets the size of the image of the blast
    def update(self): #Draws the blast on the screen and runs its logic
        self.x -= math.sqrt(self.speed)
        if self.x < 100 and self.y+self.size >= PlayerPosition+15 >= (self.y-80): #If the blast hits the players mech make it explode and deal dmg to the player
            global PlayerHealth
            PlayerHealth -= self.dmg
            EBlasts.remove(self)
        elif self.x < 35 and self.y+self.size >= PlayerPosition+15 >= (self.y-100):
            PlayerHealth -= self.dmg
            EBlasts.remove(self)
        elif self.x < 0-self.size*2: #Else if the blast is off the screen destroy it
            if self in EBlasts:
                EBlasts.remove(self)
        Screen.blit(self.img,(int(self.x),self.y)) #Draw the blast
    
class Boom(): #The class for explosions
    def __init__(self,x,y,size):
        if random.randint(1,2) == 1: #Picks a random image list for the explosion so that explosions don't all look the same
            self.explosion = Explosion1
        else:
            self.explosion = Explosion2
        self.frame = 0 #Which frame the explosion is on
        self.size = int(size*1.5) #The size of the explosion
        self.x = x +((size-self.size)//4) #The x position of the explosion
        self.y = y+((size-self.size)//2) #The y position of the explosion
    def update(self): #Draws the explosion on the screen and deletes it when its animation completes
        img = pygame.transform.scale(self.explosion[int(self.frame)], (self.size, self.size)) #Changes the explosion frame image size to the size of the explosion 
        Screen.blit(img,(self.x,self.y)) #Draws the explosion
        self.frame += 0.5 #Skips to the next frame once every other run of this function
        if self.frame > 30: #If it has reached the end of the animation then delete this explosion
            Explosions.pop(0)
            
class LevelButton():
    def __init__(self,row,column,unlocked):
        self.row = row
        self.column = column
        self.level = (column+1)+(10*row)
        self.unlocked = (unlocked>=self.level)
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        myfont = pygame.font.SysFont('Arial Black', 25,True) #Set a font to arial black size 75 and bold
        if self.unlocked:
            textsurface = myfont.render(str(self.level), False, Cyan, Black) #Make a text 'Button' using that font with the color Cyan and a black background
        else:
            textsurface = myfont.render(str(self.level), False, Red) #Make a text 'Button' using that font with the color Red
        if (50*self.column)+125 <= mouse[0] <= (50*self.column)+150 and 50*self.row <= mouse[1] <= (50*self.row)+25 and self.unlocked:
            textsurface = myfont.render(str(self.level), False, Cyan, Red) #Make a text 'Button' using that font with the color Cyan and a red background
            if click[0] == 1: #If the player clicks this button
                global ComputerLevel
                ComputerLevel = self.level #Set the computers level to the same as the button's
                GameLoop() #Start the game
        Screen.blit(textsurface,((50*self.column)+125,50*self.row)) #Draw the texts on the screen
                
class PlayerButton():
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
    def update(self):
        myfont = pygame.font.SysFont('Arial Black', 50,True) #Set a font to arial black size 50 and bold
        player = myfont.render(self.name, False, DarkOrange, Black) #Show a button with the text of the player's name
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= mouse[0] <= self.x+player.get_width() and self.y <= mouse[1] <= self.y+player.get_height(): #If the user is hovering over this button
            player = myfont.render(self.name, False, DarkOrange, Orange) #Add an orange background to the button
            if click[0] == 1: #If the user clicks
                global PlayerData
                PlayerData = Player.LoadPlayer(self.name) #Load the player data of the name of this button
                ChooseLevel() #Open the choose level menu
        Screen.blit(player,(self.x,self.y))
                
class NewPlayer(): #A button that creates a new player
    def update(self):
        myfont = pygame.font.SysFont('Arial Black', 50,True) #Set a font to arial black size 50 and bold
        text = myfont.render("New Player", False, DarkOrange, Black)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 200 <= mouse[0] <= 200+text.get_width() and 500 <= mouse[1] <= 500+text.get_height(): #If the mouse is hovering over the button
            text = myfont.render("New Player", False, DarkOrange, Orange) #Give it an orange background
            if click[0] == 1: #If the player clicks
                typing = True
                newname = "" #The name of the new player
                while typing:
                    Screen.fill(Black) #Makes the screen blank
                    pygame.draw.line(Screen, White, (100,350), (700,350), 1) #Draws a white line across the screen
                    text = myfont.render(newname, False, White) #Renders a text that displays the name of the new player
                    Screen.blit(text,(400-(text.get_width()//2),275)) #Draws that text on the white line
                    pygame.display.update() #Refreshes the screen
                    for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
                        if event.type == pygame.QUIT: #If the user clicked the close button
                            kill() #Close the window and stop the program
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
                                
                    Clock.tick(25)
        Screen.blit(text,(200,500))
        pygame.display.update()
        
class TextButton(): #Exits to the main menu from the choose level screen
    def __init__(self,x,y,text,function):
        self.x = x
        self.y = y
        self.text = text
        self.function = function
    def update(self):
        myfont = pygame.font.SysFont('Arial Black', 25,True) #Set a font to arial black size 25 and bold
        player = myfont.render(self.text, False, DarkOrange, Black) #Show a button with the text of the player's name
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= mouse[0] <= self.x+player.get_width() and self.y <= mouse[1] <= self.y+player.get_height(): #If the user is hovering over this button
            player = myfont.render(self.text, False, DarkOrange, Orange) #Add an orange background to the button
            if click[0] == 1: #If the user clicks
                wait(.25)
                self.function() #Trigger the button's function
        Screen.blit(player,(self.x,self.y))
                
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
    if wait(3.75): #If the player does not hit space while waiting
        pygame.draw.rect(Screen, Blue, [0,425,100,70]) #Draws the player's mech
        pygame.draw.polygon(Screen, Blue, ((0,490),(50,490),(30,510),(0,510)))
        Screen.blit(MechImg,(0,400)) #Draw a blue mech
        pygame.display.update()
        if wait(6.75):
            pygame.draw.rect(Screen, DarkRed, [screen_width-100,425,100,70]) #Draws the computer's mech
            pygame.draw.polygon(Screen, DarkRed, ((screen_width,490),(screen_width-50,490),(screen_width-30,510),(screen_width,510)))
            Screen.blit(EMechImg,(screen_width-150,400)) #Draw a red mech
            pygame.display.update() 
            if wait(4):
                Img =  pygame.transform.scale(BlastImg, (70, 35)) #Draw a blue blast 
                Screen.blit(Img,(225,462))
                Img =  pygame.transform.scale(EBlastImg, (70, 35))  #Draw a red blast
                Screen.blit(Img,(screen_width-200,462))
                Img = pygame.transform.scale(Explosion1[25],(52,52)) #Draw an explosion
                Screen.blit(Img,(350,453))
                Img = pygame.transform.scale(Explosion1[24],(52,52)) #Draw an explosion
                Screen.blit(Img,(375,453))
                pygame.display.update() 
                if wait(3.5):
                    myfont = pygame.font.SysFont('Arial Black', 75,True) #Set a font to arial black size 75 and bold
                    textsurface1 = myfont.render('Button ', False, Cyan) #Make a text 'Button ' using that font with the color Cyan
                    textsurface2 = myfont.render('Blasters', False, Red) #Make a text 'Blasters' using that font with the color Red
                    Screen.blit(textsurface1,(25,50)) #Draw the texts on the screen
                    Screen.blit(textsurface2,(375,50))
                    pygame.display.update() 
                    if wait(10.25):
                        Screen.fill(Black) #Make the screen black
                        pygame.display.update() 
                        wait(7)
    pygame.mixer.music.stop() #Stop the intro music
    
def MenuLoop(): #The function that runs the main menu
    inMenu = True #If it should stay in the menu
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    while inMenu:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        Screen.fill(Black) #Blacks out the screen
        titlefont = pygame.font.SysFont('Arial Black', 75,True) #Set a font to arial black size 75 and bold
        title1 = titlefont.render('Button ', False, Cyan) #Make a text 'Button ' using that font with the color Cyan
        title2 = titlefont.render('Blasters', False, Red) #Make a text 'Blasters' using that font with the color Red
        optionfont = pygame.font.SysFont('Arial Black', 50,True) #Set a font to arial black size 50 and bold
        if 175 < mouse[0] < 570 and 268 < mouse[1] < 320: #If the mouse is hovering over the singleplayer button switch its colors else draw it normally
            singleback = optionfont.render("singleplayer", False, Cyan)
            singlefront = optionfont.render("singleplayer", False, Red)
            if click[0] == 1:
                ChoosePlayer()
        else:
            singleback = optionfont.render("singleplayer", False, Red)
            singlefront = optionfont.render("singleplayer", False, Cyan)
        if 175 < mouse[0] < 540 and 343 < mouse[1] < 395: #If the mouse is hovering over the multiplayer button switch its colors else draw it normally
            multiback = optionfont.render("multiplayer", False, Cyan)
            multifront = optionfont.render("multiplayer", False, Red)
            if click[0] == 1:
                Multiplayer.ChoosePlayers(Screen)
                pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
                pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
        else:
            multiback = optionfont.render("multiplayer", False, Red)
            multifront = optionfont.render("multiplayer", False, Cyan)
        if 175 < mouse[0] < 460 and 418 < mouse[1] < 470: #If the mouse is hovering over the settings button switch its colors else draw it normally
            settingsback = optionfont.render("settings", False, Cyan)
            settingsfront = optionfont.render("settings", False, Red)
            if click[0] == 1:
                SettingsLoop()
        else:
            settingsback = optionfont.render("settings", False, Red)
            settingsfront = optionfont.render("settings", False, Cyan)
        if 175 < mouse[0] < 350 and 493 < mouse[1] < 545: #If the mouse is hovering over the settings button switch its colors else draw it normally
            exitback = optionfont.render("exit", False, Cyan)
            exitfront = optionfont.render("exit", False, Red)
            if click[0] == 1:
                kill()
        else:
            exitback = optionfont.render("exit", False, Red)
            exitfront = optionfont.render("exit", False, Cyan)
        Screen.blit(title1,(25,50)) #Draw the texts on the screen
        Screen.blit(title2,(375,50))
        Screen.blit(singleback,(202,254))
        Screen.blit(singlefront,(200,250))
        Screen.blit(multiback,(202,329))
        Screen.blit(multifront,(200,325))
        Screen.blit(settingsback,(202,404))
        Screen.blit(settingsfront,(200,400))
        Screen.blit(exitback,(202,479))
        Screen.blit(exitfront,(200,475))
        pygame.display.update() 
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
        Clock.tick(30)
        
def ChoosePlayer():
    Screen.fill(Black) #Blanks the screen
    pygame.display.update()
    Players = Player.GetPlayers() #Gets a list of saved players
    Buttons = [] #A list of buttons on the screens
    i = 1
    for p in Players: #Creates a player button for every saved player and adds it to the list of buttons
        Buttons.append(PlayerButton(150,100*i,p))
        i += 1
    if len(Buttons) < 5: #If there are less than 5 saved players
        Buttons.append(NewPlayer()) #Add a new player button to the list of buttons
    choosing = True
    while choosing:
        for button in Buttons: #Have all of the buttons run their update method
            button.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE: #If the escape key is being pressed
                    MenuLoop() #Go back to the main menu
        Clock.tick(10)
        
def UpgradeMenu():        
    global PlayerData
    Upgrade.Main(Screen,PlayerData['Name'],MechImg)
    PlayerData = Player.LoadPlayer(PlayerData['Name'])
    
def ChooseLevel():
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    Screen.fill(Black)
    Levels = []
    for row in range(10): #For each of 10 rows
        for column in range(10): #For each of 10 columns
            pygame.display.update()
            Levels.append(LevelButton(row,column,PlayerData['Unlocked'])) #Add a level button to the list of levels with the current row, column, and highest level the player has unlocked
    Levels.append(TextButton(600,500,"Main Menu",MenuLoop))
    Levels.append(TextButton(400,500,"Upgrades",UpgradeMenu))
    choosing = True
    while choosing:
        Screen.fill(Black)
        for button in Levels: #Has all of the level buttons run their update method
            button.update()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
        pygame.display.update()
        Clock.tick(10)

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
    #Reset the computer's stats
    ComputerHealth = 10
    ComputerDmg = 1
    ComputerFireSpeed = 1
    ComputerBlastSpeed = 1
    ComputerMoveSpeed = 1
    #Reset the player's health
    PlayerHealth = PlayerData['Health']
    #Reset mech positions
    ComputerPosition = 400
    PlayerPosition = 400
    pygame.mixer.music.load(Music[random.randint(0,len(Music)-1)]) #Load a random song from the music list
    #pygame.mixer.music.set_volume(Settings['Master']*Settings['Music'])
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the song 
    EnemyColor = Colors[random.randint(0,(len(Colors)-1))]
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
                if PlayerPosition > ComputerPosition < screen_height-150:
                    ComputerPosition += ComputerMoveSpeed
                elif PlayerPosition < ComputerPosition > 0:
                    ComputerPosition -= ComputerMoveSpeed
        else:
            if rand == 1: #If rand is 1 then move away from the player
                if PlayerPosition > ComputerPosition > 0:
                    ComputerPosition -= ComputerMoveSpeed
                elif PlayerPosition < ComputerPosition < screen_height-150:
                    ComputerPosition += ComputerMoveSpeed
                else:
                    newrand = randint(1,2)
                    if newrand == 1 and ComputerPosition > 0:
                        ComputerPosition -= ComputerMoveSpeed
                    elif newrand == 2 and ComputerPosition < screen_height-150:
                        ComputerPosition -= ComputerMoveSpeed
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
    for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
        if event.type == pygame.QUIT: #If the user clicked the close button
            kill() #Close the window and stop the program
        if event.type == pygame.KEYDOWN: #If a key is being pressed
            if event.key == pygame.K_SPACE: #If that key is space
                if not Reloading: #If the mech is not reloading
                    Blasts.append(Blast(PlayerData['BlastSpeed'],PlayerData['Damage'],BlastImg)) #Create a blast with the speed of BlastSpeed dmg and size of BlastDmg and with the image of BlastImg
                    pygame.mixer.Sound.play(lazer) #Play the lazer blast sound effect
                    Reloading = True #Set reloading to true
            if event.key == pygame.K_ESCAPE: #If the player presses escape
                Pause() #Pause the game
            if event.key == pygame.K_UP and PlayerPosition > 0: #If the player presses the up arrow and their mech is not at the top
                PlayerPosition -= PlayerData['MoveSpeed'] #Move their mech upward at their move speed
            if event.key == pygame.K_DOWN and PlayerPosition < screen_height-150: #If the player presses the down arrow and their mech is not at the bottom
                PlayerPosition += PlayerData['MoveSpeed'] #Move their mech downward at their move speed
                    
def DrawScreen(): #Draws the screen
    Screen.fill(Black) #Resets the screen to black
    for Blast in Blasts: #Draws all of the player blasts on the screen
        Blast.update()
    for Blast in EBlasts: #Draws all of the computer blasts on the screen
        Blast.update()
    pygame.draw.rect(Screen, PlayerData['Color'], [0,PlayerPosition+25,100,70]) #Draws the player's mech
    pygame.draw.polygon(Screen, PlayerData['Color'], ((0,PlayerPosition+90),(50,PlayerPosition+90),(30,PlayerPosition+110),(0,PlayerPosition+110)))
    Screen.blit(MechImg,(0,PlayerPosition))
    pygame.draw.rect(Screen, EnemyColor, [screen_width-100,ComputerPosition+25,100,70]) #Draws the computer's mech
    pygame.draw.polygon(Screen, EnemyColor, ((screen_width,ComputerPosition+90),(screen_width-50,ComputerPosition+90),(screen_width-30,ComputerPosition+110),(screen_width,ComputerPosition+110)))
    Screen.blit(EMechImg,(screen_width-150,ComputerPosition))
    for Boom in Explosions: #Draws all of the explosions on the screen
        Boom.update()
    chealth = ComputerHealth
    hindex = 0
    while chealth > 0: #Draws the computer's health bar
        if chealth >= 500:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [screen_width-250,10,250,35])
            chealth -= 500
        else:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [screen_width-chealth//2,10,chealth//2,35])
            chealth -= chealth
        hindex += 1
    phealth = PlayerHealth
    hindex = 0
    while phealth > 0: #Draws the player's health bar
        if phealth >= 500:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [0,10,250,35])
            phealth -= 500
        else:
            pygame.draw.rect(Screen, HealthBarColors[hindex], [0,10,phealth//2,35])
            phealth -= phealth
        hindex += 1
    pygame.display.update() #Updates the screen so the user can see the new screen
    
def Pause():
    paused = True
    font = pygame.font.SysFont('Arial Black', 50,True) #Set a font to arial black size 50 and bold
    back = font.render("Back To Game", False, DarkOrange)
    menu = font.render("Exit To Menu", False, DarkOrange)
    Screen.blit(back,(200,250))
    Screen.blit(menu,(200,350))
    pygame.display.update()
    while paused:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 200 < mouse[0] < 200+back.get_width() and 270 < mouse[1] < 270+back.get_height(): #If the mouse is hovering over the back to game button
            if click[0] == 1: #If the player clicks
                paused = False #Unpause the game
        if 225 < mouse[0] < 225+menu.get_width() and 370 < mouse[1] < 370+menu.get_height(): #If the mouse is hovering over the menu button
            if click[0] == 1: #If the player clicks
                #Return to the choose level menu
                Blasts.clear()
                EBlasts.clear()
                Explosions.clear()
                wait(.25)
                ChooseLevel()
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE: #If that key is escape
                    paused = False #Unpause the game
        Clock.tick(10)
        
def Win(): #Displays the win screen
    global PlayerData
    global ComputerLevel
    mainfont = pygame.font.SysFont('Arial Black', 75,True)
    text = mainfont.render('YOU WON!', False, Cyan) #Render the text 'YOU WON!' in Cyan
    Screen.blit(text,(screen_width//2-(text.get_width()//2),screen_height//2-(text.get_height()//2))) #Display the text
    XP = randint(ComputerLevel//2,ComputerLevel) #The amount of xp gained
    PlayerData['XP'] += XP #Add the gained xp to the player's xp
    statsfont = pygame.font.SysFont('Arial Black', 60,False)
    bonuschance = randint(ComputerLevel//PlayerData['Level'],100) #The chance the player will get points
    bonus = 0 #The amount of points gained
    while PlayerData['XP'] >= PlayerData['Level']**2 and PlayerData['Level'] < 100: #If the player can level up
        PlayerData['XP'] -= PlayerData['Level']**2 #Subtract the needed xp for the level up
        PlayerData['Level'] += 1 #Level up
        bonus += int(math.sqrt(PlayerData['Level'])) #Give points for leveling up
    xptext = statsfont.render('+{} {}/{} Level:{}'.format(XP,PlayerData['XP'],PlayerData['Level']**2,PlayerData['Level']), False, Blue) #Display the amount of xp gained, the player's total xp, the amount of xp needed to level up, and the player's current level
    Screen.blit(xptext,(screen_width//2-(text.get_width()//2),screen_height//2+(text.get_height()//2)))
    if bonuschance == 100: #If the bonus chance is 100
        bonus += randint(1,PlayerData['Level']) #Add bonus points
    if bonus > 0: #If the player got points
        PlayerData['Points'] += bonus #Add the points to the player's
        pointstext = statsfont.render('Points +'+str(bonus),False,Blue) #Render the amount of points gained
        Screen.blit(pointstext,(screen_width//2-(text.get_width()//2),screen_height//2+(text.get_height()//2)+xptext.get_height())) #Display how many points they gained
    if ComputerLevel == PlayerData['Unlocked']:
        PlayerData['Unlocked'] += 1
    Player.SavePlayer(PlayerData) #Save the player's stats
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE:
                    ChooseLevel() #Returns to the choose level menu
        Clock.tick(10)
    
def Lose(): #Displays the game over screen
    global PlayerData
    global ComputerLevel
    mainfont = pygame.font.SysFont('Arial Black', 75,True)
    text = mainfont.render('GAME OVER', False, Red) #Render the text 'GAME OVER' in Red
    Screen.blit(text,(screen_width//2-(text.get_width()//2),screen_height//2-(text.get_height()//2))) #Display the text
    XP = randint(0,ComputerLevel//10) #The amount of xp gained
    PlayerData['XP'] += XP #Add the gained xp to the player's xp
    statsfont = pygame.font.SysFont('Arial Black', 60,False)
    bonuschance = randint(ComputerLevel//PlayerData['Level'],1000) #The chance the player will get points
    bonus = 0 #The amount of points gained
    while PlayerData['XP'] >= PlayerData['Level']**2 and PlayerData['Level'] < 100: #If the player can level up
        PlayerData['XP'] -= PlayerData['Level']**2 #Subtract the needed xp for the level up
        PlayerData['Level'] += 1 #Level up
        bonus += int(math.sqrt(PlayerData['Level'])) #Give points for leveling up
    xptext = statsfont.render('+{} {}/{} Level:{}'.format(XP,PlayerData['XP'],PlayerData['Level']**2,PlayerData['Level']), False, Blue) #Display the amount of xp gained, the player's total xp, the amount of xp needed to level up, and the player's current level
    Screen.blit(xptext,(screen_width//2-(text.get_width()//2),screen_height//2+(text.get_height()//2)))
    if bonuschance == 1000: #If the bonus chance is 1000
        bonus += randint(1,PlayerData['Level']) #Add bonus points
    if bonus > 0: #If the player got points
        PlayerData['Points'] += bonus #Add the points to the player's
        pointstext = statsfont.render('Points +'+str(bonus),False,Blue) #Render the amount of points gained
        Screen.blit(pointstext,(screen_width//2-(text.get_width()//2),screen_height//2+(text.get_height()//2)+xptext.get_height())) #Display how many points they gained
    Player.SavePlayer(PlayerData) #Save the player's stats
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
            if event.type == pygame.KEYDOWN: #If a key is being pressed
                if event.key == pygame.K_ESCAPE:
                    ChooseLevel() #Returns to the choose level menu
        Clock.tick(10)
        
def SettingsLoop():
    pygame.mixer.music.load(Directory+'\Sounds\Menu\Videogame2.wav') #Load the menu music
    pygame.mixer.music.play(loops=-1, start=0_0) #Play the menu music and make it loop indefinitely
    inSettings = True
    while inSettings:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        Screen.fill(Black) #Blacks out the screen
        optionfont = pygame.font.SysFont('Arial Black', 30,True) #Set a font to arial black size 30 and bold
        masterfront = optionfont.render("Master Volume", False, Cyan)
        musicfront = optionfont.render("Music Volume", False, Cyan)
        effectfront = optionfont.render("Effect Volume", False, Cyan)
        numberfont = pygame.font.SysFont('Arial Black', 50,True) #Set a font to arial black size 50 and bold
        masternumber = numberfont.render(str(Settings['Master']),False,Cyan)
        musicnumber = numberfont.render(str(Settings['Music']),False,Cyan)
        effectnumber = numberfont.render(str(Settings['Effects']),False,Cyan)
        #If the mouse is hovering over a button switch its colors else draw it normally and check if it is being pressed
        #Volume downs
        if 500 < mouse[0] < 550 and 250 < mouse[1] < 300:
            pygame.draw.polygon(Screen, Cyan, ((495,275),(553,245),(553,305)), 0) 
            pygame.draw.polygon(Screen, Red, ((500,275),(550,250),(550,300)), 0) 
            if click[0] == 1:
                Settings['Master'] = change_volume(Settings['Master'], -1)
                update_volume()
        else:
            pygame.draw.polygon(Screen, Red, ((495,275),(553,245),(553,305)), 0) 
            pygame.draw.polygon(Screen, Cyan, ((500,275),(550,250),(550,300)), 0) 
        if 500 < mouse[0] < 550 and 325 < mouse[1] < 375:
            pygame.draw.polygon(Screen, Cyan, ((495,350),(553,320),(553,380)), 0) 
            pygame.draw.polygon(Screen, Red, ((500,350),(550,325),(550,375)), 0)
            if click[0] == 1:
                Settings['Music'] = change_volume(Settings['Music'], -1)
                update_volume()
        else:
            pygame.draw.polygon(Screen, Red, ((495,350),(553,320),(553,380)), 0) 
            pygame.draw.polygon(Screen, Cyan, ((500,350),(550,325),(550,375)), 0) 
        if 500 < mouse[0] < 550 and 400 < mouse[1] < 450:
            pygame.draw.polygon(Screen, Cyan, ((495,425),(553,395),(553,455)), 0) 
            pygame.draw.polygon(Screen, Red, ((500,425),(550,400),(550,450)), 0)
            if click[0] == 1:
                Settings['Effects'] = change_volume(Settings['Effects'], -1)
                update_volume()
        else:
            pygame.draw.polygon(Screen, Red, ((495,425),(553,395),(553,455)), 0) 
            pygame.draw.polygon(Screen, Cyan, ((500,425),(550,400),(550,450)), 0)
        #Volume ups    
        if 675 < mouse[0] < 725 and 250 < mouse[1] < 300:
            pygame.draw.polygon(Screen, Cyan, ((725,275),(675,245),(675,305)), 0) 
            pygame.draw.polygon(Screen, Red, ((720,275),(678,250),(678,300)), 0) 
            if click[0] == 1:
                Settings['Master'] = change_volume(Settings['Master'], 1)
                update_volume()
        else:
            pygame.draw.polygon(Screen, Red, ((725,275),(675,245),(675,305)), 0) 
            pygame.draw.polygon(Screen, Cyan, ((720,275),(678,250),(678,300)), 0) 
        if 675 < mouse[0] < 725 and 325 < mouse[1] < 375:
            pygame.draw.polygon(Screen, Cyan, ((725,350),(675,320),(675,380)), 0) 
            pygame.draw.polygon(Screen, Red, ((720,350),(678,325),(678,375)), 0)
            if click[0] == 1:
                Settings['Music'] = change_volume(Settings['Music'], 1)
                update_volume()
        else:
            pygame.draw.polygon(Screen, Red, ((725,350),(675,320),(675,380)), 0) 
            pygame.draw.polygon(Screen, Cyan, ((720,350),(678,325),(678,375)), 0) 
        if 675 < mouse[0] < 725 and 400 < mouse[1] < 450:
            pygame.draw.polygon(Screen, Cyan, ((725,425),(675,395),(675,455)), 0) 
            pygame.draw.polygon(Screen, Red, ((720,425),(678,400),(678,450)), 0)
            if click[0] == 1:
                Settings['Effects'] = change_volume(Settings['Effects'], 1)
                update_volume()
        else:
            pygame.draw.polygon(Screen, Red, ((725,425),(675,395),(675,455)), 0) 
            pygame.draw.polygon(Screen, Cyan, ((720,425),(678,400),(678,450)), 0)
        #Back 
        if 75 < mouse[0] < 175 and 533 < mouse[1] < 565:
            backback = optionfont.render("Back", False, Cyan)
            backfront = optionfont.render("Back", False, Red)
            if click[0] == 1:
                MenuLoop()
        else:
            backback = optionfont.render("Back", False, Red)
            backfront = optionfont.render("Back", False, Cyan)
        Screen.blit(masterfront,(200,250))
        Screen.blit(musicfront,(200,325))
        Screen.blit(effectfront,(200,400))
        Screen.blit(masternumber,(560,240))
        Screen.blit(musicnumber,(560,315))
        Screen.blit(effectnumber,(560,390))
        Screen.blit(backback,(77,529))
        Screen.blit(backfront,(75,525))
        pygame.display.update() 
        for event in pygame.event.get(): #For all of the events(mouse/key actions) that are currently happening
            if event.type == pygame.QUIT: #If the user clicked the close button
                kill() #Close the window and stop the program
        Clock.tick(30)
    
update_volume()
Intro()
MenuLoop()
