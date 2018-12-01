#Based off of: Displaying a video feed with OpenCv and Tkinter -- Adrian Rosebrock

from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading 
import imutils
import cv2
import os

class PhotoApp:
    def __init__(self, vs, outputPath):
        """Store the video stream object and output path, then initialize
        the most recently read frame, thread from reading frames and the
        thread stop event
            Inputs: vs-instantiation of a VideoStream
                    outputPath-path we want to store our captured snapshots
        """
        
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        
        #Initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
        
        #Create a button that when pressed, will take the current frame and save to file
        btn = tki.Button(self.root, text="Save Image!", command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        
        #Start a thread that constantly pools the video sensor for the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        
        #Set a Callback to handle when the window is closed (NEEDS WORK)
        self.root.wm_title("C & C Security")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        
    def videoLoop(self):
        """This function monitors our video stream for new frames"""
        try:
            #Keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                #Grab the frame from the video stream and resize it to have max width of 300px
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)
                
                #OpenCV represents images in BGR order but PIL represents images in
                # RGB order so we need to swap the changes and conver to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                
                #If the panel is nontNone, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                
                #Otherwise update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
                
        except RuntimeError:
            print("[INFO] caught a RuntimeError.")
            
    def takeSnapshot(self):
        """This function takes an image on take Image button click and saves the image as intruder.jpg"""
        filename = "intruder.jpg"
        p = os.path.sep.join((self.outputPath, filename))
        
        #Save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] save {}".format(filename))
        
    def onClose(self):
        """This function sets the stop event, cleans up the camera and allows the rest
            of the quit process to continue"""
        print("[INFO] closing..")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
            
    
        
        
        
