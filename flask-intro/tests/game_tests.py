'''
This program runs as a test suite for the game.py module when it is imported.
This modules is run using  :>python game_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial https://docs.python.org/3.6/library/unittest.html
'''
from base_classes import Base, BaseDict
from database import EZDB
from game import Hero
import complex_relationships
import prebuilt_objects

import pdb

import unittest

class HeroTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = Hero(name="Haldon")
        self.db = EZDB('sqlite:///tests/test.db', debug=False)

    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()
    
    def rebuild_instance(self):
        """Tidy up and rebuild database instance.

        ... otherwise you may not be retrieving the actual data
        from the database only from memory.
        """
        
        self.db.session.commit()
        self.tearDown(delete=False)
        self.setUp()
            
    def test_hero(self):
        """Prove that hero object builds and loads properly.
        
        NOTE: Max_health set by Primary Attributes values.
        NOTE2: Relationships (Abilities, inventory and primary_attributes, etc.) are accessed by the
        self.__mapper__.relationships.keys
        
        I will need to update all of the other database objects to account for relationships.
        """
        self.db.session.add(self.hero)
        self.db.session.commit()
        
        str_hero = str(self.hero)        
        
        self.rebuild_instance()
        
        hero2 = self.db.session.query(Hero).filter_by(name="Haldon").first()
        self.assertEqual(str_hero, str(hero2))  

    def test_current_city(self):
        self.hero.current_world = prebuilt_objects.world
        self.hero.current_location = prebuilt_objects.current_location
        self.hero.current_city = prebuilt_objects.current_location
        self.db.session.add(self.hero)
        self.db.session.commit()
        str_hero = str(self.hero)        
        str_city = str(self.hero.current_city)
        
        self.rebuild_instance()
        hero2 = self.db.session.query(Hero).filter_by(name="Haldon").first()
        self.assertEqual(str_hero, str(hero2))
        self.assertEqual(str_city, str(hero2.current_city))
        

class PrimaryAttributesTestCase(unittest.TestCase):
    """Test hero primary_attributes

    Tests increment
    Tests that two heroes primary_attributes are not the same object (that one was anoying).
    Tests that list iteration works.
    Tests that data is retrieved as an ordered list when printing.
    Tests this from a saving/loading perspective as well.
    
    NOTE: actual data order is dictionary random.
    NOTE: query should occur using a new database object or it will simply return the old object
    without actually pulling it from the database. I need to fix this in my other test suites.
    """
        
    def setUp(self):
        self.hero = Hero(name="Haldon")
        self.db = EZDB('sqlite:///tests/test.db', debug=False)

    def tearDown(self, delete=True):
        self.db.session.close()
        self.db.engine.dispose()
        if delete:
            self.db._delete_database()

    def test_increment(self):   
        self.hero.primary_attributes["Strength"] += 3
        self.assertEqual(self.hero.primary_attributes["Strength"], 4)

    def test_is_new_object(self):
        hero = Hero()
        self.assertNotEqual(id(self.hero.primary_attributes), id(hero.primary_attributes))  
        
    def test_increment_all(self):
        for attribute in self.hero.primary_attributes:
            self.hero.primary_attributes[attribute] += 1
        self.assertEqual(str(self.hero.primary_attributes), "{'Agility': 2, 'Charisma': 2, 'Divinity': 2, 'Fortitude': 2, 'Fortuity': 2, 'Perception': 2, 'Reflexes': 2, 'Resilience': 2, 'Strength': 2, 'Survivalism': 2, 'Vitality': 2, 'Wisdom': 2}")
    
    def test_save_load(self):
        #Test save/load
        self.hero.primary_attributes["Strength"] += 3
        self.db.session.add(self.hero)
        self.db.session.commit()
        
        self.tearDown(delete=False)
        self.setUp()
        self.hero = self.db.session.query(Hero).filter_by(name='Haldon').first()
        self.assertEqual(self.hero.primary_attributes["Strength"], 4)

    #This belongs in hero test case.
    def testKillQuests(self):
        
        self.hero.kill_quests['Kill a wolf'] = "Find and kill a wolf!"
        
        #Convert this to a string before closing the session or it will not
        #load the data contain in itself.
        old_quests = str(self.hero.kill_quests)
        
        self.db.session.add(self.hero)
        self.db.session.commit()
        
        self.tearDown(delete=False)
        self.setUp()
        self.hero = self.db.session.query(Hero).filter_by(name='Haldon').first()
        self.assertEqual(old_quests, str(self.hero.kill_quests))
    
    
if __name__ == '__main__':
    unittest.main()
    
