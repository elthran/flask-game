"""
Author: Marlen Brunner and Elthran B.

1. This module should provide a class for each type of location within
     the game.
2. These classes should use inheritance as much as possible.
3. Each class should provide a render function which uses a flask template and
can be inserted into the main website.

Basic layout should be:
BaseLocation
    BaseMap
        WorldMap
        TownMap
        CaveMap
        Map
    Location
        Town
        Cave
        Shop
        Arena (might be a shop?)

Display
    MapDisplay
    LocationDisplay
    ...?

BaseLocation
    BaseMap?
        WorldMap
            LocationMap
                Location
                    Town?
    
Each object should have separate data and display properties.
eg.

Location
    id
    name
    adjacent_locations = many to many relationship with self.
    internal_locations = shops, arena
    encompassing_location (a.k.a. world_map)
    url (/Town/Thornwall, e.g. /{type}/{name}.lower())
        or url = encompassing.url + /type/name
    type (e.g. town)
    display
        display_name - Specially formatted name?
        page_title - specially formatted version of 'name'
        page_heading - specially formatted version of 'name'
        page_image - derived from 'name'
        paragraph - description of location
        places_of_interest - replace with adjacent_locations?
    
"""

import pdb

from sqlalchemy import Column, Integer, String, Table, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property
# ###!IMPORTANT!####
# Sqlite does not implement sqlalchemy.ARRAY so don't try and use it.

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from base_classes import Base, BaseListElement


class Display(Base):
    """Stores data for location and map objects that is displayed in the game
    using html.

    Note: When modifing attributes ...

    places_of_interest is not implemented ... except during initialization.
    """
    __tablename__ = "display"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    page_title = orm.synonym('name')
    page_heading = Column(String)
    page_image = Column(String)
    paragraph = Column(String)

    def __init__(self, obj, page_heading=None, paragraph=None):
        """Build display object based on objects attributes.
        """

        self.name = obj.name
        self.page_heading = page_heading

        # eg. page_image = town if Town object is passed or cave if Cave
        # object is passed.
        self.page_image = obj.type.lower()
        self.paragraph = paragraph

#     def __repr__(self):
#         return """
#     <{}(
#         page_title = '{}',
#         page_heading = '{}',
#         page_image = '{}',
#         paragraph = '{}'
#     )>
# """.format("Display", self.page_title,
#            self.page_heading, self.page_image, self.paragraph)


class Location(Base):
    __tablename__ = 'location'
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/
    # declarative/table_config.html
    # __table_args__ = (
    #     UniqueConstraint(
    #         'parent', 'children', 'siblings', name='non_circular')
    # )

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('location.id'))
    name = Column(String)
    url = Column(String)
    type = Column(String)
    children = relationship("Location", back_populates="parent")
    parent = relationship("Location", remote_side=[id],
                          back_populates="children")

    display_id = Column(Integer, ForeignKey('display.id'))
    display = relationship("Display")

    # siblings = relationship("Location", join parent_id, sibling.parent_id)

    @hybrid_property
    def siblings(self):
        """Shortcut for parent.children.
        """
        if self.parent is not None:
            return self.parent.children
        else:
            return []

    @siblings.setter
    def siblings(self, siblings):
        """Assign a normalized parent between siblings if possible.

        If multiple parents exist ... complain.
        If no parents exists ... complain.
        """

        if not siblings:
            return

        potential_parents = set() if self.parent is None else {self.parent}
        for sibling in siblings:
            parent = sibling.parent
            if parent is not None:
                potential_parents.add(parent)

        if len(potential_parents) > 1:
            raise Exception(
                "I can't find a _harmonized_ parent between these"
                " siblings. Possible parents are {}".format(
                    Base.pretty_list(potential_parents)
                )
            )
        elif len(potential_parents) == 0:
            raise Exception(
                "I can't find _any_ parent between these siblings. Try setting"
                " the 'parent' attribute for these objects instead."
            )
        else:
            parent = potential_parents.pop()
            self.parent = parent
            for sibling in siblings:
                sibling.parent = parent

    # Need validators for children - child can't be parent or sibling
    # Need validator for parent - parent can't be child or sibling
    # Need validator for siblings - can't be parent or child, max of 6
    # Think a hex grid
    def __init__(self, name, location_type, parent=None, children=[],
                 siblings=[]):
        self.name = name
        self.type = location_type
        self.parent = parent
        self.children = children
        self.siblings = siblings
        self.url = self.build_url()
        self.display = Display(self)
        self.init_on_load()

    @orm.reconstructor
    def init_on_load(self):
        self.siblings = self.siblings

    def build_url(self):
        if self.parent is None:
            return "/{}/{}".format(self.type, self.name)
        else:
            return self.parent.url + "/{}/{}".format(
                self.type, self.name)


# # Marked for refactor
# # Consider using a grid and implementing (x,y) coordinates for each location.
# class Location(Base):
#     """A place a hero can travel to that is storable in the database.
#
#     Note: adjacent_locations is a list of integers. Note a list of locations,
#     I could figure out how to do that.
#     Maybe when I implement x,y coordinates for each location it could
#     calculate the adjacent ones
#     automatically.
#     Note: 'location_type' is now 'type'. But you can still use location_type
#     because orm.synonym! ... bam!
#
#     Use:
#     loc1 = Location(id=1, name="test")
#     loc1.adjacent_locations = [2, 3, 4]
#     """
#     __tablename__ = "location"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     type = Column(String)
#     location_type = orm.synonym('type')
#     url = Column(String)
#
#     map_id = Column(Integer, ForeignKey('map.id'))
#     map = relationship("Map", foreign_keys=[map_id], back_populates="locations")
#     location_world = orm.synonym('map')
#
#     display = relationship("Display", uselist=False)
#
#     def __init__(self, name, id=None):
#         self.id = id
#         self.name = name
#         self.adjacent_locations = []
#         self.url = "/{}/{}".format(self.type, self.name)
#
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Location',
#         'polymorphic_on':type
#     }
#
#
#     @hybrid_property
#     def adjacent_locations(self):
#         """Return a list of ids of adjacent locations.
#         """
#         return [element.value for element in self._adjacent_locations]
#
#
#     @adjacent_locations.setter
#     def adjacent_locations(self, values):
#         """Create list of BaseListElement objects.
#         """
#         self._adjacent_locations = [BaseListElement(value) for value in values]
#
#
# class Town(Location):
#     """Town object database ready class.
#
#     Basically adds a display and identity of "Town" to the location object.
#     """
#     __tablename__ = "town"
#
#     id = Column(Integer, ForeignKey('location.id'), primary_key=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Town',
#     }
#
#
# class Cave(Location):
#     """Cave object database ready class.
#
#     Basically adds a display and identity of "Cave" to the location object.
#     """
#     __tablename__ = "cave"
#
#     id = Column(Integer, ForeignKey('location.id'), primary_key=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Cave',
#     }
#
#
# class Map(Base):
#     """Basically a location clone but without the mess of joins and relationship problems :P.
#
#     Solves: Incest ...
#     """
#     __tablename__ = "map"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     type = Column(String)
#     location_type = orm.synonym('type')
#
#     locations = relationship("Location", foreign_keys='[Location.map_id]', back_populates="map")
#     all_map_locations = orm.synonym('locations')
#
#     display = relationship("Display", uselist=False)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'Map',
#         'polymorphic_on':type
#     }
#
#     @hybrid_property
#     def adjacent_locations(self):
#         """Return a list of ids of adjacent locations.
#         """
#         return [element.value for element in self._adjacent_locations]
#
#
#     @adjacent_locations.setter
#     def adjacent_locations(self, values):
#         """Create list of BaseListElement objects.
#         """
#         self._adjacent_locations = [BaseListElement(value) for value in values]
#
#
#     # def __str__(self):
#         # locations = str([location.name for location in self.locations])
#         # try:
#             # return """<{}(id={}, name='{}', type='{}', adjacent_locations={}, locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, locations, self.display)
#         # except AttributeError:
#             # return """<{}(id={}, name='{}', type='{}', adjacent_locations={}, locations={}, display={}>""".format(self.type, self.id, self.name, self.type, self.adjacent_locations, locations, self.display)
#
#
# class WorldMap(Map):
#     __tablename__ = "world_map"
#
#     id = Column(Integer, ForeignKey('map.id'), primary_key=True)
#
#     __mapper_args__ = {
#         'polymorphic_identity':'WorldMap',
#     }
#
#     #Marked for rebuild
#     #Creates attribute map_cities. Prehaps should be a relations?
#     #And map_cities should probably be map_city? Or some other name that actually explains
#     #what it does??
#     #This function modifes the object and returns a value. It should only do one or the other.
#     def show_directions(self, current_location):
#         """Return a list of directions you can go from your current_location.
#
#         ALSO! modifies the attribute map_cities and places_of_interest.
#         map_cities is only a single value of either a cave or a town.
#         """
#         assert current_location in self.locations
#
#         directions = current_location.adjacent_locations
#         if directions == []:
#             directions = [1,2,3]
#
#         self.map_cities = []
#         if current_location.type in ["Town", "Cave"]:
#             self.map_cities = [current_location]
#
#         if self.map_cities:
#             city = self.map_cities[0]
#             self.display.places_of_interest = [("/{}/{}".format(city.type, city.name), city.name)]
#
#         return directions
#
#
#     # temporarily location_id is the same as the index in the list of all_map_locations
#     def find_location(self, location_id):
#         return self.all_map_locations[location_id]
#
#
# #Just another synonym for backwards compatability (which id don't know if it even works?)
# World_Map = WorldMap

 
if __name__ == "__main__":
    pass


