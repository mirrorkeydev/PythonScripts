"""
Given: a large unsorted text file of appcodes in the form:
 
    <item component="ComponentInfo{...}" drawable="zowi" />
    <item component="ComponentInfo{...}" drawable="other" />
    <item component="ComponentInfo{...}" drawable="zowi" />
    ...

Return: a text file with all appcodes grouped and sorted by drawable tag:

        <!--zowi-->
        <item component="ComponentInfo{...}" drawable="zowi" />
        <item component="ComponentInfo{...}" drawable="zowi" />

        <!--other-->
        <item component="ComponentInfo{...}" drawable="other" />
        ...
"""

import os

os.chdir("C:\\Users\\Melanie\\Documents\\GitHub\\PythonScripts\\Appstract")

f = open("unsortedlist.txt", "r")

def getDrawable(str):
    tempstr = ""
    for i in range(len(str)-5):
        if str[i] == "a" and str[i+1] == "b" and str[i+2] == "l" and str[i+3] == "e" and str[i+4] == "=" and str[i+5] == "\"":
            currentchar = 6
            while str[i + currentchar] != "\"":
                tempstr += str[i + currentchar]
                currentchar += 1
    return tempstr

dict = {} #to be filled in the form: {"drawable tag": ["<item component ... />", "<item component ... />"]}

for line in f:
    drawable = getDrawable(line)
    if drawable in dict:
        dict[drawable].append(line)
    else:
        dict[drawable] = []
        dict[drawable].append(line)

print(dict)
f.close()

#at this point, the dictionary is sorted. Now it has to be outputted to a new file

f = open("sortedlist.txt","w")

for key in dict:
    f.write("\n<!---" + str(key) + "--->\n")
    for element in dict[key]:
        f.write(element)
    
f.close()