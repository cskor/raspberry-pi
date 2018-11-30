import raspiListener
import takeImage

MAX_FREQ = 600
TO_ADDRESS = "cassidy.skor@gmail.com"
AUDIO_FILE = 'unlock.wav'

if __name__ == "__main__":
    """Currently, we are just recording a sound and if the max freq of that
        sound is greater than the MAX_FREQ we are saying that is an intruder 
        and to run the intruder code 
    """
    #Record the audio as file unlock.wav
    raspiListener.writeInputToFile(AUDIO_FILE)
    
    #Reading the wav file and saving the max freq
    recordedMaxFreq = raspiListener.readWavFile(AUDIO_FILE)
    
    #This is the current version of an intruder
    if(recordedMaxFreq > MAX_FREQ):
        #Take the photo of the intruder
        takeImage.takePhoto()
        
        #Send the email to the supplied address
        takeImage.sendPhoto(TO_ADDRESS)
        
    else:
        print("Your device has been unlocked.")
    
    
