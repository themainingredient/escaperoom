import unittest
import time
from .. import *

class TestAction(unittest.TestCase):
    def setUp(self):
        # setup stuff 

        # wait a little
        time.sleep(0.5)

    def actionMethod(self, **kwargs):
        return True

    def applyAction(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            return(action_method(**kwargs))            
        else:
            raise Exception("The action should be valid")

    def test_actionCreate(self):
        testaction = action.Action(method=self.actionMethod)
        self.assertTrue(testaction != None)
        self.assertTrue(testaction.method.__name__ == "actionMethod")

    def test_actionApply(self):
        testaction = action.Action(method=self.actionMethod)
        self.assertTrue(self.applyAction(testaction) == True)

if __name__ == '__main__':
    unittest.main()
