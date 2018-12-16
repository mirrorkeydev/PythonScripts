## Explanations of the various subprojects
### Appstract (Icon Pack)
Building an icon pack requires processing and formatting a lot of data. Below are scripts I've written in order to automate processing this data. Each directory holds both the script and input(when possible) and output files.
#### - colorsensor
This directory holds a script that analyzes the dominant color of icons I designed held in a local directory, and then generates an xml-style text file grouping the icons by color.
#### - componentinfoscript
This directory holds a script that takes a gigantic unordered text file of the [form](https://raw.githubusercontent.com/Delta-Icons/android/master/app/src/main/res/xml/appfilter.xml) and generates a file that groups all of the lines with the same "drawable" attribute.
#### - xmlscript
This directory holds a script that simply returns the filenames without the file extension of every icon I've designed (held in a local directory), formatted in the xml style required for the preview function of the app.
#### - whitelines
This directory holds a script that fills a local directory with svgs after changing all of a svg's #000000 elements to #ffffff.
