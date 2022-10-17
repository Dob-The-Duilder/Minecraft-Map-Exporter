from tkinter import *
from PIL import Image, ImageTk
from functools import partial

bannerDict = {
    'arrow'     : (0, 0),
    'mansion'   : (1, 0),
    'monument'  : (2, 0),
    'cross'     : (3, 0),
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

class LoadImage:
    def __init__(self,root,file,path):
        self.frame = Frame(root)
        
        self.orig_img = file
        self.path = path
        self.new_img = self.orig_img
        self.wid, self.hei = self.orig_img.size
        scaleX = int(610/self.wid)
        scaleZ = int(610/self.hei)
        self.scale = max(min(scaleX, scaleZ), 1)
        self.orig_img = self.orig_img.resize(((self.wid*self.scale), (self.hei*self.scale)),Image.Resampling.NEAREST)
        self.wid, self.hei = self.orig_img.size

        root.geometry(str(self.wid) + 'x' + str(self.hei+25))
        
        File2 = "overlay.png"
        self.spy = Image.open(File2)
        self.spyWid, self.spyHei = self.orig_img.size
        
        self.sprites = Image.open('Sprites.png')
        self.sprite = None
        self.rotation = 0
        self.icon = None
        
        self.canvas = Canvas(self.frame,width=self.wid,height=self.hei)
        self.canvas.pack()
        self.frame.pack()
        self.filter = Image.Resampling.NEAREST
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.image_container = self.canvas.create_image(0,0,image=self.img, anchor="nw")

        self.zoomcycle = 0
        self.zimg_id = None

        root.bind("<Button-1>",self.stamp)
        root.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Motion>",self.crop)

    def stamp(self,event):
        if self.sprite:
            tmp = self.orig_img
            sprite = self.sprite.resize((8*self.scale, 8*self.scale), self.filter).convert("RGBA")
            tmp.paste(sprite, (int(self.x-sprite.width/2),int(self.y-sprite.height/2)), sprite)
            self.icon, self.sprite = None, None
            self.orig_img = tmp
            self.img = ImageTk.PhotoImage(self.orig_img)
            self.canvas.itemconfig(self.image_container,image=self.img)
            self.sprite = None


    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        self.x,self.y = int(event.x/self.scale) * self.scale , int(event.y/self.scale) * self.scale
        if self.zimg_id: self.canvas.delete(self.zimg_id)
        if (self.zoomcycle) != 0:
            if self.zoomcycle == 1:
                tmp = self.orig_img.crop((self.x-64,self.y-64,self.x+64,self.y+64))
                scale = 2
            elif self.zoomcycle == 2:
                tmp = self.orig_img.crop((self.x-32,self.y-32,self.x+32,self.y+32))
                scale = 2
            elif self.zoomcycle == 3:
                tmp = self.orig_img.crop((self.x-16,self.y-16,self.x+16,self.y+16))
                scale = 2.75
            elif self.zoomcycle == 4:
                tmp = self.orig_img.crop((self.x-8,self.y-8,self.x+8,self.y+8))
                scale = 4
            size = 256,256
            if self.icon != None:
                self.sprite = self.sprites.crop((8*bannerDict[self.icon][0], 8*bannerDict[self.icon][1], 8 + 8*bannerDict[self.icon][0], 8 + 8*bannerDict[self.icon][1])).rotate(self.rotation)
                sprite = self.sprite.resize((8*int(self.zoomcycle*scale)*self.scale, 8*int(self.zoomcycle*scale)*self.scale), self.filter)
                tmp = tmp.resize(size, self.filter).convert("RGBA")
                tmp.paste(sprite.convert("RGBA"), (int(256/2-sprite.width/2),int(256/2-sprite.height/2)), sprite.convert("RGBA"))
                
            self.zimg = ImageTk.PhotoImage(Image.alpha_composite(tmp.resize(size, self.filter).convert("RGBA"), self.spy.convert("RGBA")))
            self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg)
        else:
            if self.icon != None:
                scale = 1
                self.sprite = self.sprites.crop((8*bannerDict[self.icon][0], 8*bannerDict[self.icon][1], 8 + 8*bannerDict[self.icon][0], 8 + 8*bannerDict[self.icon][1])).rotate(self.rotation)
                self.zimg = ImageTk.PhotoImage(self.sprite.convert("RGBA").resize((8*self.scale, 8*self.scale), self.filter))
                self.zimg_id = self.canvas.create_image(self.x,self.y,image=self.zimg)

    def delete(self):
        self.canvas.delete('all')
        self.frame.destroy()