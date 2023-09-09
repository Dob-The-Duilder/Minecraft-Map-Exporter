import numpy as np
from PIL import Image
import gzip, os, struct

import nbtlib
from nbtlib.tag import ByteArray

Image.MAX_IMAGE_PIXELS = None
colorTuple = ((0,0,0), (0,0,0), (0,0,0), (0,0,0), (90,126,39), (109,153,48), (127,178,56), (67,94,29), (175,165,115), (212,200,140), (247,233,163), (130,123,86), (141,141,141), (171,171,171), (199,199,199), (105,105,105), (181,0,0), (219,0,0), (255,0,0), (135,0,0), (113,113,181), (137,137,219), (160,160,255), (84,84,135), (118,118,118), (143,143,143), (167,167,167), (88,88,88), (0,88,0), (0,106,0), (0,124,0), (0,65,0), (181,181,181), (219,219,219), (255,255,255), (135,135,135), (116,119,130), (141,144,158), (164,168,184), (86,89,97), (107,77,54), (129,93,66), (151,109,77), (80,57,40), (79,79,79), (96,96,96), (112,112,112), (59,59,59), (45,45,181), (55,55,219), (64,64,255), (33,33,135), (101,84,51), (122,102,61), (143,119,72), (75,63,38), (181,178,173), (219,216,210), (255,252,245), (135,133,129), (153,90,36), (185,109,43), (216,127,51), (114,67,27), (126,53,153), (153,65,185), (178,76,216), (94,40,114), (72,108,153), (87,131,185), (102,153,216), (54,81,114), (162,162,36), (196,196,43), (229,229,51), (121,121,27), (90,144,17), (109,175,21), (127,204,25), (67,108,13), (171,90,117), (208,109,141), (242,127,165), (128,67,87), (53,53,53), (65,65,65), (76,76,76), (40,40,40), (108,108,108), (131,131,131), (153,153,153), (81,81,81), (53,90,108), (65,109,131), (76,127,153), (40,67,81), (90,44,126), (109,54,153), (127,63,178), (67,33,94), (36,53,126), (43,65,153), (51,76,178), (27,40,94), (72,53,36), (87,65,43), (102,76,51), (54,40,27), (72,90,36), (87,109,43), (102,127,51), (54,67,27), (108,36,36), (131,43,43), (153,51,51), (81,27,27), (17,17,17), (21,21,21), (25,25,25), (13,13,13), (177,168,54), (215,204,66), (250,238,77), (132,126,40), (65,155,151), (79,188,183), (92,219,213), (48,116,112), (52,90,181), (63,110,219), (74,128,255), (39,67,135), (0,154,41), (0,186,49), (0,217,58), (0,115,30), (91,61,34), (110,73,42), (129,86,49), (68,45,25), (79,1,0), (96,1,0), (112,2,0), (59,1,0), (148,125,114), (179,152,138), (209,177,161), (110,93,85), (112,58,25), (136,70,30), (159,82,36), (84,43,19), (105,61,76), (128,74,92), (149,87,108), (78,46,57), (79,76,97), (96,92,118), (112,108,138), (59,57,73), (132,94,25), (159,114,30), (186,133,36), (98,70,19), (73,83,37), (88,100,45), (103,117,53), (54,62,28), (113,54,55), (137,66,67), (160,77,78), (84,40,41), (40,29,24), (49,35,30), (57,41,35), (30,21,18), (95,75,69), (116,92,84), (135,107,98), (71,56,51), (61,65,65), (74,79,79), (87,92,92), (46,48,48), (86,51,62), (104,62,75), (122,73,88), (64,38,46), (53,44,65), (65,53,79), (76,62,92), (40,32,48), (53,35,24), (65,43,30), (76,50,35), (40,26,18), (54,58,30), (65,70,36), (76,82,42), (40,43,22), (100,42,32), (122,51,39), (142,60,46), (75,31,24), (26,15,11), (31,18,13), (37,22,16), (19,11,8), (134,34,34), (162,41,42), (189,48,49), (100,25,25), (105,44,68), (127,54,83), (148,63,97), (78,33,51), (65,17,20), (79,21,24), (92,25,29), (48,13,15), (15,89,95), (18,108,115), (22,126,134), (11,66,71), (41,100,99), (49,122,120), (58,142,140), (30,75,74), (61,31,44), (73,37,53), (86,44,62), (45,23,32), (14,127,94), (17,154,114), (20,180,133), (10,95,70), (71,71,71), (86,86,86), (100,100,100), (53,53,53), (153,124,104), (185,150,126), (216,175,147), (114,92,77), (90,118,106), (109,143,129), (127,167,150), (67,88,79))

#  colorTuple = tuple(tuple(i) for i in colorList)

bannerDict = {
    'arrow'     : (1, 0),
    'white'     : (0, 4),
    'light_gray': (1, 4),
    'gray'      : (2, 4),
    'black'     : (3, 4),
    'red'       : (0, 5),
    'orange'    : (1, 5),
    'yellow'    : (2, 5),
    'lime'      : (3, 5),
    'green'     : (0, 6),
    'blue'      : (1, 6),
    'cyan'      : (2, 6),
    'light_blue': (3, 6),
    'pink'      : (0, 7),
    'magenta'   : (1, 7),
    'purple'    : (2, 7),
    'brown'     : (3, 7)
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

def closest_color(color, colors):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return tuple(smallest_distance[0])

def makeImgs(imagePath, nbtPath):        
    img = Image.open(imagePath).convert('RGB')
    pixels = []
    colors = []

    if (img.size != (128, 128)): img = img.resize((128, 128))
    
    print(img.getpixel((0,0)))
    
    for y in range(0, 128, 1):
        for x in range(0, 128, 1):
            colorTemp = closest_color(img.getpixel((x, y)), colorTuple)
            colors.append(colorTemp)
            colorVal = colorTuple.index(colorTemp)
            if (colorVal > 129):
                colorVal = colorVal - len(colorTuple) - 8
            pixels.append(colorVal)
    
    with nbtlib.load(nbtPath) as map:
        map['data']['colors'] = ByteArray(pixels)
        
    array = np.array(colors, dtype=np.uint8).reshape(128, 128, 3)
    print(array)
    
    return Image.fromarray(array, 'RGB')

def makeMaps(pathSetting, path, merge, extras):
    folder_path = pathSetting
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    coordX, coordZ, size = None, None, None
    
    mapInt = os.path.basename(path).replace('map_','').replace('.dat','')

    with gzip.open(path, mode='rb') as map:
        in_stream = InputStream(map.read())
        map_data = parse_nbt(in_stream)      
        blocksList = tuple(map_data.get('data').get('colors').get())
        if merge or extras:
            coordX = map_data.get('data').get('xCenter').get()
            coordZ = map_data.get('data').get('zCenter').get()
            size = map_data.get('data').get('scale').get()
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


    array = np.array(pixels, dtype=np.uint8)

    new_image = Image.fromarray(array, 'RGB')
    newPath = "".join([folder_path,'/map_',str(mapInt),'.png'])
    if extras:
        try:
            new_image = extraAdd(banList, frmList, new_image, coordX, coordZ)
        except:
            pass
    new_image.save(newPath)
    
    return[128,128, new_image, size, coordX, coordZ]

def extraAdd(banList, frmList, new_image, coordsX, coordsZ):
    banList = banList.replace(" Pos size 3 = {IntTag 'X' = ", '').replace('IntTag ', '').replace(" 'Y' = ", '').replace(" 'Z' = ", '').replace("}], StringTag: Color = '", ',').replace("'}], ", '').replace("'}]]", '').split('CompundTag:')
    frmList = frmList.replace(" Pos size 3 = {IntTag 'X' = ", '').replace('IntTag ', '').replace(" 'Y' = ", '').replace(" 'Z' = ", '').replace("}], 'Rotation' = ", ',').replace("}], ", '').replace("}]]", '').split('CompundTag:')

    sprites = Image.open('Sprites.png')
    
    if len(banList) > 1:
        banList.pop(0)
        banList = banList[1::2]
        for x in range(len(banList)):
            banList[x] = banList[x].split(',')
        banX = coordsX - 61
        banZ = coordsZ - 60
        banPos = []
        for banner in banList:
            banPos.append((-(banX - int(banner[0])), -(banZ - int(banner[2])), banner[3].replace("'", ""))) 
        for banner in banPos:
                try:
                    subSprite = sprites.crop((8*bannerDict[banner[2]][0], 8*bannerDict[banner[2]][1], 8 + 8*bannerDict[banner[2]][0], 8 + 8*bannerDict[banner[2]][1]))
                    new_image.paste(subSprite, (banner[0], banner[1]), subSprite.convert('RGBA'))
                except:
                    pass
    if len(frmList) > 1:
        frmList.pop(0)
        frmList = frmList[1::2]
        frmX = coordsX - 61
        frmZ = coordsZ - 60
        frmPos = []
        for frame in frmList:
            frame = frame.split(',')
            frmPos.append((-(frmX - int(frame[0])), -(frmZ - int(frame[2])), -int(frame[3])))
        for frame in frmPos:
            try:
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
            except:
                pass
    return new_image

def imageCombine(coordsX, coordsZ, imgList, sizList, folder_path):
    if len(sizList) == 0:
        return [128,128, imgList[0], 'Not enought images.']
    if (np.max(sizList) != np.min(sizList)): 
        return [128,128, imgList[0], 'Maps are not the same scale.']

    image_size = ((max(coordsX)-min(coordsX)+128),(max(coordsZ)-min(coordsZ)+128))
    combo = Image.new('RGB', image_size)
    for i in range(0, len(imgList), 1):
        combo.paste(imgList[i], ((coordsX[i]-min(coordsX)),(coordsZ[i]-min(coordsZ))))
        combo.save(folder_path + '/Full Map.png')
    
    return [image_size[0],image_size[1],combo, folder_path + '/Full Map.png', '']

def imageCombineMulti(coordsX, coordsZ, imgList, sizList, folder_path):
    if len(sizList) == 0:
        return [128,128, imgList[0], 'Not enought images.']

    zoom0, zoom1, zoom2, zoom3, zoom4, btmRt = [],[],[],[],[],[]

    for item in range(0, len(imgList), 1):
        if sizList[item] > 0:
            size = 128*(2**sizList[item]),128*(2**sizList[item])
            imgList[item] = imgList[item].resize(size, Image.Resampling.NEAREST)
        if sizList[item] == 4: 
            zoom4.append(item)
            coordsX[item] -= 1024
            coordsZ[item] -= 1024
            btmRt.append((coordsX[item] + 2048, coordsZ[item] + 2048))
        elif sizList[item] == 3: 
            zoom3.append(item)
            coordsX[item] -= 512
            coordsZ[item] -= 512
            btmRt.append((coordsX[item] + 1024, coordsZ[item] + 1024))
        elif sizList[item] == 2: 
            zoom2.append(item)
            coordsX[item] -= 256
            coordsZ[item] -= 256
            btmRt.append((coordsX[item] + 512, coordsZ[item] + 512))
        elif sizList[item] == 1: 
            zoom1.append(item)
            coordsX[item] -= 128
            coordsZ[item] -= 128
            btmRt.append((coordsX[item] + 256, coordsZ[item] + 256))
        else: 
            zoom0.append(item)
            coordsX[item] -= 64
            coordsZ[item] -= 64
            btmRt.append((coordsX[item] + 128, coordsZ[item] + 128))
    
    image_size = 2048,2048
    image_size = (max(btmRt, key=lambda tup: tup[0])[0]-min(coordsX),max(btmRt, key=lambda tup: tup[1])[1]-min(coordsZ))
    combo = Image.new('RGB', image_size)

    for index in zoom4:
        combo.paste(imgList[index], ((coordsX[index]-min(coordsX)),(coordsZ[index]-min(coordsZ))))
    for index in zoom3:
        combo.paste(imgList[index], ((coordsX[index]-min(coordsX)),(coordsZ[index]-min(coordsZ))))
    for index in zoom2:
        combo.paste(imgList[index], ((coordsX[index]-min(coordsX)),(coordsZ[index]-min(coordsZ))))
    for index in zoom1:
        combo.paste(imgList[index], ((coordsX[index]-min(coordsX)),(coordsZ[index]-min(coordsZ))))
    for index in zoom0:
        combo.paste(imgList[index], ((coordsX[index]-min(coordsX)),(coordsZ[index]-min(coordsZ))))

    combo.save(folder_path + '/Full Map.png')
    
    return [image_size[0],image_size[1],combo, folder_path + '/Full Map.png', '']

def write_string(stream, string):
    stream.write(len(string).to_bytes(2, byteorder='big', signed=False))
    for c in string:
        stream.write(ord(c).to_bytes(1, byteorder='big', signed=False))

def register_parser(id, clazz):
    global _parsers

    _parsers[id] = clazz

def create_simple_nbt_class(tag_id, class_tag_name, tag_width, tag_parser):

    class DataNBTTag:

        clazz_width = tag_width
        clazz_name = class_tag_name
        clazz_parser = tag_parser
        clazz_id = tag_id

        @classmethod
        def parse(cls, stream, name):
            return cls(
                tag_value=struct.unpack(
                    cls.clazz_parser, 
                    stream.read(cls.clazz_width)
                )[0],
                tag_name=name
            )

        def __init__(self, tag_value, tag_name='None'):
            int(tag_value)
            self.tag_name = tag_name
            self.tag_value = tag_value

        def print(self, indent=''):
            print(indent + self.__repr__())

        def get(self):
            return self.tag_value

        def name(self):
            return self.tag_name

        def serialize(self, stream, include_name=True):
            if include_name:
                stream.write(type(self).clazz_id.to_bytes(1, byteorder='big', signed=False))
                write_string(stream, self.tag_name)

            stream.write(struct.pack(type(self).clazz_parser, self.tag_value))

        def clone(self):
            return type(self)(self.tag_value, tag_name=self.tag_name)

        def __repr__(self):
            return f'{type(self).clazz_name}Tag \'{self.tag_name}\' = {str(self.tag_value)}'

        def __eq__(self, other):
            return self.tag_name == other.tag_name and self.tag_value == other.tag_value

    register_parser(tag_id, DataNBTTag)

    return DataNBTTag

def create_string_nbt_class(tag_id):
    class DataNBTTag:

        clazz_id = tag_id

        @classmethod
        def parse(cls, stream, name):
            payload_length = int.from_bytes(stream.read(2), byteorder='big', signed=False)
            payload = stream.read(payload_length).decode('utf-8')
            return cls(payload, tag_name=name)

        def __init__(self, tag_value, tag_name='None'):
            self.tag_name = tag_name
            self.tag_value = tag_value

        def print(self, indent=''):
            print(indent + 'String: ' + self.tag_name + ' = ' + str(self.tag_value))

        def get(self):
            return self.tag_value

        def name(self):
            return self.tag_name

        def serialize(self, stream, include_name=True):
            if include_name:
                stream.write(type(self).clazz_id.to_bytes(1, byteorder='big', signed=False))
                write_string(stream, self.tag_name)
            
            stream.write(len(self.tag_value).to_bytes(2, byteorder='big',signed=False))
            for c in self.tag_value:
                stream.write(ord(c).to_bytes(1, byteorder='big', signed=False))

        def clone(self):
            return type(self)(self.tag_value, tag_name=self.tag_name)

        def __repr__(self):
            return f'StringTag: {self.tag_name} = \'{self.tag_value}\''

        def __eq__(self, other):
            return self.tag_name == other.tag_name and self.tag_value == other.tag_value

    register_parser(tag_id, DataNBTTag)

    return DataNBTTag

def create_array_nbt_class(tag_id, tag_name, sub_type):
    class ArrayNBTTag:

        clazz_sub_type = sub_type
        clazz_name = tag_name
        clazz_id = tag_id

        @classmethod
        def parse(cls, stream, name):
            payload_length = int.from_bytes(stream.read(4), byteorder='big', signed=True)
            tag = cls(tag_name=name)
            for _i in range(payload_length):
                tag.add_child(cls.clazz_sub_type.parse(stream, 'None'))
            return tag

        def __init__(self, tag_name='None', children=[]):
            self.tag_name = tag_name
            self.children = children[:]
        
        def add_child(self, tag):
            self.children.append(tag)

        def name(self):
            return self.tag_name

        def print(self, indent=''):
            str_dat = ', '.join([str(c.get()) for c in self.children])
            print(f'{indent}{type(self).clazz_name}: {self.tag_name} size {str(len(self.children))} = [{str_dat}]')

        def get(self):
            return [int(c.get()) for c in self.children]

        def serialize(self, stream, include_name=True):
            if include_name:
                stream.write(type(self).clazz_id.to_bytes(1, byteorder='big', signed=False))
                write_string(stream, self.tag_name)
                
            stream.write(len(self.children).to_bytes(4, byteorder='big', signed=True))

            for tag in self.children:
                tag.serialize(stream, include_name=False)

        def clone(self):
            return type(self)(tag_name=self.tag_name, children=[c.clone() for c in self.children])

        def __repr__(self):
            str_dat = ', '.join([str(c.get()) for c in self.children])
            return f'{type(self).clazz_name}: {self.tag_name} size {str(len(self.children))} = [{str_dat}]'

        def __eq__(self, other):
            return self.tag_name == other.tag_name and \
                len(self.children) == len(other.children) and \
                not any(not self.children[i] == other.children[i] for i in range(len(self.children)))

    register_parser(tag_id, ArrayNBTTag)

    return ArrayNBTTag

def create_list_nbt_class(tag_id):
    class ListNBTTag:

        clazz_id = tag_id

        @classmethod
        def parse(cls, stream, name):
            global _parsers

            sub_type = int.from_bytes(stream.read(1), byteorder='big', signed=False)
            payload_length = int.from_bytes(stream.read(4), byteorder='big', signed=True)
            tag = cls(sub_type, tag_name=name)
            for _i in range(payload_length):
                tag.add_child(_parsers[sub_type].parse(stream, 'None'))
            return tag

        def __init__(self, sub_type_id, tag_name='None', children=[]):
            self.tag_name = tag_name
            self.sub_type_id = sub_type_id
            self.children = children[:]
        
        def add_child(self, tag):
            self.children.append(tag)

        def get(self):
            return [c.get() for c in self.children]

        def name(self):
            return self.tag_name

        def print(self, indent=''):
            print(indent + 'List: ' + self.tag_name + ' size ' + str(len(self.children)))
            for c in self.children:
                c.print(indent + '  ')
        
        def serialize(self, stream, include_name=True):
            if include_name:
                stream.write(type(self).clazz_id.to_bytes(1, byteorder='big', signed=False))
                write_string(stream, self.tag_name)
            
            stream.write(self.sub_type_id.to_bytes(1, byteorder='big', signed=False))
            stream.write(len(self.children).to_bytes(4, byteorder='big', signed=True))

            for tag in self.children:
                tag.serialize(stream, include_name=False)

        def clone(self):
            return type(self)(self.sub_type_id, tag_name=self.tag_name, children=[c.clone() for c in self.children])

        def __repr__(self):
            str_dat = ', '.join([c.__repr__() for c in self.children])
            return f'ListTag: {self.tag_name} size {str(len(self.children))} = [{str_dat}]'

        def __eq__(self, other):
            return self.tag_name == other.tag_name and \
                len(self.children) == len(other.children) and \
                (len(self.children) == 0 or not any(not self.children[i] == other.children[i] for i in range(len(self.children))))

    register_parser(tag_id, ListNBTTag)

    return ListNBTTag

def create_compund_nbt_class(tag_id):
    class CompundNBTTag:

        clazz_id = tag_id

        @classmethod
        def parse(cls, stream, name):
            tag = cls(tag_name=name)
            while stream.peek() != 0:
                tag.add_child(parse_nbt(stream))
            stream.read(1)
            return tag

        def __init__(self, tag_name='None', children=[]):
            self.tag_name = tag_name
            self.children = { c.tag_name: c for c in children[:] }
        
        def add_child(self, tag):
            self.children[tag.tag_name] = tag

        def get(self, name):
            return self.children[name]

        def name(self):
            return self.tag_name

        def has(self, name):
            return name in self.children

        def to_dict(self):
            nd = {}
            for p in self.children:
                nd[p] = self.children[p].get()
            return nd

        def print(self, indent=''):
            print(indent + 'Compound: ' + self.tag_name + ' size ' + str(len(self.children)))
            for c in self.children:
                self.children[c].print(indent + '  ')

        def serialize(self, stream, include_name=True):
            if include_name:
                stream.write(type(self).clazz_id.to_bytes(1, byteorder='big', signed=False))
                write_string(stream, self.tag_name)
            
            for tag_name in self.children:
                self.children[tag_name].serialize(stream, include_name=True)
            
            stream.write((0).to_bytes(1, byteorder='big', signed=False))

        def clone(self):
            return type(self)(tag_name=self.tag_name, children=[v.clone() for k, v in self.children.items()])

        def __repr__(self):
            str_dat = ', '.join([c.__repr__() for name, c in self.children.items()])
            return f'CompundTag: {self.tag_name} size {str(len(self.children))} = {{{str_dat}}}]'

        def __eq__(self, other):
            passed = True
            for name, v in self.children.items():
                if name not in other.children:
                    passed = False
                elif other.children[name] != v:
                    passed = False
            return self.tag_name == other.tag_name and \
                len(self.children) == len(other.children) and \
                passed

    register_parser(tag_id, CompundNBTTag)

    return CompundNBTTag

_parsers = {}

ByteTag = create_simple_nbt_class(1, 'Byte', 1, '>b')
ShortTag = create_simple_nbt_class(2, 'Short', 2, '>h')
IntTag = create_simple_nbt_class(3, 'Int', 4, '>i')
LongTag = create_simple_nbt_class(4, 'Long', 8, '>q')
FloatTag = create_simple_nbt_class(5, 'Float', 4, '>f')
DoubleTag = create_simple_nbt_class(6, 'Double', 8, '>d')

ByteArrayTag = create_array_nbt_class(7, 'ByteArray', ByteTag)

StringTag = create_string_nbt_class(8)
ListTag = create_list_nbt_class(9)
CompoundTag = create_compund_nbt_class(10)

IntArrayTag = create_array_nbt_class(11, 'IntArray', IntTag)
LongArrayTag = create_array_nbt_class(12, 'LongArray', LongTag)

def parse_nbt(stream):
    global _parsers

    tag_type = int.from_bytes(stream.read(1), byteorder='big', signed=False)
    tag_name_length = int.from_bytes(stream.read(2), byteorder='big', signed=False)
    tag_name = stream.read(tag_name_length).decode('utf-8')
    
    return _parsers[tag_type].parse(stream, tag_name)