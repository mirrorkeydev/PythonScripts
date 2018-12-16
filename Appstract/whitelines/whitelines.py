"""
Given: a local directory of svg files

Perform: parse through the files and change all #000000 elements to #ffffff

Return: a directory with svgs that do not contain #000000 elements

Planed Extension: using Inkscape, batch export the svgs to 192x192 px pngs
"""

import os, re

os.chdir("C:\\Users\\Melanie\\Google Drive\\MISC\\Appstract\\F - Inkscape Files") #input files

dirs = os.listdir()

for svg in dirs:
    print(svg)
    oldfile = open(svg, "rt").readlines() #open the old svg
    
    #need to delete old version since the file will be opened in append mode 
    if os.path.exists("C:\\Users\\Melanie\\Google Drive\\MISC\\Appstract\\WhiteInkscape\\" + svg): 
        os.remove("C:\\Users\\Melanie\\Google Drive\\MISC\\Appstract\\WhiteInkscape\\" + svg)
    
    #where the edited svg will go
    newfile = open("C:\\Users\\Melanie\\Google Drive\\MISC\\Appstract\\WhiteInkscape\\" + svg, "a+") 

    for line in oldfile:
        if ((line.find("stroke:#") != -1 or line.find("fill:#") != -1) and 
            line[line.find(":#")+2] == "0" and line[line.find(":#")+3] == "0" and 
            line[line.find(":#")+4] == "0" and line[line.find(":#")+5] == "0" and 
            line[line.find(":#")+6] == "0" and line[line.find(":#")+7] == "0"):
            #case: this line contains details regarding a #000000 element
            
            templine = "" #will contain the edited line
            zerosindexes = [m.start() for m in re.finditer("000000", line)] #indexes of the first 0 in 000000 after an ":#"
            zerosindexesall = [] #indexes of all 0's in a "000000"

            for index in zerosindexes:
                zerosindexesall.append(index)
                for i in range(6): #the first 0 of 000000 is indexed, but we need to add the other 5 indexes
                    zerosindexesall.append(index + i)

            for i in range(len(line)): #replacing the 0's with f's
                if i in zerosindexesall:
                    templine += "f"
                else:
                    templine += line[i]

            newfile.write(templine)

        else:
            #case: this line is not relevent to an #000000 element
            newfile.write(line)

    newfile.close()