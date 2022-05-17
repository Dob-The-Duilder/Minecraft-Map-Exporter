import tkinter, os, sys, time, threading
from tkinter import Tk, PhotoImage, constants, filedialog, messagebox
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

import mapGen
import zoomOG as zoom

ran = 0

def error():
   messagebox.showerror("Error", "Sorry, this is still a work in progress >.<")

def GenerateMaps():
    global settingsList
    
    var = mapGen.makeMaps(settingsList[1][1], filedialog.askopenfilenames(initialdir = settingsList[0][1], parent=mainScreen, title='Choose a file'), settingsList[2][1])
    setBackground(var[0],var[1],var[2])

def setBackground(X,Z,bigImg):
    global ran
    global bg
    global canvas
    if ran == 0:
        canvas = tk.Canvas(mainScreen, width=X*2, height=Z*2)
    else:
        canvas.delete(bg)
        canvas.config(width=X*2, height=Z*2)
    canvas.pack(side = 'top')
    ran = 1
    
    if (Z*2+30 <= 1080):
        mainScreen.geometry('{}x{}'.format((X*2), (Z*2+30)))
        bigImg = bigImg.resize(((X*2), (Z*2)),Image.NEAREST)
    else:
        mainScreen.geometry('{}x{}'.format(X, (Z+30)))
    
    img = ImageTk.PhotoImage(bigImg)
    bg = canvas.create_image( 0, 0, image = img, anchor = "nw")
    mainScreen.mainloop()
    
def defineSettings():
    global settingsList
    
    print(settingsList)

    settingsList = []
    settingsList.append(['LoadPath', ''])
    settingsList[0][1] = filedialog.askdirectory(parent=mainScreen, title='Find The Minecraft Saves Folder')
    
    settingsList.append(['SavesPath', ''])
    settingsList[1][1] = filedialog.askdirectory(parent=mainScreen, title='Find Where Files Should Be Saved')
    
    settingsList.append(['merge', ''])
    settingsList[2][1] = messagebox.askokcancel("Merging","Do you want to automatically merge images?")
    
    print(settingsList)
    
    settingsFile = open('settings.txt', 'w')
    
    for setting in settingsList:
        line = str(setting[0]) + '=' + str(setting[1]) + '\n'
        settingsFile.write(line)
    settingsFile.close()
    
path = os.path.abspath(__file__)
local = path.replace(os.path.basename(path), '')

if not os.path.exists(local + 'settings.txt'):
    with open(os.path.join(local, 'settings.txt'), 'w') as fp:
        pass

settingsFile = open('settings.txt', 'r')
settingsList = [line.replace('\n', '').split('=') for line in settingsFile.readlines()]
settingsFile.close()

mainScreen = Tk()

#icon = PhotoImage(file = (local + "Graphics\Icon.png"))

NavBar = Frame(mainScreen)
NavBar.pack(fill=X)

btn = Button(NavBar, text = 'Exit', command = mainScreen.destroy)
btn.pack(side = 'left')

mapbtn = Button(NavBar, text = 'Generate Maps', command = GenerateMaps)
mapbtn.pack(side = 'left')

btn2 = Button(NavBar, text="Settings", command = defineSettings)
btn2.pack(side = 'left')

mainScreen.attributes('-alpha')
#mainScreen.iconphoto(False, icon) 
mainScreen.title("  Minecraft Exporter")
mainScreen.configure(background = 'black')
mainScreen.geometry("450x500")
mainScreen.resizable(width=True, height=True)

#background = Image.open('Graphics\Icon.png')
#setBackground(128,128, background)

if (len(settingsList[0]) <= 1):
    messagebox.showerror("Error", "Settings need to be generated before program can run")
    defineSettings()
elif (settingsList[0][1] == ''):
    messagebox.showerror("Error", "Settings need to be generated before program can run")
    defineSettings()

mainScreen.mainloop()