import tkinter, os, sys, time, threading, time, numpy
from tkinter import Tk, PhotoImage, constants, filedialog, messagebox
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from itertools import repeat
from multiprocessing import Pool,freeze_support
from multiprocessing.dummy import Pool as ThreadPool

import mapGen

def error():
   messagebox.showerror("Error", "Sorry, this is still a work in progress >.<")

def GenerateMaps():
    global settingsList
    
    fileList = filedialog.askopenfilenames(initialdir = settingsList[0][1], parent=mainScreen, title='Choose a file')
    
    t0 = time.time()
    with Pool() as pool:
        results = pool.starmap(mapGen.makeMaps, zip(repeat(settingsList[1][1]), fileList, repeat(bool(settingsList[2][1])), repeat(bool(settingsList[3][1]))))
    t1 = time.time()
    print(t1-t0)
    #[128,128, new_image, size, coordX, coordZ]
    if bool(settingsList[2][1]):
        resNew = numpy.swapaxes(numpy.array(results, dtype="object"), 0, 1)
        results.append(mapGen.imageCombine(resNew[4], resNew[5], resNew[2], resNew[3], settingsList[1][1]))
    print(results[-1][-1])
    var = results[-1]
    setBackground(var[0],var[1],var[2])

def setBackground(X,Z,bigImg):
    global bg
    try:
        canvas.delete(bg)
    except:
        pass
    
    canvas.config(width=X*2, height=Z*2)
    canvas.pack(side = 'top')
    
    if (Z*2+30 <= 1080):
        mainScreen.geometry('{}x{}'.format((X*2), (Z*2+30)))
        bigImg = bigImg.resize(((X*2), (Z*2)),Image.Resampling.NEAREST)
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
    settingsList[2][1] = messagebox.askyesno("Merging","Do you want to automatically merge images?")
    
    settingsList.append(['extras', ''])
    settingsList[3][1] = messagebox.askyesno("Extras","Do you want to add map icons?\n(Banners and Item Frame Locations)")
    
    print(settingsList)
    
    settingsFile = open('settings.txt', 'w')
    
    for setting in settingsList:
        line = str(setting[0]) + '=' + str(setting[1]) + '\n'
        settingsFile.write(line)
    settingsFile.close()
    
def newSettings():
     
    # Toplevel object which will
    # be treated as a new window
    settingsWindow = Toplevel(mainScreen)
 
    # sets the title of the
    # Toplevel widget
    settingsWindow.title("Settings")
    settingsWindow.iconphoto(False, icon)
 
    # sets the geometry of toplevel
    settingsWindow.geometry("200x200")
 
    # A Label widget to show in toplevel
    Label(settingsWindow,
          text ="This is a new window").pack()

if __name__ == "__main__":
    freeze_support()
    path = os.path.abspath(__file__)
    local = path.replace(os.path.basename(path), '')

    if not os.path.exists(local + 'settings.txt'):
        with open(os.path.join(local, 'settings.txt'), 'w') as fp:
            pass

    settingsFile = open('settings.txt', 'r')
    settingsList = [line.replace('\n', '').split('=') for line in settingsFile.readlines()]
    settingsFile.close()
    
    mainScreen = Tk()

    icon = PhotoImage(file = ("Icon.png"))
    back = Image.open("Icon.png")

    NavBar = Frame(mainScreen)
    NavBar.pack(fill=X)

    btn = Button(NavBar, text = 'Exit', command = mainScreen.destroy)
    btn.pack(side = 'left')

    mapbtn = Button(NavBar, text = 'Generate Maps', command = GenerateMaps)
    mapbtn.pack(side = 'left')

    btn2 = Button(NavBar, text="Settings", command = defineSettings)
    btn2.pack(side = 'left')

    #btn2 = Button(NavBar, text="Settings", command = newSettings)
    #btn2.pack(side = 'left')


    mainScreen.attributes('-alpha')
    mainScreen.iconphoto(False, icon) 
    mainScreen.title("  Minecraft Exporter")
    mainScreen.configure(background = 'black')
    mainScreen.geometry("450x500")
    mainScreen.resizable(width=True, height=True)

    canvas = tk.Canvas(mainScreen, width=256, height=256)
    setBackground(256,256,back)

    #background = Image.open('Graphics\Icon.png')
    #setBackground(128,128, background)

    if (len(settingsList) < 4):
        messagebox.showerror("Error", "Settings need to be generated before program can run")
        defineSettings()
    elif (settingsList[3][1] == ''):
        messagebox.showerror("Error", "Settings need to be generated before program can run")
        defineSettings()

    mainScreen.mainloop()
