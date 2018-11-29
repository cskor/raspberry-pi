import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft

locked = False

def main():
	writeInputToFile()
	readWavFile()


def writeInputToFile(filename="default.wav"):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 1
	WAVE_OUTPUT_FILENAME = filename

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		input_device_index=4,
                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


def readWavFile(filename='default.wav', debug=False, key=803):
	frequencyRate, data = wav.read("default.wav") # load the data

	firstChannelAudio = data.T[0]
	print(firstChannelAudio[20000])
	min = 0
	max = 0

	for i in range(0, len(firstChannelAudio)):
		if firstChannelAudio[i] < min:
			min = firstChannelAudio[i]
		elif firstChannelAudio[i] > max:
			max = firstChannelAudio[i]

	# this is 16-bit signed track, now normalized on [-1,1)
	normalizedData = [(element/(2**15.)) for element in firstChannelAudio]

	# analyzed FFT data from normalized data
	analyzedData = fft(normalizedData)

	# find max freq from complex numbers
	maxSpl = -1
	maxFreq = -1
	for i in range(0, len(analyzedData)//2):
		# each index is a frequency
		if abs(analyzedData[i]) > maxSpl:
			maxSpl = abs(analyzedData[i])
			maxFreq = i
			

	print("MAX FREQUENCY: " + str(maxFreq) + "Hz")
	if (abs(key-maxFreq) < 3):
		toggleLock()
	else: shutDown()

	plt.plot(abs(analyzedData[:(len(analyzedData)//2)]),'r')
	plt.show()
	
def toggleLock():
	global locked
	locked = not(locked)
	print("Locked is : " + str(locked))

def shutDown():
	print("Shutting down for 30 seconds")

if __name__ == '__main__':
	main()
