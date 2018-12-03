import os

def execute(filename):
    path = "python tf/tensorflow/examples/speech_commands/label_wav.py --graph=/home/pi/CS370/raspberry-pi/tf_data/my_frozen_graph.pb --labels=/home/pi/CS370/raspberry-pi/tf_data/conv_labels.txt --wav=/home/pi/CS370/raspberry-pi/"
    path += filename + "\n"
    os.system(path)
