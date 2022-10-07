import numpy as np
from PIL import Image
from nbt import parse_nbt
import time
import gzip, os, itertools

Image.MAX_IMAGE_PIXELS = None
colorTuple = ((0,0,0), (0,0,0), (0,0,0), (0,0,0), (90,126,39), (109,153,48), (127,178,56), (67,94,29), (175,165,115), (212,200,140), (247,233,163), (130,123,86), (141,141,141), (171,171,171), (199,199,199), (105,105,105), (181,0,0), (219,0,0), (255,0,0), (135,0,0), (113,113,181), (137,137,219), (160,160,255), (84,84,135), (118,118,118), (143,143,143), (167,167,167), (88,88,88), (0,88,0), (0,106,0), (0,124,0), (0,65,0), (181,181,181), (219,219,219), (255,255,255), (135,135,135), (116,119,130), (141,144,158), (164,168,184), (86,89,97), (107,77,54), (129,93,66), (151,109,77), (80,57,40), (79,79,79), (96,96,96), (112,112,112), (59,59,59), (45,45,181), (55,55,219), (64,64,255), (33,33,135), (101,84,51), (122,102,61), (143,119,72), (75,63,38), (181,178,173), (219,216,210), (255,252,245), (135,133,129), (153,90,36), (185,109,43), (216,127,51), (114,67,27), (126,53,153), (153,65,185), (178,76,216), (94,40,114), (72,108,153), (87,131,185), (102,153,216), (54,81,114), (162,162,36), (196,196,43), (229,229,51), (121,121,27), (90,144,17), (109,175,21), (127,204,25), (67,108,13), (171,90,117), (208,109,141), (242,127,165), (128,67,87), (53,53,53), (65,65,65), (76,76,76), (40,40,40), (108,108,108), (131,131,131), (153,153,153), (81,81,81), (53,90,108), (65,109,131), (76,127,153), (40,67,81), (90,44,126), (109,54,153), (127,63,178), (67,33,94), (36,53,126), (43,65,153), (51,76,178), (27,40,94), (72,53,36), (87,65,43), (102,76,51), (54,40,27), (72,90,36), (87,109,43), (102,127,51), (54,67,27), (108,36,36), (131,43,43), (153,51,51), (81,27,27), (17,17,17), (21,21,21), (25,25,25), (13,13,13), (177,168,54), (215,204,66), (250,238,77), (132,126,40), (65,155,151), (79,188,183), (92,219,213), (48,116,112), (52,90,181), (63,110,219), (74,128,255), (39,67,135), (0,154,41), (0,186,49), (0,217,58), (0,115,30), (91,61,34), (110,73,42), (129,86,49), (68,45,25), (79,1,0), (96,1,0), (112,2,0), (59,1,0), (148,125,114), (179,152,138), (209,177,161), (110,93,85), (112,58,25), (136,70,30), (159,82,36), (84,43,19), (105,61,76), (128,74,92), (149,87,108), (78,46,57), (79,76,97), (96,92,118), (112,108,138), (59,57,73), (132,94,25), (159,114,30), (186,133,36), (98,70,19), (73,83,37), (88,100,45), (103,117,53), (54,62,28), (113,54,55), (137,66,67), (160,77,78), (84,40,41), (40,29,24), (49,35,30), (57,41,35), (30,21,18), (95,75,69), (116,92,84), (135,107,98), (71,56,51), (61,65,65), (74,79,79), (87,92,92), (46,48,48), (86,51,62), (104,62,75), (122,73,88), (64,38,46), (53,44,65), (65,53,79), (76,62,92), (40,32,48), (53,35,24), (65,43,30), (76,50,35), (40,26,18), (54,58,30), (65,70,36), (76,82,42), (40,43,22), (100,42,32), (122,51,39), (142,60,46), (75,31,24), (26,15,11), (31,18,13), (37,22,16), (19,11,8), (134,34,34), (162,41,42), (189,48,49), (100,25,25), (105,44,68), (127,54,83), (148,63,97), (78,33,51), (65,17,20), (79,21,24), (92,25,29), (48,13,15), (15,89,95), (18,108,115), (22,126,134), (11,66,71), (41,100,99), (49,122,120), (58,142,140), (30,75,74), (61,31,44), (73,37,53), (86,44,62), (45,23,32), (14,127,94), (17,154,114), (20,180,133), (10,95,70), (71,71,71), (86,86,86), (100,100,100), (53,53,53), (153,124,104), (185,150,126), (216,175,147), (114,92,77), (90,118,106), (109,143,129), (127,167,150), (67,88,79))

bannerDict = { 
    'white'     : (0, 0),
    'light_gray': (1, 0),
    'gray'      : (2, 0),
    'black'     : (3, 0),
    'red'       : (0, 1),
    'orange'    : (1, 1),
    'yellow'    : (2, 1),
    'lime'      : (3, 1),
    'green'     : (0, 2),
    'blue'      : (1, 2),
    'cyan'      : (2, 2),
    'light_blue': (3, 2),
    'pink'      : (0, 3),
    'magenta'   : (1, 3),
    'purple'    : (2, 3),
    'brown'     : (3, 3)
    }
textBack = (0, 0, 0, 127)

class InputStream:
    def __init__(self, data):
        self.pos = 0
        self.buffer = data

    def read(self, num):
        rtn = self.buffer[self.pos:self.pos + num]
        self.pos = self.pos + num
        return rtn

    def peek(self):
        return self.buffer[self.pos]

def makeMaps(pathSetting, path, merge, extras):
    folder_path = pathSetting
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    coordsX, coordsZ, imgList, sizList = [], [], [], []
    
    mapInt = os.path.basename(path).replace('map_','').replace('.dat','')

    with gzip.open(path, mode='rb') as map:
        in_stream = InputStream(map.read())
        map_data = parse_nbt(in_stream)      
        blocksList = tuple(map_data.get('data').get('colors').get())
        if (bool(merge) == True) or (bool(extras) == True):
            coordsX.append(map_data.get('data').get('xCenter').get())
            coordsZ.append(map_data.get('data').get('zCenter').get())
            sizList.append(map_data.get('data').get('scale').get())
            try:    
                banList = str(map_data.get('data').get('banners'))
                frmList = str(map_data.get('data').get('frames'))
            except:
                banList = 'N'
                frmList = 'N'
    pixels = []

    for y in range(0, 128, 1):
      pixels.append([])
      for x in range(0, 128, 1):
        num = int(blocksList[(y*128) + x])
        if(0 < num < 129):
          pixels[y].append(colorTuple[num])
        elif(num < 0):
          #The +4 in this is due to minecraft only using 248 of the 256 avalible colors
          pixels[y].append(colorTuple[num+8])
        else:
          pixels[y].append((214, 190, 150))


    # Convert the pixels into an array using numpy
    array = np.array(pixels, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array, 'RGB')
    newPath = "".join([folder_path,'/map_',str(mapInt),'.png'])
    #if bool(extras):
        #new_image = extraAdd(banList, frmList, new_image, coordsX, coordsZ)
    new_image.save(newPath)
    imgList.append(newPath)
    
    return[128,128, new_image]

def extraAdd(banList, frmList, new_image, coordsX, coordsZ):
    banList = banList.replace(" Pos size 3 = {IntTag 'X' = ", '').replace('IntTag ', '').replace(" 'Y' = ", '').replace(" 'Z' = ", '').replace("}], StringTag: Color = '", ',').replace("'}], ", '').replace("'}]]", '').split('CompundTag:')
    frmList = frmList.replace(" Pos size 3 = {IntTag 'X' = ", '').replace('IntTag ', '').replace(" 'Y' = ", '').replace(" 'Z' = ", '').replace("}], 'Rotation' = ", ',').replace("}], ", '').replace("}]]", '').split('CompundTag:')

    sprites = Image.open('Sprites.png')
    
    if len(banList) > 1:
        banList.pop(0)
        banList = banList[1::2]
        for x in range(len(banList)):
            banList[x] = banList[x].split(',')
        banX = coordsX[-1] - 61
        banZ = coordsZ[-1] - 60
        banPos = []
        for banner in banList:
            banPos.append((-(banX - int(banner[0])), -(banZ - int(banner[2])), banner[3])) 
        for banner in banPos:
                try:
                    subSprite = sprites.crop((8*bannerDict[banner[2]][0], 8 + 8*bannerDict[banner[2]][1], 8 + 8*bannerDict[banner[2]][0], 16 + 8*bannerDict[banner[2]][1]))
                    new_image.paste(subSprite, (banner[0], banner[1]), subSprite.convert('RGBA'))
                except:
                    print("Named Banners Not Supported")
                    print(banner)                  
    if len(frmList) > 1:
        frmList.pop(0)
        frmList = frmList[1::2]
        frmX = coordsX[-1] - 61
        frmZ = coordsZ[-1] - 60
        frmPos = []
        for frame in frmList:
            frame = frame.split(',')
            frmPos.append((-(frmX - int(frame[0])), -(frmZ - int(frame[2])), -int(frame[3])))
        for frame in frmPos:
            subSprite = sprites.crop((0, 0, 8, 8)).rotate(frame[2] + 180)
            if frame[2] == 0:
                xOff, zOff  = 0, 1          
            elif frame[2] == -90:
                xOff, zOff = -1, 1
            elif frame[2] == -180:
                xOff, zOff = -1, 0
            else:
                xOff, zOff = 0,0
            new_image.paste(subSprite, (frame[0] + xOff, frame[1] + zOff), subSprite.convert('RGBA'))
    return new_image

def imageCombine(coordsX, coordsZ, imgList, sizList, folder_path, merge, t):
    if len(sizList) == 0:
        return [128,128, imgList[0], t]
    if (sizList.count(sizList[0]) != len(sizList)): 
        t = str(t) + ' Maps not the same scale'
        return [128,128, imgList[0], t]
    scale = sizList[0]

    image_size = ((max(coordsX)-min(coordsX)+128),(max(coordsZ)-min(coordsZ)+128))
    combo = Image.new('RGB', image_size)
    for i in range(0, len(imgList), 1):
        img = Image.open(imgList[i])
        combo.paste(img, ((coordsX[i]-min(coordsX)),(coordsZ[i]-min(coordsZ))))
        combo.save(folder_path + '/Full Map.png')
    
    return [(max(coordsX)-min(coordsX)+128),(max(coordsZ)-min(coordsZ)+128),combo, t]
