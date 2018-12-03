import tkinter as tk
from PIL import Image, ImageTk
import picamera
from time import sleep
import argparse

import vuMeter
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
    camera.preview_fullscreen=False
    placeCamera()
    camera.resolution=(640,480)
    camera.start_preview()
    
def unlockDevice():
    
    cameraOn()
    #Disable unlock device button
    unlockButton.config(state=tk.DISABLED)    

    #Remove lock image from screen
    #placeVoiceWaves()
    canvas.delete(lockImage)
    canvas.update()
    
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

        #Turn off the camera
        cameraOFF()
        
        #Display the lock image
        lockImg = Image.open('./images/lock.png')
        lockImg = lockImg.resize((400, 400))
        lockImg = ImageTk.PhotoImage(lockImg)
        lImg = canvas.create_image(56, 30, anchor=tk.NW, image=lockImg)
        canvas.image =lockImg
        
        #Alert the user the device remains locked
        tk.Label(root, text="AUTHENTICATION FAILED. DEVICE REMAINS LOCKED", fg="red", font="Unbuntu 32 bold").pack(fill=tk.X)
    else:
        #Turn off the camera
        cameraOFF()
        
        #Display the unlock image
        unlockImg = Image.open('./images/unlock.png')
        unlockImg = unlockImg.resize((400, 400))
        unlockImg = ImageTk.PhotoImage(unlockImg)
        uImg = canvas.create_image(0, 50, anchor=tk.NW, image=unlockImg)
        canvas.image=unlockImg

        #Alert the user their device has been unlocked
        tk.Label(root, text="YOUR DEVICE HAS BEEN UNLOCKED", fg="red", font="Unbuntu 32 bold").pack(fill=tk.X)

def cameraOFF():
    camera.stop_preview()
    
def EXIT():
    root.destroy
    camera.stop_preview()
    camera.close()
    quit()

def placeVoiceWaves():
    """This function places the voice wave graph on the left side of the gui"""
       
    #Calculate the height and width plot
    #Width and height are in inches and we are using 100 px per inch
    waveWidth = (root.winfo_screenwidth()*SPACE_FACTOR*0.5)/100
    waveHeight = (root.winfo_screenheight()*SPACE_FACTOR*0.5)/100

    #Place the plot on the left side of the GUI
    x = root.winfo_screenwidth() - waveWidth
    y = root.winfo_screenheight() - waveHeight
    
    print(waveWidth, waveHeight, x, y)
    vuMeter.plotStream(3, 3, 100, 100)
    #Generate the plot
    #vuMeter.plotStream(waveWidth, waveHeight, x, y)

def placeCamera():
    """This function places the camera on the right side of the gui"""
    
    #Calculate the height and width of the GUI
    guiWidth = root.winfo_screenwidth()*SPACE_FACTOR
    guiHeight = root.winfo_screenheight()*SPACE_FACTOR
    
    #The camera will take up half of the GUI space
    #cameraWidth = guiWidth*0.5
    #cameraHeight = guiHeight*0.5
    
    cameraWidth = guiWidth * 0.7
    cameraHeight = guiHeight * 0.7

    #Place the camera on the right side of GUI centered
    #x = (root.winfo_screenwidth() * 0.5) 
    y = (root.winfo_screenheight() * 0.55) - (cameraHeight * 0.5)
    x = (root.winfo_screenwidth() * 0.55) - (cameraWidth * 0.55)    
    print(guiWidth, guiHeight)
    print(x,y, cameraWidth, cameraHeight)
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
    canvas = tk.Canvas(root, width=512, height=542)
    canvas.pack()
    
    #Resize the image and place in canvase
    img = Image.open("./images/lock.png")
    img = img.resize((400,400))
    img = ImageTk.PhotoImage(img)
    lockImage = canvas.create_image(56, 30, anchor=tk.NW, image=img)
    
    #Option to start program or exit program
    tk.Button(root, text="EXIT PROGRAM", command=EXIT, font="Unbuntu 24 bold").pack(side=tk.BOTTOM, fill=tk.X)
    unlockButton = tk.Button(root, text="UNLOCK YOUR DEVICE", command=unlockDevice, font = "Unbuntu 24 bold")
    unlockButton.pack(side=tk.BOTTOM, fill=tk.X)

    #enable next line to lock window in place                     
    #root.overrideredirect(True)

    root.mainloop()
