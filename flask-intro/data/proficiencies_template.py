"""This file is generated by "data/build_code.py"
It has been set to read only so that you don't edit it without using
build_code.py.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base_classes import Base

{% include "proficiencies_data.py" %}

class Proficiencies(Base):
    __tablename__ = 'proficiencies'
    
    id = Column(Integer, primary_key=True)

    #Relationships     
    {%- for name in ALL_PROFICIENCIES %}
    {{ name }}_id = Column(Integer, ForeignKey('proficiency.id'))
    {{ name }} = relationship("Proficiency", uselist=False, foreign_keys="[Proficiencies.{{ name }}_id]")
    {%- endfor %}
    
    def __init__(self):
        {% for prof in PROFICIENCY_INFORMATION %}
        self.{{ prof[0].lower().replace(' ', '_') }} = Proficiency("{{ prof[0] }}", "{{ prof[1] }}", "{{ prof[2] }}", "{{ prof[3] }}")
        {%- endfor %}
        

    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like ([(key, value), (key, value), ...])
        """
        return ((key, getattr(self, key)) for key in ALL_PROFICIENCIES)
        
        
    def __iter__(self):
        return (getattr(self, key) for key in ALL_PROFICIENCIES)

        
class Proficiency(Base):
    """Proficiency class that stores data about a hero object.
    """
    __tablename__ = "proficiency"
    
    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)
    attribute_type = Column(String)
    type = Column(String)
    level = Column(Integer)
    value = Column(Integer)
    next_value = Column(Integer)
    max_level = Column(Integer)

    def __init__(self, name, description, attribute_type, type):
        self.name = name
        self.description = description
        self.attribute_type = attribute_type
        self.type = type
        
        self.level = 1
        self.value = 10
        self.next_value = 15
        self.max_level = 1

    def update_testing(self, myHero):
        self.max_level = myHero.attributes.vitality // 2
        if self.max_level < 1:
            self.max_level = 1
        self.value = (self.level * 5) + 5
        self.next_value = ((self.level + 1) * 5) + 5

