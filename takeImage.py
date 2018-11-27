from picamera import PiCamera
from time import sleep
import emailImage

def takePhoto():
    camera = PiCamera()
    
    camera.start_preview()
    sleep(10)
    camera.capture('./intruder.jpg')
    camera.stop_preview()

def sendPhoto():
    fromAddress = "CandCSec370@gmail.com"
    toAddress = "pearcenatalie96@gmail.com"
    password = "grounds4lyfe"
    
    attachFile = ["intruder.jpg", "./intruder.jpg"]
    contents = ["Attempted Access", emailImage.generateEmailBody(attachFile[0])]
    
    emailImage.sendEmail(fromAddress, toAddress, password, contents, attachFile)
    print("Your email to %s has been sent." % toAddress)
    
if __name__ == "__main__":
    takePhoto()
    sendPhoto()