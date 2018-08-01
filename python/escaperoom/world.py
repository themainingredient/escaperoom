import escaperoom
from escaperoom.item import Item
from escaperoom.action import Action
from escaperoom.state import StateMachine
from escaperoom.utils import getDictDescription, getListDescription

# Add Events ! Self destruct timer 
# Add Agent  : Rat
# Add factory

# single room world 
#
class World():
    def __init__(self):
                
        # actions 
        #
        action_lookAround  = Action(method=self.actionLookAround)       
        action_open        = Action(method=self.actionOpen)
        action_close       = Action(method=self.actionClose)
        action_pickup      = Action(method=self.actionPickup)
        action_drop        = Action(method=self.actionDrop)
        action_lookAt      = Action(method=self.actionLookAt)
        action_use         = Action(method=self.actionUse)
        action_inventory   = Action(method=self.actionInventory)
        action_listActions = Action(method=self.actionListActions)
        action_getPoints   = Action(method=self.actionGetPoints)
        action_read        = Action(method=self.actionRead)
        action_exit        = Action(method=self.actionExit)
        action_quit        = Action(method=self.actionQuit)
        self.actions = {"LookAround":action_lookAround, 
                        "Open":action_open,
                        "Close":action_close, 
                        "OpenDoor":action_open,
                        "Pickup":action_pickup,
                        "Drop":action_drop,
                        "LookAt":action_lookAt,
                        "Use":action_use,
                        "Inventory":action_inventory,
                        "ListActions":action_listActions,
                        "GetPoints":action_getPoints,
                        "Read":action_read,
                        "Exit":action_exit,
                        "Quit":action_quit}

        # items
        #                
        key     = Item(name="key",      short="A key", description="A big silver key.", canPickup=True, points=10)
        drawer  = Item(name="drawer",   short="A drawer", description="A rickety old drawer.", items=[key], canDrop=True)        
        key.container = drawer

        desktop = Item(name="desktop",  short="A desktop", description="A scratched desktop surface.", canDrop=True)
        legs    = Item(name="legs",     short="Four table legs", description="Four wobbly table legs.")
        desk    = Item(name="desk",     short="A desk", description="An old, mouldy wooden desk.", parts=[drawer, desktop, legs])
        drawer.parent = desk
        legs.parent = desk
        desktop.parent = desk

        lock    = Item(name="lock",     short="A lock", description="A big silver lock.")
        door    = Item(name="door",     short="A door", description="A heavy wooden door.", parts=[lock])        
        lock.parent = door 

        smallkey= Item(name="small key",short="A small key", description="A small rusty key.", canPickup=True, points=10)        
        writing = Item(name="writing",  short="Scribbly writing", description="Seriously bad handwriting. A doctor must have been involved in writing it.")
        paper   = Item(name="paper",    short="A small piece of paper", description="A scrap of paper. There seems to be something written on it.", parts=[writing], canPickup=True, points=5)
        writing.parent = paper 

        box     = Item(name="box",      short="A box", description="A cardboard box.", items=[smallkey, paper], canDrop=True)        
        smallkey.container = box
        paper.container = box

        room    = Item(name="room",     short="A room", description="A small dusty room.", parts=[desk, door, box], canDrop=True)        
        door.parent = room 
        desk.parent = room 

        self.items = {"key": key,
                      "small key": smallkey,
                      "drawer": drawer,
                      "desktop": desktop,
                      "legs": legs,
                      "desk": desk,
                      "door": door,
                      "lock": lock,
                      "room": room,
                      "paper": paper,
                      "writing":writing,
                      "box": box}       

        drawer.statemachine.addState("isLocked", "It seems to be locked.", active=True)
        drawer.statemachine.addState("isClosed", "It's closed.")
        drawer.statemachine.addState("isOpen", "It's open.")
        drawer.statemachine.addTransition("isLocked", "Usesmall key", "isClosed", result="You unlocked the drawer.", points=5)
        drawer.statemachine.addTransition("isLocked", "UseKey", "isLocked", result="The key doesn't fit.")
        drawer.statemachine.addTransition("isLocked", "Open",   "isLocked", result="It's locked.")
        drawer.statemachine.addTransition("isLocked", "Close",  "isLocked", result="It's already closed.")
        drawer.statemachine.addTransition("isClosed", "Usesmall key", "isLocked", result="You locked the drawer.")
        drawer.statemachine.addTransition("isClosed", "Usekey", "isClosed", result="The key doesn't fit.")
        drawer.statemachine.addTransition("isClosed", "Open",   "isOpen",   result="You opened the drawer.", points=5)
        drawer.statemachine.addTransition("isClosed", "Close",  "isClosed", result="It's already closed.")
        drawer.statemachine.addTransition("isOpen",   "Usesmall key", "isOpen",   result="Close it first.")
        drawer.statemachine.addTransition("isOpen",   "Usekey", "isOpen",   result="The key doesn't fit.")
        drawer.statemachine.addTransition("isOpen",   "Open",   "isOpen",   result="It's already open.")
        drawer.statemachine.addTransition("isOpen",   "Close",  "isClosed", result="You closed the drawer.")        
        
        door.statemachine.addState("isLocked", "It seems to be locked.", active=True)
        door.statemachine.addState("isClosed", "It's closed.")
        door.statemachine.addState("isOpen", "It's open.")
        door.statemachine.addTransition("isLocked", "Usekey", "isClosed", result="You unlocked the door.", points=10)
        door.statemachine.addTransition("isLocked", "Usesmall key", "isClosed", result="The key doesn't fit.")
        door.statemachine.addTransition("isLocked", "Open",   "isLocked", result="It's locked.")
        door.statemachine.addTransition("isLocked", "Close",  "isLocked", result="It's already closed.")
        door.statemachine.addTransition("isClosed", "Usekey", "isLocked", result="You locked the door.")
        door.statemachine.addTransition("isClosed", "Usesmall key", "isClosed", result="The key doesn't fit.")
        door.statemachine.addTransition("isClosed", "Open",   "isOpen",   result="You opened the door.", points=10)
        door.statemachine.addTransition("isClosed", "Close",  "isClosed", result="It's already closed.")
        door.statemachine.addTransition("isOpen",   "Usekey", "isOpen",   result="Close it first.")     
        door.statemachine.addTransition("isOpen",   "Usesmall key", "isOpen", result="The key doesn't fit.")
        door.statemachine.addTransition("isOpen",   "Open",   "isOpen",   result="It's already open.")         
        door.statemachine.addTransition("isOpen",   "Close",  "isClosed", result="You closed the door.")        

        self.startMessage = "You wake up in a dusty room with a headache and no memory of how you got here. All you know is that you must escape as soon as possible!"

        # player state 
        # 
        self.inventory = []
        self.knows = ["room"]        
        self.points = 0 
        self.maxpoints = len(self.items) + 25 + 25 + 30 # looked at items, pickedup items, each of the successful state transitions, and bonus points defined below
        self.won = False
        self.quit = False

    # -----------------------------------------------------
    # What does the player know 
    # -----------------------------------------------------
    #
    def knowsAbout(self, item_name):
        return (item_name in self.knows)
    
    def addToKnowledge(self, item_name):  
        if not self.knowsAbout(item_name):            
            self.knows.append(item_name)

    def removeFromKnowledge(self, item_name):
        if self.knowsAbout(item_name):
            self.knows.remove(item_name)

    def getItem(self, item_name):
        return self.items.get(item_name)

    def addToScore(self, points):
        self.points = self.points + points 
        return self.getScore()

    def getPoints(self): 
        return self.points + len(self.knows)

    # -----------------------------------------------------
    # Main functions 
    # -----------------------------------------------------    
    def getWorldState(self):
        state = "" 
        for item in self.items:
            state = state + self.items[item].name             
            state = state + " state:" + str(self.items[item].statemachine.activeState) 
            state = state + " items:" + str(self.items[item].items)                        
            state = state + "\n"
        state = state + "inventory:" + str(self.inventory)
        state = state + "\n"
        state = state + "points:" + str(self.points) + "/" + str(self.maxpoints)
        state = state + "\n"
        state = state + "won:" + self.won
        return state


    def getInventory(self):
        if (len(self.inventory)==0):
            return "You check your pockets but you're not carrying anything!"
        
        descr = getListDescription(self.inventory)        
 
        return "You check your pockets and you find " + descr 


    def getKnowledge(self):
        return "I know about " + getListDescription(self.knows)

    def getScore(self):
        return "You have scored " + str(self.getPoints()) + " out of a possible " + str(self.maxpoints) + "." 


    def getActions(self):
        descr = getDictDescription(self.actions)
        
        if (descr == ""):
            return "You are all out of options!"
        else:
            return "I understand the following commands: " + descr


    def applyAction(self, action_label, **kwargs):
        action = self.actions.get(action_label)
        if action:
            action_method = getattr(self, action.method.__name__)
            if action_method:
                return(action_method(**kwargs))            
            else:
                return "Something went wrong."
        else:
            return "I don't know how to do that."    


    # -----------------------------------------------------
    # Actions
    # -----------------------------------------------------

    def actionLookAround(self, **kwargs):
        self.addToKnowledge("room")
        return self.actionLookAt("room")

    def actionInventory(self, **kwargs):
        return self.getInventory()
    
    def actionListActions(self, **kwargs):
        return self.getActions()

    def actionGetPoints(self, **kwargs):
        return self.getScore()

    def actionQuit(self, **kwargs):
        self.quit = True
        return "You feel slightly disappointed as you stop the game without escaping the room."

    def actionLookAt(self, item_name, **kwargs):                   
        if self.knowsAbout(item_name):
            item = self.getItem(item_name)     
            if item != None:                       
                # add the immediately visible parts         
                # 
                for part in item.parts:
                    self.addToKnowledge(part.name)

                # add any accessible contained items 
                #   
                if item.canBeAccessed():          
                    for subitem in item.items:            
                        if subitem.canBeAccessed():
                            self.addToKnowledge(subitem.name)

                return "You see "+str(item)
        return "What "+item_name+"?"
        

    def actionOpen(self, item_name, **kwargs):
        if not self.knowsAbout(item_name):
            return "What "+item_name+"?"        
        
        item = self.getItem(item_name)

        # check if the transition is available 
        # and if not, why not.  
        #
        if item.statemachine.canApplyTransition("Open"):
            result, points = item.statemachine.applyTransition("Open")
            self.addToScore(points)
            return result

        return "You can't open " + item_name
    
    def actionClose(self, item_name, **kwargs):
        if not self.knowsAbout(item_name):
            return "What "+item_name+"?"        
        
        item = self.getItem(item_name)

        if item.statemachine.canApplyTransition("Close"):
            result, points = item.statemachine.applyTransition("Close")
            self.addToScore(points)
            return result

        return "You can't open " + item_name

    def actionPickup(self, item_name, **kwargs):
        if not self.knowsAbout(item_name):
            return "What "+item_name+"?"     

        item = self.getItem(item_name)
        if item.canPickup == True:            
            # check if it is already in the inventory 
            #
            if item in self.inventory:
                return "It's already in your pocket."
            
            # check if it is contained in anything that is closed or locked
            # 
            if (item.checkParentTree("isLocked") or item.checkParentTree("isClosed")):
                return "You can't see it."
            else: 
                if item.container:
                    item.container.removeItem(item)
                self.inventory.append(item)

                # points 
                #
                self.addToScore(item.extractPoints())

                return "You picked up the "+item_name+"."

        else:
            return "You can't pick that up."

    def actionDrop(self, item_name, seconditem_name=None):
        if not self.knowsAbout(item_name):
            return "You don't know about "+item_name+"."             

        item = self.getItem(item_name)

        container = self.getItem("room")
        if seconditem_name:
            if not self.knowsAbout(seconditem_name):
                return "What "+seconditem_name+"?"             
            container = self.getItem(seconditem_name)

        if item in self.inventory:                                            
            self.inventory.remove(item)
            container.storeItem(item)            
            return "You dropped the "+item_name+" in the " + container.name + "."

        else:
            return "You don't have it."

    def actionUse(self, item_name, seconditem_name=None):
        if item_name == None:
            return "I didn't quite get that. Can you repeat it?"
        if not self.knowsAbout(item_name):
            return "What "+item_name+"?"             

        item = self.getItem(item_name)

        subject = self.getItem("room")
        if seconditem_name:
            if not self.knowsAbout(seconditem_name):
                return "What "+seconditem_name+"?"             
            subject = self.getItem(seconditem_name)

        if item in self.inventory:     

            action = "Use"+item.name
            if subject.statemachine.canApplyTransition(action):
                result, points = subject.statemachine.applyTransition(action)
                self.addToScore(points)
                return result
            else:
                return "You can't use "+item.name+" like that."

        else:
            return "You don't have it."

    # An example of a specific action that only works with one item
    #
    def actionRead(self, item_name, **kwargs):
        if item_name == None:
            return "Yes, reading is a great way to spend time. It usually requires something to read, though."
        if not self.knowsAbout(item_name):
            return "What "+item_name+"?" 

        item = self.getItem(item_name)
        writing = self.getItem("writing")
        paper = self.getItem("paper")

        if not paper in self.inventory: 
            return "You definitely can't read those scribbles from here. Try picking up the paper first."

        if item != writing: 
            return "You try to read the " + item_name + " but there is not much writing to be found on it. It makes you feel silly."
         
        self.addToScore(10)
        return "You manage to decipher some words: 'whoever reads this is awarded ten points!'. You feel your score has been greatly increased. Nobody will be able to take this away from you."

    # This action only works in a specific state of the game 
    # 
    def actionExit(self, item_name, **kwargs):
        if (item_name == None) or (not self.knowsAbout(item_name)):
            return "Exit what?"

        item = self.getItem(item_name)
        door = self.getItem("door")
        room = self.getItem("room")

        if item != room:
            return "You try to exit the " + item_name + " but it seems pointless."

        if door.getState() != "isOpen":
            return "The door is in the way"

        self.won = True
        self.addToScore(20)
        message = "You did not get all of the points though! Mysteries remain to be solved..."
        if (self.getPoints() == self.maxpoints):
            message = "You got all of the points! Congratulations! This room has no secrets for you!"

        return "You successfully exit the room. You feel overwhelmed by your great accomplishment. You won! " + message 

theworld = World()