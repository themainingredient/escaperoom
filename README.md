# Escaperoom Text Adventure with Google Dialog Flow and Speech API

The background story is presented [here](https://medium.com/p/1542df2e8203/edit). 

## Getting Started
It is highly recommended to setup a python virtual environment for this project. The Google Cloud dependencies can impact other installed packages.

### Installing
`python setup.py`

If you're doing it by hand: make sure you are *not* installing (or have installed) the base `google.cloud` as it has been recently deprecated and will make a mess. They want you to install only the components you need. 

### Prerequisites 
To be able to use Dialogflow, you'll need a Dialogflow project and a service account. Please follow [these steps](https://medium.com/r/?url=https%3A%2F%2Fdialogflow.com%2Fdocs%2Freference%2Fv2-auth-setup) to setup the service account, but don't install the cloud API from this page as it should already be installed! You'll need to download the Service Account's credentials file as json and create the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to that file as instructed.  

To listen, we need Google Cloud Speech API. To speak, we'll use TextToSpeech Beta. These both require a Google Cloud account. We'll use the same Service Account as we used for Dialogflow, with the same project id. In Google Cloud Console, you'll need to activate several API's for that account, namely Dialogflow, Google Speech API and Google TextToSpeech API. More detailed instructions (with pictures) can be found [here](https://medium.com/p/1542df2e8203/edit). 

To make everything work, you need to setup Dialogflow. In the blogpost you can also find how to do that. In the repository there is a .zip file with all the settings you need. You can upload this in Dialogflow to get the exact same setup. 

### Running the Game
Run using `python setup.py --speech_in --speech_out` for speech based setup or `python setup.py` for text only version in the console. 

### Tests
Tests have been created using python's unittest framework. I used Visual Studio Code to setup running the tests. Your setup may require the import statements to be organized differently.

## References 
In building this game, I modified code coming from these awesome repos:

* [JeysonMC Google Speech Scripts](https://github.com/jeysonmc/python-google-speech-scripts/blob/master/stt_google.py)
* [Google Dialogflow Python Client](https://dialogflow-python-client-v2.readthedocs.io/en/latest/)


