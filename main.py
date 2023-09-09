import os, time, numpy, json
from tkinter import Tk, PhotoImage, filedialog, messagebox, Frame, X
import tkinter as tk
from PIL import Image, ImageTk
from itertools import repeat
from functools import partial
from multiprocessing import Pool,freeze_support

import mapGen, zoom
sprites = {1:{"player_White":None, "player_Green":None, "player_Red":None, "player_Blue":None},
            2:{"temple_Jungle Temple":None, "temple_Witch Hut":None, "temple_Woodland Mansion":None, "temple_Ocean Monument":None},
            3:{"hamlet_Plains Village":None, "hamlet_Savanna Village":None, "hamlet_Snowy Village":None, "hamlet_Taiga Village":None},
            4:{"hamlet_Desert Village":None, "unused_Red X":None, "unused_Target X":None, "unused_Target Point":None},
            5:{"banner_White":None, "banner_Light Grey":None, "banner_Grey":None, "banner_Black":None},
            6:{"banner_Red":None, "banner_Orange":None, "banner_Yellow":None, "banner_Lime":None},
            7:{"banner_Green":None, "banner_Blue":None, "banner_Cyan":None, "banner_Light Blue":None},
            8:{"banner_Pink":None, "banner_Magenta":None, "banner_Purple":None, "banner_Brown":None}}

def error():
   messagebox.showerror("Error", "A faital error occured.")

def ImageOpen(path, recent):
    if path == '': 
        path = filedialog.askopenfilename(initialdir = settingsJson["Path Settings"]["Load Path"]["data"],
                                          parent=mainScreen, title='Choose an Image File.')
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
    except NameError:
        pass

    if (X/Z > 4) or (X/Z < 0.25):
        messagebox.showerror("Error", "Image proportions too large. Your image has been saved but the background has not been updated.")
        setBackground(256,256,background)
        pass

    if path != '' and not(recent):
        settingsJson["Recents"].insert(0, path)
        
        if len(settingsJson["Recents"]) > settingsJson["Recent Max Count"]:
            settingsJson["Recents"].pop()
            
        with open('settings.json', 'w') as settingsFile:
            settingsFile.write(json.dumps(settingsJson, indent=4))

    App = zoom.LoadImage(mainScreen, bigImg, path)
    mainScreen.mainloop()

def saveFile(image, path):
    App.path = path
    image.save(path)

def GenerateMaps():
    global settingsJson
    
    fileList = filedialog.askopenfilenames(initialdir = settingsJson["Path Settings"]["Load Path"]["data"],
                                           parent=mainScreen, title='Choose a file')
    
    t0 = time.time()

    with Pool() as pool:
        results = pool.starmap(mapGen.makeMaps, zip(repeat(settingsJson["Path Settings"]["Save Path"]["data"]), fileList,
                                                    repeat(settingsJson["Generator Settings"]["Basic Merging"]["data"]),
                                                    repeat(settingsJson["Generator Settings"]["Additional Icons"]["data"])))
    
    print(time.time() - t0)
    if settingsJson["Generator Settings"]["Basic Merging"]["data"]:
        resNew = numpy.swapaxes(numpy.array(results, dtype="object"), 0, 1)
        if settingsJson["Generator Settings"]["Scaled Merging"]["data"]:
            results.append(mapGen.imageCombineMulti(resNew[4], resNew[5], resNew[2], resNew[3], settingsJson["Path Settings"]["Save Path"]["data"]))
        else:
            results.append(mapGen.imageCombine(resNew[4], resNew[5], resNew[2], resNew[3], settingsJson["Path Settings"]["Save Path"]["data"]))
        
        if len(results[-1][-1]) > 0:
            messagebox.showerror("Error", results[-1][-1])

    
    var = results[-1]
        
    setBackground(var[0],var[1],var[2], var[3])
    
def GenerateImages():
    global settingsJson
    
    imgFile = filedialog.askopenfilename(initialdir = settingsJson["Path Settings"]["Load Path"]["data"], parent=mainScreen, title='Choose a Image File')
    
    donorFile = filedialog.askopenfilename(initialdir = settingsJson["Path Settings"]["Load Path"]["data"], parent=mainScreen, title='Choose a Donar DAT File', filetypes=[("Minecraft Map File", ".dat")])

    setBackground(128, 128, mapGen.makeImgs(imgFile, donorFile), '', recent=True)

def AddIcons(item, rotation = 0):
    print(item)
    App.rotation = rotation
    if App.icon == item:
        App.icon = None
    else:
        App.icon = item

def defineSettings():
    global settingsJson
    settingsJson = {}
    
    
    settingsJson["Path Settings"] = {}
    
    settingsJson["Path Settings"]["Load"] = {"type": "Path"}
    settingsJson["Path Settings"]["Load"]   ["data"] = filedialog.askdirectory(parent=mainScreen,
                                                        title='Find The Minecraft Saves Folder')
    
    settingsJson["Path Settings"]["Save"] = {"type": "Path"}
    settingsJson["Path Settings"]["Save"]   ["data"] = filedialog.askdirectory(parent=mainScreen,
                                                 title='Find Where Files Should Be Saved')
    
    
    settingsJson["Generator Settings"] = {}
    
    settingsJson["Generator Settings"]["Basic Merging"] = {}
    settingsJson["Generator Settings"]["Basic Merging"]["type"] = "Check"
    settingsJson["Generator Settings"]["Basic Merging"]["data"] = messagebox.askyesno("Basic Merging","Do you want to automatically merge images?")
    
    settingsJson["Generator Settings"]["Additional Icons"] = {}
    settingsJson["Generator Settings"]["Additional Icons"]["type"] = "Check"
    settingsJson["Generator Settings"]["Additional Icons"]["data"] = messagebox.askyesno("Additional Icons","Do you want to add map icons?\n(Banners and Item Frame Locations)")
    
    settingsJson["Generator Settings"]["Scaled Merging"] = {}
    settingsJson["Generator Settings"]["Scaled Merging"]["type"] = "Check"
    settingsJson["Generator Settings"]["Scaled Merging"]["data"] = messagebox.askyesno("Scaled Merging","Do you want to merge images of diffrent scales?")
    settingsJson["Generator Settings"]["Scaled Merging"]["reqr"] = "Basic Merging"
    
    settingsJson["Recent Max Count"] = 5
    settingsJson["Recents"] = ["icon.png"]
    
    with open('settings.json', 'w') as settingsFile:
        settingsFile.write(json.dumps(settingsJson, indent=4))
    
def newSettings(parent, name, val):
    settingsJson[parent][name]["data"] = val
    
    with open('settings.json', 'w') as settingsFile:
        settingsFile.write(json.dumps(settingsJson, indent=4))
     
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

    if not os.path.exists(local + 'settings.json'):
        with open(os.path.join(local, 'settings.json'), 'w') as fp:
            pass
    
    mainScreen = Tk()

    ico = PhotoImage(file = "Icon.png")
    back = Image.open("Icon.png")

    with open('settings.json') as settingsFile:
        settingsJson = json.loads(settingsFile.read())
    
    NavBar = Frame(mainScreen, background='white')
    NavBar.pack(fill=X)
    
    mb = tk.Menubutton(NavBar, text="File", background='white', activebackground='#E5F3FF', bd=0)
    mb.menu = tk.Menu( mb, tearoff = 0 )
    mb["menu"] =  mb.menu
    
    mb.menu.add_command(label="Load Image", command = partial(ImageOpen, '', False))
    menu = tk.Menu( mb, tearoff = 0 )
    for count, item in enumerate(settingsJson["Recents"]):
        menu.add_command(label=str(count) + ". " + os.path.basename(item), command = partial(ImageOpen, item, True))
    mb.menu.add_cascade(label="Recent Images", menu=menu)
    
    mb.menu.add_separator()
    mb.menu.add_command(label='Save', command = lambda: saveFile(App.orig_img, App.path))
    mb.menu.add_command(label='Save As', command = lambda: saveFile(App.orig_img, filedialog.askopenfilename(initialdir = settingsJson["Path Settings"]["Save Path"]["data"], parent=mainScreen, title='Save File as:')))

    mb.menu.add_separator()
    mb.menu.add_command(label='Exit', command = endProgram)
    mb.pack(side = 'left')

    mb = tk.Menubutton(NavBar, text="Settings", background='white', activebackground='#E5F3FF', bd=0)
    mb.menu = tk.Menu( mb, tearoff = 0 )
    mb["menu"] =  mb.menu
    
    mb.menu.add_command(label='All Settings', command = defineSettings)
    
    settingsMenu = {}
    for parent, group in settingsJson.items():
        if not isinstance(group, dict): continue
        for name, setting  in group.items():
            match setting["type"]:
                case "Path":
                    mb.menu.add_command(label=name, command = lambda parent = parent, name = name: newSettings(parent, name, filedialog.askdirectory(parent=mainScreen, title='')))
                case "Check":
                    settingsMenu[name] = tk.BooleanVar()
                    settingsMenu[name].set(settingsJson[parent][name]["data"])
                    mb.menu.add_checkbutton(label=name, variable=settingsMenu[name], command = lambda  parent = parent, name = name, bool=settingsMenu[name]: newSettings(parent, name, bool.get()))
        mb.menu.add_separator()    
    mb.pack(side = 'left')

    map = HoverButton(NavBar, text = 'Generate Images', command = GenerateMaps, background='white', activebackground='#E5F3FF', bd=0)
    map.pack(side = 'left')
    
    itm = HoverButton(NavBar, text = 'Generate Maps', command = GenerateImages, background='white', activebackground='#E5F3FF', bd=0)
    itm.pack(side = 'left')

    spritesRaw = Image.open('Sprites.png').convert("RGBA")
    
    spritesTemp = {}
    for row, rowDict in sprites.items():
        for column, name in enumerate(rowDict.keys()):
            if name[:6] not in spritesTemp: spritesTemp[name[:6]] = {}
            spritesTemp[name[:6]][name] = ImageTk.PhotoImage(spritesRaw.crop((column*8, row*8-8, column*8+8, row*8+8-8)).resize((16,16), Image.Resampling.NEAREST))

    spritesMenu = {}
    for name, group in spritesTemp.items():
        spritesMenu[name] = tk.Menubutton(NavBar, image=list(group.values())[0], background='white', activebackground='#E5F3FF', bd=0)
        spritesMenu[name].menu = tk.Menu(spritesMenu[name], tearoff = 0 )
        for icon in group.keys():
            spritesMenu[name].menu.add_command(label=icon[7:], command = partial(AddIcons, icon))
        spritesMenu[name]["menu"] =  spritesMenu[name].menu
        spritesMenu[name].pack(side = 'left')

    mainScreen.attributes('-alpha')
    mainScreen.iconphoto(False, ico) 
    mainScreen.title("  Minecraft Exporter")
    mainScreen.configure(background = 'black')
    mainScreen.resizable(width=True, height=True)

    canvas = tk.Canvas(mainScreen, width=256, height=256)
    setBackground(256,256,back, '')

    mainScreen.mainloop()