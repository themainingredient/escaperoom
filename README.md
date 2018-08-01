# Escaperoom Text Adventure with Google Dialog Flow and Speech API

First, we'll build a simple escape room text adventure using Google Speech-to-text, Dialog Flow, and Speech API. And then we'll make it run on Google AIY Voice Kit, or Google Assistant. 

## Development

### Installs 
`pip install --upgrade google-cloud`

### Listening to speech
The first step is to make the system recognize speech. We'll start by loading a wav file and processing the speech in it. Then, we'll add microphone capability.  

#### Installing Cloud Speech To Text
[https://cloud.google.com/speech-to-text/](https://cloud.google.com/speech-to-text/)

[Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart) 

`pip install --upgrade google-cloud-speech` 

#### Record from microphone 

`pip install --upgrade pyaudio`



#### Triggering
The speech recognizer will need to determine when to listen for commands. We need a trigger ('wake word' or 'hotword') for that. 

In this case, I use a setup that listens for new sentences all the time. This means, it will respond as soon as someone is speaking. There is no hotword. 


### Talking Back

Again, we'll start by recording the speech to a wav file. Then, we'll play that file. 

#### Installing Text-to-speech API on MacOSX 

[https://cloud.google.com/text-to-speech/](https://cloud.google.com/text-to-speech/) 
* Get cloud text-to-speech API 
* follow the steps to setup the credentials 
* run the quickstart example 

#### Record to file 
done. 

#### Play sound 
done.

### Creating a Dialog 

#### Installing Dialog Flow API on MacOSX 

`pip install dialogflow`

#### Link Python to Dialog Flow 
http://dialogflow-python-client-v2.readthedocs.io/en/latest/

#### Create a basic Dialog Test 

### Escape Room 

#### Adding the adventure logic 

### Playing the game 

## On Google AIY Voice Kit



## Deploying to Google Assistant 


Installing update 
use 
```
pip install google-cloud-speech
pip install google-cloud-texttospeech
pip install dialogflow 
```
google-cloud as import has just been deprecated and will lead to conflict as google.oauth2 will end up to be duplicate. 
