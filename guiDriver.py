from __future__ import print_function
from PhotoApp import PhotoApp
from imutils.video import VideoStream
import argparse
import time

#Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the PiCamera should be used")
args = vars(ap.parse_args())

#Initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"]>0).start()
time.sleep(2.0)

#Start the app
app = PhotoApp(vs, "./")
app.root.mainloop()