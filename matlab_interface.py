print "Loading, please wait..."

#first, import the matlab engine
try:
    import matlab.engine
except:
    print "Please install the matlab package before running this program. See"
    print "https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html"
    exit(1)
#start the engine
eng = matlab.engine.start_matlab()
#run the test program
status = eng.grapher("1")
#output the returned value
print status

#this is so the program doesn't immediatly exit after showing the
#graph for a moment
raw_input("Press enter to exit program.")


"""

About the status:

This has two purposes. First of all, it demonstrates getting a value
back from the matlab program. Second, the programs didn't want to work
together unless I made the matlab side return something. I don't have
to do anything with it on the python side.

"""
