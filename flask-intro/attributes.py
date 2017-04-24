"""This file is generated by "data/build_code.py"
It has been set to read only so that you don't edit it without using
build_code.py.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base

ATTRIBUTE_INFORMATION = [
    ("Agility", "A measure of how agile a character is. Dexterity controls attack and movement speed and accuracy, as well as evading an opponent's attack ."),
    ("Charisma", "A measure of a character's social skills, and sometimes their physical appearance."),
    ("Divinity", "A measure of a character's common sense and/or spirituality."),
    ("Fortitude", "A measure of how resilient a character is."),
    ("Fortuity", "A measure of a character's luck. "),
    ("Perception", "A measure of a character's openness to their surroundings."),
    ("Reflexes", "A measure of how agile a character is. "),
    ("Resilience", "A measure of how resilient a character is. "),
    ("Strength", "A measure of how physically strong a character is. "),
    ("Survivalism", "A measure of a character's openness to their surroundings. "),
    ("Vitality", "A measure of how sturdy a character is."),
    ("Wisdom", "A measure of a character's problem-solving ability.")
]

ALL_ATTRIBUTES = [attrib[0].lower() for attrib in ATTRIBUTE_INFORMATION]

class Attributes(Base):
    __tablename__ = 'attributes'
    
    id = Column(Integer, primary_key=True)

    
    def __init__(self):
        
        self.agility = Attribute("Agility", "A measure of how agile a character is. Dexterity controls attack and movement speed and accuracy, as well as evading an opponent's attack .")
        self.charisma = Attribute("Charisma", "A measure of a character's social skills, and sometimes their physical appearance.")
        self.divinity = Attribute("Divinity", "A measure of a character's common sense and/or spirituality.")
        self.fortitude = Attribute("Fortitude", "A measure of how resilient a character is.")
        self.fortuity = Attribute("Fortuity", "A measure of a character's luck. ")
        self.perception = Attribute("Perception", "A measure of a character's openness to their surroundings.")
        self.reflexes = Attribute("Reflexes", "A measure of how agile a character is. ")
        self.resilience = Attribute("Resilience", "A measure of how resilient a character is. ")
        self.strength = Attribute("Strength", "A measure of how physically strong a character is. ")
        self.survivalism = Attribute("Survivalism", "A measure of a character's openness to their surroundings. ")
        self.vitality = Attribute("Vitality", "A measure of how sturdy a character is.")
        self.wisdom = Attribute("Wisdom", "A measure of a character's problem-solving ability.")
        

    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like ([(key, value), (key, value), ...])
        """
        return ((key, getattr(self, key)) for key in ALL_ATTRIBUTES)
        
        
    def __iter__(self):
        return (getattr(self, key) for key in ALL_ATTRIBUTES)

        
class Attribute(Base):
    """Attribute class that stores data about a hero object.
    """
    __tablename__ = "attribute"
    
    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)
    level = Column(Integer)
    
    def __init__(self, name, description):
        """Build the initial Attribute object.
        
        Set all values to 1.
        """
        
        self.name = name
        self.description = description
        self.level = 1


#Relationships
Attributes.agility_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.agility = relationship("Attribute", uselist=False, foreign_keys="[Attributes.agility_id]")
Attributes.charisma_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.charisma = relationship("Attribute", uselist=False, foreign_keys="[Attributes.charisma_id]")
Attributes.divinity_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.divinity = relationship("Attribute", uselist=False, foreign_keys="[Attributes.divinity_id]")
Attributes.fortitude_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.fortitude = relationship("Attribute", uselist=False, foreign_keys="[Attributes.fortitude_id]")
Attributes.fortuity_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.fortuity = relationship("Attribute", uselist=False, foreign_keys="[Attributes.fortuity_id]")
Attributes.perception_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.perception = relationship("Attribute", uselist=False, foreign_keys="[Attributes.perception_id]")
Attributes.reflexes_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.reflexes = relationship("Attribute", uselist=False, foreign_keys="[Attributes.reflexes_id]")
Attributes.resilience_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.resilience = relationship("Attribute", uselist=False, foreign_keys="[Attributes.resilience_id]")
Attributes.strength_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.strength = relationship("Attribute", uselist=False, foreign_keys="[Attributes.strength_id]")
Attributes.survivalism_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.survivalism = relationship("Attribute", uselist=False, foreign_keys="[Attributes.survivalism_id]")
Attributes.vitality_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.vitality = relationship("Attribute", uselist=False, foreign_keys="[Attributes.vitality_id]")
Attributes.wisdom_id = Column(Integer, ForeignKey('attribute.id'))
Attributes.wisdom = relationship("Attribute", uselist=False, foreign_keys="[Attributes.wisdom_id]")
