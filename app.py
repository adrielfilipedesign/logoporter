import os
import yaml
import shutil
import pathlib
import subprocess
from PyPDF2 import PdfReader

#open command file
with open("./files/commands.yml", "r", encoding='utf-8') as commands:
    cmd = yaml.safe_load(commands)

#open config file
with open("./files/config.yml", "r", encoding='utf-8') as configs:
    cfg = yaml.safe_load(configs)

#variables
inputLogo = "logo.pdf"
sys = cfg['sys']
file = "logos.svg"
rgbExt = cfg['rgbExt']
exportCMD = cmd[sys]['exportFormat']
exportPARAM = cmd[sys]['exportParams']
tempFolder = cmd[sys]['tempFolder']
inkscapeVer = cfg['inkscapeVer']
name_of_temp_files = os.listdir(tempFolder)
namepage = ""

#cheking system and inkscape version
if sys == "unix":

    if inkscapeVer == "apt":
        inkscapeVer = "inkscape "

    if inkscapeVer == "flatpak":
        inkscapeVer = "flatpak run org.inkscape.Inkscape "

def createTempFolder():

    if os.path.isdir(tempFolder):
        print("temp folder find")
    else:
        os.mkdir(cmd[sys]['tempFolder'])

def getPDFName():

    if sys == "unix":
        #using pdftk to extract dump data of pdf file 
        namePage = os.system("pdftk " + tempFolder + str(count) + '.pdf' + " dump_data output " + tempFolder + 'info' + str(count) + '.txt')
    
def SVG2PDF():
    
    os.system(inkscapeVer + file + exportCMD['PDF'] + exportPARAM['FILENAME'] + inputLogo)
    shutil.move(inputLogo, cmd[sys]['tempFolder'])

def separatePDFPages():

    global count
    count = 1

    #check how many pages are on pdf file
    number_of_pages = len(PdfReader(tempFolder + inputLogo).pages)
    
    #get name page 
    pageNameTag = "PageLabelPrefix:"
    
    while count <= number_of_pages:
        os.system(inkscapeVer + " " + tempFolder + inputLogo + exportCMD['PDF'] + exportPARAM['PAGES']+ str(count) + exportPARAM['FILENAME'] + tempFolder + str(count) + ".pdf")
        getPDFName()
        count += 1

    #rename files
    count = 1
    while count <= number_of_pages:
        
        with open(tempFolder + "info" + str(count) + ".txt" ,'r', encoding='utf-8') as doc:
            lines = doc.readlines()
            for numberLine, lines in enumerate(lines, start=1):
                if pageNameTag in lines:
                    nameOfPage = f'{lines}'.replace(pageNameTag,'').replace(' ','').replace('\n','')
                    os.rename(tempFolder + str(count) + ".pdf", tempFolder + nameOfPage + ".pdf")        
        
        os.remove(tempFolder + "info" + str(count) + ".txt")
        doc.close()
        count += 1

    os.remove(tempFolder + inputLogo) 
    
def PDF2SVG():

    count = 1
    
    for item in name_of_temp_files:
        print(item[:-4])
        os.system(inkscapeVer + " " + tempFolder + item + exportCMD['SVG'] + exportPARAM['FILENAME'] + tempFolder + item[:-4] + ".svg")
        count += 1
        os.remove(tempFolder + item)

def createFolders():

    for Files in name_of_temp_files:
        os.mkdir(tempFolder + Files[:-4])

def exportRGBFiles():

    #createFolders()
    for svgFiles in name_of_temp_files:
        if svgFiles.endswith(".svg"):
            for ext in rgbExt:
                #parei aqui
                rgbFileName = svgFiles[:-4] + "-RGB"
                os.system(inkscapeVer + exportCMD[ext] + exportPARAM['FILENAME'] + tempFolder + rgbFileName)
                shutil.move(tempFolder + rgbFileName, tempFolder + ext)

#def initialSettings():

#    createTempFolder()
#    SVG2PDF()
#    separatePDFPages()
#    PDF2SVG()

#initialSettings()

exportRGBFiles()
configs.close()
commands.close()