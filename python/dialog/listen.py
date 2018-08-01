# Based on: https://github.com/jeysonmc/python-google-speech-scripts/blob/master/stt_google.py 
#

import pyaudio
import wave
import audioop
from collections import deque
import os
import time
import math

import io
import string

# Imports the Google Cloud client libraries
#
from google.cloud import texttospeech
from google.cloud import speech

LANG_CODE = 'en-US'  # Language to use

# FLAC_CONV = 'flac -f'  # We need a WAV to FLAC converter. flac is available
#                        # on Linux

# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000
THRESHOLD = 2000  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.

file_name = os.path.join(
    os.path.dirname(__file__),
    '..',
    'resources',
    'record.wav')

WAVE_FILENAME = file_name

def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    print("Getting intensity values from mic.")
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
              for x in range(num_samples)]
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print(" Finished ")
    print(" Average audio intensity is ", r)
    stream.close()
    p.terminate()
    return r

def listen_for_speech(threshold=THRESHOLD):
    """
    Listens to Microphone, extracts phrases from it and sends it to
    Google's TTS service and returns response. a "phrase" is sound
    surrounded by silence (according to threshold). num_phrases controls
    how many phrases to process before finishing the listening process
    (-1 for infinite).
    """

    # Open stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening... ")

    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=int(SILENCE_LIMIT * rel))
    
    # Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=int(PREV_AUDIO * rel))
    started = False
    finished = False 
    
    while (not finished):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))

        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                print("Starting record of phrase.")
                started = True
            audio2send.append(cur_data)
        elif (started is True):                                    
            # The limit was reached, cleanup, finish capture and deliver.
            #
            finished = True
            print("Finished recording.")
            stream.close()
            p.terminate()

            filename = save_speech(list(prev_audio) + audio2send, p)

            # Return the filename 
            # 
            return filename            

        else:
            prev_audio.append(cur_data)

    raise Exception("Reached the end of listen_for_speech without capturing audio")

def save_speech(data, p):
    """ Saves mic data to temporary WAV file. Returns filename of saved
        file """
    
    filename = os.path.join(os.path.dirname(__file__),
                            '..',
                            'resources',
                            'output_'+str(int(time.time())) + '.wav')

    # writes data to WAV file
    # data = ''.join(data)
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(data))
    waveFile.close()

    return filename

# for testing 
# 
if(__name__ == '__main__'):
    listen_for_speech()  # listen to mic.
    print("done")