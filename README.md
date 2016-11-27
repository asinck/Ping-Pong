#Ping Pong

This is an implementation for a robot to play ping pong.
 
###Overview of program
This program uses a webcam to track movement of items of a selected color (default is red). It will then decide what area is moving the most, and tell the robotic arms where to go.


There are two dots that jump around the output feed: a green dot and a white dot. The green dot is where the program thinks the most motion (for the chosen color) is. The white dot is a little more conservative than the green dot, in that it won't move too far at a time. This is for possible sanity checks for where the object being tracked could be, because the object can only move so far at a time.


There are also a couple gray lines. These represent the linear actuators that the robot uses. These are what will position the ping pong paddle (the blue dot). On the Raspberry Pi, the frame rate is slow enough that it simulates where the arms are. On a computer, the frame rate is too high and the arms will jump all over.


###Running the program
To run this program, run testDependencies.py to check that all the required libraries are installed (see Dependencies for more details). If that works, then run pingpong.py. This will begin the program, defaulting to motion detection of red objects. See Supported Colors for more information. 

 
###Supported Colors:
The following eight colors are supported:
Red, orange, and yellow are easily seen, but have a fair amount of noise and overlap.
Blue and aqua work fairly well.
Purple and pink detection can depend on the lighting.
Green color detection doesn't work too well, except for light green.

Use the first letter of a color to select it for color detection. Pink is selected with 'i'.


###Dependencies
This program uses python 2.7. Please make sure you're using the correct version. You can check this with `python -V` or `python --version`.
The following libraries are required to run this program.
 - opencv: This is the image processing library. This is central to the program.
 - numpy: This works with opencv.
 - time and math: These are general libraries for the program.
 - RPi.GPIO: This is a library for running the program on a Raspberry Pi, which is the hardware side of the project. If this is not installed, the program will run in simulation mode.

Time and math should be installed already on linux.

To install opencv and numpy on linux, run `sudo apt-get install -y python-numpy python-opencv`.
