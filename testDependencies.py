#!/usr/bin/env python

#this is a list of import commands. If the user doesn't have Tkinter
#or other libraries installed, it will fail gracefully instead of
#crashing.
imports = [
    "import cv2 as cv",
    "import numpy as np",
    "import time",
    "import math"
]
#failedPackages will keep a record of the names of the packages that
#failed to import, so that the program can go through the entire list
#of packages that it wants to import. This will allow the program to
#give the user a complete list of packages that they need to install,
#instead of only telling the user one at a time.
failedPackages = ''
for i in imports:
    try:
        exec(i)
    except ImportError as error:
        failedPackages += str(error) + '\n'
#if there were any errors in the imports, tell the user what packages
#didn't import, and exit.
if len(failedPackages) > 0:
    print "Some packages could not be imported:"
    print failedPackages
    print "\nPlease install these packages before running any of the webcam programs.\n"
    exit(1)

else:
    print "All dependencies satisfied."
