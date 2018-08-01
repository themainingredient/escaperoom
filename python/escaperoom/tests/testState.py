import unittest
import time
from .. import *

class TestState(unittest.TestCase):
    def setUp(self):
        # setup stuff 

        # wait a little
        time.sleep(0.5)

    def test_stateCreate(self):
        teststate = state.State("State1", "The first test state")
        self.assertTrue(teststate != None)
        self.assertTrue(teststate.name == "State1")
        self.assertTrue(teststate.description == "The first test state")
        self.assertTrue(teststate.transitions == {})        

    def test_transitionCreate(self):
        teststate1 = state.State("State1", "The first test state")
        self.assertTrue(teststate1 != None)
        teststate2 = state.State("State2", "The second test state")
        self.assertTrue(teststate2 != None)
        testtransition = state.Transition("Test", teststate1, teststate2, result="Test OK.")
        self.assertTrue(testtransition != None)
        self.assertTrue(testtransition.name == "Test")
        self.assertTrue(testtransition.fromState == teststate1)
        self.assertTrue(testtransition.toState == teststate2)
        self.assertTrue(testtransition.result == "Test OK.")

    def test_statemachineCreate(self):
        teststatemachine = state.StateMachine()
        self.assertTrue(teststatemachine != None)
        self.assertTrue(teststatemachine.states == {})
        self.assertTrue(teststatemachine.activeState == None)
    
    def test_stateAddTransition(self):
        teststate1 = state.State("State1", "The first test state")
        teststate2 = state.State("State2", "The second test state")
        testtransition = state.Transition("Test", teststate1, teststate2, result="Test OK.")
        teststate1.addTransition(testtransition)
        self.assertTrue(teststate1.transitions == {"Test":testtransition})

    def test_stateGetTransition(self):
        teststate1 = state.State("State1", "The first test state")
        teststate2 = state.State("State2", "The second test state")
        testtransition = state.Transition("Test", teststate1, teststate2, result="Test OK.")
        teststate1.addTransition(testtransition)
        t = teststate1.getTransition("Test")
        self.assertTrue(t == testtransition)
        exceptionfound = False
        exception = None
        try:
            t2 = teststate1.getTransition("NonexistentTransition")
        except Exception as e:
            exception = e
            exceptionfound = True
            self.assertTrue(type(e).__name__ == "AssertionError")   
        
        self.assertTrue(exceptionfound)
        self.assertTrue(type(exception).__name__ == "AssertionError")   

    def test_stateHasTransition(self):
        teststate1 = state.State("State1", "The first test state")
        teststate2 = state.State("State2", "The second test state")
        testtransition = state.Transition("Test", teststate1, teststate2, result="Test OK.")
        teststate1.addTransition(testtransition)
        nonexistenttransition = state.Transition("NonexistentTransition", teststate1, teststate2, result="Test OK.")
        self.assertTrue(teststate1.hasTransition(testtransition))
        self.assertFalse(teststate1.hasTransition(nonexistenttransition))

    def test_stateCanApplyTransition(self):
        teststate1 = state.State("State1", "The first test state")
        teststate2 = state.State("State2", "The second test state")
        testtransition = state.Transition("Test", teststate1, teststate2, result="Test OK.")
        teststate1.addTransition(testtransition)
        nonexistenttransition = state.Transition("NonexistentTransition", teststate1, teststate2, result="Test OK.")
        self.assertTrue(teststate1.canApplyTransition(testtransition))
        self.assertFalse(teststate1.canApplyTransition(nonexistenttransition))

    def test_stateApplyTransition(self):
        teststate1 = state.State("State1", "The first test state")
        teststate2 = state.State("State2", "The second test state")

        # state 1 to state 2
        testtransition1 = state.Transition("Forward", teststate1, teststate2, result="Test OK.")
        teststate1.addTransition(testtransition1)

        # nonexistent 
        nonexistenttransition = state.Transition("NonexistentTransition", teststate1, teststate2, result="Test OK.")

        # succesful transition teststate1 -> teststate2
        toState = teststate1.applyTransition(testtransition1)  
        self.assertTrue(toState == testtransition1.toState, "Applicable transition should return transition toState.")

        toState = teststate1.applyTransition(nonexistenttransition)  
        self.assertTrue(teststate1.applyTransition(nonexistenttransition) == testtransition1.fromState, msg="Nonexistent transitions should return fromState.")

    def test_statmachineAddState(self):
        teststatemachine = state.StateMachine()
        teststatemachine.addState("TestState","TestDescription")
        self.assertTrue("TestState" in teststatemachine.states, msg="TestState should now be part of states")
        self.assertTrue(teststatemachine.activeState == None, msg="Active state should not be changed")
        teststatemachine.addState("TestState2","TestDescription", True)
        self.assertTrue("TestState2" in teststatemachine.states, msg="TestState2 should now be part of states")
        self.assertTrue(teststatemachine.activeState == teststatemachine.states["TestState2"], msg="Active state should be changed")

    def test_statmachineGetState(self):
        teststatemachine = state.StateMachine()
        teststatemachine.addState("TestState","TestDescription")

        teststate = teststatemachine.getState()
        self.assertTrue(teststate == None, msg="Active state should not be changed unless adding state with active=True")
        self.assertTrue(teststate == teststatemachine.activeState)

        teststatemachine.addState("TestState2","TestDescription", True)
        teststate = teststatemachine.getState()
        self.assertTrue(teststate == teststatemachine.states["TestState2"], msg="Active state should be changed when adding state with active=True")
        self.assertTrue(teststate == teststatemachine.activeState)

    def test_statmachineHasState(self):
        teststatemachine = state.StateMachine()
        teststatemachine.addState("TestState","TestDescription")

        self.assertTrue(teststatemachine.hasState("TestState") == True)
        self.assertTrue(teststatemachine.hasState("NonexistentState") == False)

    def test_statmachineAddTransition(self):
        teststatemachine = state.StateMachine()
        teststatemachine.addState("TestState","TestDescription")
        teststatemachine.addState("TestState2","TestDescription")
        teststatemachine.addTransition("TestState", "Transition", "TestState2", result="Halp")
        self.assertTrue(teststatemachine.hasState("TestState") == True)
        self.assertTrue(teststatemachine.hasState("TestState2") == True)

        teststate  = teststatemachine.states["TestState"]
        teststate2 = teststatemachine.states["TestState2"]

        self.assertTrue("Transition" in teststate.transitions) 
        self.assertFalse("Transition" in teststate2.transitions) 

    def test_statmachineCanApplyTransition(self):
        teststatemachine = state.StateMachine()
        teststatemachine.addState("TestState","TestDescription", True)
        teststatemachine.addState("TestState2","TestDescription")
        teststatemachine.addTransition("TestState", "Transition", "TestState2", result="Halp")
        teststatemachine.addTransition("TestState2", "NotApplicableTransition", "TestState", result="Halp")

        self.assertTrue(teststatemachine.canApplyTransition("Transition"))
        self.assertFalse(teststatemachine.canApplyTransition("NotApplicableTransition"))

        self.assertFalse(teststatemachine.canApplyTransition("NonexistentTransition"))

    def test_statmachineApplyTransition(self):
        teststatemachine = state.StateMachine()
        teststatemachine.addState("TestState1","TestDescription 1", True)
        teststatemachine.addState("TestState2","TestDescription 2")

        teststatemachine.addTransition("TestState1", "Forward", "TestState2", result="Forward", points=10)
        teststatemachine.addTransition("TestState2", "Back", "TestState1", result="Back", points=20)
        teststatemachine.addTransition("TestState1", "NotApplicableTransition", "TestState2", result="Nopper", points=30)

        self.assertTrue(teststatemachine.activeState.name == "TestState1", msg="Start state is incorrect.")

        # TestState1 -> TestState2 
        #
        result, points = teststatemachine.applyTransition("Forward")
        self.assertTrue(result == "Forward")
        self.assertTrue(points == 10, msg="First transition should award 10 points")
        self.assertTrue(teststatemachine.activeState.name == "TestState2", msg="Should have ended up in TestState2")

        # TestState2 -> nonexistent link 
        result, points = teststatemachine.applyTransition("NotApplicableTransition")
        self.assertTrue(result == "You can't do that.", msg="Should not be possible from this state.")
        self.assertTrue(points == 0, msg="This should not award points.")

        # TestState2 -> TestState1 
        # 
        result, points = teststatemachine.applyTransition("Back")
        self.assertTrue(result == "Back")
        self.assertTrue(points == 20, msg="First transition should award 10 points")
        self.assertTrue(teststatemachine.activeState.name == "TestState1", msg="Should have ended up in TestState1")

        # TestState1 -> TestState2 second time
        #
        result, points = teststatemachine.applyTransition("Forward")
        self.assertTrue(result == "Forward")
        self.assertTrue(points == 0, msg="Subsequent transitions should award 0 points")
        self.assertTrue(teststatemachine.activeState.name == "TestState2", msg="Should have ended up in TestState2")

if __name__ == '__main__':
    unittest.main()
