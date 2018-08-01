import escaperoom
from escaperoom.action import Action
from escaperoom.state import StateMachine, State, Transition
from escaperoom.utils import getDictDescription

# Reform statemachine so it can set flags, instead of probing specific states probe flags 
# Rename to Objects
# instead of things like canPickup make a list of abilities (as state is now)

class Item():

    # Items right now are all unique. 
    #
    def __init__(self, name, short, description, parts=None, items=None, parent=None, container=None, canPickup=False, canDrop=False, points=0):
        self.name = name
        self.short = short
        self.description = description
        self.parts = parts        
        self.items = items
        self.parent = parent
        self.container = container
        self.canPickup = canPickup         
        self.canDrop = canDrop         
        self.points = points

        if items == None:
            self.items = []
        if parts == None:
            self.parts = []
        
        self.statemachine = StateMachine()

    # Todo get prettified parts lists and so on in sep functions 
    #
    def __str__(self):
        # basic description
        descr = self.description.lower()
        
        # parts list 
        parts = self.getParts()
        spacer = ""
        if (parts != ""):
            spacer = " "
        descr = descr + spacer + parts        

        # is it part of something?
        parent = "" 
        spacer = ""
        if self.parent != None:
            if self.parent.name != "room":
                parent = "It's part of the " + self.parent.name + "."        
        if parent != "":
            spacer = " "
        descr = descr + spacer + parent

        # is it contained? 
        container = "" 
        spacer = ""
        if self.container != None:
            container = "It's in the " + self.container.name + "."
        if container != "":
            spacer = " "
        descr = descr + spacer + container  

        # items contained and accessible 
        items = self.getAccessibleItems()
        spacer = ""
        if (items != ""):
            spacer = " "
        descr = descr + spacer + items

        # current state 
        state = ""
        spacer = ""
        if self.statemachine.activeState != None:
            state = self.statemachine.activeState.description
        if (state != ""):
            spacer = " "
        descr = descr + spacer + state
         
        return descr 

    def getAccessibleItems(self):
        descr = ""
        if self.canBeAccessed():                
            if len(self.items) > 0:                
                descr = descr + "It contains "
                descr = descr + getDictDescription(self.items)
        return descr
    
    def getParts(self):
        descr = ""
        if len(self.parts) > 0:            
            descr = descr + "It has "
            descr = descr + getDictDescription(self.parts)            
        return descr    

    def getState(self):
        return str(self.statemachine.getState())

    def hasState(self, stateName):
        return self.statemachine.hasState(stateName)
    
    def serialize(self, json):
        raise NotImplementedError

    def deserialize(self, json):
        raise NotImplementedError

    def getPoints(self):
        return self.points

    # get the points value and reset it to zero
    # to make sure we count only once 
    # 
    def extractPoints(self):
        points = self.points
        self.points=0
        return points

    # remove an item 
    # 
    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            item.container = None
    
    # store an item 
    # 
    def storeItem(self, item):
        if self.canDrop:
            self.items.append(item)
            item.container = self

    # contains an item 
    #
    def containsItem(self, item):
        return item in self.items

    # detach a part
    # 
    def detachPart(self, part):
        self.parts.remove(part)
    
    # attach a part
    # 
    def attachPart(self, part):
        self.parts.append(part)

    # contains a part 
    #
    def containsPart(self, part):
        return part in self.parts    

    # can be accessed
    #
    def canBeAccessed(self):        
        if (self.hasState("isOpen")):
            if (self.getState() == "isOpen"):
                return True             
            else:
                return False
        return True

    # check up the tree for the state being true 
    #
    def checkParentTree(self, state):
        if self.statemachine.getState() == state:       
            return True
        if (self.container != None):
            return self.container.checkParentTree(state)
        if (self.parent != None):
            return self.parent.checkParentTree(state)
        return False

        