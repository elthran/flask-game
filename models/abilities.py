"""
This file is generated by 'build_code.py'.
It has been set to read only so that you don't edit it without using
'build_code.py'. Thought that may change in the future.
"""

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
from flask import render_template_string

from models import proficiencies
# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from models.base_classes import Base, attribute_mapped_dict_hybrid

ALL_ABILITIES = [('Apprentice', 'AuraAbility', 'Archetype', 'Ascetic', 3, 'You are capable of learning additional spells.', '{{ (level) * 1 }}', '{{ (level + 1) * 1 }}', True, 'SpellLimit', 1, 'Understanding', 0, 'Null', 'Null'), ('Arcanum', 'AuraAbility', 'Basic', 'None', 5, 'Gain maximum sanctity. Master this ability to unlock the Philosopher archetype.', '{{ (level) * 2 }}', '{{ (level + 1) * 2 }}', True, 'Sanctity', 2, 'Understanding', 0, 'Null', 'Null'), ('Backstab', 'AuraAbility', 'Archetype', 'Scoundrel', 3, 'You are more likely to attack first in combat.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'FirstStrike', 5, 'Understanding', 0, 'Null', 'Null'), ('Bash', 'AuraAbility', 'Archetype', 'Brute', 3, '(BROKEN)You deal more damage with blunt weapons.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('Blackhearted', 'AuraAbility', 'Archetype', 'Scoundrel', 3, '(BROKEN)Lose virtue faster.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('Charmer', 'AuraAbility', 'Archetype', 'Opportunist', 3, '(BROKEN)You are more likely to succeed when choosing charm dialogues.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('Discipline', 'AuraAbility', 'Basic', 'None', 5, 'Gain devotion faster. Master this ability to unlock the Ascetic archetype.', '{{ (level) * 1 }}%', '{{ (level + 1) * 1 }}%', True, 'Piety', 1, 'Understanding', 0, 'Null', 'Null'), ('Haggler', 'AuraAbility', 'Archetype', 'Opportunist', 3, 'Prices at shops are cheaper.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Bartering', 5, 'Understanding', 0, 'Null', 'Null'), ('MartialArts', 'AuraAbility', 'Archetype', 'Ascetic', 3, 'You deal more damage in combat.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Damage', 5, 'Understanding', 0, 'Null', 'Null'), ('Meditation', 'AuraAbility', 'Archetype', 'Ascetic', 3, 'Regenerate sanctity per day.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Redemption', 5, 'Understanding', 0, 'Null', 'Null'), ('Poet', 'AuraAbility', 'Basic', 'None', 5, 'Gain renown faster. Master this ability to unlock the Opportunist archetype.', '{{ (level) * 1 }}', '{{ (level + 1) * 1 }}', True, 'Reputation', 1, 'Understanding', 0, 'Null', 'Null'), ('Relentless', 'AuraAbility', 'Basic', 'None', 5, 'Gain maximum health. Master this ability to unlock the Brute archetype.', '{{ (level) * 3 }}', '{{ (level + 1) * 3 }}', True, 'Health', 3, 'Understanding', 0, 'Null', 'Null'), ('Scholar', 'AuraAbility', 'Archetype', 'Philosopher', 3, 'Gain experience faster.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Understanding', 5, 'Understanding', 0, 'Null', 'Null'), ('Skinner', 'AuraAbility', 'Archetype', 'Survivalist', 3, '(BROKEN)You have a chance of obtaining a usable fur after kiling a beast.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('Strider', 'AuraAbility', 'Archetype', 'Survivalist', 3, '(BROKEN)Traveling on the map requires less endurance.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('Student', 'AuraAbility', 'Archetype', 'Philosopher', 3, '(BROKEN)You are capable of learning additional spells.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('Traveler', 'AuraAbility', 'Basic', 'None', 5, 'Reveal more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.', '{{ (level) * 1 }}', '{{ (level + 1) * 1 }}', True, 'Vision', 1, 'Understanding', 0, 'Null', 'Null'), ('Trickster', 'AuraAbility', 'Basic', 'None', 5, 'Become harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.', '{{ (level) * 3 }}', '{{ (level + 1) * 3 }}', True, 'Stealth', 3, 'Understanding', 0, 'Null', 'Null'), ('Vigilance', 'AuraAbility', 'Archetype', 'Survivalist', 3, '(BROKEN)You are less likely to be ambushed.', '{{ (level) * 5 }}', '{{ (level + 1) * 5 }}', True, 'Health', 0, 'Understanding', 0, 'Null', 'Null'), ('FameBombTest', 'CastableAbility', 'Basic', 'None', 3, 'Spend 2 sanctity to gain instant fame with this silly test spell.', '{{ (level) * 3 }}', '{{ (level + 1) * 3 }}', True, 'Renown', 0, 'Understanding', 0, '2', '0'), ('VirtueBombTest', 'CastableAbility', 'Basic', 'None', 3, 'Spend 1 endurance to gain instant virtue with this silly spell for testing purposes.', '{{ (level) * 2 }}', '{{ (level + 1) * 2 }}', True, 'Virtue', 0, 'Understanding', 0, '0', '1'), ('IgnoreTest1', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('IgnoreTest2', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('IgnoreTest3', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('IgnoreTest4', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('IgnoreTest5', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('IgnoreTest6', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('IgnoreTest7', 'CastableAbility', 'Basic', 'None', 3, 'Irrelevant', 'Irrelevant', 'Irrelevant', True, 'Virtue', 0, 'Understanding', 0, '0', '0'), ('VampiricAura', 'AuraAbility', 'Basic', 'None', 3, 'You steal life per hit', 'Amount stolen: {{ (level) * 1 }}', 'Amount stolen: {{ (level + 1) * 1 }}', True, 'LifestealStatic', 1, 'Understanding', 0, 'Null', 'Null'), ('Lifeleech', 'AuraAbility', 'Basic', 'None', 3, 'You steal life based on how much damage you deal in combat', 'Percent of damage dealt: {{ (level) * 5 }}', 'Percent of damage dealt: {{ (level + 1) * 5 }}', True, 'LifestealPercent', 5, 'Understanding', 0, 'Null', 'Null')]

ALL_NAMES = ['Apprentice', 'Arcanum', 'Backstab', 'Bash', 'Blackhearted', 'Charmer', 'Discipline', 'Fame bomb test', 'Haggler', 'Ignore test1', 'Ignore test2', 'Ignore test3', 'Ignore test4', 'Ignore test5', 'Ignore test6', 'Ignore test7', 'Lifeleech', 'Martial arts', 'Meditation', 'Poet', 'Relentless', 'Scholar', 'Skinner', 'Strider', 'Student', 'Traveler', 'Trickster', 'Vampiric aura', 'Vigilance', 'Virtue bomb test']
ALL_ATTRIBUTE_NAMES = ['apprentice', 'arcanum', 'backstab', 'bash', 'blackhearted', 'charmer', 'discipline', 'fame_bomb_test', 'haggler', 'ignore_test1', 'ignore_test2', 'ignore_test3', 'ignore_test4', 'ignore_test5', 'ignore_test6', 'ignore_test7', 'lifeleech', 'martial_arts', 'meditation', 'poet', 'relentless', 'scholar', 'skinner', 'strider', 'student', 'traveler', 'trickster', 'vampiric_aura', 'vigilance', 'virtue_bomb_test']
ALL_CLASS_NAMES = ['Apprentice', 'Arcanum', 'Backstab', 'Bash', 'Blackhearted', 'Charmer', 'Discipline', 'FameBombTest', 'Haggler', 'IgnoreTest1', 'IgnoreTest2', 'IgnoreTest3', 'IgnoreTest4', 'IgnoreTest5', 'IgnoreTest6', 'IgnoreTest7', 'Lifeleech', 'MartialArts', 'Meditation', 'Poet', 'Relentless', 'Scholar', 'Skinner', 'Strider', 'Student', 'Traveler', 'Trickster', 'VampiricAura', 'Vigilance', 'VirtueBombTest']


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
    name = Column(String(50))  # Maybe 'unique' is not necessary?
    level = Column(Integer)
    max_level = Column(Integer)
    # Maybe description should be unique? use: unique=True as keyword.
    description = Column(String(200))
    castable = Column(Boolean)
    _current = Column(String(50))
    _next = Column(String(50))
    sanctity_cost = Column(Integer)
    endurance_cost = Column(Integer)

    # Note: Original code used default of "Unknown"
    # I chopped the BasicAbility class as redundant. Now I am going to
    # have to add the fucker back in.
    type = Column(String(50))
    ability_type = orm.synonym('type')

    # This determines if the ability is hidden and can not be learned or seen by the player
    hidden = Column(Boolean)
    learnable = Column(Boolean)

    # This decides which of the 4 types of abilities it is (default is basic)

    tree = Column(String(50))
    tree_type = Column(String(50))
    image = Column(String(50))

    # Relationships
    # Hero to self is one to one.
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="abilities")

    # Ability to Proficiencies is One to Many
    proficiencies = relationship(
        "Proficiency",
        collection_class=attribute_mapped_dict_hybrid('name'),
        back_populates='ability',
        cascade="all, delete-orphan")

    attrib_name = 'ability'
    adjective = ["I", "II", "III", "IV", "V", "VI"]

    @property
    def display_name(self):
        return self.adjective[self.level - 1]

    @property
    def learn_name(self):
        return self.adjective[self.level]

    @property
    def current(self):
        return render_template_string(self._current, level=self.level)

    @property
    def next(self):
        return render_template_string(self._next, level=self.level)

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

    def __init__(self, name, max_level, description, spell_thing="", current=0, next=0, hidden=True, learnable=False, tree="basic", tree_type="", proficiency_data=(), spell_data=(), sanctity_cost=0, endurance_cost=0):
        """Build a basic ability object.

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
        self.max_level = max_level  # Highest level that this ability can get to
        self.description = description  # Describe what it does
        self.castable = False
        self._current = current
        self._next = next
        if learnable:   # If the ability starts as a default of learnable, then it shouldn't start hidden to the player
            self.hidden = False
        else:
            self.hidden = hidden    # If the player can see it
        self.learnable = learnable  # If the player currently has the requirements to learn/upgrade it
        self.tree = tree  # Which research tree it belongs to (basic, archetype, class, religious)
        self.tree_type = tree_type  # Which specific tree (ie. if the tree is religious, then which religion is it)
        self.image = "ability_icon_" + self.name

        # Initialize proficiencies
        # Currently doesn't add any proficiencies.
        for class_name, arg_dict in proficiency_data:
            Class = getattr(proficiencies, class_name)
            # pdb.set_trace()
            obj = Class(**arg_dict)
            self.proficiencies[obj.name] = obj

        # Jacob did this. I need some help setting it up. This should be for casting spells.
        for class_name, arg_dict in spell_data:
            Class = getattr(proficiencies, class_name)
            # pdb.set_trace()
            obj = Class(**arg_dict)
            self.proficiencies[obj.name] = obj

        # These and the one above should only be in castable.
        self.sanctity_cost = sanctity_cost
        self.endurance_cost = endurance_cost

    # @property
    # def display_name(self):
    #     return self.name.capitalize()

    @orm.validates('level')
    def validate_level(self, key, current):
        """Set the base and modifier off the current level.

        x = 7
        for y in range(1, 10):
            x = (x // (y - 1 or 1)) * y (base)
            x = (x / (y - 1 or 1)) * y (modifier)

        NOTE: hero get_summed_proficiecies must check if level of Ability is 0
        """
        for prof in self.proficiencies:
            if current > 0:
                prof.base = (prof.base // (current-1 or 1)) * current
                prof.modifier = (prof.modifier // (current-1 or 1)) * current
        return current

    def get_description(self):
        return render_template_string(self.description)

    def get_current_bonus(self):
        return render_template_string(self.current, level=self.level)

    def get_next_bonus(self):
        return render_template_string(self.next, level=self.level)

    def is_max_level(self):
        """Return True if level is at max_level."""
        return self.level >= self.max_level

    def update_stats(self, hero):
        pass
        # hero.refresh_proficiencies()

    def activate(self, hero):
        return self.cast(hero)

    def update_owner(self, hero):
        print("Ability to Hero relationship is now Many to Many.")
        print("Instead of One Hero to Many Ablities.")
        exit("Removed in favor of add_hero and remove_hero")
        # self.heroes = [hero]


class CastableAbility(Ability):
    __mapper_args__ = {
        'polymorphic_identity': 'CastableAbility',
    }

    def __init__(self, *args, **kwargs):
        """Build a new ArchetypeAbility object.

        Note: self.type must be set in __init__ to polymorphic_identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        super().__init__(*args, **kwargs)
        self.castable = True

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """

        temp = """<h1>{{ ability.name }} (Level {{ ability.level }})</h1>
                      <h2>{{ ability.description }}</h2>
                      {% if ability.level %}<h3>Current: {{ ability.current }}</h3>{% endif %}
                      {% if not ability.is_max_level() %}<h3>Next: {{ ability.next }}</h3>{% else %}<h3>This ability is at its maximum level.</h3>{% endif %}
                      {% if not ability.is_max_level() and ((ability.tree == "Basic" and ability.hero.basic_ability_points) or (ability.tree == "Archetype" and ability.hero.archetype_ability_points))%}
                      <button id=levelUpAbilityButton class="upgradeButton" onclick="sendToPy(event, abilityTooltip, 'update_ability', {'id': {{ ability.id }}});"></button>
                      {% endif %}"""
        return render_template_string(temp, ability=self)

    def cast(self, hero):
        """Use the ability. Like casting a spell.

        use:
        ability.activate(hero)
        NOTE: returns False if spell is too expensive (cost > proficiencies.sanctity.current)
        If cast is succesful then return value is True.
        """
        if hero.base_proficiencies['sanctity'].current < self.sanctity_cost:
            print("Trying to cast a spell but you have not enough sanctity.")
            return "error: not enough sanctity"
        if hero.base_proficiencies['endurance'].current < self.endurance_cost:
            print("Trying to cast a spell but you have not enough endurance.")
            return "error: not enough endurance"
        hero.base_proficiencies['sanctity'].current -= self.sanctity_cost
        hero.base_proficiencies['endurance'].current -= self.endurance_cost
        return "success"

class AuraAbility(Ability):
    __mapper_args__ = {
        'polymorphic_identity': 'AuraAbility',
    }

    def __init__(self, *args, **kwargs):
        """Build a new Archetype_Ability object.

        Note: self.type must be set in __init__ to polymorphic identity.
        If no __init__ method then type gets set automagically.
        If type not set then call to 'super' overwrites type.
        """
        super().__init__(*args, **kwargs)

    @property
    def tooltip(self):
        """Create a tooltip for each variable.

        Modifies the final and next_value with the Class's format spec.
        """

        temp = """<h1>{{ ability.name }} (Level {{ ability.level }})</h1>
                      <h2>{{ ability.description }}</h2>
                      {% if ability.level %}<h3>Current: {{ ability.current }}</h3>{% endif %}
                      {% if not ability.is_max_level() %}<h3>Next: {{ ability.next }}</h3>{% else %}<h3>This ability is at its maximum level.</h3>{% endif %}
                      {% if not ability.is_max_level() and ((ability.tree == "Basic" and ability.hero.basic_ability_points) or (ability.tree == "Archetype" and ability.hero.archetype_ability_points))%}
                      <button id=levelUpAbilityButton class="upgradeButton" onclick="sendToPy(event, abilityTooltip, 'update_ability', {'id': {{ ability.id }}});"></button>
                      {% endif %}"""
        return render_template_string(temp, ability=self)


class Apprentice(AuraAbility):
    attrib_name = "apprentice"

    __mapper_args__ = {
        'polymorphic_identity': 'Apprentice',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Apprentice', tree='Archetype', tree_type='Ascetic', max_level=3, description='You are capable of learning additional spells.', current='{{ (level) * 1 }}', next='{{ (level + 1) * 1 }}', learnable=True, proficiency_data=[('SpellLimit', {'base': 1}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Arcanum(AuraAbility):
    attrib_name = "arcanum"

    __mapper_args__ = {
        'polymorphic_identity': 'Arcanum',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Arcanum', tree='Basic', tree_type='None', max_level=5, description='Gain maximum sanctity. Master this ability to unlock the Philosopher archetype.', current='{{ (level) * 2 }}', next='{{ (level + 1) * 2 }}', learnable=True, proficiency_data=[('Sanctity', {'base': 2}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Backstab(AuraAbility):
    attrib_name = "backstab"

    __mapper_args__ = {
        'polymorphic_identity': 'Backstab',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Backstab', tree='Archetype', tree_type='Scoundrel', max_level=3, description='You are more likely to attack first in combat.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('FirstStrike', {'base': 5}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Bash(AuraAbility):
    attrib_name = "bash"

    __mapper_args__ = {
        'polymorphic_identity': 'Bash',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Bash', tree='Archetype', tree_type='Brute', max_level=3, description='(BROKEN)You deal more damage with blunt weapons.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Blackhearted(AuraAbility):
    attrib_name = "blackhearted"

    __mapper_args__ = {
        'polymorphic_identity': 'Blackhearted',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Blackhearted', tree='Archetype', tree_type='Scoundrel', max_level=3, description='(BROKEN)Lose virtue faster.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Charmer(AuraAbility):
    attrib_name = "charmer"

    __mapper_args__ = {
        'polymorphic_identity': 'Charmer',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Charmer', tree='Archetype', tree_type='Opportunist', max_level=3, description='(BROKEN)You are more likely to succeed when choosing charm dialogues.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Discipline(AuraAbility):
    attrib_name = "discipline"

    __mapper_args__ = {
        'polymorphic_identity': 'Discipline',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Discipline', tree='Basic', tree_type='None', max_level=5, description='Gain devotion faster. Master this ability to unlock the Ascetic archetype.', current='{{ (level) * 1 }}%', next='{{ (level + 1) * 1 }}%', learnable=True, proficiency_data=[('Piety', {'base': 1}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Haggler(AuraAbility):
    attrib_name = "haggler"

    __mapper_args__ = {
        'polymorphic_identity': 'Haggler',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Haggler', tree='Archetype', tree_type='Opportunist', max_level=3, description='Prices at shops are cheaper.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Bartering', {'base': 5}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class MartialArts(AuraAbility):
    attrib_name = "martial_arts"

    __mapper_args__ = {
        'polymorphic_identity': 'MartialArts',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='MartialArts', tree='Archetype', tree_type='Ascetic', max_level=3, description='You deal more damage in combat.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Damage', {'base': 5}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Meditation(AuraAbility):
    attrib_name = "meditation"

    __mapper_args__ = {
        'polymorphic_identity': 'Meditation',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Meditation', tree='Archetype', tree_type='Ascetic', max_level=3, description='Regenerate sanctity per day.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Redemption', {'base': 5}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Poet(AuraAbility):
    attrib_name = "poet"

    __mapper_args__ = {
        'polymorphic_identity': 'Poet',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Poet', tree='Basic', tree_type='None', max_level=5, description='Gain renown faster. Master this ability to unlock the Opportunist archetype.', current='{{ (level) * 1 }}', next='{{ (level + 1) * 1 }}', learnable=True, proficiency_data=[('Reputation', {'base': 1}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Relentless(AuraAbility):
    attrib_name = "relentless"

    __mapper_args__ = {
        'polymorphic_identity': 'Relentless',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Relentless', tree='Basic', tree_type='None', max_level=5, description='Gain maximum health. Master this ability to unlock the Brute archetype.', current='{{ (level) * 3 }}', next='{{ (level + 1) * 3 }}', learnable=True, proficiency_data=[('Health', {'base': 3}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Scholar(AuraAbility):
    attrib_name = "scholar"

    __mapper_args__ = {
        'polymorphic_identity': 'Scholar',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Scholar', tree='Archetype', tree_type='Philosopher', max_level=3, description='Gain experience faster.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Understanding', {'base': 5}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Skinner(AuraAbility):
    attrib_name = "skinner"

    __mapper_args__ = {
        'polymorphic_identity': 'Skinner',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Skinner', tree='Archetype', tree_type='Survivalist', max_level=3, description='(BROKEN)You have a chance of obtaining a usable fur after kiling a beast.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Strider(AuraAbility):
    attrib_name = "strider"

    __mapper_args__ = {
        'polymorphic_identity': 'Strider',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Strider', tree='Archetype', tree_type='Survivalist', max_level=3, description='(BROKEN)Traveling on the map requires less endurance.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Student(AuraAbility):
    attrib_name = "student"

    __mapper_args__ = {
        'polymorphic_identity': 'Student',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Student', tree='Archetype', tree_type='Philosopher', max_level=3, description='(BROKEN)You are capable of learning additional spells.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Traveler(AuraAbility):
    attrib_name = "traveler"

    __mapper_args__ = {
        'polymorphic_identity': 'Traveler',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Traveler', tree='Basic', tree_type='None', max_level=5, description='Reveal more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.', current='{{ (level) * 1 }}', next='{{ (level + 1) * 1 }}', learnable=True, proficiency_data=[('Vision', {'base': 1}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Trickster(AuraAbility):
    attrib_name = "trickster"

    __mapper_args__ = {
        'polymorphic_identity': 'Trickster',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Trickster', tree='Basic', tree_type='None', max_level=5, description='Become harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.', current='{{ (level) * 3 }}', next='{{ (level + 1) * 3 }}', learnable=True, proficiency_data=[('Stealth', {'base': 3}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Vigilance(AuraAbility):
    attrib_name = "vigilance"

    __mapper_args__ = {
        'polymorphic_identity': 'Vigilance',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Vigilance', tree='Archetype', tree_type='Survivalist', max_level=3, description='(BROKEN)You are less likely to be ambushed.', current='{{ (level) * 5 }}', next='{{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('Health', {'base': 0}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class FameBombTest(CastableAbility):
    attrib_name = "fame_bomb_test"

    __mapper_args__ = {
        'polymorphic_identity': 'FameBombTest',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='FameBombTest', tree='Basic', tree_type='None', max_level=3, description='Spend 2 sanctity to gain instant fame with this silly test spell.', current='{{ (level) * 3 }}', next='{{ (level + 1) * 3 }}', learnable=True, proficiency_data=[], spell_data=[('Renown', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=2, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class VirtueBombTest(CastableAbility):
    attrib_name = "virtue_bomb_test"

    __mapper_args__ = {
        'polymorphic_identity': 'VirtueBombTest',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='VirtueBombTest', tree='Basic', tree_type='None', max_level=3, description='Spend 1 endurance to gain instant virtue with this silly spell for testing purposes.', current='{{ (level) * 2 }}', next='{{ (level + 1) * 2 }}', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=1)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest1(CastableAbility):
    attrib_name = "ignore_test1"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest1',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest1', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest2(CastableAbility):
    attrib_name = "ignore_test2"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest2',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest2', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest3(CastableAbility):
    attrib_name = "ignore_test3"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest3',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest3', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest4(CastableAbility):
    attrib_name = "ignore_test4"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest4',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest4', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest5(CastableAbility):
    attrib_name = "ignore_test5"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest5',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest5', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest6(CastableAbility):
    attrib_name = "ignore_test6"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest6',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest6', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class IgnoreTest7(CastableAbility):
    attrib_name = "ignore_test7"

    __mapper_args__ = {
        'polymorphic_identity': 'IgnoreTest7',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='IgnoreTest7', tree='Basic', tree_type='None', max_level=3, description='Irrelevant', current='Irrelevant', next='Irrelevant', learnable=True, proficiency_data=[], spell_data=[('Virtue', {'base': 0}), ('Understanding', {'base': 0})], sanctity_cost=0, endurance_cost=0)
        for key, value in kwargs:
            setattr(self, key, value)


class VampiricAura(AuraAbility):
    attrib_name = "vampiric_aura"

    __mapper_args__ = {
        'polymorphic_identity': 'VampiricAura',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='VampiricAura', tree='Basic', tree_type='None', max_level=3, description='You steal life per hit', current='Amount stolen: {{ (level) * 1 }}', next='Amount stolen: {{ (level + 1) * 1 }}', learnable=True, proficiency_data=[('LifestealStatic', {'base': 1}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)


class Lifeleech(AuraAbility):
    attrib_name = "lifeleech"

    __mapper_args__ = {
        'polymorphic_identity': 'Lifeleech',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(name='Lifeleech', tree='Basic', tree_type='None', max_level=3, description='You steal life based on how much damage you deal in combat', current='Percent of damage dealt: {{ (level) * 5 }}', next='Percent of damage dealt: {{ (level + 1) * 5 }}', learnable=True, proficiency_data=[('LifestealPercent', {'base': 5}), ('Understanding', {'base': 0})])
        for key, value in kwargs:
            setattr(self, key, value)