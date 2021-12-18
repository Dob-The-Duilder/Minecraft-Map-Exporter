# Minecraft-Map-Exporter
A tool to convert maps from inside the minecraft game to regular PNG files

**To start credit to DonoA for making [PyAnvil](https://github.com/DonoA/PyAnvilEditor), which is what does a lot of the heavy lifting for this program**

## Code Breakdown

This section here opens the dialog box to select any files you want converted, this works for batches of any size.
```python
root = tk.Tk()
paths = filedialog.askopenfilenames(parent=root, title='Choose a file')
```
A list of all the colors that a map uses is then loaded from a text file and cleaned up a bit
```python
colorFile = open('colors.txt', 'r')
colorList = [line.replace('\n', '') for line in colorFile.readlines()]
colorFile.close()
```
### Every step past this point is ran on each selected map file individualy
The next major step is getting the list of block ideas from the map file which is where [PyAnvil](https://github.com/DonoA/PyAnvilEditor) comes in.
```python
mapFile = os.path.basename(path)
mapInt = mapFile.replace('map_','').replace('.dat','')

with gzip.open(path, mode='rb') as map:
  in_stream = InputStream(map.read())
  map_data = nbt.parse_nbt(in_stream)
  blocksList = map_data.get('data').get('colors').get()
```
With both Block-Ids and colors stored in lists its simply a bit of math and a few if statments to figure out which color is which.
```python
for y in range(0, 128, 1):
  pixels.append([])
  for x in range(0, 128, 1):
    num = int(blocksList[(y*128) + x])
    if(0 < num < 129):
      pixels[y].append(eval(colorList[num]))
    elif(num < 0):
      #The +8 in this is due to minecraft only using 248 of the 256 avalible colors
      pixels[y].append(eval(colorList[num+8]))
    else:
      log = log + num + '\n'
      pixels[y].append((00, 00, 00))
```
Every color value was stores into an array of lists and is then converted into individual pixel points on a image which is then saved
```python
# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array, 'RGB')
new_image.save(path.replace(mapFile, '') + 'map_' + str(mapInt) + '.png')
```
