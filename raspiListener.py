import pyaudio
import wave
from scipy.io import wavfile


def main():
	writeInputToFile()
	readWavFile()


def writeInputToFile(filename="default.wav"):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 4
	WAVE_OUTPUT_FILENAME = filename

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
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


def readWavFile(filename='default.wav', debug=False):
	fs, data = wavfile.read(filename)
	
	if debug:
		print(fs)
		for val in data:
			print(val)

if __name__ == '__main__':
	main()