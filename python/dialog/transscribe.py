# Transscribe audio file 
#
import io

# Imports the Google Cloud client libraries
#
from google.cloud import texttospeech
from google.cloud import speech

RATE = 24000
LANG_CODE = 'en-US'  # Language to use

def transscribe(filename):
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    # file_name = os.path.join(
    #     os.path.dirname(__file__),
    #     'resources',
    #     'output.wav')

    # Loads the audio into memory
    with io.open(filename, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=LANG_CODE)

    # Detects speech in the audio file
    #
    response = client.recognize(config, audio)

    # show the response
    #
    # print(response)

    text = ""
    for result in response.results:
        # print('Transcript: {}'.format(result.alternatives[0].transcript))
        transcript = str(result.alternatives[0].transcript)
        text = text + transcript

    return(text, response)