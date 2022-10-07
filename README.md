# Minecraft-Map-Exporter
A tool to convert maps from inside the minecraft game to regular PNG files

**To start credit to DonoA for making [PyAnvil](https://github.com/DonoA/PyAnvilEditor), which is what does a lot of the heavy lifting for this program**

## How to run

### - Beta Downloads
This is the easiest way to run the program is with the compiled windows program. Windows may flag the software as dangerous but I assure everyone it is completly safe. Feel free to ispect the source code yourself. Other than that, the software is pretty self explanitory. If is your first time running the program it may ask you to assign some settings, these are important to the functionality of the program and should not be skipped.

### - Souce Files
Download everything except the previous builds folder. Naviagte to the directory where you have stored all the files and run 'python3 main.py' in command prompt. A GUI should open and there are labeled buttons on the top to help you.

## Code Breakdown

Apon clicking the "Generate Maps" button a dialog box will apear to select any files you want converted, this works for batches of most sizes (Very large batches can sometimes crash the program).
```python
mapGen.makeMaps(settingsList[1][1], filedialog.askopenfilenames(initialdir = settingsList[0][1], parent=mainScreen, title='Choose a file'), settingsList[2][1])
```
A list of all 248 colors that a map uses is hard coded into the program but hopefully soon dynamic mapping will be reintroduced. (Previosly removed due to preformance concerns)
```python
colorTuple = ((0,0,0), (0,0,0), ... , (127,167,150), (67,88,79))
```
### Every step past this point is ran on each selected map file individualy
The next major step is getting the list of block ideas, and various other information, from the map file which is where [PyAnvil](https://github.com/DonoA/PyAnvilEditor) comes in.
```python
  mapInt = os.path.basename(path).replace('map_','').replace('.dat','')

  with gzip.open(path, mode='rb') as map:
      in_stream = InputStream(map.read())
      map_data = nbt.parse_nbt(in_stream)      
      blocksList = tuple(map_data.get('data').get('colors').get())
      if merge == True:
          coordsX += tuple((map_data.get('data').get('xCenter').get()))
          coordsZ += tuple((map_data.get('data').get('zCenter').get()))
          sizList += tuple((map_data.get('data').get('mpScale').get()))
```
With both Block-Ids and colors stored in lists its simply a bit of math and a few if statments to figure out which color is which. The final else statment is purely to handle parts of the map left completly blank and instead contains the color for the empty map texture.
```python
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
```
Every color value was stores into an array of lists and is then converted into individual pixel points on a image which is then saved
```python
array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(array, 'RGB')
        newPath = "".join([folder_path,'/map_',str(mapInt),'.png'])
        new_image.save(newPath)
        imgList.append(newPath)
```

If merging images is selected, and if the total size is small enough, the center X and Y coordinates is retrived from the map file and used to assemble them all together in one image.
