import cv2 as cv
import numpy as np
import time
import math

positionx = 0
positiony = 0

#this will look at the difference between frames
def diffImg(t0, t1, t2):
    d1 = cv.absdiff(t2, t1)
    d2 = cv.absdiff(t1, t0)
    return cv.bitwise_or(d1, d2)

prevLocation = None
#this function returns coordinates. if the provided coordinates are
#close enough to the previous ones, it returns them. if not, it
#returns the previous set
def coordinates((x, y)):
    global prevLocation
    tolerance = 250 #how many pixels it can jump
    #if a previous location was not recorded, return the current one
    if (not prevLocation):
        prevLocation = (x, y)
        return x, y

    px, py = prevLocation[0], prevLocation[1]
    dist = math.sqrt(pow(px-x, 2) + pow(py-y, 2))
    if (dist > tolerance):
        return px, py

    prevLocation = (x, y)
    return x, y

#this function scales points to match what's needed.
scaleX = 1000
scaleY = 1000
webcamX = 0
webcamY = 0

def scale((x, y)):
    #ratio
    #inputX / webcamX = outputY / scaleX
    #inputY / webcamY = outputY / scaleY

    #solving, 
    #outputY =  scaleX * (inputX / webcamX)
    #outputY = scaleY * (inputY / webcamY)

    #note: this might have an issue if the origin (x, y) is in a
    #different corner
    # x increases left to right
    # y increases top to bottom
    # for the webcam, (0, 0) is in the top left corner
    outputX = int(scaleX * ((x*1.0)/(webcamX*1.0)))
    outputY = int(scaleY * ((y*1.0)/(webcamY*1.0)))
    return (outputX, outputY)
    


# see color-notes.txt for the explanation of the colors below.
colors = {
    "r" :  ([  0, 100, 120], [ 10, 255, 255]),
    "g" :  ([ 60, 100,  20], [ 90, 255, 255]),
    "b" :  ([110, 100, 100], [130, 255, 255]),
    "a" :  ([ 90, 100,  50], [110, 255, 255]),
    "p" :  ([130, 100,  50], [150, 255, 175]),
    "i" :  ([140, 100, 100], [160, 255, 255]),
    "y" :  ([ 10, 100,  50], [ 40, 255, 255]),
    "o" :  ([  5, 100,  00], [ 20, 255, 214])
}

colorFilter = colors['r']
lower = np.array(colorFilter[0])
upper = np.array(colorFilter[1])

#connect to the webcam

#this is to allow the user to choose what webcam they want if they
#have multiple webcams plugged in
num = raw_input("webcam number?  ")
webcam = None
try:
    webcam = cv.VideoCapture(int(num)-1)
except:
    print "Enter webcam number."
    exit(1)

#make sure it's a valid webcam
try:
    cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)
except:
    print "\nError: Could not read data from webcam %s. Is it plugged in?\n" %num
    exit(1)

# Read three images first:
t_minus = cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)
t = cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)
t_plus = cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)

webcamY, webcamX = t.shape[:2]
print "Using webcam dimensions: %dx%d" %(webcamX, webcamY)
print "Scaling to dimensions: %dx%d" %(scaleX, scaleY)

#window reference and title
capture = "Color Motion Tracker"
#make a window
cv.namedWindow(capture, cv.CV_WINDOW_AUTOSIZE)
jump = (0, 0)

#keep taking frames
while True:

    # Read next image
    t_minus = t
    t = t_plus
    color = webcam.read()[1]
    HSV = cv.cvtColor(color, cv.COLOR_BGR2HSV)
    t_plus = cv.cvtColor(color, cv.COLOR_RGB2GRAY)
    
    #take a frame
    frame = diffImg(t_minus, t, t_plus)
    frame = cv.GaussianBlur(frame, (3,3), 0)

    #mask = cv.inRange(color, lower, upper)
    mask = cv.inRange(HSV, lower, upper)
    maskedFrame = cv.bitwise_and(color, color, mask = mask)
    colorMotionMask = cv.bitwise_and(frame, frame, mask = mask)
    still = int(cv.mean(colorMotionMask)[0]*100) < 4
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(colorMotionMask)
    #(dx, dy) = (maxLoc1[0]-maxLoc2[0], maxLoc1[0]-maxLoc2[0])
    
    #if nothing's going on in the image, don't update
    if (not still):
        x, y = coordinates(maxLoc)
        #jump = maxLoc
        jump = (x, y)

    cv.circle(maskedFrame, maxLoc, 4, (0, 255, 0), 5)
    cv.circle(maskedFrame, jump, 4, (255, 255, 255), 5)
    print "_"*75
    print "Relevant area 1:", maxLoc
    print "Relevant area 2:", jump
    
    print "Area of most motion", scale(maxLoc)
    print "Denoised area of most motion", scale(jump)
    print "_"*75
    print

    #show the frame
    cv.imshow(capture, maskedFrame)
    #cv.imshow("color motion", colorMotionMask)
    #cv.imshow(capture, color)

    #if a key is pressed, deal with it
    key = cv.waitKey(10)
    code_offset = 1048576
    if (key > code_offset):
        key -= code_offset
    #quit if key is escape
    if key == 27: #this is the code for Esc
        cv.destroyWindow(capture)
        break    
    #if it's the key for red, green, blue, ...
    elif key > 0 and key < 256 and chr(key) in "rgbapiyo":
        colorFilter = colors[chr(key)]
        #changeColor(key)
        print chr(key)
        lower = np.array(colorFilter[0])
        upper = np.array(colorFilter[1])
        prevLocation = None

