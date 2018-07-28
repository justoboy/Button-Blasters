'''
Created on Jul 10, 2018

@author: justo
'''
import tkinter.messagebox
import pickle
try:
    File = open('Settings.dat', 'wb')
except Exception as Error:
    tkinter.messagebox.showerror('ERROR', str(Error))
Settings = {'Master':0.5,'Music':1.0,'Effects':1.0}
pickle.dump(Settings,File)
