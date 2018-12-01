#lists all of the icons I have already created in the format needed for the app

import os,sys

os.chdir("C:\\Users\\Melanie\\Documents\\GitHub\\PythonScripts\\Appstract\\componentinfoscript")

path = "C:\\Users\\Melanie\\Documents\\GitHub\\Appstract\\app\\src\\main\\res\\drawable-nodpi"

dirs = os.listdir(path)

print(dirs)

f = open("xmloutput.txt","w+")

for element in dirs:
    element = element[0:(len(element))-4]
    f.write("\n<item>" + str(element) + "</item>")

print(dirs)
    
f.close()