# ////////////////////////////////////////////////////////////////////////////#
#                                                                             #
#  Author: Elthran B, Jimmy Zhang                                             #
#  Email : jimmy.gnahz@gmail.com                                              #
#                                                                             #
# ////////////////////////////////////////////////////////////////////////////#

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base
import pdb

{% include "abilities_data.py" %}

# "determination", 5, "Increases Endurance by 3 for each level."


class Abilities(Base):
    __tablename__ = 'abilities'

    id = Column(Integer, primary_key=True)

    # Relationships
    # Each hero can have one list of abilities (bi, one to one)
    hero_id = Column(Integer, ForeignKey('hero.id'))
    hero = relationship("Hero", back_populates='abilities')

    # Relationships to a particular ability.
    {%- for name in ALL_ABILITIES %}
    {{ name }} = relationship(
        "Ability",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='{{ name }}')",
        back_populates="abilities", uselist=False)
    {%- endfor %}

    def __init__(self):
        {%- for name in ALL_ABILITIES %}
        self.{{ name }} = Ability('{{ name | capitalize }}', 5, "Gain 1000 health per level")
        {%- endfor %}

    def items(self):
        """Return each Ability and its name.

        Returns a list of 2-tuples
        Basically a dict.items() clone that looks like ([(key, value),
            (key, value), ...])

        Usage:
        for name, ability in abilities.items():
            name -- the name of the attribute
            ability -- the object that corresponds to the named attribute.
        """

        return ((key, getattr(self, key)) for key in ALL_ABILITIES)

    def __iter__(self):
        """Allow this object to be used in a for call.

        for ability in abilities:
            ability -- where the ability is each of the attribute objects of
                the abilities class.
        """
        return (getattr(self, key) for key in ALL_ABILITIES)


class Ability(Base):
    """Ability object base class.

    Relates to the Abilities class which is a meta list of all Abilities ...
    with maybe some extra functions to make it worth while? I guess so that
    you can call the items by name.

    How to use:
    name : Name of the Item, e.x. "power bracelet"
    buy_price : Price to buy the item
    level_req : level requirement
    """
    __tablename__ = "ability"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # Maybe 'unique' is not necessary?
    level = Column(Integer)
    max_level = Column(Integer)
    # Maybe description should be unique? use: unique=True as keyword.
    description = Column(String)

    # Note: Original code used default of "Unknown"
    # I chopped the BasicAbility class as redundant. Now I am going to
    # have to add the fucker back in.
    type = Column(String)
    ability_type = orm.synonym('type')

    castable = Column(Boolean)
    activated = orm.synonym('castable')
    cost = Column(Integer)
    learnable = Column(Boolean)

    # Relationships.
    # Ability to abilities. Abilities is a list of ability objects.
    abilities_id = Column(Integer, ForeignKey('abilities.id'))
    abilities = relationship("Abilities")

    # Requirements is a One to Many relationship to self.
    """
    Use (pseudo-code):
    hero.can_learn(ability)
    if all hero.abilities are in ability.requirements.
    """
    # ability_id = Column(Integer, ForeignKey('ability.id'))
    # requirements = relationship("Ability")

    __mapper_args__ = {
        'polymorphic_identity': 'Basic',
        'polymorphic_on': type
    }

    def __init__(self, name, max_level, description, hero=None, castable=False,
                 cost=0, learnable=False):
        """Build a basic ability object.

        Castable=True/False denotes whether the Ability is a spell or not.

        Note: arguments (name, hero, max_level, etc.) that require input are
        the same as setting nullable=False as a Column property.
        Note2: can't currently set 'level' attribute.
        Note3: Ability to Hero relationship is Many to Many. This will require
        some major restructuring.

        Future:
        add in 'toggleable'=True/False for abilities that can be turned on and
        off add in active=True/False for whether the ability is turned on or
        off right now.
        Or possibly extend the Ability class into a Spell Class and make a
        Toggleable Class that various Abilities could inherit from.
        """
        self.name = name
        self.level = 0
        self.max_level = max_level
        self.description = description
        self.type = "Basic"
        self.castable = castable
        self.cost = cost
        self.learnable = learnable

        # Use internal method to properly add hero object to the
        # self.heroes relationship.
        self.add_hero(hero)

        self.init_on_load()

        # On load ... not implemented.

    @orm.reconstructor
    def init_on_load(self):
        self.adjective = ["I", "II", "III", "IV", "V", "VI"]
        self.display_name = self.adjective[self.level - 1]
        self.learn_name = self.adjective[self.level]

    # @property
    # def display_name(self):
    #     return self.name.capitalize()

    def is_max_level(self):
        """Return True if level is at max_level."""
        return self.level >= self.max_level

    def update(self, hero):
        """Update a hero's stats to reflect them possessing this ability.

        Use:
        To update hero from inside hero class:
        for ability in self.abilities:
            ability.update_stats(self)
        from outside hero class:
        for ability in hero.abilities:
            ability.update_stats(hero)
        """
        # Possibly use a dictionary + lambda function. Switch/Case
        if self.name == "Ironhide":
            hero.proficiencies.health.maximum += 3 * self.level

    def activate(self, hero):
        return self.cast(hero)

    def cast(self, hero):
        """Use the ability. Like casting a spell.

        use:
        ability.activate(hero)
        NOTE: returns False if spell is too expensive (cost > proficiencies.sanctity.current)
        If cast is succesful then return value is True.
        """
        if hero.proficiencies.sanctity.current < self.cost:
            return False
        else:
            hero.proficiencies.sanctity.current -= self.cost
            if self.name == "Gain Gold to Test":
                hero.gold += 3 * self.level
            elif self.name == 'foo':
                pass  # Do some stuff.
            return True

    def update_display(self):
        self.display_name = self.adjective[self.level - 1]
        if self.level < self.max_level:
            self.learn_name = self.adjective[self.level]

    def update_owner(self, hero):
        print("Ability to Hero relationship is now Many to Many.")
        print("Instead of One Hero to Many Ablities.")
        exit("Removed in favor of add_hero and remove_hero")
        # self.heroes = [hero]

    def add_hero(self, hero):
        """Give a hero this ability.
        """
        if hero is None:
            return
        if hero not in self.heroes:
            self.heroes.append(hero)
        else:
            raise Exception("ValueError: Hero already has this ability.")

    def remove_hero(self, hero):
        """Remove this ability from a hero.
        """
        try:
            self.heroes.remove(hero)
        except ValueError:
            raise Exception("ValueError: Hero doesn't have this ability")


class Archetype_Ability(Ability):
    __tablename__ = "archetype_ability"

    id = Column(Integer, ForeignKey('ability.id'), primary_key=True)
    archetype = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'Archetype',
    }

    def __init__(self, *args, archetype="All", **kwargs):
        """Build a new Archetype_Ability object.

        Note: self.type must be set in __init__ to polymorphic_identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        if len(args) > 3:
            raise TypeError(
                "__init__() takes 3 positional arguments but {} were given.".format(
                    len(args)))
        super().__init__(*args, **kwargs)
        self.type = 'Archetype'
        self.archetype = archetype


class Class_Ability(Ability):
    __tablename__ = "class_ability"

    id = Column(Integer, ForeignKey('ability.id'), primary_key=True)
    specialization = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'Class',
    }

    def __init__(self, *args, specialization="All", **kwargs):
        if len(args) > 3:
            raise TypeError(
                "__init__() takes 3 positional arguments but {} were given.".format(
                    len(args)))
        super().__init__(*args, **kwargs)
        self.type = 'Class'
        self.specialization = specialization


class Religious_Ability(Ability):
    __tablename__ = "religious_ability"

    id = Column(Integer, ForeignKey('ability.id'), primary_key=True)
    religion = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'Religious',
    }

    def __init__(self, *args, religion="All", **kwargs):
        if len(args) > 3:
            raise TypeError("__init__() takes 3 positional arguments but {}"
                            " were given.".format(len(args)))
        super().__init__(*args, **kwargs)
        self.type = 'Religious'
        self.religion = religion
