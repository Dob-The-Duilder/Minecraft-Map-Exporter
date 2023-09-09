from tkinter import Frame, Canvas
from PIL import Image, ImageTk

spritesDict = {"player_White":(0, 0), "player_Green":(8, 0), "player_Red":(16, 0), "player_Blue":(24, 0),
               "temple_Jungle Temple":(0, 8), "temple_Witch Hut":(8, 8), "temple_Woodland Mansion":(16, 8), "temple_Ocean Monument":(24, 8),
               "hamlet_Plains Village":(0,16), "hamlet_Savanna Village":(8,16), "hamlet_Snowy Village":(16,16), "hamlet_Taiga Village":(24,16),
               "hamlet_Desert Village":(0,24), "unused_Red X":(8,24), "unused_Target X":(16,24), "unused_Target Point":(24,24),
               "banner_White":(0,32), "banner_Light Grey":(8,32), "banner_Grey":(16,32), "banner_Black":(24,32),
               "banner_Red":(0,40), "banner_Orange":(8,40), "banner_Yellow":(16,40), "banner_Lime":(24,40),
               "banner_Green":(0,48), "banner_Blue":(8,48), "banner_Cyan":(16,48), "banner_Light Blue":(24,48),
               "banner_Pink":(0,56), "banner_Magenta":(8,56), "banner_Purple":(16,56), "banner_Brown":(24,56)}

class LoadImage:
    def __init__(self,root,file,path_):
        self.frame = Frame(root)
        
        self.orig_img = file
        self.path = path_
        self.new_img = self.orig_img
        self.wid, self.hei = self.orig_img.size
        scaleX = int(610/self.wid)
        scaleZ = int(610/self.hei)
        self.scale = max(min(scaleX, scaleZ), 1)
        self.zoomScale = 1
        self.orig_img = self.orig_img.resize((self.wid*self.scale, self.hei*self.scale),Image.Resampling.NEAREST)
        self.wid, self.hei = self.orig_img.size
        self.backImg = self.orig_img
        self.widBack, self.heiBack = self.backImg.size

        if self.wid > 900 or self.hei > 900:
            self.zoomScale = 2
            self.backImg = self.backImg.resize((int(self.wid*0.5), int(self.hei*0.5)),Image.Resampling.NEAREST)
            self.widBack, self.heiBack = self.backImg.size

        root.geometry(str(self.widBack) + "x" + str(self.heiBack+25))
        
        File2 = "overlay.png"
        self.spy = Image.open(File2)
        self.spyWid, self.spyHei = self.backImg.size
        
        self.sprites = Image.open("Sprites.png")
        self.sprite = None
        self.rotation = 0
        self.icon = None
        
        self.canvas = Canvas(self.frame,width=self.wid,height=self.hei)
        self.canvas.pack()
        self.frame.pack()
        self.filter = Image.Resampling.NEAREST
        self.img = ImageTk.PhotoImage(self.backImg)
        self.image_container = self.canvas.create_image(0,0,image=self.img, anchor="nw")

        self.zoomcycle = 0
        self.zimg_id = None

        root.bind("<Button-1>",self.stamp)
        root.bind("<MouseWheel>",self.zoomer)
        root.bind("<KeyPress-r>",self.rotate)
        self.canvas.bind("<Motion>",self.crop)

    def rotate(self,event):
        self.rotation += 90
        event.y -= 22
        self.crop(event)
    
    def stamp(self,event):
        if self.sprite and (0 < self.x < self.widBack-1)and (0 < self.y < self.heiBack-1):
            tmp = self.orig_img
            sprite = self.sprite.resize(( 8*self.scale, 8*self.scale), self.filter).convert("RGBA")
            tmp.paste(sprite, (int(self.x-sprite.width/2),int(self.y-sprite.height/2)), sprite)
            self.icon, self.sprite = None, None
            self.orig_img = tmp
            if self.zoomScale == 2:
                tmp = tmp.resize((int(self.wid*0.5), int(self.hei*0.5)),Image.Resampling.NEAREST)
            self.img = ImageTk.PhotoImage(tmp)
            self.canvas.itemconfig(self.image_container,image=self.img)
            self.sprite = None

    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        self.x,self.y = int(event.x/self.scale) * self.scale * self.zoomScale, int(event.y/self.scale) * self.scale * self.zoomScale
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
            if self.icon is not None:
                self.sprite = self.sprites.crop((spritesDict[self.icon][0], spritesDict[self.icon][1], 8 + spritesDict[self.icon][0], 8 + spritesDict[self.icon][1])).rotate(self.rotation)
                sprite = self.sprite.resize((8*int(self.zoomcycle*scale)*self.scale, 8*int(self.zoomcycle*scale)*self.scale), self.filter)
                tmp = tmp.resize(size, self.filter).convert("RGBA")
                tmp.paste(sprite.convert("RGBA"), (int(256/2-sprite.width/2),int(256/2-sprite.height/2)), sprite.convert("RGBA"))
                
            self.zimg = ImageTk.PhotoImage(Image.alpha_composite(tmp.resize(size, self.filter).convert("RGBA"), self.spy.convert("RGBA")))
            self.zimg_id = self.canvas.create_image(min(self.wid-130, max(130, event.x)),min(self.hei-128, max(128, event.y)),image=self.zimg)
        else:
            if self.icon is not None:
                scale = 1
                self.sprite = self.sprites.crop((spritesDict[self.icon][0], spritesDict[self.icon][1], 8 + spritesDict[self.icon][0], 8 + spritesDict[self.icon][1])).rotate(self.rotation)
                self.zimg = ImageTk.PhotoImage(self.sprite.convert("RGBA").resize((8*self.scale, 8*self.scale), self.filter))
                self.zimg_id = self.canvas.create_image(self.x,self.y,image=self.zimg)

    def delete(self):
        self.canvas.delete('all')
        self.frame.destroy()