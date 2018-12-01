import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time

RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second

def plotStream():
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    plt.show()
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('xkcd:black')
    ax.axis([0, CHUNK, -5000, 5000])
    ax.patch.set_facecolor('xkcd:black')
    line, = ax.plot(data)

    while True: # Main loop which updates the plot line
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        line.set_ydata(data)
        plt.pause(0.001)

    plt.close()       
    stream.stop_stream()
    stream.close()
    p.terminate()
    

if __name__ == "__main__":
    plotStream()