from picamera import PiCamera
from time import sleep

if __name__ == "__main__":
    camera = PiCamera()
    
    camera.start_preview()
    sleep(10)
    camera.stop_preview()