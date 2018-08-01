import os
import sys
import string
import uuid
import argparse

from dialog.dialog import *
from dialog.listen import *
from dialog.speak import *
from dialog.transscribe import *

from escaperoom import *
from escaperoom.world import theworld

# json support
#
from google.protobuf.json_format import MessageToJson
import json

SESSION_ID = str(uuid.uuid4())          # A random generated session ID to identify this session with DialogFlow
PROJECT_ID = "<YOUR GOOGLE PROJECT ID>" # The name of your DialogFlow project
LANG_CODE = 'en-US'                     # Language to use
USE_SPEECH_IN = False                   # will be overwritten by args
USE_SPEECH_OUT = False                  # will be overwritten by args
DEBUG = False                           # will be overwritten by args

# Parsing arguments
#
ap = argparse.ArgumentParser(description="Escaperoom text-adventure game with Dialogflow")
ap.add_argument('--speech_out', action="store_true", help='Use the speech generator if present, text output otherwise.')
ap.add_argument('--speech_in', action="store_true", help='Use the speech recognizer if present, text input otherwise.')
ap.add_argument('--debug', action="store_true", help="If present, print extra debug output.")
args, _ = ap.parse_known_args()

print(args)

if args.speech_in:
    USE_SPEECH_IN = True
if args.speech_out:
    USE_SPEECH_OUT = True
if args.debug:
    DEBUG = True

# Debug print
#
def print_gamestate() :
    print("---------------------------------------------")
    print(world.theworld.getWorldState())

# Get text input
#
def get_text_input():
    text = input(">")
    return text

# Detect the intent from transscript
#
def detect_intent(transscript):
    if (transscript != "" and transscript != None):

        intent, response = detect_intent_texts(PROJECT_ID,SESSION_ID, [transscript], LANG_CODE)

        if DEBUG:
            print("Intent detected:",intent, response.query_result)

        jsonObj = MessageToJson(response.query_result)
        params = json.loads(jsonObj)["parameters"]

        return intent, params
    return None, None

# Handle action
#
def handle_intent(intent, params=None):
    if intent != None:
        arg1 = None
        arg2 = None

        if (params != None):
            if 'Item' in params:
                if (isinstance(params['Item'], list)):
                    if (len(params['Item'])>0):
                        arg1 = params['Item'][0]
                else:
                    arg1 = params['Item']
            if 'Item1' in params:
                if (isinstance(params['Item1'], list)):
                    if (len(params['Item1'])>0):
                        arg2 = params['Item1'][0]
                else:
                    arg2 = params['Item1']

        result = theworld.applyAction(intent, item_name=arg1, seconditem_name=arg2)

        return result
    return None

# speak the reply
#
def speak_reply(reply):
    result, filename = speak(reply)
    if (result):
        play(filename)
    else:
        result, filename = speak("I didn't get that.")
        play(filename)

# just print the reply
#
def print_reply(reply):
    print(reply)

if(__name__ == '__main__'):
    if USE_SPEECH_OUT:
        speak_reply(world.theworld.startMessage)
    else:
        print_reply(world.theworld.startMessage)

    while (world.theworld.won == False) and (world.theworld.quit == False):
        if USE_SPEECH_IN:
            filename = listen_for_speech()
            transscript, _ = transscribe(filename)
            os.remove(filename)
        else:
            transscript = get_text_input()
        intent, params = detect_intent(transscript)
        reply = handle_intent(intent, params)
        if USE_SPEECH_OUT:
            speak_reply(reply)
        else:
            print_reply(reply)
