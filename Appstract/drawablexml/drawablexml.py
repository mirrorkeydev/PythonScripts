"""
Given: a local directory filled with png icons in the format airbnb.png, etc,
       having mostly 1-4 colors.

Return: a text file with all icons' filenames in the xml format:

        <item drawable="airbnb" />
        <item drawable ="bing" />
        <item drawable = "chrome" />
        ...

    followed by the icons organized by color in the xml format:

        -------------red-------------
        <item drawable ="nameofredicon" />
        <item drawable = "youtube" />
        <item drawable = "netflix" />
        ...
"""

import PIL
import os
import sys
from PIL import Image
import colorsys

inputpath = "C:\\Users\\Melanie\\Google Drive\\MISC\\Appstract\\Icons Light"
outputpath = "Appstract/drawablexml/drawable.xml"

# ---------------FUNCTIONS---------------

def rgb2hsv(r, g, b):  # converts rgb to hsv
  r, g, b = r/255.0, g/255.0, b/255.0
  mx = max(r, g, b)
  mn = min(r, g, b)
  df = mx-mn
  if mx == mn:
    h = 0
  elif mx == r:
    h = (60 * ((g-b)/df) + 360) % 360
  elif mx == g:
    h = (60 * ((b-r)/df) + 120) % 360
  elif mx == b:
    h = (60 * ((r-g)/df) + 240) % 360
  if mx == 0:
    s = 0
  else:
    s = df/mx
  v = mx
  return h, s, v


def getMaxNum(d):  # returns key and value with the greates value in a tuple
  maximum = 0
  maxkey = ()
  for key in d:
    if d[key] > maximum:
      maximum = d[key]
      maxkey = key
  return (maxkey, maximum)


def getColor(path):  # returns either a dominant color (roygbp) or None
  # returns iterable object with pixel rgba values
  data = list(PIL.Image.open(path, mode='r').getdata())
  # will contain {(color): howmanypixels, i.e. (255,255,255): 3, (0,0,0):23, ... etc}
  d = {}

  for pixel in data:
    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0 and pixel[3] == 0:  # rgba for transparent
      continue
    elif pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0 and pixel[3] == 255:  # rgba for pure black
      continue
    else:
      value = (pixel[0], pixel[1], pixel[2])  # rgba -> rgb
      if value in d:
        d[value] += 1
      else:
        d[value] = 1

  greatestkey = getMaxNum(d)[0]
  # greatest value in d; the corresponding key is getMaxNum(d)[0]
  greatestvalue = getMaxNum(d)[1]
  allothervalues = 0  # will contain the sum of all of the other values in d

  for key in d:  # adds up all of the other values in d other than the max
    if key != greatestkey:
      allothervalues += d[key]

  if greatestvalue*0.5 > allothervalues:  # if more than half of the icon is filled with a single color a
    # then classify greatestkey as either r, o, y, g, b, or p
    hue = round(rgb2hsv(greatestkey[0], greatestkey[1], greatestkey[2])[0])
    sat = round(
      rgb2hsv(greatestkey[0], greatestkey[1], greatestkey[2])[1]*100)

    if sat <= 15:
      return "gray"
    elif hue >= 0 and hue < 9:
      return "red"
    elif hue >= 9 and hue < 36:
      return "orange"
    elif hue >= 36 and hue < 80:
      return "yellow"
    elif hue >= 80 and hue < 160:
      return "green"
    elif hue >= 160 and hue < 225:
      return "blue"
    elif hue >= 225 and hue < 290:
      return "purple"
    else:
      return "red"
  else:  # less than half of the icon is a single color; thus, the icon cannot be categorized
    return None

# ---------BEGIN-----------

dirs = os.listdir(inputpath)

f = open(outputpath, "w")

f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
f.write("\n<resources>")
f.write("\n\t<version>1</version>\n")

# -------ADD ALL ICONS-------

for element in dirs:
  print(element)
  element = element[0:(len(element))-4]
  f.write("\n\t<item drawable =\"" + str(element) + "\" />")

# -------CLASSIFY THE ICONS-------
os.chdir(inputpath)

colors = {"red": [], "orange": [], "yellow": [],
          "green": [], "blue": [], "purple": [], "gray": [], "multicolored": []}

for name in dirs:
  print(name)
  if getColor(name) == "red":
    colors["red"].append(name)
  elif getColor(name) == "orange":
    colors["orange"].append(name)
  elif getColor(name) == "yellow":
    colors["yellow"].append(name)
  elif getColor(name) == "green":
    colors["green"].append(name)
  elif getColor(name) == "blue":
    colors["blue"].append(name)
  elif getColor(name) == "purple":
    colors["purple"].append(name)
  elif getColor(name) == "gray":
    colors["gray"].append(name)
  else:
    colors["multicolored"].append(name)

for color in colors:
  f.write("\n\n\t<category title =\"" + str(color) + "\" />")
  # loop through each sorted name in each color
  for i in range(len(colors[color])):
    temp = colors[color][i][0:(len(colors[color][i]))-4]
    f.write("\n\t<item drawable=\"" + str(temp) + "\" />")

f.write("\n</resources>")
f.close()
