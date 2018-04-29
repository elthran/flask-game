"""
This file is generated by 'build_code.py'.
It has been set to read only so that you don't edit it without using
'build_code.py'. Thought that may change in the future.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models.base_classes import Base

ALL_ATTRIBUTES = [('Agility', 'A measure of how skilfully you can move.'), ('Brawn', 'A measure of how strong you are.'), ('Charisma', 'A measure of how well you interact with other people'), ('Divinity', 'A measure of your connection with the spirit world.'), ('Fortuity', 'A measure of your luck.'), ('Intellect', 'A measure of your mental prowess and knowledge.'), ('Pathfinding', 'A measure of your ability to traverse the world.'), ('Quickness', 'A measure of how fast you can move.'), ('Resilience', 'A measure of how tough you are.'), ('Survivalism', 'A measure of how well you can adapt to your surroundings.'), ('Vitality', 'A measure of how healthy you are.'), ('Willpower', 'A measure of how disciplined you are.')]

ALL_NAMES = ['Agility', 'Brawn', 'Charisma', 'Divinity', 'Fortuity', 'Intellect', 'Pathfinding', 'Quickness', 'Resilience', 'Survivalism', 'Vitality', 'Willpower']
ALL_ATTRIBUTE_NAMES = ['agility', 'brawn', 'charisma', 'divinity', 'fortuity', 'intellect', 'pathfinding', 'quickness', 'resilience', 'survivalism', 'vitality', 'willpower']
ALL_CLASS_NAMES = ['Agility', 'Brawn', 'Charisma', 'Divinity', 'Fortuity', 'Intellect', 'Pathfinding', 'Quickness', 'Resilience', 'Survivalism', 'Vitality', 'Willpower']


class Attribute(Base):
    """Attribute class that stores data about a hero object.
    """
    __tablename__ = "attribute"
    
    id = Column(Integer, primary_key=True)

    type_ = Column(String(50))
    name = Column(String(50))
    description = Column(String(200))
    level = Column(Integer)

    # Relationships
    # Hero to self is one to one.
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="attributes")

    attrib_name = 'attribute'

    __mapper_args__ = {
        'polymorphic_identity': 'Attribute',
        'polymorphic_on': type_
    }
    
    def __init__(self, name, description):
        """Build the initial Attribute object.
        
        Set all values to 1.
        """
        
        self.name = name
        self.description = description
        self.level = 1


class Agility(Attribute):
    attrib_name = "agility"

    __mapper_args__ = {
        'polymorphic_identity': 'Agility',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Agility", "A measure of how skilfully you can move.")

        for key, value in kwargs:
            setattr(self, key, value)


class Brawn(Attribute):
    attrib_name = "brawn"

    __mapper_args__ = {
        'polymorphic_identity': 'Brawn',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Brawn", "A measure of how strong you are.")

        for key, value in kwargs:
            setattr(self, key, value)


class Charisma(Attribute):
    attrib_name = "charisma"

    __mapper_args__ = {
        'polymorphic_identity': 'Charisma',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Charisma", "A measure of how well you interact with other people")

        for key, value in kwargs:
            setattr(self, key, value)


class Divinity(Attribute):
    attrib_name = "divinity"

    __mapper_args__ = {
        'polymorphic_identity': 'Divinity',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Divinity", "A measure of your connection with the spirit world.")

        for key, value in kwargs:
            setattr(self, key, value)


class Fortuity(Attribute):
    attrib_name = "fortuity"

    __mapper_args__ = {
        'polymorphic_identity': 'Fortuity',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Fortuity", "A measure of your luck.")

        for key, value in kwargs:
            setattr(self, key, value)


class Intellect(Attribute):
    attrib_name = "intellect"

    __mapper_args__ = {
        'polymorphic_identity': 'Intellect',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Intellect", "A measure of your mental prowess and knowledge.")

        for key, value in kwargs:
            setattr(self, key, value)


class Pathfinding(Attribute):
    attrib_name = "pathfinding"

    __mapper_args__ = {
        'polymorphic_identity': 'Pathfinding',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Pathfinding", "A measure of your ability to traverse the world.")

        for key, value in kwargs:
            setattr(self, key, value)


class Quickness(Attribute):
    attrib_name = "quickness"

    __mapper_args__ = {
        'polymorphic_identity': 'Quickness',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Quickness", "A measure of how fast you can move.")

        for key, value in kwargs:
            setattr(self, key, value)


class Resilience(Attribute):
    attrib_name = "resilience"

    __mapper_args__ = {
        'polymorphic_identity': 'Resilience',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Resilience", "A measure of how tough you are.")

        for key, value in kwargs:
            setattr(self, key, value)


class Survivalism(Attribute):
    attrib_name = "survivalism"

    __mapper_args__ = {
        'polymorphic_identity': 'Survivalism',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Survivalism", "A measure of how well you can adapt to your surroundings.")

        for key, value in kwargs:
            setattr(self, key, value)


class Vitality(Attribute):
    attrib_name = "vitality"

    __mapper_args__ = {
        'polymorphic_identity': 'Vitality',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Vitality", "A measure of how healthy you are.")

        for key, value in kwargs:
            setattr(self, key, value)


class Willpower(Attribute):
    attrib_name = "willpower"

    __mapper_args__ = {
        'polymorphic_identity': 'Willpower',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Willpower", "A measure of how disciplined you are.")

        for key, value in kwargs:
            setattr(self, key, value)