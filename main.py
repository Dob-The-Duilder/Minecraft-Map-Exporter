import os, time, time, numpy
from tkinter import Tk, PhotoImage, filedialog, messagebox
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from itertools import repeat
from functools import partial
from multiprocessing import Pool,freeze_support

import mapGen, zoom
iconDict = {
    'arrow'     : (0, 0),
    'mansion'   : (1, 0),
    'monument'  : (2, 0),
    'cross'     : (3, 0)}
bannerDict = {
    'white'     : (0, 1),
    'light_gray': (1, 1),
    'gray'      : (2, 1),
    'black'     : (3, 1),
    'red'       : (0, 2),
    'orange'    : (1, 2),
    'yellow'    : (2, 2),
    'lime'      : (3, 2),
    'green'     : (0, 3),
    'blue'      : (1, 3),
    'cyan'      : (2, 3),
    'light_blue': (3, 3),
    'pink'      : (0, 4),
    'magenta'   : (1, 4),
    'purple'    : (2, 4),
    'brown'     : (3, 4)
    }

def error():
   messagebox.showerror("Error", "A faital error occured.")

def ImageOpen(path, recent):
    if path == '': path = filedialog.askopenfilename(initialdir = settingsList[1][1], parent=mainScreen, title='Choose an Image File.')
    newImg = Image.open(path)
    if recent:
        setBackground(newImg.width,newImg.height,newImg,path,recent)
        pass
    setBackground(newImg.width,newImg.height,newImg,path)

def setBackground(X,Z,bigImg,path,recent = False):
    global App
    global background
    
    background = bigImg

    try:
        App.delete()
    except:
        pass

    if (X/Z > 4) or (X/Z < 0.25):
        messagebox.showerror("Error", "Image proportions too large. Your image has been saved but the background has not been updated.")
        setBackground(256,256,background)
        pass

    if path != '' and not(recent):
        settingsFile = open('settings.txt', 'w')
        settingsList[4].insert(0, path)
        if len(settingsList[4]) > 5: settingsList[4].pop(5)
        for setting in settingsList:
            line = '='.join(str(e) for e in setting) + '\n'
            settingsFile.write(line)
        settingsFile.close()

    App = zoom.LoadImage(mainScreen, bigImg, path)
    mainScreen.mainloop()

def saveFile(image, path):
    App.path = path
    image.save(path)

def GenerateMaps():
    global settingsList
    
    fileList = filedialog.askopenfilenames(initialdir = settingsList[0][1], parent=mainScreen, title='Choose a file')
    
    t0 = time.time()

    with Pool() as pool:
        results = pool.starmap(mapGen.makeMaps, zip(repeat(settingsList[1][1]), fileList, repeat(eval(settingsList[2][1])), repeat(eval(settingsList[3][1]))))
    
    t1 = time.time()
    if eval(settingsList[2][1]):
        resNew = numpy.swapaxes(numpy.array(results, dtype="object"), 0, 1)
        if eval(settingsList[5][1]):
            results.append(mapGen.imageCombineMulti(resNew[4], resNew[5], resNew[2], resNew[3], settingsList[1][1]))
        else:
            results.append(mapGen.imageCombine(resNew[4], resNew[5], resNew[2], resNew[3], settingsList[1][1]))
        
        if len(results[-1][-1]) > 0:
            messagebox.showerror("Error", results[-1][-1])

    
    var = results[-1]
        
    setBackground(var[0],var[1],var[2], var[3])

def AddIcons(item, rotation = 0):
    App.rotation = rotation
    if App.icon == item:
        App.icon = None
    else:
        App.icon = item

def defineSettings():
    global settingsList
    
    settingsList = []
    settingsList.append(['LoadPath', ''])
    settingsList[0][1] = filedialog.askdirectory(parent=mainScreen, title='Find The Minecraft Saves Folder')
    
    settingsList.append(['SavesPath', ''])
    settingsList[1][1] = filedialog.askdirectory(parent=mainScreen, title='Find Where Files Should Be Saved')
    
    settingsList.append(['merge', ''])
    settingsList[2][1] = messagebox.askyesno("Merging","Do you want to automatically merge images?")
    
    settingsList.append(['extras', ''])
    settingsList[3][1] = messagebox.askyesno("Extras","Do you want to add map icons?\n(Banners and Item Frame Locations)")
    
    settingsList.append(['icon.png'])

    settingsList.append(['scaleMerge', ''])
    settingsList[2][1] = messagebox.askyesno("Scaled Merging","Do you want to merge images of diffrent scales?")
        
    settingsFile = open('settings.txt', 'w')
    
    for setting in settingsList:
        line = '='.join(str(e) for e in setting) + '\n'
        settingsFile.write(line)
    settingsFile.close()
    
def newSettings(num, val):
    settingsList[num][1] = str(val)

    settingsFile = open('settings.txt', 'w')
    for setting in settingsList:
        line = '='.join(str(e) for e in setting) + '\n'
        settingsFile.write(line)
    settingsFile.close()
     

def endProgram():
    App.delete()
    mainScreen.destroy()

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.defaultThick = self['bg']
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
        self['bd'] = -1

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['bd'] = 0

if __name__ == "__main__":
    freeze_support()
    path = os.path.abspath(__file__)
    local = path.replace(os.path.basename(path), '')

    if not os.path.exists(local + 'settings.txt'):
        with open(os.path.join(local, 'settings.txt'), 'w') as fp:
            pass
    
    mainScreen = Tk()

    icon = PhotoImage(file = ("Icon.png"))
    back = Image.open("Icon.png")

    settingsFile = open('settings.txt', 'r')
    settingsList = [line.replace('\n', '').split('=') for line in settingsFile.readlines()]
    settingsFile.close()

    if (len(settingsList) < 6):
        messagebox.showerror("Error", "Settings need to be generated before program can run")
        defineSettings()
    elif (settingsList[5][0] == ''):
        messagebox.showerror("Error", "Settings need to be generated before program can run")
        defineSettings()
    
    NavBar = Frame(mainScreen, background='white')
    NavBar.pack(fill=X)
    
    mb = tk.Menubutton(NavBar, text="File", background='white', activebackground='#E5F3FF', bd=0)
    mb.menu = tk.Menu( mb, tearoff = 0 )
    mb["menu"] =  mb.menu
    
    mb.menu.add_command(label="Load Image", command = partial(ImageOpen, '', False))
    menu = tk.Menu( mb, tearoff = 0 )
    count = 0
    if settingsList[4][0] != '':
        for item in settingsList[4]:
            count += 1
            menu.add_command(label=str(count) + ". " + os.path.basename(item), command = partial(ImageOpen, item, True))
        mb.menu.add_cascade(label="Recent Images", menu=menu)
    
    mb.menu.add_separator()
    mb.menu.add_command(label='Save', command = lambda: saveFile(App.orig_img, App.path))
    mb.menu.add_command(label='Save As', command = lambda: saveFile(App.orig_img, filedialog.askopenfilename(initialdir = settingsList[1][1], parent=mainScreen, title='Save File as:')))

    mb.menu.add_separator()
    mb.menu.add_command(label='Exit', command = endProgram)
    mb.pack(side = 'left')

    mb = tk.Menubutton(NavBar, text="Settings", background='white', activebackground='#E5F3FF', bd=0)
    mb.menu = tk.Menu( mb, tearoff = 0 )
    mb["menu"] =  mb.menu
    
    merge = tk.BooleanVar()
    merge.set(eval(settingsList[2][1]))
    scaleMerge = tk.BooleanVar()
    scaleMerge.set(eval(settingsList[5][1]))
    extra = tk.BooleanVar()
    extra.set(eval(settingsList[3][1]))

    mb.menu.add_command(label='All Settings', command = defineSettings)
    mb.menu.add_separator()    
    mb.menu.add_command(label='Map Locations', command = lambda: newSettings(0, filedialog.askdirectory(parent=mainScreen, title='Find The Minecraft Saves Folder')))
    mb.menu.add_command(label='Image Locations', command = lambda: newSettings(1, filedialog.askdirectory(parent=mainScreen, title='Find Where Files Should Be Saved')))
    mb.menu.add_separator()
    mb.menu.add_checkbutton(label='Merge Images', variable=merge, command = lambda: newSettings(2, merge.get()))
    mb.menu.add_checkbutton(label='Scaled Merge', variable=scaleMerge, command = lambda: newSettings(5, scaleMerge.get()))
    mb.menu.add_checkbutton(label='Banner/Item Frames', variable=extra, command = lambda: newSettings(3, extra.get()))
    mb.pack(side = 'left')

    map = HoverButton(NavBar, text = 'Generate Maps', command = GenerateMaps, background='white', activebackground='#E5F3FF', bd=0)
    map.pack(side = 'left')

    sprites = Image.open('Sprites.png').convert("RGBA")

    spr1 = ImageTk.PhotoImage(sprites.crop((8, 0, 16, 8)).resize((16,16), Image.Resampling.NEAREST))
    ico1 = HoverButton(NavBar, image=spr1, command = partial(AddIcons, 'mansion'), background='white', activebackground='#E5F3FF', bd=0)
    ico1.pack(side = 'left')

    spr2 = ImageTk.PhotoImage(sprites.crop((16, 0, 24, 8)).resize((16,16), Image.Resampling.NEAREST))
    ico2 = HoverButton(NavBar, image=spr2, command = partial(AddIcons, 'monument'), background='white', activebackground='#E5F3FF', bd=0)
    ico2.pack(side = 'left')

    spr3 = ImageTk.PhotoImage(sprites.crop((24, 0, 32, 8)).resize((16,16), Image.Resampling.NEAREST))
    ico3 = HoverButton(NavBar, image=spr3, command = partial(AddIcons, 'cross'), background='white', activebackground='#E5F3FF', bd=0)
    ico3.pack(side = 'left')
    
    spr4 = ImageTk.PhotoImage(sprites.crop((0, 0, 8, 8)).resize((16,16), Image.Resampling.NEAREST))
    mb = tk.Menubutton(NavBar, image=spr4, background='white', activebackground='#E5F3FF', bd=0)
    mb.menu = tk.Menu( mb, tearoff = 0 )

    mb.menu.add_command(label='North', command = partial(AddIcons, 'arrow'))
    mb.menu.add_command(label='East', command = partial(AddIcons, 'arrow', 270))
    mb.menu.add_command(label='South', command = partial(AddIcons, 'arrow', 180))
    mb.menu.add_command(label='West', command = partial(AddIcons, 'arrow', 90))
    mb["menu"] =  mb.menu
    mb.pack(side = 'left')

    spr5 = ImageTk.PhotoImage(sprites.crop((16, 16, 24, 24)).resize((16,16), Image.Resampling.NEAREST))
    mb = tk.Menubutton(NavBar, image=spr5, background='white', activebackground='#E5F3FF', bd=0)
    mb.menu = tk.Menu( mb, tearoff = 0 )

    for banner in bannerDict:
        mb.menu.add_command(label=banner.replace('_', ' ').title(), command = partial(AddIcons, banner))
    mb["menu"] =  mb.menu
    mb.pack(side = 'left')

    mainScreen.attributes('-alpha')
    mainScreen.iconphoto(False, icon) 
    mainScreen.title("  Minecraft Exporter")
    mainScreen.configure(background = 'black')
    mainScreen.resizable(width=True, height=True)

    canvas = tk.Canvas(mainScreen, width=256, height=256)
    setBackground(256,256,back, '')

    mainScreen.mainloop()
