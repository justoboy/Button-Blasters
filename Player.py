'''
Created on Aug 3, 2018

@author: justo
'''
import os
import glob
import pickle
Directory = os.getcwd() #Gets the directory this script is in
Directory += '\\Data\\Players\\'
if not os.path.exists(Directory):
    os.makedirs(Directory)
    
def GetPlayers(): #Returns a list of player saves
    Players = []
    for name in glob.glob(Directory+'*.dat'): #Iterates over all .dat files in the Players folder
        path, filename = os.path.split(name) #Gets the filename from the current file example: Player1.dat
        Players.append(filename[:-4]) #Adds the name without the .dat extension to the players list
    return Players
        
def CreatePlayer(Name): #Creates a new player
    Data = {'FireSpeed':1,'BlastSpeed':1,'Health':10,'MoveSpeed':1,'Damage':1,'Level':1,'XP':0,'Color':(0,0,255),'Unlocked':1,'Name':Name,'Points':0} #Creates a data dictionary using the default player stats
    File = open(Directory+'{}.dat'.format(Name), 'wb') #Creates a binary file in the players folder with its name the same as the player's
    pickle.dump(Data,File) #Saves the dictionary in the file
    
def LoadPlayer(Name): #Loads a player's data
    File = open(Directory+'{}.dat'.format(Name), 'rb') #Opens a player save file with the given name
    return pickle.load(File) #Returns the dictionary contained inside

def SavePlayer(Data):
    File = open(Directory+'{}.dat'.format(Data['Name']), 'wb') #Opens a player save file with the name stored in the given dictionary 
    pickle.dump(Data,File) #Saves the given dictionary in the file
