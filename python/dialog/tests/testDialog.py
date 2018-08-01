import unittest
import time
import uuid
from dialog.dialog import *
from dialog.speak import *
from dialog.transscribe import *
from dialog.listen import *

class TestDialog(unittest.TestCase):
    # def setUp(self):
    #     # setup stuff 

    def test_speak_transscribe(self):
        # check if text is recorded to wav file 
        #

        # punctuation is removed in the output so setup translator 
        # for punctuation removal 
        translator = str.maketrans('', '', string.punctuation)

        testphrases = ["testing 1 2 3", "hello world!", "alas, dear Yorick!"]        
        for testphrase in testphrases:

            # speak to tmp file 
            #
            result, filename = speak(testphrase)            
            self.assertTrue(result == True)

            # transscribe back from file 
            #  
            text, response = transscribe(filename)
            self.assertTrue(text == testphrase.translate(translator))
    
    # the listen module is harder to test since it depends on mic... 
    #     

    # dialog is dependent on the setup in DialogFlow 
    # 
    def test_dialog(self):

        SESSION_ID = str(uuid.uuid4())
        PROJECT_ID = "hackathon-ai-voice"
        LANG_CODE = 'en-US'  # Language to use

        testphrases     = ["Hello", "What do i see?", "Pickup the key", "Use the small key on the door", "Open the box", "Drop the box"]
        expectedintents = ["Default Welcome Intent", "LookAround", "Pickup", "Use", "Open", "Drop"]
        for i in range(len(testphrases)):
            testphrase       = testphrases[i]
            expectedintent   = expectedintents[i] 
            intent, response = detect_intent_texts(PROJECT_ID, SESSION_ID, [testphrase], LANG_CODE)
            self.assertTrue(expectedintent == intent, msg="("+str(i)+") Expected intent "+expectedintent+" but got "+intent)

if __name__ == '__main__':
    unittest.main()
