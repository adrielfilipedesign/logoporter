import os
import yaml
import shutil
import pathlib
from PyPDF2 import PdfReader

#OPEN COMMAND FILE
with open("./files/commands.yml", "r", encoding='utf-8') as commands:
    cmd = yaml.safe_load(commands)

#variables
logoPDF = "logo.pdf"

#input svg filename
file = "logos.svg"

#CHECKING THE INKSCAPE VERSION

#set default to to inkscape APT version,
#if you use a FLATPAK inkscape change to FALSE:
sys = "unix"

inkscapeVer = "true"

if inkscapeVer == "true":
    inkscapeVer = "inkscape "
else:
    inkscapeVer = "flatpak run org.inkscape.Inkscape "

exportCMD = cmd[sys]['exportFormat']
exportPARAM = cmd[sys]['exportParams']
tempFolder = cmd[sys]['tempFolder']
namePage = cmd[sys]['getNamePage']

def createTempFolder():

    if os.path.isdir(tempFolder):
        print("temp folder find")
    else:
        os.mkdir(cmd[sys]['tempFolder'])

def SVG2PDF():
    
    os.system(inkscapeVer + file + exportCMD['PDF'] + exportPARAM['FILENAME'] + logoPDF)
    shutil.move(logoPDF, cmd[sys]['tempFolder'])

def separatePDFPages():

    #check how many pages are on pdf file
    count = 1
    
    number_of_pages = len(PdfReader(tempFolder + logoPDF).pages)

    #get name page 
    pageNameTag = "PageLabelPrefix:"

    while count <= number_of_pages:
        os.system(inkscapeVer + " " + tempFolder + logoPDF + exportCMD['PDF'] + exportPARAM['PAGES']+ str(count) + exportPARAM['FILENAME'] + tempFolder + str(count) + ".pdf")
        os.system(namePage[0] + tempFolder + str(count) + ".pdf" + namePage[1] + namePage[2] + " " + tempFolder + "info" + str(count) + ".txt")
        count += 1

    #rename files
    count = 1
    while count <= number_of_pages:
        #print(count)
        with open(tempFolder + "info" + str(count) + ".txt" ,'r', encoding='utf-8') as doc:
            lines = doc.readlines()
            for numberLine, lines in enumerate(lines, start=1):
                if pageNameTag in lines:
                    nameOfPage = f'{lines}'.replace(pageNameTag,'').replace(' ','').replace('\n','')
                    os.rename(tempFolder + str(count) + ".pdf", tempFolder + nameOfPage + ".pdf")        
        doc.close()
        count += 1

    os.remove(tempFolder + logoPDF) 
    
def PDF2SVG():

    countSVG = 1
    number_of_pdf_files = os.listdir(tempFolder).__len__()
    name_of_pdf_files = os.listdir(tempFolder)

    for item in name_of_pdf_files:
       os.system( inkscapeVer + " " + tempFolder + item + exportCMD['SVG'] + exportPARAM['FILENAME'] + tempFolder + str(countSVG) + ".svg")
       countSVG += 1
       os.remove(tempFolder + item)
  
def initialSettings():
    #createTempFolder()
    SVG2PDF()
    separatePDFPages()
    #PDF2SVG()

initialSettings()

commands.close()