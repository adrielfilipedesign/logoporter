import os
from turtle import mode
import yaml
import shutil
import requests
import pathlib
import subprocess
from PIL import Image as PilImage
from PyPDF2 import PdfReader
from tkinter import *
from tkinter import filedialog

#open command file
with open("./files/commands.yml", "r", encoding='utf-8') as commands:
    cmd = yaml.safe_load(commands)

#open config file
with open("./files/config.yml", "r", encoding='utf-8') as configs:
    cfg = yaml.safe_load(configs)

#order file
with open("./order.yml", "w") as order:
    pass
order.close()

with open("./order.yml", "w") as order:
    order.writelines('inputFile: ' + '\n')
    order.writelines('outDir: ')
order.close()

with open("./order.yml", "r", encoding='utf-8') as order:
    ord = yaml.safe_load(order)

#variables
sys = cfg['sys']
slash = cmd[sys]['slash']
outputDir = ord['outDir']
rgbExt = cfg['rgbExt']
exportCMD = cmd[sys]['exportFormat']
exportPARAM = cmd[sys]['exportParams']
tempFolder = cmd[sys]['tempFolder']
jpgBgColor = cfg['jpgBgColor']
jpgBgPositive = cfg['jpgBgPositive']
jpgBgNegative = cfg['jpgBgNegative']
inkscapeVer = cfg['inkscapeVer']
namePage = ""
dirProgram=os.getcwd()

order.close()

#cheking system and inkscape version
if sys == "unix":

    if inkscapeVer == "apt":
        inkscapeRun = "inkscape "

    if inkscapeVer == "flatpak":
        inkscapeRun = "flatpak run org.inkscape.Inkscape "

def createTempFolder():

    if not os.path.isdir(tempFolder):
        os.mkdir(tempFolder)
    else:
        print()

    if os.path.isdir(tempFolder):
        shutil.rmtree(tempFolder)
        os.mkdir(tempFolder)
    else:
        print()
    global name_of_temp_inputFiles
    name_of_temp_files = os.listdir(tempFolder)
   
def getPDFName():

    if sys == "unix":
        #using pdftk to extract dump data of pdf file 
        namePage = os.system("pdftk " + tempFolder + str(count) + '.pdf' + " dump_data output " + tempFolder + 'info' + str(count) + '.txt')
    
def SVG2PDF():
    
    dirProgram=os.getcwd()
    
    with open("./order.yml", "r", encoding='utf-8') as order:
        ord = yaml.safe_load(order)

    inputFile=ord['inputFile']
    outDir=ord['outDir']
    fixInputFileDir=inputFile.replace("'","")
    fixOutDir=outDir.replace("'", "")

    os.chdir("/")
    
    exportPDF=os.system(inkscapeRun + inputFile + exportCMD['PDF'] + exportPARAM['FILENAME'] + fixOutDir + '/' + 'exported')
    exportPDF

    shutil.move(fixOutDir + '/exported.pdf', dirProgram + "/" + cmd[sys]['tempFolder'])
    
    os.chdir(dirProgram)
    order.close()

def separatePDFPages():

    global count
    count = 1
    inputLogo = "exported.pdf"

    #check how many pages are on pdf file
    number_of_pages = len(PdfReader(tempFolder + inputLogo).pages)
    
    #get name page 
    pageNameTag = "PageLabelPrefix:"
    
    while count <= number_of_pages:
        os.system(inkscapeRun + " " + tempFolder + inputLogo + exportCMD['PDF'] + exportPARAM['PAGES']+ str(count) + exportPARAM['FILENAME'] + tempFolder + str(count) + ".pdf")
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

    name_of_temp_files = os.listdir(tempFolder)
    count = 1
    
    for item in name_of_temp_files:
        print(item[:-4])
        os.system(inkscapeRun + " " + tempFolder + item + exportCMD['SVG'] + exportPARAM['FILENAME'] + tempFolder + item[:-4] + ".svg")
        count += 1
        os.remove(tempFolder + item)

def exportRGBFiles():

    numberOfFiles = int(os.listdir(tempFolder).__len__())
    name_of_temp_files = os.listdir(tempFolder)
    colorSpace = "RGB"

    #create a RGB directory folder
    if os.path.isdir(tempFolder + colorSpace):
        print(colorSpace + " folder created")
    else:
        os.mkdir(tempFolder + colorSpace)
    
    def export():
        for svgFiles in name_of_temp_files:
        
            if svgFiles.endswith(".svg"):

                colorSpaceFileName = svgFiles[:-4] + "-" + colorSpace
            
                folderName = colorSpace + slash + svgFiles[:-4]
            
                #checking if the logo version directory has created
                if os.path.isdir(tempFolder + folderName):
                    print()
                else:
                    os.mkdir(tempFolder + folderName)

                #parei aqui implementar a exportação jpg e adicionar o parametro de fundo branco ou preto, usar imagemagick dentro do python
                for ext in rgbExt:
                    print()
                    os.system(inkscapeRun + tempFolder + svgFiles + exportCMD[ext] + exportPARAM['FILENAME'] + tempFolder + folderName + slash + colorSpaceFileName)
            
                jpgFile = tempFolder + folderName + slash + colorSpaceFileName

                #JPG file export
                def jpgWhiteBG():
                    
                    imgDir=tempFolder + folderName + slash + colorSpaceFileName + ".png"
                    imgDirSave= tempFolder + folderName + slash +colorSpaceFileName + ".jpg"

                    img=PilImage.open(imgDir)
                    whiteBG=PilImage.new("RGBA", img.size, (255,255,255))
                    composeImg=PilImage.alpha_composite(whiteBG.convert("RGBA"), img).convert('RGB')
                    composeImg.save(imgDirSave)

                def jpgBlackBG():
                    
                    imgDir=tempFolder + folderName + slash + colorSpaceFileName + ".png"
                    imgDirSave= tempFolder + folderName + slash +colorSpaceFileName + ".jpg"

                    img=PilImage.open(imgDir)
                    whiteBG=PilImage.new("RGBA", img.size, (0,0,0))
                    composeImg=PilImage.alpha_composite(whiteBG.convert("RGBA"), img).convert('RGB')
                    composeImg.save(imgDirSave)

                if svgFiles[:-4] == 'Positiva':
                    jpgWhiteBG()
                    print("jpg positivo exportado")
            
                if svgFiles[:-4] == 'Negativa':
                    jpgBlackBG()
                    print("jpg negativo exportado")
    export()

def moveFilesToOutDir():

    with open("./order.yml", "r", encoding='utf-8') as order:
        ord = yaml.safe_load(order)

    outDir=ord['outDir']
    fixOutDir=outDir.replace("'", "")
    rgbDir=tempFolder+'RGB'
    moveFiles=shutil.move(rgbDir,fixOutDir)
    moveFiles
  
    order.close()

def closeYML():

    configs.close()
    commands.close()
    order.close()

def initProgram():
    
    createTempFolder()
    SVG2PDF()
    separatePDFPages()
    PDF2SVG()
    exportRGBFiles()
    moveFilesToOutDir()
    #closeYML()

def UI():

    window = Tk()
    window.title("Logopotter")
    window.geometry("300x300")

    def openFile():
        filePath = filedialog.askopenfilename()
        with open ('order.yml', 'w') as orderFile:
            dirs=filePath.split(os.path.sep)
            newDir=os.path.sep.join([f"'{dir}'" for dir in dirs]).strip("'").replace("''", "'")
            orderFile.writelines('inputFile: ' + newDir + "'" + '\n') 
        orderFile.close()

    def folderOutput():
        folderPath = filedialog.askdirectory()
        with open('order.yml', 'a') as orderFile:
            dirs=folderPath.split(os.path.sep)
            newDir=os.path.sep.join([f"'{dir}'" for dir in dirs]).strip("'").replace("''", "'")
            orderFile.writelines('outDir: ' + newDir + "'")
        orderFile.close()

    firstText = Label(window, text="Open logo file")
    firstText.grid(column=1, row=0)

    inputButton = Button(window, text="Select a file",command=openFile)
    inputButton.grid(column=1, row=1)

    outputButton = Button(window, text="Select output folder", command=folderOutput)
    outputButton.grid(column=1, row=2)

    exportLogo = Button(window, text="Export Files", command=initProgram)
    exportLogo.grid(column=1, row=6)

    window.mainloop()
    
UI()    