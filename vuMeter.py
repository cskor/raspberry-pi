import pyaudio
#import alsaaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import time
#import array

# constants
CHANNELS = 1
RATE = 16000
CHUNK = 1024 # RATE / number of updates per second

def plotStream(width, height, x, y):
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=CHANNELS,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    plt.rcParams['toolbar'] = 'None'
    plt.show()
    data = np.fromstring(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
    
    fig, ax = plt.subplots(figsize=(width, height))
    fig.canvas.manager.window.wm_geometry("+%d+%d" % (x,y))
    fig.patch.set_facecolor('xkcd:black')
    ax.axis([0, CHUNK, -5000, 5000])
    ax.patch.set_facecolor('xkcd:black')
    line, = ax.plot(data)
    

    while True: # Main loop which updates the plot line
        data = np.fromstring(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
        line.set_ydata(data)
        plt.pause(0.001)

    plt.close()       
    stream.stop_stream()
    stream.close()
    p.terminate()
    

if __name__ == "__main__":
    plotStream()
