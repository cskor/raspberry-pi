import tkinter as tk
from PIL import Image, ImageTk
import picamera
from time import sleep
import argparse

import raspiListener
import takeImage
import parseResults
import runTensorflow
import evaluateCommand

AUDIO_FILE = 'unlock.wav'
SPACE_FACTOR = 0.8
OUTPUT_FILE = './results.txt'
ACCEPTED_WORDS = ['yes', 'down', 'left']
#ACCEPTED_WORDS = ['cassidy', 'caleb', 'shrideep']
THRESHOLD = .65

def cameraOn():
    canvas.delete(lockImage)
    camera.preview_fullscreen=False
    placeCamera()
    #TODO play with resolutions
    camera.resolution=(640,480)
    camera.start_preview()
    
def unlockDevice():
    cameraOn()
    
    #Record the audio as file unlock.wav
    raspiListener.writeInputToFile(AUDIO_FILE)
    
    #Run tensorflow on the recorded file
    runTensorflow.execute(AUDIO_FILE)
    
    #Parse the results of the tensorflow
    word, certainty = parseResults.parseResults(OUTPUT_FILE)
    
    #Evaluate where to unlock or not
    unlock = evaluateCommand.evaluate(word, certainty, THRESHOLD, ACCEPTED_WORDS)
   
    #Unauthorized access to account
    if not unlock:
        #Take the photo of the intruder
        camera.capture('./intruder.jpg')
        
        #Send the email to the supplied address
        takeImage.sendPhoto(toAddress)
        
    else:
        #Turn off the camera
        cameraOFF()
        
        #Alert the user their device has been unlocked
        tk.Label(root, text="YOUR DEVICE HAS BEEN UNLOCKED", fg="red", font="Unbuntu 32 bold").pack(fill=tk.X)

def cameraOFF():
    camera.stop_preview()
    
def EXIT():
    root.destroy
    camera.stop_preview()
    camera.close()
    quit()

def placeCamera():
    """This function places the camera on the right side of the gui"""
    
    #Calculate the height and width of the GUI
    guiWidth = root.winfo_screenwidth()*SPACE_FACTOR
    guiHeight = root.winfo_screenheight()*SPACE_FACTOR
    
    #The camera will take up half of the GUI space
    cameraWidth = guiWidth*0.5
    cameraHeight = guiHeight*0.5
    
    #Place the camera on the right side of GUI centered
    x = (root.winfo_screenwidth() * 0.5) 
    y = (root.winfo_screenheight() * 0.5) - (cameraHeight * 0.5)
    camera.preview_window=(int(x), int(y), int(cameraWidth), int(cameraHeight))

def centerWindow():
    """This function places the GUI in the center of the screen
            Outputs: width, height
    """
    #Get the size of the screen
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    
    #We want our GUI to take up part of the screen
    width = screenWidth*SPACE_FACTOR
    height = screenHeight*SPACE_FACTOR
    
    #Place the GUI in the center of the screen
    x = (screenWidth/2) - (width/2)
    y = (screenHeight/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.resizable(width=False, height=False)
    return width, height

if __name__ == "__main__":
    #Optional argument for email to send message to
    ap = argparse.ArgumentParser()
    ap.add_argument("email", nargs='?')
    args = vars(ap.parse_args())
    if args['email']:
        toAddress = args['email']
    else:
        toAddress = "CandCSec370@gmail.com"

    #Create the GUI
    root = tk.Tk()
    
    #Initialize the Camera
    camera = picamera.PiCamera()
    
    #Center the Gui
    width, height = centerWindow()
    
    #GUI Layout
    root.title("C & C Security")
    tk.Label(root, text="WELCOME TO YOUR C & C SECURITY DEVICE", fg="black",font="Unbuntu 36 bold").pack(fill=tk.X, pady=5)
       
    #Place a lock image on the GUI
    canvas = tk.Canvas(root, width=400, height=550)
    canvas.pack()

    #Resize the image and place in canvase
    img = Image.open("./images/lock.png")
    img = img.resize((400,400))
    img = ImageTk.PhotoImage(img)
    lockImage = canvas.create_image(0, 50, anchor=tk.NW, image=img)

    #Option to start program or exit program
    tk.Button(root, text="EXIT PROGRAM", command=EXIT, font="Unbuntu 24 bold").pack(side=tk.BOTTOM, fill=tk.X)
    tk.Button(root, text="UNLOCK YOUR DEVICE", command=unlockDevice, font = "Unbuntu 24 bold").pack(side=tk.BOTTOM, fill=tk.X)

    #enable next line to lock window in place                     
    #root.overrideredirect(True)

    root.mainloop()
