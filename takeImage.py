from picamera import PiCamera
from time import sleep
import emailImage

WAIT_TIME = 5

def takePhoto(): 
    """ This function uses the picamera library to take a photo 
        and save in it the current directory as intruder.jpg
    """
        
    camera = PiCamera()
    
    camera.start_preview()
    sleep(WAIT_TIME)
    camera.capture('./intruder.jpg')
    camera.stop_preview()

def sendPhoto(toAddress):
    """This function sends an email to the provided address
        Inputs:
            toAddress: address you want to send the email to
    """
    fromAddress = "CandCSec370@gmail.com"
    password = "grounds4lyfe"
 
    attachFile = ["intruder.jpg", "./intruder.jpg"]
    contents = ["Attempted Access", emailImage.generateEmailBody(attachFile[0])]
    
    emailImage.sendEmail(fromAddress, toAddress, password, contents, attachFile)
    print("Your email to %s has been sent." % toAddress)
    
if __name__ == "__main__":
    takePhoto()
    sendPhoto("cassidy.skor@gmail.com")
