'''
Created on Aug 21, 2018

@author: justo
'''
import pygame 
import os
import pickle
Directory = os.getcwd() #Gets the directory this script is in
Screen = None
screen_width = 800
screen_height = 600
aspect_ratio = screen_width/screen_height
Clock = pygame.time.Clock()
Black = (0,0,0)
Red = (255,0,0)
Cyan = (0,255,255)
DarkOrange = (255,85,0)
Orange = (255,170,0)
Keybinds = []
Cursor0 = pygame.image.load(Directory+'/Images/Cursor0.png') #Loads the arrow cursor
Cursor1 = pygame.image.load(Directory+'/Images/Cursor1.png') #Loads the pointer cursor
Cursor = pygame.transform.scale(Cursor0, (int(screen_height/25), int(screen_height/25))) #Sets cursor to arrow
ControlsFile = open(Directory+'\Data\Controls.dat','rb')
Controls = pickle.load(ControlsFile)
ControlsFile.close()
DefaultKeybinds = [{'name':'Mouse','keybind':{'type':'mouse'}},{'name':'Click','keybind':{'type': 'click', 'value': 1}},{'name':'Shoot','keybind':{'type': 'key', 'value': 32}},{'name':'Up','keybind':{'type': 'key', 'value': 273}},{'name':'Down','keybind':{'type': 'key', 'value': 274}},{'name':'Left','keybind':{'type': 'key', 'value': 276}},{'name':'Right','keybind':{'type': 'key', 'value': 275}},{'name':'Back','keybind':{'type': 'key', 'value': 27}},{'name':'Enter','keybind':{'type': 'key', 'value': 13}},{'name':'A','keybind':{'type': 'key', 'value': 97}},{'name':'B','keybind':{'type': 'key', 'value': 98}},{'name':'X','keybind':{'type': 'key', 'value': 120}},{'name':'Y','keybind':{'type': 'key', 'value': 121}}]
#ControlsFile = open(Directory+'\Data\Controls.dat', 'wb')
#pickle.dump(DefaultKeybinds, ControlsFile)
#ControlsFile.close()

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
        
def Convert(kbs):
    keybinds = {}
    for kb in kbs:
        keybinds[kb['name']] = kb['keybind']
    return keybinds
controls = Convert(Controls)

def DeConvert(kbs):
    keybinds = []
    for key, value in kbs.items():
        keybinds.append({'name':key,'keybind':value})
    return keybinds

def Main(s,a,w,h):
    global screen_height, screen_width, aspect_ratio, Screen, Controls, Keybinds, Clock
    Screen, aspect_ratio, screen_width, screen_height = s, a, w, h
    for keybind in Controls:
        Keybinds.append(Keybind(keybind['name'],keybind['keybind']))
    done = False
    pygame.joystick.quit()
    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        if not joystick.get_init(): joystick.init()
    while not done:
        done = Update()
        if controls['Mouse']['type'] == 'joystick':
            ControllerHelp(controls['Mouse'])
        Clock.tick(30)
    Keybinds.clear()
    return screen_width, screen_height

def CheckForJoystick():
    for key, value in controls.items():
        if value['type'] == 'joystick' or value['type'] == 'button' or value['type'] == 'hat':
            try:
                joystick = pygame.joystick.Joystick(value['joystick'])
                if not joystick.get_init(): joystick.init()
                return True
            except Exception:
                return False
            
def Update():
    global Screen, screen_height, screen_width, Cursor, controls
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
                    if GetKey(event) and GetKey(event).items() >= controls['Click'].items():
                        Keybinds[i].new_keybind()
                    elif Keybinds[i].get_name() == 'Click' and controls['Click']['type'] != 'click' and controls['Click']['type'] != 'key' and not CheckForJoystick() and event.type == pygame.MOUSEBUTTONDOWN: #If this is the click keybind and the click button is on a controller that is disconnected and the player clicks the mouse
                        Keybinds[i].new_keybind()
            Screen.blit(value,(screen_width*.1,screen_height*(i/15)))
        elif i <= 21:
            Screen.blit(name,(screen_width*.375,screen_height*((i-11)/15)))
            if screen_width*.475 <= mouse[0] <= screen_width*.475+value.get_width() and screen_height*((i-11)/15) <= mouse[1] <= screen_height*((i-11)/15)+value.get_height():
                Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                value = font.render(GetKeyName(Keybinds[i].keybind), False, Cyan,Red)
                for event in events:
                    if GetKey(event) and GetKey(event).items() >= controls['Click'].items():
                        Keybinds[i].new_keybind()
            Screen.blit(value,(screen_width*.475,screen_height*((i-11)/15)))
        elif i <= 32:
            Screen.blit(name,(screen_width*.75,screen_height*((i-22)/15)))
            if screen_width*.85 <= mouse[0] <= screen_width*.85+value.get_width() and screen_height*((i-22)/15) <= mouse[1] <= screen_height*((i-22)/15)+value.get_height():
                Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
                value = font.render(GetKeyName(Keybinds[i].keybind), False, Cyan,Red)
                for event in events:
                    if GetKey(event) and GetKey(event).items() >= controls['Click'].items():
                        Keybinds[i].new_keybind()
            Screen.blit(value,(screen_width*.85,screen_height*((i-22)/15)))
    back = font.render('Back', False, DarkOrange)
    reset = font.render('Reset', False, DarkOrange)
    save = font.render('Save', False, DarkOrange)
    if screen_width*.1 <= mouse[0] <= screen_width*.1+back.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+back.get_height():
        back = font.render('Back', False, DarkOrange, Orange)
        Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
        for event in events:
            if GetKey(event) and GetKey(event).items() >= controls['Click'].items():
                return True
    if screen_width*.4 <= mouse[0] <= screen_width*.4+reset.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+reset.get_height():
        reset = font.render('Reset', False, DarkOrange, Orange)
        Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
        for event in events:
            if GetKey(event) and (GetKey(event).items() >= controls['Click'].items() or GetKey(event).items() >= {'type':'click','value':1}.items()):
                Reset()
                return True
    if screen_width*.7 <= mouse[0] <= screen_width*.7+save.get_width() and screen_height*.9 <= mouse[1] <= screen_height*.9+save.get_height():
        save = font.render('Save', False, DarkOrange, Orange)
        Cursor = pygame.transform.scale(Cursor1, (int(screen_height/25), int(screen_height/25)))
        for event in events:
            if GetKey(event) and GetKey(event).items() >= controls['Click'].items():
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
            return True
        elif event.type == pygame.VIDEORESIZE:
            Resize(event.size)
    return False

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
    
def GetKeyName(keybind):
    if keybind['type'] == 'mouse':
        return 'Mouse'
    elif keybind['type'] == 'click':
        return ['left click','middle click','right click','scroll up','scroll down'][keybind['value']-1]
    elif keybind['type'] == 'key':
        return pygame.key.name(keybind['value']) if pygame.key.name(keybind['value']) != '' else 'UNKNOWN'
    elif keybind['type'] == 'joystick':
        try:
            return f'joystick {keybind["joystick"]}:{keybind["axi"]}'
        except:
            return f'joystick {keybind["joystick"]}:({keybind["axis"]}:{keybind["value"]})'
    elif keybind['type'] == 'button':
        return f'js{keybind["joystick"]},button{keybind["button"]}'
    elif keybind['type'] == 'hat':
        return f'js{keybind["joystick"]},hat{keybind["hat"]}:{keybind["value"]}'
    else:
        return 'UNKNOWN'
   
def GetKey(event):
    key = None
    if event.type == pygame.JOYHATMOTION:
        if event.value != (0,0):
            key = {'type':'hat','joystick':event.joy,'hat':event.hat,'value':event.value}
    elif event.type == pygame.JOYBUTTONDOWN:
        key = {'type':'button','joystick':event.joy,'button':event.button}
    elif event.type == pygame.JOYBALLMOTION:
        key = {'type':'ball','joystick':event.joy,'ball':event.ball,'value':event.rel}
    elif event.type == pygame.JOYAXISMOTION:
        value = event.value
        if value > 0:
            value = 1
        elif value < -1:
            value = 0
        elif value < 0:
            value = -1
        if event.axis%2 == 0:
            axi = (event.axis,event.axis+1)
        else:
            axi = (event.axis-1,event.axis)
        key = {'type':'joystick','joystick':event.joy,'axis':event.axis,'axi':axi,'value':value}
    elif event.type == pygame.KEYDOWN:
        key = {'type':'key','value':event.key}
    elif event.type == pygame.MOUSEBUTTONDOWN:
        key = {'type':'click','value':event.button}
    elif event.type == pygame.MOUSEMOTION:
        key = {'type':'mouse'} 
    return key
    
def GetInput(name):
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        if not joysticks[i].get_init(): joysticks[i].init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYHATMOTION and name != 'Mouse':
                return {'type':'hat','joystick':event.joy,'hat':event.hat,'value':event.value}
            elif event.type == pygame.JOYBUTTONDOWN and name != 'Mouse':
                return {'type':'button','joystick':event.joy,'button':event.button}
            elif event.type == pygame.JOYBALLMOTION:
                return {'type':'ball','joystick':event.joy,'ball':event.ball,'value':event.rel}
            elif event.type == pygame.JOYAXISMOTION and name != 'Click':
                if name == 'Mouse':
                    if event.axis%2 == 0:
                        axi = (event.axis,event.axis+1)
                    else:
                        axi = (event.axis-1,event.axis)
                    return {'type':'joystick','joystick':event.joy,'axi':axi}
                else:
                    value = event.value
                    if value > 0:
                        value = 1
                    elif value < -1:
                        value = 0
                    elif value < 0:
                        value = -1
                    return {'type':'joystick','joystick':event.joy,'axis':event.axis,'value':value}
            elif event.type == pygame.KEYDOWN and name != 'Mouse':
                return {'type':'key','value':event.key}
            elif event.type == pygame.MOUSEBUTTONDOWN and name != 'Mouse':
                return {'type':'click','value':event.button}
            elif event.type == pygame.MOUSEMOTION and name == 'Mouse':
                return {'type':'mouse'}
            elif event.type == pygame.VIDEORESIZE:
                Resize(event.size)
            elif event.type == pygame.QUIT:
                pygame.quit()  
                quit()  
        pygame.time.Clock().tick(30)
        
def Reset():
    global DefaultKeybinds, Controls, controls, Screen, aspect_ratio, screen_width, screen_height
    ControlsFile = open(Directory+'\Data\Controls.dat', 'wb')
    pickle.dump(DefaultKeybinds, ControlsFile)
    Controls = DefaultKeybinds
    controls = Convert(Controls)
    Keybinds.clear()
    Main(Screen, aspect_ratio, screen_width, screen_height)

def Save():
    global Controls, controls
    Controls = DeConvert(controls)
    ControlsFile = open(Directory+'\Data\Controls.dat', 'wb')
    pickle.dump(Controls, ControlsFile)
    ControlsFile.close()
        
if __name__ == '__main__': #If this script is running by itself instead of being imported by another script start a pygame window
    import ctypes
    pygame.init()
    pygame.font.init()
    Icon = pygame.image.load(Directory+'\Images\Icon.png') #Loads the icon for the game window
    pygame.display.set_icon(Icon) #Sets the game window icon
    Screen = pygame.display.set_mode((0, 0),pygame.RESIZABLE) #Create the game window
    user32 = ctypes.WinDLL('user32')
    user32.ShowWindow(user32.GetForegroundWindow(), 3) #Maximizes the window
    for event in pygame.event.get(): #Sets the new screen size
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
    Screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)
    aspect_ratio = screen_width/screen_height
    pygame.display.update()
    pygame.display.set_caption('Button Blasters') #Set the windows display name
    pygame.mouse.set_visible(False)
    Main(Screen, aspect_ratio, screen_width, screen_height)