print "Loading, please wait..."

#first, import the matlab engine
import matlab.engine
#start the engine
eng = matlab.engine.start_matlab()
#run the test program
status = eng.grapher("1")
#output the returned value
print status

raw_input("Press enter to exit program.")


"""

About the status:

This has two purposes. First of all, it demonstrates getting a value
back from the matlab program. Second, the programs didn't want to work
together unless I made the matlab side return something. I don't have
to do anything with it on the python side.

"""
