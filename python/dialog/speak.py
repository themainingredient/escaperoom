# Based on: https://github.com/jeysonmc/python-google-speech-scripts/blob/master/stt_google.py 
#

import io
import os
import string
import sys

import pyaudio
import wave

# Imports the Google Cloud client libraries
#
from google.cloud import texttospeech
from google.cloud import speech

file_name = os.path.join(
    os.path.dirname(__file__),
    '..',
    'resources',
    'output.wav')

# Speak to a text file
#
def speak(text):
    if (text != None and text != ""):
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        #
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

        # Select the type of audio file you want returned
        #
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        #
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        #
        with open(file_name, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            # print('Audio content written to file "',file_name,'"')
        return True, file_name 
    return False, None

# play text file
def play(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    chunk = 1024
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

# For testing 
# 
if __name__ == '__main__':
    text = "The Main Street!"
    filename = speak(text)
    play(filename)
    print("done")
