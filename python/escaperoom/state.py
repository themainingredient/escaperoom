# State machine 
#

class StateMachine():
    def __init__(self):
        self.states = {}
        self.activeState = None

    def addState(self, stateName, description, active=False):
        state = State(stateName, description)
        self.states[state.name] = state 
        if (active):
            self.activeState = state             

    def addTransition(self, fromStateName, transitionName, toStateName, result="Ok.", points=0):
        assert fromStateName in self.states
        assert toStateName in self.states
        fromState = self.states[fromStateName]
        toState = self.states[toStateName]
        transition = Transition(transitionName, fromState, toState, result, points)
        fromState.addTransition(transition)

    def getState(self):
        return self.activeState

    def hasState(self, stateName):
        return stateName in self.states

    def canApplyTransition(self, transitionName):
        if self.activeState != None:
            if transitionName in self.activeState.transitions:
                transition = self.activeState.getTransition(transitionName)
                return self.activeState.canApplyTransition(transition)
        return False

    def applyTransition(self, transitionName):
        if self.activeState != None:
            if self.canApplyTransition(transitionName):
                transition = self.activeState.getTransition(transitionName)
                self.activeState = self.activeState.applyTransition(transition)
                
                # Only award points the first time 
                #
                points = transition.points 
                transition.points = 0

                return transition.result, points
            else: 
                return "You can't do that.", 0
        raise Exception("There is no active state.")

class State():    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.transitions = {}

    def __str__(self):
        return self.name

    def addTransition(self, transition):
        self.transitions[transition.name] = transition

    def getTransition(self, transitionName):
        assert transitionName in self.transitions
        return self.transitions[transitionName]

    def hasTransition(self, transition):
        return transition.name in self.transitions

    def canApplyTransition(self, transition):
        if self.hasTransition(transition):
            return True
        else:
            return False

    def applyTransition(self, transition):        
        if self.canApplyTransition(transition): 
            return transition.toState
        return self


class Transition():
    def __init__(self, name, fromState, toState, result="Ok.", points=0):
        self.name = name
        self.fromState = fromState
        self.toState = toState 
        self.result = result
        self.points = points

    
