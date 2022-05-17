import numpy as np
import tkinter as tk
from PIL import Image
from PIL import ImageColor
import nbt, gzip, os
from tkinter import filedialog

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

root = tk.Tk()
root.withdraw()
paths = filedialog.askopenfilenames(parent=root, title='Choose a file')

colorFile = open('colors.txt', 'r')
colorList = [line.replace('\n', '') for line in colorFile.readlines()]
colorFile.close()

folder_path = paths[0].replace(os.path.basename(paths[0]), '') + 'Map Images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

log = ''

for path in paths:
    mapFile = os.path.basename(path)
    mapInt = mapFile.replace('map_','').replace('.dat','')

    with gzip.open(path, mode='rb') as map:
      in_stream = InputStream(map.read())
      map_data = nbt.parse_nbt(in_stream)
      blocksList = map_data.get('data').get('colors').get()
      
    path = path.replace(mapFile, 'Map Images/' + mapFile)

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
    new_image.save(path.replace(mapFile, '') + 'map_' + str(mapInt) + '.png')
    
    if(log != ''):
        print(log)
