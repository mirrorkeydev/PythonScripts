"""
Given: a local directory filled with png icons in the format airbnb.png, etc

Return: a text file with all icons' filenames in the xml format:

        <item drawable="airbnb" />
        <item drawable ="bing" />
        <item drawable = "chrome" />
        ...
"""

import os,sys

os.chdir("C:\\Users\\Melanie\\Documents\\GitHub\\PythonScripts\\Appstract\\xmlscript")

path = "C:\\Users\\Melanie\\Documents\\Appstract\\candybar-sample-master\\app\\src\\main\\res\\drawable-nodpi"

dirs = os.listdir(path)

f = open("xmloutput.txt","w")

for element in dirs:
    print(element)
    element = element[0:(len(element))-4]
    f.write("\n<item drawable =\"" + str(element) + "\" />")
    
f.close()