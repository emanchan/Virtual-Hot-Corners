# Hot Corners
# Requires OpenCV 2.0 and Python 2.7
# GUI - Toggle showing of live color video feed, with boxes superimposed?
# GUI - Toggle showing of hand detection for lighting. Have parameters for 
#testing, like if 4 corners are white, warn user that lighting needs to be changed# Size of hot corners toggle, sensitivity of color detection using histogram, #Countdown popup from 3...2...1...Launching x!. 
# To Do, implement Showing of 4 corners in TKINTER Green/REd for True False
# Set show live window and test window toggle. With RadioButtons
# Connect slider bars/menu with program - 50%
# Input Areas: For Delay, Activation Time
# Figure out Canvas Size 

import cv
import time
import Tkinter, tkFileDialog, Tkconstants, tkMessageBox, tkFont
import os 
from PIL import Image, ImageTk

def getColors(): #This function returns a list of the RGB values 
                #for each of the four corners. 
    size = canvas.data.cropWidth**2
    colorslist = []
    crop1 = Image.open("crop1.jpg").convert("RGB")
    crop2 = Image.open("crop2.jpg").convert("RGB")
    crop3 = Image.open("crop3.jpg").convert("RGB")
    crop4 = Image.open("crop4.jpg").convert("RGB")
    #print crop1.mode
    #RGB = im.convert("RGB", crop1)
    colors1 = crop1.getcolors()
    colors2 = crop2.getcolors()
    colors3 = crop3.getcolors()
    colors4 = crop4.getcolors()
    colorslist = [crop1.getcolors(size), crop2.getcolors(size), \
    crop3.getcolors(size), crop4.getcolors(size)]    
    #print colors
    #print "colorslist =", colorslist
    #print colors1, colors2, colors3, colors4
    return colorslist
   
def getColorsSort(colorslist): #This function sorts the RGB values 
                        #into Black/White depending on their RGB Values. 
    sortedColorsList = []
    cornerblack1 = 0
    cornerblack2 = 0
    cornerblack3 = 0
    cornerblack4 = 0
    cornerwhite1 = 0
    cornerwhite2 = 0
    cornerwhite3 = 0
    cornerwhite4 = 0
    #print "colorslist =", colorslist
    for value in colorslist[0]:
        tempvalue = []
        #print "value =", value
        if type(value[1] ) == int:
            #print "wrong data, skipping"
            continue
        if value[1][1] >= canvas.data.whitesensitivity:
            cornerwhite1 += value[0]
        elif value[1][1] <= canvas.data.blacksensitivity:
            cornerblack1 += value[0]
        #print "got here"
    for value in colorslist[1]:
        tempvalue = []
        #print "value =", value
        if type(value[1] ) == int:
            #print "wrong data, skipping"
            continue
        if value[1][1] >= canvas.data.whitesensitivity:
            cornerwhite2 += value[0]
        elif value[1][1] <= canvas.data.blacksensitivity:
            cornerblack2 += value[0]
        #print "got here"
    for value in colorslist[2]:
        tempvalue = []
        #print "value =", value
        if type(value[1] ) == int:
            #print "wrong data, skipping"
            continue
        if value[1][1] >= canvas.data.whitesensitivity:
            cornerwhite3 += value[0]
        elif value[1][1] <= canvas.data.blacksensitivity:
            cornerblack3 += value[0]
        #print "got here"
    for value in colorslist[3]:
        tempvalue = []
        #print "value =", value
        if type(value[1] ) == int:
            #print "wrong data, skipping"
            continue
        if value[1][1] >= canvas.data.whitesensitivity:
            cornerwhite4 += value[0]
        elif value[1][1] <= canvas.data.blacksensitivity:
            cornerblack4 += value[0]
        #print "got here"
    sortedColorsList = [cornerwhite1, cornerblack1, cornerwhite2, \
    cornerblack2, cornerwhite3, cornerblack3, cornerwhite4, cornerblack4]
    #print "black = ", sortedColorsList[0], "white =", sortedColorsList[1]
    #print sortedColorsList
    return sortedColorsList

def getColorsPercentage(sortedColorsList): #Converts # of whites to % 
    imagesize = canvas.data.cropWidth*canvas.data.cropHeight
    corner1 = round(float(sortedColorsList[0])/float(imagesize)*100)
    corner2 = round(float(sortedColorsList[2])/float(imagesize)*100)
    corner3 = round(float(sortedColorsList[4])/float(imagesize)*100)
    corner4 = round(float(sortedColorsList[6])/float(imagesize)*100)
    percentColorsList = [corner1,corner2,corner3,corner4]
    return percentColorsList
    
def getColorsAnalysis(percentColorsList): #Sets points to True/False 
                #depending on the perecent white/black of each corner
    activePoints = []
    i = 0
    for percent in percentColorsList:
        if percent >= canvas.data.sensitivity:
            activePoints += [True]
        else:
            activePoints += [False]
    canvas.data.corner1List += [activePoints[0]]
    canvas.data.corner2List += [activePoints[1]]
    canvas.data.corner3List += [activePoints[2]]
    canvas.data.corner4List += [activePoints[3]]
    return activePoints

def checkAction(): #Sets action depending on duration designated by user. 
    CornerList = [canvas.data.corner1List, canvas.data.corner2List, \
    canvas.data.corner3List, canvas.data.corner4List]
    listsize = int(canvas.data.activationTime/canvas.data.framespersecond*1.0)
    #Total Number Of Frames /1Activation Time
    activenumber = int(listsize)#*(canvas.data.sensitivity/100.0))
    if canvas.data.activationTime == 500:
        activenumber = int(listsize/2)
    #canvas.data.listsize = listsize
    for corner in CornerList:
        while len(corner) > listsize: 
            corner.pop(0)
        if len(corner) < listsize:
            continue 
    for i in range(len(CornerList)):
        if canvas.data.corner1List.count(True) < activenumber and i == 0:
            canvas.data.corner1Status = False
        elif canvas.data.corner2List.count(True) < activenumber and i == 1:
            canvas.data.corner2Status = False
        elif canvas.data.corner3List.count(True) < activenumber and i == 2:
            canvas.data.corner3Status = False
        elif canvas.data.corner4List.count(True) < activenumber and i == 3:
            canvas.data.corner4Status = False
    for i in range(len(CornerList)):
        if canvas.data.corner1List.count(True) >= activenumber and i == 0:
            canvas.data.corner1Status = True
        elif canvas.data.corner2List.count(True) >= activenumber and i == 1:
            canvas.data.corner2Status = True
        elif canvas.data.corner3List.count(True) >= activenumber and i == 2:
            canvas.data.corner3Status = True
        elif canvas.data.corner4List.count(True) >= activenumber and i == 3:
            canvas.data.corner4Status = True 
    #print "checked Lists!"
    #print "activenumber =", activenumber
    #print "fps = ", canvas.data.framespersecond
    #print "list size = ", listsize
    #print "activation time=", canvas.data.activationTime
    #print "corner1 =", canvas.data.corner1Status, canvas.data.corner1List, canvas.data.corner1List.count(True)
    #print "corner2 =", canvas.data.corner2Status, canvas.data.corner2List, canvas.data.corner2List.count(True)
    #print "corner3 =", canvas.data.corner3Status, canvas.data.corner3List, canvas.data.corner3List.count(True)
    #print "corner4 =", canvas.data.corner4Status, canvas.data.corner4List, canvas.data.corner4List.count(True)

def doAction(): #Does action, sets lists back to all False
    if (canvas.data.corner1Status == True and canvas.data.program1 != "None"):
        launchProgram(canvas.data.program1)
        canvas.data.corner1Status = False
        canvas.data.corner1List = [False]*canvas.data.listsize
    if (canvas.data.corner2Status == True and canvas.data.program2 != "None"):
        launchProgram(canvas.data.program2)
        canvas.data.corner2Status = False
        canvas.data.corner2List = [False]*canvas.data.listsize
    if (canvas.data.corner3Status == True and canvas.data.program3 != "None"):
        launchProgram(canvas.data.program3)
        canvas.data.corner3Status = False
        canvas.data.corner3List = [False]*canvas.data.listsize
    if (canvas.data.corner4Status == True and canvas.data.program4 != "None"):
        launchProgram(canvas.data.program4) 
        canvas.data.corner4Status = False
        canvas.data.corner4List = [False]*canvas.data.listsize
        
def launchProgram(path): #Launches Program
    try:
        os.startfile(path)
    except WindowsError as error:
            tkMessageBox.showinfo("Error!", \
            "Looks like Windows can't open the file you selected. Please select another file.")
 
def histogramAnalysis(): #Unused
    crop1 = Image.open("crop1.jpg")
    crop2 = Image.open("crop2.jpg")
    crop3 = Image.open("crop3.jpg")
    crop4 = Image.open("crop4.jpg")
    images = [crop1, crop2, crop3, crop4]
    rgbvalues = []
    for img in images:
        histogram = img.histogram
        red = histogram[0:256]
        green = histogram[256:256*2]
        blue = histogram[256*2:256*3]
        redaverage = sum(i*w for i, w in enumerate(red)/sum(red))
        greenaverage = sum(i*w for i, w in enumerate(green)/sum(green))
        blueaverage = sum(i*w for i, w in enumerate(blue)/sum(blue))
        rgbvalues += [(redaverage,greenaverage,blueaverage )]
    print rgbvalues

def cornerCrop(): #Crops 4 corners based on cropheight/cropwidth 
    try:
        image = Image.open("hands.jpg")
    except IOError: 
        print "Oops, for some reason I wasn't able to access the image. Try running again" 
    upperleftcorner = image.crop((0, 0, canvas.data.cropWidth, \
    canvas.data.cropHeight))
    upperrightcorner = image.crop((canvas.data.videoWidth- \
    canvas.data.cropWidth, 0, canvas.data.videoWidth, \
    canvas.data.cropHeight))
    lowerleftcorner = image.crop((0, \
    canvas.data.videoHeight-canvas.data.cropHeight, \
    canvas.data.cropWidth, canvas.data.videoHeight))
    lowerrightcorner = image.crop((canvas.data.videoWidth- \
    canvas.data.cropWidth, canvas.data.videoHeight-canvas.data.cropHeight, \
    canvas.data.videoWidth, canvas.data.videoHeight))
    #print "this ran"
    try:
        upperleftcorner.save("crop1.jpg")
        upperrightcorner.save("crop2.jpg")
        lowerleftcorner.save("crop3.jpg")
        lowerrightcorner.save("crop4.jpg")
    except IOError: 
        print "Oops, for some reason I wasn't able to access the image. Try running again" 
    return upperleftcorner, upperrightcorner, \
    lowerleftcorner, lowerrightcorner

def cornerPoints(point): #Returns X/Y values for drawing video overlay 
    if point == 0: 
        return [1, 1, canvas.data.cropWidth, canvas.data.cropHeight]
    elif point == 1:
        return [canvas.data.videoWidth-canvas.data.cropWidth, 1, \
        canvas.data.videoWidth, canvas.data.cropHeight]
    elif point == 2:
        return [0, canvas.data.videoHeight-canvas.data.cropHeight, \
        canvas.data.cropWidth, canvas.data.videoHeight-2]
    elif point == 3:
        return [canvas.data.videoWidth-canvas.data.cropWidth, \
        canvas.data.videoHeight-canvas.data.cropHeight, \
        canvas.data.videoWidth, canvas.data.videoHeight-2]
        
def get_img(capture): #Gets image from webcam. 
    img = cv.QueryFrame(capture)
    cv.Flip(img,img , 1)
    #print "FPS=" ,cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
    return img

def get_hands(image): #Image Filtering. Filtering was from outside source in sources.txt file.
    """ Returns the hand as white on black. Uses value in HSV to determine
        hands."""
    live = image
    size = cv.GetSize(image)
    hsv = cv.CreateImage(size, 8, 3)
    hue = cv.CreateImage(size, 8, 1)
    sat = cv.CreateImage(size, 8, 1)
    val = cv.CreateImage(size, 8, 1)
    hands = cv.CreateImage(size, 8, 1)
    cv.CvtColor(image, hsv, cv.CV_BGR2HSV)
    cv.Split(hsv, hue, sat, val, None)
    red = cv.CV_RGB(255,0,0)
    green = cv.CV_RGB(0,255,0)
    #print cornerPoints(4)
    if canvas.data.liveVideo.get() == "True": 
        if canvas.data.showActiveCorners.get() == "True": #Drawing Video Overlay
            for i in range(len(canvas.data.activePoints)):
                points = cornerPoints(i)
                point1 = points[0]
                point2 = points[1]
                point3 = points[2]
                point4 = points[3]
                if canvas.data.activePoints[i] == True:
                    cv.Rectangle(live, (point1,point2), (point3,point4), \
                    green,2) 
                else:
                    cv.Rectangle(live, (point1, point2), (point3, point4), \
                    red,2)
        cv.ShowImage('Live', live)
    #cv.ShowImage('Hue', hue)
    #cv.ShowImage('Saturation', sat)
    cv.Threshold(hue, hue, 10, 255, cv.CV_THRESH_TOZERO) #set to 0 if <= 10, otherwise leave as is
    cv.Threshold(hue, hue, 244, 255, cv.CV_THRESH_TOZERO_INV) #set to 0 if > 244, otherwise leave as is
    cv.Threshold(hue, hue, 0, 255, cv.CV_THRESH_BINARY_INV) #set to 255 if = 0, otherwise 0
    cv.Threshold(sat, sat, 64, 255, cv.CV_THRESH_TOZERO) #set to 0 if <= 64, otherwise leave as is
    cv.EqualizeHist(sat, sat)
    cv.Threshold(sat, sat, 64, 255, cv.CV_THRESH_BINARY) #set to 0 if <= 64, otherwise 255
    #cv.ShowImage('Saturation threshold', sat)
    #cv.ShowImage('Hue threshold', hue)
    cv.Mul(hue, sat, hands)
    #smooth + threshold to filter noise
    #cv.Smooth(hands, hands, smoothtype=cv.CV_GAUSSIAN, param1=13, param2=13)
    #cv.Threshold(hands, hands, 200, 255, cv.CV_THRESH_BINARY)
    if canvas.data.testVideo.get() == "True":
        cv.ShowImage('Hands', hands)
    cv.SaveImage("hands.jpg",  hands)
    #openCVtoPIL(hands)
    cornerCrop()
    colorslist = getColors()
    #print colorslist
    sortedlist = getColorsSort(colorslist)
    percentcolorslist = getColorsPercentage(sortedlist)
    canvas.data.activePoints = getColorsAnalysis(percentcolorslist)
    checkAction() 
    doAction()
    #histogramAnalysis()
    return hands

def init():
    #cv.NamedWindow('Live Video!', cv.CV_WINDOW_AUTOSIZE)
    canvas.data.capture = cv.CaptureFromCAM(0)
    #set up connection to camera
    if not canvas.data.capture:
        print "Error opening capture device"
        sys.exit(1)
    cv.SetCaptureProperty(canvas.data.capture, cv.CV_CAP_PROP_FRAME_WIDTH, \
    640)
    cv.SetCaptureProperty(canvas.data.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, \
    480)
    canvas.data.width = 800 #dunno if need this
    canvas.data.height = 600 # ditto
    canvas.data.videoWidth = 640
    canvas.data.videoHeight = 480
    canvas.data.cropWidth = 75
    canvas.data.cropHeight = 75
    canvas.data.mode = False
    canvas.data.sensitivity = 30
    canvas.data.whitesensitivity = 50
    canvas.data.blacksensitivity = 200 # Tie in sensitivty? 
    canvas.data.screenAwake = False
    canvas.data.corner1Status = False
    canvas.data.corner2Status = False
    canvas.data.corner3Status = False
    canvas.data.corner4Status = False
    canvas.data.corner1List = []
    canvas.data.corner2List = []
    canvas.data.corner3List = []
    canvas.data.corner4List = []
    canvas.data.program1 = "None"
    canvas.data.program2 = "None"
    canvas.data.program3 = "None"
    canvas.data.program4 = "None"
    canvas.data.nowebcamerror = False
    try:
        programs = []
        file = open("preferences.py", "r")
        for line in file:
            newline = line.rstrip()
            programs += [newline] 
        canvas.data.program1 = programs[0]
        canvas.data.program2 = programs[1]
        canvas.data.program3 = programs[2]
        canvas.data.program4 = programs[3]
        for i in xrange(1,5):
            #print i
            createActionImage(canvas, i)
    except IOError as e:
        tkMessageBox.showinfo("Welcome!", "Looks like this is your first time running this program! Information about how to use this program is located in the Help option in the Menu. Also, save a preferences file so I'll remember your settings next time!")
    canvas.data.isPaused = True
    canvas.data.listsize = 0
    canvas.data.activationTime = 3000 #milliseconds
    canvas.data.delay = 200
    canvas.data.framespersecond = 15
    canvas.data.startButtonText = "Start!"
    canvas.data.activePoints = [False, False, False, False]
    #canvas.data.activeprograms = checkActivePrograms()
    #canvas.data.startButtonText = "Start"
    #print canvas.data.isPaused 
    
def timerFired(): #Introduce Delay For GetCrop()? 
    #redrawAll()
    #print canvas.data.isPaused
    second = 1000
    if canvas.data.isPaused == False:
        image = get_img(canvas.data.capture)
        hands = get_hands(image)
        # handle events
        k = cv.WaitKey(5) # need this? 
    canvas.data.sensitivity = canvas.data.sensitivitySlider.get()
    canvas.data.activationTime = (float(canvas.data.activationTimeSpinBox.get()))*second
    canvas.data.cropWidth = int(canvas.data.imageSizeSpinBox.get())
    canvas.data.cropHeight = int(canvas.data.imageSizeSpinBox.get())
    #print canvas.data.activationTime, type(canvas.data.activationTime)
    #print canvas.data.sensitivity
    canvas.data.framespersecond = int(float(second/canvas.data.framesPerSecondSlider.get()))
    #print canvas.data.showActive.get()
    if canvas.data.showActive.get() == "True" and canvas.data.isPaused \
    == False:
        drawActivePoints()
        canvas.create_text(425, 30, text="Point 1:", fill="black")
        canvas.create_text(525, 30, text="Point 2:", fill="black")
        canvas.create_text(625, 30, text="Point 3:", fill="black")
        canvas.create_text(725, 30, text="Point 4:", fill="black")
    canvas.after(canvas.data.framespersecond, timerFired)
    
def drawActivePoints(): #Drawing active points on GUI 
   #print canvas.data.activePoints
    for i in range(len(canvas.data.activePoints)):
        #print i
        #print canvas.data.activePoints[i]
        if canvas.data.activePoints[i] == True:
            canvas.create_rectangle(450+(i*100),15,475+(i*100),40, \
            fill = "green")    
        else:
            canvas.create_rectangle(450+(i*100),15,475+(i*100),40, \
            fill = "red")
    
def redrawAll(): #Unused 
    canvas.delete(Tkinter.ALL)
    Application()

def toggleDetection(): #Changes text for buttons 
    canvas.data.isPaused = not canvas.data.isPaused
    #print canvas.data.isPaused
    if canvas.data.startButton["text"] == "Start!": #Error
        canvas.data.startButton["text"] = "Stop!"
    else:
        canvas.data.startButton["text"] = "Start!"

def Application(): 
    #canvas.grid()
    createWidgets(canvas)
    actionButtons(canvas)
    userInput(canvas)
    userCheckBox(canvas)
    createLabels(canvas)

def aboutMessageBox():
    tkMessageBox.showinfo("About...", "Programmed by Ethan Chan (Carnegie Mellon University) 15-112")

def helpMessageBox(): 
    tkMessageBox.showinfo("Help", "Welcome to Virtual Hot Corners! This program creates 4 virtual buttons that you can activate by positioning your hands in the four corners of the webcam image. For best results, use in a well-lit area, with a light (preferably white) background. \n\nCorner 1 = Top Left,  Corner 2 = Top Right, Corner 3 = Bottom Left, Corner 4 = Bottom Right.  \n\nInformation: \n\nSensitivity: How much of your hand has to be detected in each corner, Lower Sensitivity = More sensitive, Higher Sensitivity = Less Sensitive \n\nFrames Per Second: Speed of detection \n\nActivation Time: How long your hand has to be detected to launch an action \n\nDetection Size: Area of corners to be analyzed.")
    
def createWidgets(canvas):
    #canvas.quitButton = Tkinter.Button(canvas, text="Quit", command = canvas.destroy)
    #canvas.quitButton.grid()
    menuFont = tkFont.Font(family="Arial", size = 14, weight=tkFont.BOLD)
    canvas.data.startButton = Tkinter.Button(canvas, text="Start!", \
    font=menuFont, command = toggleDetection)
    canvas.data.startButton.grid(row=5, column =4, rowspan=3, columnspan=3, \
    sticky = Tkinter.N+Tkinter.E+Tkinter.W+Tkinter.S, pady=10)
    #self.startButton = Tkinter.Button(self, text='Start', command = self.start)
    canvas.menuButton = Tkinter.Menubutton(canvas, text='Menu', \
    relief=Tkinter.RAISED)
    canvas.menuButton.grid(row=0, column = 0, rowspan=2, pady =20)
    canvas.menuButton.menu = Tkinter.Menu(canvas.menuButton, tearoff=0)
    canvas.menuButton["menu"] = canvas.menuButton.menu
    canvas.aVar = Tkinter.IntVar()
    canvas.bVar = Tkinter.IntVar()
    canvas.menuButton.menu.add_command (label="About", \
    command= aboutMessageBox)
    canvas.menuButton.menu.add_command(label="Help", command = helpMessageBox)
    #print canvas.grid_size()
    canvas.file_opt = options = {}
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = canvas
    options['title'] = 'Open a File...'
        
def userInput(canvas):
    canvas.sensitivity = Tkinter.IntVar()
    canvas.framespersecond = Tkinter.IntVar()
    canvas.data.sensitivitySlider = Tkinter.Scale(canvas, from_=5, to=90, \
    orient=Tkinter.HORIZONTAL,variable=canvas.sensitivity)
    canvas.data.sensitivitySlider.grid(row=3,column=0, sticky=Tkinter.S)
    canvas.data.sensitivitySlider.set(30)
    #print canvas.data.sensitivity 
    Tkinter.Label(canvas, text ="Sensitivity:").grid(row=2, column=0)
    canvas.data.activationTimeSpinBox = Tkinter.Spinbox(canvas, from_ =0.5, \
    to=5, increment=0.5, width=15)
    canvas.data.activationTimeSpinBox.grid(row=3, column=2, \
    sticky=Tkinter.S, pady=4)
    Tkinter.Label(canvas,text ="Activation Time (sec):").grid(row=2, column=2)
    canvas.data.imageSizeSpinBox = Tkinter.Spinbox(canvas, from_ =75, \
    to=200, increment=5, width=15)
    canvas.data.imageSizeSpinBox.grid(row=3, column=3, sticky=Tkinter.S, \
    pady=4)
    Tkinter.Label(canvas, text ="Detection Size:").grid(row=2, column=3)
    canvas.data.framesPerSecondSlider = Tkinter.Scale(canvas, from_=1, \
    to=30, orient=Tkinter.HORIZONTAL, variable=canvas.framespersecond)
    canvas.data.framesPerSecondSlider.set(15)
    canvas.data.framesPerSecondSlider.grid(row=3, column=1)
    Tkinter.Label(canvas, text ="Frames per Second:").grid(row=2, column=1)

def userCheckBox(canvas):
    canvas.data.liveVideo = Tkinter.StringVar()
    canvas.data.testVideo = Tkinter.StringVar()
    canvas.data.showActiveCorners = Tkinter.StringVar()
    canvas.data.savePreferences = Tkinter.StringVar()
    canvas.data.showActive = Tkinter.StringVar()
    #canvas.data.videoMode = Tkinter.StringVar()
    canvas.data.liveVideoCheckBox = Tkinter.Checkbutton(canvas, \
    text="Enable Live Video", variable= canvas.data.liveVideo, \
    onvalue= "True",offvalue ="False")
    canvas.data.liveVideoCheckBox.grid(row=2, column=4)
    canvas.data.testVideoCheckBox = Tkinter.Checkbutton(canvas, \
    text="Enable Filtered Video", variable= canvas.data.testVideo, \
    onvalue = "True",offvalue ="False")
    canvas.data.testVideoCheckBox.grid(row=3, column=4)
    canvas.data.showActiveCornersCheckBox = Tkinter.Checkbutton(canvas, \
    text="Show Active Corners on Live Video", \
    variable= canvas.data.showActiveCorners, \
    onvalue = "True",offvalue ="False")
    canvas.data.showActiveCornersCheckBox.grid(row=3, column=5)
    canvas.data.showActiveCheckBox = Tkinter.Checkbutton(canvas, \
    text="Show Active Points on GUI", variable= canvas.data.showActive, \
    onvalue = "True",offvalue ="False")
    canvas.data.showActiveCheckBox.grid(row=2, column=5)
    #canvas.data.LightRadioButton = Tkinter.Radiobutton(canvas, text="Light", variable= canvas.data.videoMode, value = "Light")
    #canvas.data.LightRadioButton.grid(row=4, column =5)
    #canvas.data.DarkRadioButton = Tkinter.Radiobutton(canvas, text="Dark", variable= canvas.data.videoMode, value= "Dark")
    #canvas.data.DarkRadioButton.grid(row=5, column = 5)
    canvas.data.liveVideoCheckBox.deselect()
    canvas.data.testVideoCheckBox.deselect()
    canvas.data.showActiveCornersCheckBox.deselect()
    canvas.data.showActiveCheckBox.deselect()
    #canvas.data.LightRadioButton.select()
    Tkinter.Button(canvas, text="Save Preferences", \
    command=savePreferences).grid(row=0, column=1)
    Tkinter.Button(canvas, text="Open Preferences", \
    command=openPreferences).grid(row=1, column=1)
    
def actionButtons(canvas):
    #actionList = ("Open a File", "Increase Volume", "Decrease Volume", "Increase Brightness", "Decrease Brightness")
    actionList = ("Open a File")
    canvas.data.actionvariable1 = Tkinter.StringVar()
    canvas.data.actionvariable2 = Tkinter.StringVar()
    canvas.data.actionvariable3 = Tkinter.StringVar()
    canvas.data.actionvariable4 = Tkinter.StringVar()
    canvas.action1 = Tkinter.OptionMenu(canvas, \
    canvas.data.actionvariable1, actionList, command=callCheck())
    canvas.action1.grid(row=4, column=1)
    canvas.action2 = Tkinter.OptionMenu(canvas, \
    canvas.data.actionvariable2, actionList, command=callCheck())
    canvas.action2.grid(row=5, column=1)
    canvas.action3 = Tkinter.OptionMenu(canvas, \
    canvas.data.actionvariable3, actionList, command=callCheck())
    canvas.action3.grid(row=6, column=1)
    canvas.action4 = Tkinter.OptionMenu(canvas, \
    canvas.data.actionvariable4, actionList, command=callCheck())
    canvas.action4.grid(row=7, column=1)

def createLabels(canvas):
    actiontext1 = ""
    actiontext2 = ""
    actiontext3 = ""
    actiontext4 = ""
    if canvas.data.program1 != "None" and len(canvas.data.program1) > 0:
        #print "got here"
        text1 = canvas.data.program1.split("/")
        #print len(text1)
        actiontext1 = text1[len(text1)-1]
        #print actiontext1
        if len(actiontext1) > 30:
            actiontext1 = actiontext1[:30] + "..."
        if len(actiontext1) < 30:
            actiontext1 = actiontext1 + " "*(50-len(actiontext1))
    if canvas.data.program2 != "None" and len(canvas.data.program2) > 0:
        text2 = canvas.data.program2.split("/")
        actiontext2 = text2[len(text2)-1]
        #print actiontext2
        if len(actiontext2) > 30:
            actiontext2 = actiontext2[:30] + "..."
        if len(actiontext2) < 30:
            actiontext2 = actiontext2 + " "*(50-len(actiontext2))
    if canvas.data.program3 != "None" and len(canvas.data.program3) > 0:
        text3 = canvas.data.program3.split("/")
        actiontext3 = text3[len(text3)-1]
        if len(actiontext3) > 30:
            actiontext3 = actiontext3[:30] + "..."
        if len(actiontext3) < 30:
            actiontext3 = actiontext3 + " "*(50-len(actiontext3))
    if canvas.data.program4 != "None" and len(canvas.data.program4) > 0:
        text4 = canvas.data.program4.split("/")
        actiontext4 = text4[len(text4)-1]
        if len(actiontext4) > 30:
            actiontext4 = actiontext4[:30] + "..."
        if len(actiontext4) < 30:
            actiontext4 = actiontext4 + " "*(50-len(actiontext4))
    canvas.data.Label1 = Tkinter.Label(canvas, \
    text ="Action 1: "+actiontext1).grid(row=4, column=0, sticky = Tkinter.W)
   #Label1.rowconfigure(4, minsize = len(str("Action 1:"+actiontext1)))
    canvas.data.Label2 = Tkinter.Label(canvas,  \
    text ="Action 2: "+actiontext2).grid(row=5, column=0, sticky = Tkinter.W)
    Tkinter.Label(canvas, text ="Action 3: "+actiontext3).grid(row=6,  \
    column=0, sticky = Tkinter.W)
    Tkinter.Label(canvas, text ="Action 4: "+actiontext4).grid(row=7, \
    column=0, sticky = Tkinter.W)

def FileType(programextension):
    musicextensions = [".mp3", ".wma", ".flac", ".ogg"]
    videoextensions = [".wmv", ".avi", ".mp4", ".mkv", ".flv", \
    ".mov", ".mpg", ".mpeg"]
    textextensions = [".doc", ".docx", ".log", ".pages", ".txt"] 
    imageextensions = [".jpg", ".jpeg", ".gif", ".bmp", ".png"] 
    programextensions = [".exe", ".app"] 
    programmingextensions= [".py", ".c", ".java", ".pl", ".cs"] 
    musicicon = "icons/music_icon.png"
    videoicon = "icons/video_icon.png"
    texticon =  "icons/text_icon.png"
    imageicon = "icons/image_icon.png"
    programicon = "icons/program_icon.png"
    programmingicon =  "icons/programming_icon.png"
    if programextension in musicextensions:
        return musicicon
    elif programextension in videoextensions:
        return videoicon
    elif programextension in textextensions:
        return texticon
    elif programextension in imageextensions:
        return imageicon
    elif programextension in programextensions:
        return programicon
    elif programextension in programmingextensions:
        return programmingicon
        
def createActionImage(canvas, actionnumber):
    #print "program =" , program
    rownumber = actionnumber+3 
    #print  "rownumber =  ", rownumber
    if actionnumber == 1:
        #program = canvas.data.program1
        programsplit = canvas.data.program1.split("/")
        programname = programsplit[len(programsplit)-1]
        extensionlocation = programname.rfind(".")
        programextension = programname[extensionlocation:]
        #print "programextension =", programextension
        filepath = FileType(programextension)
        #print "filepath" , filepath
        fileimage = ImageTk.PhotoImage(Image.open(filepath))
        actionlabel1 = Tkinter.Label(canvas, \
        image = fileimage).grid(row=rownumber, column=3, sticky=Tkinter.W)
        canvas.data.actionlabel1image = fileimage
    elif actionnumber ==2:
        #program = canvas.data.program2
        programsplit = canvas.data.program2.split("/")
        programname = programsplit[len(programsplit)-1]
        extensionlocation = programname.rfind(".")
        programextension = programname[extensionlocation:]
        filepath = FileType(programextension) 
        try:
            fileimage = ImageTk.PhotoImage(Image.open(filepath))
            actionlabel2 = Tkinter.Label(canvas, \
            image = fileimage).grid(row=rownumber, column=3, sticky=Tkinter.W)
            canvas.data.actionlabel2image = fileimage
        except AttributeError as error:
            pass
    elif actionnumber == 3:
        #program = canvas.data.program3
        programsplit = canvas.data.program3.split("/")
        programname = programsplit[len(programsplit)-1]
        extensionlocation = programname.rfind(".")
        programextension = programname[extensionlocation:]
        filepath = FileType(programextension) 
        fileimage = ImageTk.PhotoImage(Image.open(filepath))
        canvas.actionlabel3 = Tkinter.Label(canvas, \
        image = fileimage).grid(row=rownumber, column=3, sticky=Tkinter.W)
        canvas.data.actionlabel3image = fileimage
    elif actionnumber ==4:
        #program = canvas.data.program4
        programsplit = canvas.data.program4.split("/")
        programname = programsplit[len(programsplit)-1]
        extensionlocation = programname.rfind(".")
        programextension = programname[extensionlocation:]
        filepath = FileType(programextension) 
        fileimage = ImageTk.PhotoImage(Image.open(filepath))
        actionlabel4 = Tkinter.Label(canvas, \
        image = fileimage).grid(row=rownumber, column=3, sticky=Tkinter.W)
        canvas.data.actionlabel4image = fileimage
    
def callCheck():
    canvas.data.actionvariable1.trace("w", callBack)
    canvas.data.actionvariable2.trace("w", callBack)
    canvas.data.actionvariable3.trace("w", callBack)    
    canvas.data.actionvariable4.trace("w", callBack)
    
def callBack(*args):
    #print "Variable Changed!!!!" 
    Action1(canvas)
    Action2(canvas)
    Action3(canvas)
    Action4(canvas)
    
def Action1(canvas): 
    #print canvas.data.actionvariable1.get(), "CAW CAW"
    if canvas.data.actionvariable1.get() == ("Open a File"):
        Tkinter.Button(canvas, text="Select File...", \
        command=askOpenFileName1).grid(row=4, column=2)
        
def Action2(canvas): 
    #print canvas.data.actionvariable2.get(), "CAW CAW2"
    if canvas.data.actionvariable2.get() == ("Open a File"):
        Tkinter.Button(canvas, text="Select File...", \
        command=askOpenFileName2).grid(row=5, column=2)
        
def Action3(canvas): 
    #print canvas.data.actionvariable3.get(), "CAW CAW3"
    if canvas.data.actionvariable3.get() == ("Open a File"):
        Tkinter.Button(canvas, text="Select File...", \
        command=askOpenFileName3).grid(row=6, column=2)
        
def Action4(canvas): 
    #print canvas.data.actionvariable4.get(), "CAW CAW4"
    if canvas.data.actionvariable4.get() == ("Open a File"):
        Tkinter.Button(canvas, text="Select File...", \
        command=askOpenFileName4).grid(row=7, column=2)

def savePreferences():
    if canvas.data.isPaused == False:
        tkMessageBox.showinfo("Error", \
        "Please stop before saving a new preferences file!")
        return None
    actions = [canvas.data.program1, canvas.data.program2, \
    canvas.data.program3, canvas.data.program4]
    filename = tkFileDialog.asksaveasfile(mode='w', \
    defaultextension = ".py", initialfile = "preferences.py")
    #filename = open("filename", "w")
    for path in actions:
        filename.write(path+"\n")
    filename.close()
    
def openPreferences():
    if canvas.data.isPaused == False:
        tkMessageBox.showinfo("Error", \
        "Please stop before opening a new preferences file!")
        return None
    try:
        programs = []
        filename = tkFileDialog.askopenfilename(**canvas.file_opt) 
        file = open(filename, "r")
        for line in file:
            newline = line.rstrip()
            programs += [newline] 
        canvas.data.program1 = programs[0]
        canvas.data.program2 = programs[1]
        canvas.data.program3 = programs[2]
        canvas.data.program4 = programs[3]
        createLabels(canvas)
    except IOError as error:
            tkMessageBox.showinfo("Error", \
            "Looks like you didn't select a preference file. Please try again")
    except IndexError as error:
            tkMessageBox.showinfo("Error", \
            "Looks like you didn't select a valid perference file. Please try again")
    createActionImage(canvas,1)
    createActionImage(canvas,2)
    createActionImage(canvas,3)
    createActionImage(canvas,4)
        
def askOpenFileName1():
    if canvas.data.isPaused == False:
        tkMessageBox.showinfo("Error", \
        "Please stop before selecting a new file!")
        return None
    filename = tkFileDialog.askopenfilename(**canvas.file_opt)
    print filename
    canvas.data.program1 = filename 
    try:
        canvas.data.Label1.destroy()
    except AttributeError as error:
        pass
    createLabels(canvas)
    createActionImage(canvas, 1)

def askOpenFileName2():
    if canvas.data.isPaused == False:
        tkMessageBox.showinfo("Error", \
        "Please stop before selecting a new file!")
        return None
    filename = tkFileDialog.askopenfilename(**canvas.file_opt)
    print filename
    canvas.data.program2 = filename
    try:
        canvas.data.Label2.destroy()
    except AttributeError as error:
        pass 
    createLabels(canvas)
    createActionImage(canvas, 2)

def askOpenFileName3():
    if canvas.data.isPaused == False:
        tkMessageBox.showinfo("Error", \
        "Please stop before selecting a new file!")
        return None
    filename = tkFileDialog.askopenfilename(**canvas.file_opt)
    print filename
    canvas.data.program3 = filename
    try:
        canvas.data.Label3.destroy()
    except AttributeError as error:
        pass 
    createLabels(canvas)
    createActionImage(canvas, 3)

def askOpenFileName4():
    if canvas.data.isPaused == False:
        tkMessageBox.showinfo("Error", \
        "Please stop before selecting a new file!")
        return None
    filename = tkFileDialog.askopenfilename(**canvas.file_opt)
    print filename
    canvas.data.program4 = filename 
    try:
        canvas.data.Label4.destroy()
    except AttributeError as error:
        pass
    createLabels(canvas)
    createActionImage(canvas, 4)
    
def run():
    global canvas
    global value
    root = Tkinter.Tk()
    canvasWidth = 10
    canvasHeight = 300
    canvas = Tkinter.Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    init()
    #root = Application()
    Application()
    root.title("Ethan's Application: Virtual Hot Corners v.1.0")
    timerFired()
    root.mainloop()
    #print "canvas is ACTIVATED!!! AWW YUEEHH"

run()

#root.mainloop()

#if __name__ == "__main__": #Change this to have TKINTER start it. 
   # cv.NamedWindow('Live Video!', cv.CV_WINDOW_AUTOSIZE)
    #set up connection to camera
    #capture = cv.CaptureFromCAM(0)
    #run()
    #if not capture:
     #   print "Error opening capture device"
      #  sys.exit(1)
    #cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    #cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    #print "stinkbug is stinky"
    #while 1:
     #   image = get_img(capture)
      #  hands = get_hands(image)
        # handle events
       # k = cv.WaitKey(5)
