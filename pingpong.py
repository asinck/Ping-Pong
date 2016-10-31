#the original of this program is in ~/programming/python/gui/colorTracker.py


#this program should control the mouse based on motion.

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


#see the following link for RGB and HSV stuff
#http://docs.opencv.org/trunk/df/d9d/tutorial_py_colorspaces.html

#My initial attempts with RGB bounds
# red    =  ([90, 90, 180], [120, 120, 255])
# green  =  ([90, 100, 90], [150, 255, 150])
# blue   =  ([60, 30, 30], [255, 150, 150])
# aqua   =  ([180, 180, 90], [255, 255, 120])
# purple =  ([180, 90, 180], [255, 120, 255])
# yellow =  ([90, 180, 180], [120, 255, 255])

#HSV
#these are the values according to the cv library for RGBAPY, respectively
#Note: these are values using full brightness in RGB
# [[[  0 255 255]]]
# [[[ 60 255 255]]]
# [[[120 255 255]]]
# [[[ 90 255 255]]]
# [[[150 255 255]]]
# [[[ 30 255 255]]]

#results with these:
# R - perfect, except for picking up skin
# G - it seems to not like dark green
# B - pretty awesome
# A - seems fine, afaict
# P - expects colors too light; picks up pink but not "dark" purple
# Y - needs "darker" yellow

#I had to substitute based on the following values (GBR)
#g: [  0, 180,   0] gave [[[ 60 255 180]]]
#p: [175,   0, 125] gave [[[141 255 175]]]
#y: [  0, 200, 200] gave [[[ 30 255 200]]]
#I also took the original purple and named it pink, and added orange:
#o: [0, 122, 204] gave [102 255 204]
#I took an "orange" color that worked for aqua and used it

#after imports, I just used this line for grabbing values,
#substituting the color values as needed
#print cv2.cvtColor(np.uint8([[[0, 200, 200]]]), cv2.COLOR_BGR2HSV)
#[142 255 200]
#[ 18 255 204]
colors = {
"r" :  ([  0, 100, 120], [ 10, 255, 255]),
"g" :  ([ 50, 100,  20], [ 70, 255, 255]),
"b" :  ([110, 100, 100], [130, 255, 255]),
"a" :  ([ 90, 100,  50], [110, 255, 255]),
"p" :  ([130, 100,  50], [150, 255, 175]),
"i" :  ([140, 100, 100], [160, 255, 255]),
"y" :  ([ 10, 100,  50], [ 40, 255, 255]),
"o" :  ([  5, 100,  00], [ 20, 255, 214])
}
#final adjustments:
#red: increase the minimum Value, to reduce noise due to skin
#green: darken it
#purple: darken it
#pink: it's the original purple
#yellow: allow darker yellow
#and some calibration

colorFilter = colors['r']
lower = np.array(colorFilter[0])
upper = np.array(colorFilter[1])

#connect to the webcam
num = raw_input("webcam number?  ")
webcam = None
try:
    webcam = cv.VideoCapture(int(num)-1)
except:
    print "Enter a number."
    exit(1)
    
#webcam = cv.VideoCapture(0)

# Read three images first:
try:
    cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)
except:
    print "\nError: Could not read data from webcam %s. Is it plugged in?\n" %num
    exit(1)

t_minus = cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)
t = cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)
t_plus = cv.cvtColor(webcam.read()[1], cv.COLOR_RGB2GRAY)

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

