import Tkinter as tk
import picamera
import raspiListener
import takeImage

MAX_FREQ = 600
TO_ADDRESS = "cassidy.skor@gmail.com"
AUDIO_FILE = 'unlock.wav'
SPACE_FACTOR = 0.8

def cameraOn():
    camera.preview_fullscreen=False
    placeCamera()
    camera.resolution=(640,480)
    camera.start_preview()
    
def unlockDevice():
    cameraOn()
    #Record the audio as file unlock.wav
    raspiListener.writeInputToFile(AUDIO_FILE)
    
    #Reading the wav file and saving the max freq
    recordedMaxFreq = raspiListener.readWavFile(AUDIO_FILE)
    
    #This is the current version of an intruder
    if(recordedMaxFreq > MAX_FREQ):
        #Take the photo of the intruder
        camera.capture('./intruder.jpg')
        
        #Send the email to the supplied address
        takeImage.sendPhoto(TO_ADDRESS)
        
    else:
        print("Your device has been unlocked.")
    
    
def CameraOFF():
    camera.stop_preview()
    
def EXIT():
    root.destroy
    camera.stop_preview()
    camera.close()
    quit()

def placeCamera():
    """This function places the camera on the right side of the gui"""
    
    guiWidth = root.winfo_screenwidth()*SPACE_FACTOR
    guiHeight = root.winfo_screenheight()*SPACE_FACTOR
    
    cameraWidth = guiWidth*0.5
    cameraHeight = guiHeight*0.5
    
    x = (root.winfo_screenwidth() * 0.5) #+ root.winfo_screenwidth()*0.1
    y = (root.winfo_screenheight() * 0.5) - (cameraHeight * 0.5)

    camera.preview_window=(int(x), int(y), int(cameraWidth), int(cameraHeight))

def centerWindow():
    """This function places the GUI in the center of the screen
            Inputs: width, height
    """
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    
    width = screenWidth*SPACE_FACTOR
    height = screenHeight*SPACE_FACTOR
    
    x = (screenWidth/2) - (width/2)
    y = (screenHeight/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.resizable(width=False, height=False)
    return width, height


root = tk.Tk()
camera = picamera.PiCamera()
width, _ = centerWindow()
root.title("C & C Security")

tk.Label(root, text="WELCOME TO YOUR C & C SECURITY DEVICE", fg="black",font="Unbuntu 36 bold").pack(fill=tk.X, pady=5)
tk.Button(root, text="UNLOCK YOUR DEVICE", command=unlockDevice, font = "Unbuntu 24 bold").pack(side=tk.BOTTOM, fill=tk.X)


#startCamera = tk.Button(root, text="Start Camera", command=CameraON, font="Unbuntu 24 bold")
#startCamera.pack(side=tk.BOTTOM) 
#killCamera = tk.Button(root, text="Kill Camera", command=CameraOFF, font="Unbuntu 24 bold")
#killCamera.pack(side=tk.BOTTOM)
#root.buttonframe = tk.Frame(root)
#root.buttonframe.grid(row=5, column=3)

#tk.Label(root, text="WELCOME TO YOUR C & C SECURITY DEVICE", fg="black",font="Unbuntu 36 bold").grid(row=1)
#tk.Button(root.buttonframe, text='Start Camera', command=CameraON).grid(row=5, column = 1)
#tk.Button(root.buttonframe, text='Kill Camera', command=CameraOFF).grid(row=5, column = 2)
#tk.Button(root.buttonframe, text='Exit Program', command=EXIT).grid(row=5, column = 3)


#enable next line to lock window in place                     
#root.overrideredirect(True)

root.mainloop()
