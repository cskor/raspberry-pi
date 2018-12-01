import Tkinter as tk
import picamera

camera = picamera.PiCamera()

def CameraON():
    camera.preview_fullscreen=False
    camera.preview_window=(90,100, 320, 240)
    camera.resolution=(640,480)
    camera.start_preview()
    
def CameraOFF():
    camera.stop_preview()
    
def EXIT():
    root.destroy
    camera.stop_preview()
    camera.close()
    quit()

root = tk.Tk()

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

guiWidth = 500
guiHeight = 300

x = (screenWidth/2) - (guiWidth/2)
y = (screenHeight/2) - (guiHeight/2)

root.geometry('%dx%d+%d+%d' % (guiWidth, guiHeight, x, y))

root.resizable(width=False, height=False)
#root.geometry("320x300+89+50")
root.title("Camera Button Test")

root.buttonframe = tk.Frame(root)
root.buttonframe.grid(row=5, column=3, columnspan=2)

tk.Button(root.buttonframe, text='Start Camera', command=CameraON).grid(row=1, column = 1)
tk.Button(root.buttonframe, text='Kill Camera', command=CameraOFF).grid(row=1, column = 2)
tk.Button(root.buttonframe, text='Exit Program', command=EXIT).grid(row=1, column = 3)


#enable next line to lock window in place                     
#root.overrideredirect(True)

root.mainloop()
