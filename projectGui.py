import Tkinter
from picamera import PiCamera

class PiCameraApp():
    def __init__(self, root, camera, title):
        self.root = root
        
        self.camera = camera
        self.camera.start_preview(fullscreen=False, window=(0,0,10,10))
        
        self.title = title
        self.root.title(title)
        
        master = root
        
        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.config(padx=5, pady=5)
        

if __name__ == '__main__':
    print("starting")
    win = Tkinter.Tk()
    camera = PiCamera()
    
    win.minsize(1024, 768)
    app = PiCameraApp(win, camera, "testing")
    
    win.mainloop()
    camera.close()
    
    
