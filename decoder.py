import numpy as np
from pydub import AudioSegment
from pathlib import Path

def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

# makes sure that input file is in correct directory
def check_for_correct_dir(file_path):
    allowed_directory = Path('./').resolve()
    
    return file_path.is_relative_to(allowed_directory)

# get audio file path
while (True):

    # take input for file to decode
    audio_file = input('Input .wav file path to decode message with (must be within this directory): ')

    # canonicalize path to file and check that its valid
    audio_file = Path(audio_file).resolve()
    if check_for_correct_dir(audio_file) and str(audio_file).lower().endswith('.wav') and audio_file.exists():
        print(audio_file)
        break
    else:
        print("Please input a proper file  or file path.")
        continue

# load mp3 into numpy array of amplitudes
audio = AudioSegment.from_wav(audio_file)
samples_array = np.array(audio.get_array_of_samples())

# extract message by looking for start and end of message
message = ''
for i in samples_array:
    message += str(i & 1)
    if message.endswith('11001100110011001'):
        message = ''
    if message.endswith('10101010101010101'):
        break

# export decoded message to new file
with open('decoded_message.txt', 'w') as file:
    file.write(binary_to_text(message[:-17]))