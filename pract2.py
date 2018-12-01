import Tkinter as tk
import picamera

SPACE_FACTOR = 0.8


def CameraON():
    camera.preview_fullscreen=False
    placeCamera()
    camera.resolution=(640,480)
    camera.start_preview()
    
def CameraOFF():
    camera.stop_preview()
    
def EXIT():
    root.destroy
    camera.stop_preview()
    camera.close()
    quit()

def placeCamera():

    guiWidth = root.winfo_screenwidth()*SPACE_FACTOR
    guiHeight = root.winfo_screenheight()*SPACE_FACTOR
    
    cameraWidth = guiWidth*SPACE_FACTOR/2
    cameraHeight = guiHeight*SPACE_FACTOR/2
    
    x = (root.winfo_screenwidth()/2) + int(root.winfo_screenwidth()*0.1)
    y = (root.winfo_screenheight()/2) + (cameraHeight/2)
            
    camera.preview_window=(x, y, cameraWidth, cameraHeight)
    
    

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


root = tk.Tk()
camera = picamera.PiCamera()
centerWindow()
root.title("Camera Button Test")

root.buttonframe = tk.Frame(root)
root.buttonframe.grid(row=5, column=3, columnspan=2)

tk.Button(root.buttonframe, text='Start Camera', command=CameraON).grid(row=1, column = 1)
tk.Button(root.buttonframe, text='Kill Camera', command=CameraOFF).grid(row=1, column = 2)
tk.Button(root.buttonframe, text='Exit Program', command=EXIT).grid(row=1, column = 3)


#enable next line to lock window in place                     
#root.overrideredirect(True)

root.mainloop()
