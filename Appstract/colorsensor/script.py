"""
Given: a local directory filled with png icons, having mostly 1-4 colors

Perform: analysis returning the dominant color of the icon, categorizing it
as either red, orange, yellow, green, blue, purple, or gray

Return: a text file with the icons organized by color in the xml format:
        -------------red-------------
        <item>nameofredicon</item>
        <item>youtube</item>
        <item>netflix</item>
        ...
"""

import PIL, os, sys
from PIL import Image
import colorsys

os.chdir("C:\\Users\\Melanie\\Documents\\GitHub\\Appstract\\app\\src\\main\\res\\drawable-nodpi") #this is the local directory with icons

#---------------FUNCTIONS---------------

def rgb2hsv(r, g, b): #converts rgb to hsv
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

def getMaxNum(d): #returns key and value with the greates value in a tuple
    maximum = 0
    maxkey = ()
    for key in d:
        if d[key] > maximum:
            maximum = d[key]
            maxkey = key
    return (maxkey,maximum)

def getColor(path): #returns either a dominant color (roygbp) or None
    data = list(PIL.Image.open(path, mode='r').getdata()) #returns iterable object with pixel rgba values
    d = {} #will contain {(color): howmanypixels, i.e. (255,255,255): 3, (0,0,0):23, ... etc}

    for pixel in data:
        if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0 and pixel[3] == 0: #rgba for transparent
            continue
        elif pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0 and pixel[3] == 255: #rgba for pure black
            continue
        else:
            value = (pixel[0], pixel[1], pixel[2]) #rgba -> rgb
            if value in d:
                d[value] += 1
            else:
                d[value] = 1
    
    greatestkey = getMaxNum(d)[0]
    greatestvalue = getMaxNum(d)[1] #greatest value in d; the corresponding key is getMaxNum(d)[0]
    allothervalues = 0 #will contain the sum of all of the other values in d

    for key in d: #adds up all of the other values in d other than the max
        if key != greatestkey:
            allothervalues += d[key]

    if greatestvalue*0.5 > allothervalues: #if more than half of the icon is filled with a single color a
        #then classify greatestkey as either r, o, y, g, b, or p
        hue = round(rgb2hsv(greatestkey[0],greatestkey[1],greatestkey[2])[0])
        sat = round(rgb2hsv(greatestkey[0],greatestkey[1],greatestkey[2])[1]*100)

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
    else: #less than half of the icon is a single color; thus, the icon cannot be categorized
        return None

#-------CLASSIFY THE ICONS-------

colors = {"red": [], "orange":[] , "yellow":[] , "green":[] , "blue":[] , "purple":[], "gray":[]}

directory =  os.listdir() #returns all the filenames

for name in directory:
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

#-------GENERATE THE XML LISTS-----

f = open("C:\\Users\\Melanie\\Documents\\GitHub\\PythonScripts\\Appstract\\colorsensor\\xmloutputcolors.txt","w+")

for color in colors:
    f.write("\n\n-------------" + str(color) + "-------------\n")
    for i in range(len(colors[color])): #loop through each sorted name in each color
        temp = colors[color][i][0:(len(colors[color][i]))-4]
        f.write("\n<item>" + str(temp) + "</item>")

f.close()