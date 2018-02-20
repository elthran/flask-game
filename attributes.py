"""This file is generated by "data/build_code.py"
It has been set to read only so that you don't edit it without using
build_code.py.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base

ATTRIBUTE_INFORMATION = [
    ("Agility", "A measure of how skilfully you can move."),
    ("Brawn", "A measure of how strong you are."),
    ("Charisma", "A measure of how well you interact with other people"),
    ("Divinity", "A measure of your connection with the spirit world."),
    ("Fortuity", "A measure of your luck."),
    ("Intellect", "A measure of your mental prowess and knowledge."),
    ("Pathfinding", "A measure of your ability to traverse the world."),
    ("Quickness", "A measure of how fast you can move."),
    ("Resilience", "A measure of how tough you are."),
    ("Survivalism", "A measure of how well you can adapt to your surroundings."),
    ("Vitality", "A measure of how healthy you are."),
    ("Willpower", "A measure of how disciplined you are.")
]

ALL_ATTRIBUTES = [attrib[0].lower() for attrib in ATTRIBUTE_INFORMATION]
ALL_NAMES = ['Agility', 'Brawn', 'Charisma', 'Divinity', 'Fortuity', 'Intellect', 'Pathfinding', 'Quickness', 'Resilience', 'Survivalism', 'Vitality', 'Willpower']
ALL_ATTRIBUTE_NAMES = ['agility', 'brawn', 'charisma', 'divinity', 'fortuity', 'intellect', 'pathfinding', 'quickness', 'resilience', 'survivalism', 'vitality', 'willpower']


class AttributeContainer(Base):
    __tablename__ = "attribute_container"

    id = Column(Integer, primary_key=True)

    # Relationships
    # Hero to self is one to one.
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="attributes")

    # Container connections are one to one.
    agility = relationship(
        "Agility",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Agility')",
        uselist=False,
        cascade="all, delete-orphan")
    brawn = relationship(
        "Brawn",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Brawn')",
        uselist=False,
        cascade="all, delete-orphan")
    charisma = relationship(
        "Charisma",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Charisma')",
        uselist=False,
        cascade="all, delete-orphan")
    divinity = relationship(
        "Divinity",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Divinity')",
        uselist=False,
        cascade="all, delete-orphan")
    fortuity = relationship(
        "Fortuity",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Fortuity')",
        uselist=False,
        cascade="all, delete-orphan")
    intellect = relationship(
        "Intellect",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Intellect')",
        uselist=False,
        cascade="all, delete-orphan")
    pathfinding = relationship(
        "Pathfinding",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Pathfinding')",
        uselist=False,
        cascade="all, delete-orphan")
    quickness = relationship(
        "Quickness",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Quickness')",
        uselist=False,
        cascade="all, delete-orphan")
    resilience = relationship(
        "Resilience",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Resilience')",
        uselist=False,
        cascade="all, delete-orphan")
    survivalism = relationship(
        "Survivalism",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Survivalism')",
        uselist=False,
        cascade="all, delete-orphan")
    vitality = relationship(
        "Vitality",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Vitality')",
        uselist=False,
        cascade="all, delete-orphan")
    willpower = relationship(
        "Willpower",
        primaryjoin="and_(AttributeContainer.id==Attribute.attribute_container_id, "
                    "Attribute.name=='Willpower')",
        uselist=False,
        cascade="all, delete-orphan")

    def __init__(self):
        self.agility = Agility()
        self.brawn = Brawn()
        self.charisma = Charisma()
        self.divinity = Divinity()
        self.fortuity = Fortuity()
        self.intellect = Intellect()
        self.pathfinding = Pathfinding()
        self.quickness = Quickness()
        self.resilience = Resilience()
        self.survivalism = Survivalism()
        self.vitality = Vitality()
        self.willpower = Willpower()

    def items(self):
        """Basically a dict.items() clone that looks like ((key, value),
            (key, value), ...)

        This is an iterator? Maybe it should be a list or a view?
        """
        return ((key, getattr(self, key)) for key in ALL_ATTRIBUTE_NAMES)

    def __iter__(self):
        """Return all the attributes of this function as an iterator."""
        return (getattr(self, key) for key in ALL_ATTRIBUTE_NAMES)

        
class Attribute(Base):
    """Attribute class that stores data about a hero object.
    """
    __tablename__ = "attribute"
    
    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    description = Column(String(200))
    level = Column(Integer)

    # Relationships
    # Ability to abilities. Abilities is a list of ability objects.
    attribute_container_id = Column(
        Integer, ForeignKey('attribute_container.id', ondelete="CASCADE"))

    __mapper_args__ = {
        'polymorphic_identity': 'Attribute',
        'polymorphic_on': name
    }
    
    def __init__(self, name, description):
        """Build the initial Attribute object.
        
        Set all values to 1.
        """
        
        self.name = name
        self.description = description
        self.level = 1


class Agility(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Agility',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Agility", "A measure of how skilfully you can move.")

        for key, value in kwargs:
            setattr(self, key, value)


class Brawn(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Brawn',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Brawn", "A measure of how strong you are.")

        for key, value in kwargs:
            setattr(self, key, value)


class Charisma(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Charisma',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Charisma", "A measure of how well you interact with other people")

        for key, value in kwargs:
            setattr(self, key, value)


class Divinity(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Divinity',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Divinity", "A measure of your connection with the spirit world.")

        for key, value in kwargs:
            setattr(self, key, value)


class Fortuity(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Fortuity',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Fortuity", "A measure of your luck.")

        for key, value in kwargs:
            setattr(self, key, value)


class Intellect(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Intellect',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Intellect", "A measure of your mental prowess and knowledge.")

        for key, value in kwargs:
            setattr(self, key, value)


class Pathfinding(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Pathfinding',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Pathfinding", "A measure of your ability to traverse the world.")

        for key, value in kwargs:
            setattr(self, key, value)


class Quickness(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Quickness',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Quickness", "A measure of how fast you can move.")

        for key, value in kwargs:
            setattr(self, key, value)


class Resilience(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Resilience',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Resilience", "A measure of how tough you are.")

        for key, value in kwargs:
            setattr(self, key, value)


class Survivalism(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Survivalism',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Survivalism", "A measure of how well you can adapt to your surroundings.")

        for key, value in kwargs:
            setattr(self, key, value)


class Vitality(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Vitality',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Vitality", "A measure of how healthy you are.")

        for key, value in kwargs:
            setattr(self, key, value)


class Willpower(Attribute):
    __mapper_args__ = {
        'polymorphic_identity': 'Willpower',
    }

    def __init__(self, *args, **kwargs):
        super().__init__("Willpower", "A measure of how disciplined you are.")

        for key, value in kwargs:
            setattr(self, key, value)
