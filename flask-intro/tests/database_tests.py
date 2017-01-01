from database import EasyDatabase
from game import Hero

"""
This program runs as a test suite for the EasyDatabase class when it is imported.
This modules is run using  :>python database_tests.py

These tests should run when the module is imported.
NOTE: every time I define a test I add it to the run_all function.

I am using this tutorial http://docs.python-guide.org/en/latest/writing/tests/
"""

def set_up():
    return EasyDatabase('static/test_database.db')

def tear_down(database):
    database._delete_database()

def test_EasyDatabase_init():
    db = set_up()
    # print(db)
    assert db #looks like it is supposed to ... that will be hard ... :P
    tear_down(db)

def test_add_new_user():
        db = set_up()
        db.add_new_user('Marlen', 'Brunner') #I should be able to add a bunch of users from a text file.
        assert 1 #Check if database has a user called Marlen with a password of Brunner in it.
        tear_down(db)


def test_get_user_id():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    user_id = db.get_user_id("Marlen")
    assert user_id == 1
    tear_down(db)

def test_add_new_character():
    db = set_up()
    db.add_new_character(1, "Haldon", "Wizard")
    assert 1 #Check if character is created that has a user_id of 1.
    tear_down(db)

def test_validate():
    """Test if the validate function in the Database class works.
    
    NOTE: my first real unit test!
    """
    db = set_up()
    username = 'Marlen'
    password = "Brunner"
    db.add_new_user(username, password)
    assert db.validate(username, password) == True
    tear_down(db)

def test_update_character():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = Hero()
    hero.user_id = 1
    hero.character_name = "Haldon"
    hero.archetype = "Wizard"
    hero.age = 25
    hero.vitality = 56
    db.update_character(1, hero)
    # I have to build this method ... *sigh*
    # assert db.fetch_character_data(row_id=1) == hero
    tear_down(db)

def test_fetch_character_data():
    db = set_up()
    db.add_new_user('Marlen', 'Brunner')
    db.add_new_character(1, "Haldon", "Wizard")
    hero = Hero()
    hero.user_id = 1
    hero.character_name = "Haldon"
    hero.archetype = "Wizard"
    hero.age = 25
    hero.vitality = 56
    db.update_character(1, hero)
    assert db.fetch_character_data(hero.user_id, hero.character_name) == hero
    tear_down(db)
    
def dict_diff(left, right):
    """Tell if two dicts are the same, return differences.
    
    Use: print(dict_diff(hero.__dict__, hero2.__dict__))
    """
    diff = dict()
    diff['left_only'] = set(left) - set(right)
    diff['right_only'] = set(right) - set(left)
    diff['different'] = {k for k in set(left) & set(right) if left[k]!=right[k]}
    return diff


def run_all():
    """Run all tests in the module.

    The test currently only fail if the code is broken ... not if the info is invalid.
    I hope to use an assert statement at some point in each test to make sure the output is correct as well.
    """
    test_EasyDatabase_init()
    test_add_new_user()
    test_get_user_id()
    test_add_new_character()
    test_validate()
    test_update_character()
    test_fetch_character_data()
    print("No Errors, yay!")

run_all()
