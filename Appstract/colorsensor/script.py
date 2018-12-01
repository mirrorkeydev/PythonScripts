#reads the dominant color of an image 
#(relies on images with few colors)
#then, creates xml file labels based off them
import PIL, os, sys
from PIL import Image
import colorsys

os.chdir("C:\\Users\\Melanie\\Documents\\GitHub\\Appstract\\app\\src\\main\\res\\drawable-nodpi")

def rgb2hsv(r, g, b):
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

def getColor(path): #returns either a dominant color (roygbp) or None if there's too many to pick a dominant
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

    if greatestvalue*0.5 > allothervalues: #if more than half of the picture is a
        #then classify greatestkey as either r, o, y, g, b, or p
        hue = round(rgb2hsv(greatestkey[0],greatestkey[1],greatestkey[2])[0])
        sat = round(rgb2hsv(greatestkey[0],greatestkey[1],greatestkey[2])[1]*100)
        print(hue)

        if sat < 10:
            return "gray"
        elif hue >= 0 and hue < 9:
            return "red"
        elif hue >= 9 and hue < 36:
            return "orange"
        elif hue >= 36 and hue < 100:
            return "yellow"
        elif hue >= 100 and hue < 144:
            return "green"
        elif hue >= 144 and hue < 225:
            return "blue"
        elif hue >= 225 and hue < 265:
            return "purple"

    else:
        return None


#-------CLASSIFY THE ICONS-------

red, orange, yellow, green, blue, purple = ([] for i in range(6))

directory =  os.listdir() #returns all the filenames

for name in directory:
    print("----------")
    print(name)
    print(getColor(name)) #appends onto the current directory
    # sort them into lists