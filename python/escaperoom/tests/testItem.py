import unittest
import time
from .. import *

# TODO 
# Add test for item description
# Add test for parts list
# Add test for contained items

class TestItem(unittest.TestCase):
    def setUp(self):
        # setup stuff 

        # wait a little
        time.sleep(0.5)

    def test_itemCreate(self):
        testitem = item.Item("TestItem","A test item", "A supercool test item", points=10, canPickup=True, canDrop=True)
        self.assertTrue(testitem.name == "TestItem")
        self.assertTrue(testitem.short == "A test item")
        self.assertTrue(testitem.description == "A supercool test item")
        self.assertTrue(testitem.points == 10)
        self.assertTrue(testitem.canPickup == True)
        self.assertTrue(testitem.canDrop == True)

        testitem2 = item.Item("TestItem2","A second test item", "Another supercool test item")
        self.assertTrue(testitem2.name == "TestItem2")
        self.assertTrue(testitem2.short == "A second test item")
        self.assertTrue(testitem2.description == "Another supercool test item")
        self.assertTrue(testitem2.points == 0)
        self.assertTrue(testitem2.canPickup == False)
        self.assertTrue(testitem2.canDrop == False)

    def test_itemGetState(self):
        testitem = item.Item("TestItem","A test item", "A supercool test item", points=10, canPickup=True, canDrop=True)
        testitem.statemachine.addState("isLocked", "It seems to be locked.", active=True)
        self.assertTrue(testitem.getState() == "isLocked")

    def test_itemStoreItem(self):
        testitem = item.Item("TestItem","A test item", "A supercool test item", points=10, canPickup=True, canDrop=True)
        testitem2 = item.Item("TestItem2","A second test item", "Another supercool test item")
        testitem3 = item.Item("TestItem3","A third test item", "Yet another supercool test item")
        
        testitem.storeItem(testitem2)
        self.assertTrue(testitem.containsItem(testitem2) == True)

        # this one should fail (not allowed to drop items in item2)
        testitem2.storeItem(testitem3)
        self.assertTrue(testitem2.containsItem(testitem3) == False)
    
    def test_itemRemoveItem(self):
        testitem = item.Item("TestItem","A test item", "A supercool test item", points=10, canPickup=True, canDrop=True)
        testitem2 = item.Item("TestItem2","A second test item", "Another supercool test item")
        testitem.storeItem(testitem2)
        self.assertTrue(testitem.containsItem(testitem2) == True)
        testitem.removeItem(testitem2)
        self.assertTrue(testitem.containsItem(testitem2) == False)

        # do it again should not give error 
        testitem.removeItem(testitem2)
        self.assertTrue(testitem.containsItem(testitem2) == False)

    def test_itemCanBeAccessed(self):
        testitem = item.Item("TestItem","A test item", "A supercool test item", points=10, canPickup=True, canDrop=True)
        self.assertTrue(testitem.canBeAccessed() == True)

        # set state to isRandomState 
        # 
        testitem.statemachine.addState("isRandomState", "It seems to be blinking.", active=True)
        self.assertTrue(testitem.canBeAccessed() == True)

        # add a state isOpen
        # 
        testitem.statemachine.addState("isOpen", "It seems to be closed.", active=True)
        self.assertTrue(testitem.canBeAccessed() == True)

        # set state to isClosed 
        # 
        testitem.statemachine.addState("isClosed", "It seems to be closed.", active=True)
        self.assertTrue(testitem.canBeAccessed() == False)

if __name__ == '__main__':
    unittest.main()
