import unittest
import time
from .. import *

actions = ["LookAround", "Open", "Close", "OpenDoor", "Pickup", "Drop", "LookAt", "Use", "Inventory", "ListActions", "GetPoints", "Read", "Exit"]
items   = ["key", "drawer", "desktop", "legs", "lock", "door", "small key", "paper", "text", "box", "room"]

def command(action, item=None, seconditem=None):
    result = world.theworld.applyAction(action, item_name=item, seconditem_name=seconditem)    
    return result
    
class TestWorld(unittest.TestCase):    
    
    def test_worldCreate(self):
        theworld = world.World()    

        for action in actions:
            self.assertTrue(action in theworld.actions, msg = "action "+action+" is missing after world setup.")

        for item in items:
            self.assertTrue(item in theworld.items, msg = "item "+item+" is missing after world setup.")

    def test_worldKnowsAbout(self):           
        world.theworld = world.World()      

        self.assertFalse(world.theworld.knowsAbout("testitem"))
        world.theworld.knows = ["testitem"]
        self.assertTrue(world.theworld.knowsAbout("testitem"))

    def test_worldAddToKnowledge(self):           
        world.theworld = world.World()      
        self.assertTrue(len(world.theworld.knows) == 1, msg="Starts with only knowing room")

        self.assertFalse(world.theworld.knowsAbout("testitem"))
        world.theworld.addToKnowledge("testitem")
        self.assertTrue(world.theworld.knowsAbout("testitem"))
        self.assertTrue(len(world.theworld.knows) == 2)

        world.theworld.addToKnowledge("testitem")
        self.assertTrue(len(world.theworld.knows) == 2, msg="no duplicates!")


    def test_worldRemoveFromKnowledge(self):
        world.theworld = world.World()      
        self.assertFalse(world.theworld.knowsAbout("testitem"))
        world.theworld.addToKnowledge("testitem")
        self.assertTrue(world.theworld.knowsAbout("testitem"))
        world.theworld.removeFromKnowledge("testitem")
        self.assertFalse(world.theworld.knowsAbout("testitem"))

    def test_worldGetItem(self):
        world.theworld = world.World()      
        testitem = world.theworld.items["key"]
        self.assertTrue(world.theworld.getItem("key")==testitem)

    def test_worldGetInventory(self):
        world.theworld = world.World()
        # print("|"+world.theworld.getInventory()+"|")
        self.assertTrue(world.theworld.getInventory() == "You check your pockets but you're not carrying anything!")
        testitem = world.theworld.items["key"]
        world.theworld.inventory = [testitem]
        # print("|"+world.theworld.getInventory()+"|")
        self.assertTrue(world.theworld.getInventory() == "You check your pockets and you find a key.")

    def test_worldGetActions(self):           
        world.theworld = world.World()
        actionlist = world.theworld.getActions()
        self.assertTrue(actionlist == "I understand the following commands: " + utils.getListDescription(actions))

    def test_worldPoints(self):
        world.theworld = world.World()      
        points = world.theworld.points + len(world.theworld.knows)
        self.assertTrue(world.theworld.getPoints()==points)

    def test_worldApplyAction(self):           
        world.theworld = world.World() 
        self.assertTrue(world.theworld.getPoints() == len(world.theworld.knows))
        self.assertTrue(world.theworld.won == False, msg="Game should start with won == False")

        commandName = "ListActions"
        result = command(commandName)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "I understand the following commands: lookaround, open, close, opendoor, pickup, drop, lookat, use, inventory, listactions, getpoints, read, and exit.", "Actions not listed correctly")
        self.assertTrue(world.theworld.getPoints() == 1, msg="Score should be 1 (only room seen)")
        self.assertTrue(len(world.theworld.knows) == 1)

        commandName = "NonexistentCommand"
        result = command(commandName)
        self.assertTrue(result == "I don't know how to do that.", msg="Nonexistent commands should fail consistently.")

        commandName = "LookAround"
        result = command(commandName)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You see a small dusty room. It has a desk, a door, and a box.", msg="Lookaround gave wrong result")
        self.assertTrue(world.theworld.getPoints() == 4, msg="Score should be 4 (4 items seen)"+world.theworld.getKnowledge())
        self.assertTrue(len(world.theworld.knows) == 4)

        commandName = "Inventory"
        result = command(commandName)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You check your pockets but you're not carrying anything!", msg="Inventory should be empty")        

        commandName = "Pickup"
        item = "key"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "What key?", msg="Shouldn't be able to pickup the key yet")

        commandName = "Inventory"
        result = command(commandName)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You check your pockets but you're not carrying anything!", msg="Inventory should still be empty")        

        commandName = "LookAt"
        item = "box"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You see a cardboard box. It contains a small key.", msg="Lookat gave wrong result")
        self.assertTrue(len(world.theworld.knows) == 5)

        commandName = "Pickup"
        item = "small key"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You picked up the small key.", msg="Pickup gave wrong result")
        smallkey = world.theworld.getItem("small key")
        self.assertTrue(smallkey in world.theworld.inventory, msg="small key should have been added to inventory")
        box = world.theworld.getItem("box")
        self.assertFalse(smallkey in box.items, msg="small key should have been removed from box")

        commandName = "Pickup"
        item = "small key"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "It's already in your pocket.", msg="Should not be able to pickup twice")

        commandName = "LookAt"
        item = "desk"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You see an old, mouldy wooden desk. It has a drawer, a desktop, and four table legs.")
        self.assertTrue(world.theworld.getPoints() == 18, msg="Score should be 18 (8 items seen + 10 points for the key)")
        self.assertTrue(len(world.theworld.knows) == 8)

        commandName = "LookAt"
        item = "drawer"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You see a rickety old drawer. It's part of the desk. It seems to be locked.")

        commandName = "LookAt"
        item = "key"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "What key?", msg="You should not be able to see the key when drawer is closed.")

        commandName = "Open"
        item = "drawer"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "It's locked.", msg=result)

        commandName = "Use"
        item = "small key"
        item2 = "drawer"
        result = command(commandName, item=item, seconditem=item2)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You unlocked the drawer.")
        self.assertTrue(world.theworld.getPoints() == 23, msg="Score should be 23 (8 items seen + 10 points for the key + 5 for unlocking the drawer)")
        self.assertTrue(len(world.theworld.knows) == 8)

        commandName = "LookAt"
        item = "key"
        result = command(commandName, item=item)
        self.assertTrue(result == "What key?")

        commandName = "Open"
        item = "drawer"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You opened the drawer.")
        self.assertTrue(world.theworld.getPoints() == 28, msg="Score should be 28 (8 items seen + 10 points for the key + 5 for unlocking the drawer + 5 for opening the drawer)")
        self.assertTrue(len(world.theworld.knows) == 8)

        commandName = "LookAt"
        item = "key"
        result = command(commandName, item=item)
        self.assertTrue(result == "What key?")

        commandName = "LookAt"
        item = "drawer"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You see a rickety old drawer. It's part of the desk. It contains a key. It's open.")
        self.assertTrue(world.theworld.getPoints() == 29, msg="Score should be 29 (9 items seen + 10 points for the key + 5 for unlocking the drawer + 5 for opening the drawer)")
        self.assertTrue(len(world.theworld.knows) == 9)

        commandName = "LookAt"
        item = "key"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You see a big silver key. It's in the drawer.")

        commandName = "Pickup"
        item = "key"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You picked up the key.", msg="Pickup gave wrong result")
        key = world.theworld.getItem("key")
        self.assertTrue(key in world.theworld.inventory, msg="key should have been added to inventory")
        drawer = world.theworld.getItem("drawer")
        self.assertFalse(smallkey in drawer.items, msg="key should have been removed from drawer")
        self.assertTrue(world.theworld.getPoints() == 39, msg="Score should be 29 (9 items seen + 10 points for the key + 5 for unlocking the drawer + 5 for opening the drawer + 10 for big key)")
        self.assertTrue(len(world.theworld.knows) == 9)

        commandName = "Close"
        item = "drawer"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You closed the drawer.")

        commandName = "Drop"
        item = "small key"
        item2 = "box"
        result = command(commandName, item=item, seconditem=item2)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You dropped the small key in the box.")

        commandName = "Open"
        item = "door"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "It's locked.")

        commandName = "Use"
        item = "key"
        item2 = "door"
        result = command(commandName, item=item, seconditem=item2)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You unlocked the door.")
        door = world.theworld.getItem("door")
        self.assertTrue(door.getState() == "isClosed", "Door should be in isClosed:" + door.getState())
        self.assertTrue(world.theworld.getPoints() == 49, msg="Score should be 49 (9 items seen + 10 points for the key + 5 for unlocking the drawer + 5 for opening the drawer + 10 for big key + 10 for unlocking the door)")
        self.assertTrue(len(world.theworld.knows) == 9)

        commandName = "Open"
        item = "door"
        result = command(commandName, item=item)
        # print("\n"+commandName+"|"+result+"|")
        self.assertTrue(result == "You opened the door.")
        door = world.theworld.getItem("door")
        self.assertTrue(door.getState() == "isOpen", "Door should be in isOpen:" + door.getState())
        self.assertTrue(world.theworld.getPoints() == 59, msg="Score should be 49 (9 items seen + 10 points for the key + 5 for unlocking the drawer + 5 for opening the drawer + 10 for big key + 10 for unlocking the door + 10 for opening the door)")
        self.assertTrue(len(world.theworld.knows) == 9)

        self.assertTrue(world.theworld.won == False, msg="Somehow the game thinks you've already won...")

        commandName = "Exit"
        item = "room"
        result = command(commandName, item=item)

        self.assertTrue(result == "You successfully exit the room. You feel overwhelmed by your great accomplishment. You won! You did not get all of the points though! Mysteries remain to be solved...", msg=result)
        self.assertTrue(world.theworld.getPoints() == 79, msg="Score should be 49 (9 items seen + 10 points for the key + 5 for unlocking the drawer + 5 for opening the drawer + 10 for big key + 10 for unlocking the door + 10 for opening the door + 20 for leaving)")
        self.assertTrue(len(world.theworld.knows) == 9)
        self.assertTrue(world.theworld.won == True)