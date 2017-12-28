"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at:
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""
import hashlib
import importlib
import os
import datetime
import random
# Testing only
import pdb
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from sqlalchemy import desc

# Base is the initialize SQLAlchemy base class. It is used to set up the
# table metadata.
# Used like so in the __init__ method: Base.metadata.create_all(engine)
# What this actually means or does I have no idea but it is neccessary.
# And I know how to use it.
# !Important!: Base can only be defined in ONE location and ONE location ONLY!
import base_classes
# Internal game modules
from game import User
from inbox import Inbox, Message
from hero import Hero
from abilities import Abilities, Ability
from locations import Location  # , WorldMap, Town, Cave
from items import ItemTemplate, Item
from quests import Quest, QuestPath
from proficiencies import Proficiency
from events import Trigger
import prebuilt_objects


# Constants#
SECOND_PER_ENDURANCE = 10


class EZDB:
    """Basic frontend for SQLAlchemy.
    
    This class allows you to use the old game methods with modern SQLAlchemy.
    At some point it may be worth using SQLAlchemy directly.
    
    All add_* methods should end with a commit!
    """
    Session = None

    def __init__(self, database="sqlite:///:memory:", debug=True,
                 testing=False):
        """Create a basic SQLAlchemy engine and session.
        
        Attribute "file_name" is used to find location of database for python.
        
        Hidden method: _delete_database is for testing and does what it
        sounds like it does :).
        """
        first_run = True
        engine = create_engine(database, echo=debug)
        self.file_name = database[10:]

        if os.path.isfile(self.file_name):
            first_run = False
        
        base_classes.Base.metadata.create_all(engine, checkfirst=True)
        EZDB.Session = sessionmaker(bind=engine)

        self.engine = engine
        self.session = EZDB.Session()
        if first_run and not testing:
            self.add_prebuilt_objects()
        
    def add_prebuilt_objects(self):
        """Add all the predefined object into the database.
        
        If one is already there then ignore and continue.
        Note: each prebuilt_object must be a list.
        NOTE2: users must come first as it somehow gets built before it gets
        built if it doesn't?
        Maybe because .. it has a hero which has a current_world? So when
        current_world gets
        built then the user gets built too? Which may mean most of my code
        here is redundant
        and I only really need to build the users list?
        """
        
        # global prebuilt_objects
        # I can't remember why I need to reload this ...
        importlib.reload(prebuilt_objects)
        
        for obj_list in [
                prebuilt_objects.users,
                prebuilt_objects.game_worlds,
                # prebuilt_objects.all_abilities,
                prebuilt_objects.all_store_items,
                prebuilt_objects.all_marketplace_items,
                prebuilt_objects.all_quests]:
            for obj in obj_list:
                try:
                    self.session.add(obj)
                    if isinstance(obj, User):
                        obj.password = hashlib.md5(
                            obj.password.encode()).hexdigest()
                        obj.timestamp = EZDB.now()
                    self.update()
                except sqlalchemy.exc.IntegrityError as ex:
                    print(ex)
                    print("Please debug database setup -> prebuilt object loading.")
                    pass  # rollback is now handled by 'update()'
        default_quest_paths = self.get_default_quest_paths()
        for hero in self.session.query(Hero).all():
            hero.journal.quest_paths = default_quest_paths
        self.update()
                    
    def delete_item(self, item_id):
        """Delete an Item object from the database.
        """
        self.delete_object_by_id("Item", item_id)

    def delete_object_by_id(self, obj_name, obj_id):
        """Delete an object given its type and id.

        NOTE: the delete will not take effect until the session is flushed/
        commited/closed.
        """
        try:
            obj = globals()[obj_name.capitalize()]
        except IndexError:
            raise Exception(
                "Object name: '{}' is not an "
                "object, or has not been imported into "
                "'database' module yet.".format(obj_name))
        db_obj = self.session.query(obj).get(obj_id)
        if db_obj:
            self.session.delete(db_obj)
        else:
            raise IndexError(
                "No '{}' with id '{}' exists.".format(obj_name, obj_id))

    def get_object_by_id(self, obj_name, obj_id):
        """Return an object given its class name and id.
        
        Return error if name doesn't exist in global scope. 
        obj = getattr(globals(), name) 
        
        Name can be capitalized or not e.g. "hero" or "Hero"
        """
        try:
            obj = globals()[obj_name.capitalize()]
            # test if obj is a class.?
            return self.session.query(obj).get(obj_id)
        except IndexError:
            raise Exception(
                "Object name: '{}' is not an "
                "object, or has not been imported into "
                "'database' module yet.".format(obj_name))

    def get_learnable_abilities(self, hero):
        """Get all learnable abilities of a given hero."""
        return self.session.query(Ability).\
            filter_by(abilities_id=hero.abilities.id).\
            filter_by(locked=False).all()

    def get_object_by_name(self, obj_class_name, obj_name):
        """Retrieve an object from the database by name.

        And error will occur if the object name is not unique.
        Or if you specify an object that doesn't exist in the database.
        """
        obj = globals()[obj_class_name]
        return self.session.query(obj).filter_by(name=obj_name).one()
        
    def get_proficiency_by_id(self, prof_id):
        """Return a proficiency object by id."""
        return self.session.query(Proficiency).get(prof_id)
    
    def get_item_by_id(self, item_id):
        """Return an item from its ID.
        """
        return self.session.query(Item).get(item_id)
                    
    def create_item(self, item_id):
        """Create a new item from a given template name.
        """
        template = self.session.query(ItemTemplate).get(item_id)
        item = Item(template)
        return item

    def get_random_item(self):
        """Return a new random item."""
        num_rows = self.session.query(ItemTemplate).count()
        item_id = random.randint(1, num_rows)
        item = self.create_item(item_id)
        return item
        
    def get_all_users(self):
        """Return all Users order_by name.
        """
        return self.session.query(User).order_by(User.id).all()

    def get_ability_by_id(self, ability_id):
        """Return an ability from its ID."""
        return self.session.query(Ability).get(ability_id)

    def get_all_store_items(self):
        """Return all items in the database ordered by name.
        """
        return self.session.query(
            ItemTemplate).filter(
            ItemTemplate.type != "Consumable").order_by(
            ItemTemplate.name).all()
        
    def get_all_marketplace_items(self):
        """Not Implemented!
        """
        return self.session.query(
            ItemTemplate).filter_by(type="Consumable").all()

    def get_default_world(self):
        """Get the default world for starting heroes.
        """
        return self.session.query(
            Location).filter_by(name="Htrae", type="map").first()
    
    def get_default_location(self):
        """Get the default location for starting heroes.
        """
        return self.session.query(Location).filter_by(name="Thornwall", type="town").first()

    def get_default_quest_paths(self):
        """Return the quest that are applied to starting heroes.

        NOTE: This is a placeholder! The implementation should probably have
        a "is_default" flag for QuestPath objects.
        """
        return self.session.query(QuestPath).filter(QuestPath.id < 3).all()

    def get_user_id(self, username):
        """Return the id of the user by username from the User's table.
        
        """
        user = self.session.query(User).filter_by(username=username).first()
        if user is None:
            return None
        return user.id
    
    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()
                
    def add_new_user(self, username, password, email=''):
        """Add a user to the username with a given a unique username and a password.
        
        The password is hashed.
        """
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user = User(username=username, password=hashed_password, email=email,
                    timestamp=EZDB.now())
        self.session.add(user)
        return user
        
    def add_new_hero_to_user(self, user):
        """Create a new blank character object for a user.
        
        May not be future proof if a user has multiple heroes.
        """
        
        self.session.add(Hero(user=user))

    def validate(self, username, password):
        """Check if password if valid for user.
        """
        user = self.session.query(User).filter_by(username=username).first()
        if user is not None:
            return user.password == hashlib.md5(password.encode()).hexdigest()
        return None
        
    def fetch_hero_by_username(self, username, character_name=None):
        """Return hero objected based on username_or_id and character_name.
        
        If no character_name is passed just return first hero.
        Note: Providing a username when you have the hero/character id is
        redundant.
        """
        user_id = self.get_user_id(username)
        if character_name is not None:
            return self.session.query(
                Hero).filter_by(
                user_id=user_id, character_name=character_name).first()
        return self.session.query(User).filter_by(id=user_id).first().heroes[0]
        
    def fetch_hero_by_id(self, hero_id):
        return self.session.query(Hero).get(hero_id)

    def fetch_sorted_heroes(self, attribute, descending = False):
        """Return a list of all heroes sorted by attribute.

        :param attribute: an attribute of the Hero object.
        :param descending: the desired direction for the sorted list ascending/descending
        :return: list sorted by attribute.

        NOTE: this code is not very flexible. If you tried to access
        hero.inventory.id it would not work.

        A more generic function might do:
        extended_attr, attr = attribute.split('.')
        join_attr = getattr(Hero, extended_attr)?
        self.session.query(Hero).join(join_attr).order_by(attr).all()

        NOTE: to order by descending:
        order_by(attribute + " desc") 
        or
        order_by(desc(attribute))

        Former does not work for numbers

        https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
        """
        if '.' not in attribute:
            if descending:
                return self.session.query(Hero).order_by(desc(attribute)).all()
            else:
                return self.session.query(Hero).order_by(attribute).all()
        elif attribute.startswith('user'):
            _, attribute = attribute.split('.')
            if descending:
                return self.session.query(Hero).join(Hero.user).order_by(desc(attribute)).all()
            else:
                return self.session.query(Hero).join(Hero.user).order_by(attribute).all()
        else:
            raise Exception("Trying to access an attribute that this code"
                            " does not accommodate.")

    def update(self):
        """Commit current session.
        
        NOTE: update function is now mostly redundant!
        Only use on program exit or logout.
        When you edit the hero ... he stays edited!
        Using any of the other methods will push him to database.
        """
        self.session.commit()

    def add_object(self, obj):
        """Add an object to the database.

        Hides the session object. And the commit :P
        """
        self.session.add(obj)

    def get_all_handlers_with_completed_triggers(self, hero):
        """Return all the handler objects with completed triggers.

        This occurs when an event has happened that 'completed' a trigger
        for a given event.
        """
        objs = [QuestPath]
        handlers = []
        for obj in objs:
            handlers += self.session.query(obj).\
                filter(obj.trigger_is_completed).\
                filter(obj._hero_id == hero.id).all()

        return handlers

    def get_all_triggers_by(self, event_name, hero_id):
        """Return all triggers for this hero that fit a given event."""

        return self.session.query(Trigger).filter_by(event_name=event_name,
                                              hero_id=hero_id).all()

    @staticmethod
    def now():
        """Return current UTC time as datetime object in string form.

        NOTE: I am using UTC as we are working in different time
        zones and I think it might screw up otherwise.
        """
        return datetime.datetime.utcnow()

    # Marked for renaming as it effects Hero endurance as well as time.
    # Consider update_endurance_and_time()
    # Or update_game_clock
    # Or update_hero_clock
    def update_time(self, hero):
        """Update the game time clock of a specific Hero and endurance values.
        
        This increases the hero's endurance by the difference between past
        timestamp and current time.
        NOTE: Updates current timestamp in character table but only if has
        been incremented.
        Which may not be a good idea but ...
        
        Suggestion: Currently only affects the passed Hero, perhaps it
        should update all heroes?
        """
        timestamp = hero.timestamp
        time_diff = (EZDB.now() - timestamp).total_seconds()
        endurance_increment = int(time_diff / SECOND_PER_ENDURANCE)
        hero.proficiencies.endurance.current += endurance_increment
            
        if hero.proficiencies.endurance.current \
                > hero.proficiencies.endurance.maximum:
            hero.proficiencies.endurance.current \
                = hero.proficiencies.endurance.maximum

        # Only update if endurance has been incremented.
        if endurance_increment:
            hero.timestamp = EZDB.now()

    # def get_world(self, name):
    #     """Return WorldMap object from database using by name.
    #     """
    #     return self.session.query(WorldMap).filter_by(name=name).first()
    
    def _delete_database(self):
        """Deletes current database file.
        
        Use with caution, mainly for testing.
        """
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            # Ignore because the file has already been deleted.
            pass
        except PermissionError:
            pass
