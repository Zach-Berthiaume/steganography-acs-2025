import numpy as np
from pydub import AudioSegment
from pathlib import Path

def text_to_binary(text):
    return ''.join(format(ord(i), '08b') for i in text)

# makes sure that input file is in correct directory
def check_for_correct_dir(file_path):
    allowed_directory = Path('./').resolve()
    
    return file_path.is_relative_to(allowed_directory)

# get text file path
while (True):

    # take input for file to decode
    text_file = input('Input .txt file path with message to encode (must be within this directory): ')

    # canonicalize path to file and check that its valid
    text_file = Path(text_file).resolve()
    if check_for_correct_dir(text_file) and str(text_file).lower().endswith('.txt') and text_file.exists():
        print(text_file)
        break
    else:
        print("Please input a proper file or file path.")
        continue

# get audio file path
while (True):

    # take input for file to decode
    audio_file = input('Input .wav file path to encode message with (must be within this directory): ')

    # canonicalize path to file and check that its valid
    audio_file = Path(audio_file).resolve()
    if check_for_correct_dir(audio_file) and str(audio_file).lower().endswith('.wav') and audio_file.exists():
        print(audio_file)
        break
    else:
        print("Please input a proper file  or file path.")
        continue



# encode message into mp3 file and output to separate .txt file

# loads message from txt and converts to binary
with open(text_file, 'r') as file:
    message = file.read()
message = text_to_binary(message)

# adds marker to end of message for decoder
message += '10101010101010101'

# load mp3 into numpy array of amplitudes
audio = AudioSegment.from_wav(audio_file)
samples_array = np.array(audio.get_array_of_samples())

# makes sure message is short enough to be encoded in the audio
if len(message) > len(samples_array):
    print("Message is too long!")
    quit()

# flip rightmost bit in sample array when message contains 1
for i in range(len(message)):
    samples_array[i] ^= 1 if message[i] == '1' else 0

# export encoded sample_array
AudioSegment(samples_array.tobytes(), frame_rate = audio.frame_rate, sample_width = audio.sample_width, channels = audio.channels).export('encoded_audio.wav', format = 'wav')