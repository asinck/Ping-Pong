#Ping Pong

This is an implementation for a robot to play ping pong.
 
###Overview of program
This program uses a webcam to track movement of items of a selected color (default is red). It will then decide what area is moving the most, and relay that point (after scaling) to matlab for it to process. Matlab will take the point, and do trajectory prediction with that point and the previous several points, and then tell a robot where to move.

###Running the program
To run this program, run testDependencies.py to check that all the required libraries are installed (see Dependencies for more details). If that works, then run pingpong.py. This will begin the program, defaulting to motion detection of red objects. See Supported Colors for more information. 

 
###Supported Colors:
The following eight colors are supported:
Red, orange, and yellow are easily seen, but have a fair amount of noise and overlap.
Blue and aqua work fairly well.
Purple and pink detection can depend on the lighting.
Green color detection doens't work too well, except for light green.

Use the first letter of a color to select it for color detection. Pink is selected with 'i'.


###Dependencies
This program uses python 2.7. Please make sure you're using the correct version. You can check this with `python -V` or `python --version`.
The following libraries are (or will be) required to run this program.
 - opencv: This is the image processing library. This is central to the program.
 - numpy: This works with opencv.
 - time and math: These are general libraries for the program.
 - matlab.engine: This is for working with the matlab side of the program. This is not currently required for the webcam program, but will be integrated as the project progresses.

Time and math should be installed already on linux.

To install opencv and numpy on linux, run `sudo apt-get install python-numpy python-opencv`.

To install matlab.engine, see
https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

