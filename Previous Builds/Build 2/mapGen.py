import numpy as np
from PIL import Image
from PIL import ImageColor
import nbt, gzip, os

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

def makeMaps(pathSetting, paths, merge):
    log = ''

    colorFile = open('colors.txt', 'r')
    colorList = [line.replace('\n', '') for line in colorFile.readlines()]
    colorFile.close()

    folder_path = pathSetting + '/Map Images'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    coordsX = []
    coordsZ = []
    imgList = []
    sizList = []

    for path in paths:
        mapFile = os.path.basename(path)
        mapInt = mapFile.replace('map_','').replace('.dat','')

        with gzip.open(path, mode='rb') as map:
            in_stream = InputStream(map.read())
            map_data = nbt.parse_nbt(in_stream)
            coordsX.append(map_data.get('data').get('xCenter').get())
            coordsZ.append(map_data.get('data').get('zCenter').get())
            sizList.append(map_data.get('data').get('scale').get())          
            blocksList = map_data.get('data').get('colors').get()
            
        path = path.replace(mapFile, folder_path + '/' + mapFile)

        pixels = []

        for y in range(0, 128, 1):
          pixels.append([])
          for x in range(0, 128, 1):
            num = int(blocksList[(y*128) + x])
            if(0 < num < 129):
              pixels[y].append(eval(colorList[num]))
            elif(num < 0):
              #The +4 in this is due to minecraft only using 248 of the 256 avalible colors
              pixels[y].append(eval(colorList[num+8]))
            else:
              log = log + str(num) + '\n'
              pixels[y].append((00, 00, 00))


        # Convert the pixels into an array using numpy
        array = np.array(pixels, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array, 'RGB')
        print(folder_path + '/map_' + str(mapInt) + '.png')
        new_image.save(folder_path + '/map_' + str(mapInt) + '.png')
        imgList.append(folder_path + '/map_' + str(mapInt) + '.png')
    
    return (imageCombine(coordsX, coordsZ, imgList, sizList, folder_path, merge))

def imageCombine(coordsX, coordsZ, imgList, sizList, folder_path, merge):
    
    if (sizList.count(sizList[0]) != len(sizList)): 
        print('Image sizes not equal') 
        return
    scale = sizList[0]

    image_size = ((max(coordsX)-min(coordsX)+128),(max(coordsZ)-min(coordsZ)+128))
    combo = Image.new('RGB', image_size)
    for i in range(0, len(imgList), 1):
        img = Image.open(imgList[i])
        combo.paste(img, ((coordsX[i]-min(coordsX)),(coordsZ[i]-min(coordsZ))))
    if merge == 'True':
        combo.save(folder_path + '/Full Map.png')
    
    return [(max(coordsX)-min(coordsX)+128),(max(coordsZ)-min(coordsZ)+128),combo]
