"""
Author: Marlen Brunner and Elthran B.

1. This module should provide a generic location class.
2. If more specific function is required you can subclass
3. Each Location should have a Display which holds the data the HTML page
    will display.
4. -potentially- The Display class could pre-render/or hold reference to
a flask template so that it can be inserted into the main website directly.

5. !Important! The location must have a list of adjacent locations. This
should be a kind of 'directed graph' or a many to many relationship.
If A is sibling to B, B should be sibling to A by default. Non bidirectional
can be added later.

Location
    Display
    
Each object should have separate data and display properties.
eg.

Location
    id
    name
    siblings = many to many relationship with self.
    children = shops, arena
    parent (a.k.a. world_map)
    url (/Town/Thornwall, e.g. /{type}/{name}.lower())
        or url = encompassing.url + /type/name
    type (e.g. town)
    display
        display_name - Specially formatted name?
        page_title - specially formatted version of 'name'
        page_heading - specially formatted version of 'name'
        page_image - derived from 'name'
        paragraph - description of location
        places_of_interest - generated list of urls that you can move to
            from this location.

Ideas:
    Maybe a long and short url?
    long: /map/Map_Name/town/Town_Name/store/Store_Name
    short: /store/Store_name (basically the last part)
"""

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property
# ###!IMPORTANT!####
# Sqlite does not implement sqlalchemy.ARRAY so don't try and use it.

# !Important!: Base can only be defined in ONE location and ONE location ONLY!
# Well ... ok, but for simplicity sake just pretend that that is true.
from models.base_classes import Base


class Display(Base):
    """Stores data for Location objects that is displayed in the game
    using html.
    """
    name = Column(String(50))
    page_title = orm.synonym('name')
    page_heading = Column(String(50))
    page_image = Column(String(50))
    paragraph = Column(String(200))

    """
    External relationships:
    
    This is set up so that each external relationship is one to one and can be
    accessed through the generic 'self.obj' attribute using
    a list of or statements ... only one should be set at a time.
    """
    # One location -> one display (bidirectional)
    location_id = Column(Integer, ForeignKey('location.id',
                                             ondelete="CASCADE"))
    _location = relationship('Location', uselist=False,
                             back_populates='display')

    @hybrid_property
    def obj(self):
        """Returns the object that this is connected to.

        Only one type of object may be connected at a time.
        This is not enforced and should be.
        """
        return self._location or None

    def __init__(self, obj, page_heading=None, paragraph=None):
        """Build display object based on objects attributes.

        I think that I should add in a link to the correct HTML template
        as well? Based on object type?

        Consider making all of these attributes property methods instead
        so that I don't have to run an update function.

        NOTE: update method overrides all attributes!
        """

        self.name = obj.name
        self.page_heading = page_heading or self.default_heading()

        # eg. page_image = town if Town object is passed or cave if Cave
        # object is passed.
        self.page_image = obj.type.lower() + '.jpg'
        self.paragraph = paragraph or self.default_paragraph()

    def default_heading(self):
        return "You are in {}".format(self.name)

    def default_paragraph(self):
        return "There are many places to visit within" \
               " the {}. Have a look!".format(self.page_image)

    def update(self):
        """Update self to reflect changes in obj properties.

        This is not automatic ... though maybe it should be.
        Currently you need to define a validator on each object
        that calls this function.

        !IMPORTANT! this could overwrite custom attributes incorrectly.

        ONLY RUN THIS if you change the object's:
            name or
            type
        after creation.
        e.g.
            USE update()
        cave = node_grid[2]
        cave.name = "Outside Creepy cave"
        cave.type = 'cave'
        cave.update()
        cave.display.page_heading = "You are outside a cave called {}".format(cave.name)
        cave.display.page_image = "generic_cave_entrance.jpg"
        cave.display.paragraph = "There are many scary places to die within the cave. Have a look!"
            DON'T USE update()
        old_mans_hut = Location("Old Man's Hut", 'house')
        old_mans_hut.display.page_heading = "Old Man's Hut"
        old_mans_hut.display.page_image = 'hut.jpg'
        old_mans_hut.display.paragraph = "Nice to see you again kid. What do you need?"
        """

        if self.page_heading == self.default_heading():
            self.page_heading = "You are in {}".format(self.obj.name)
        if self.paragraph == self.default_paragraph():
            self.paragraph = "There are many places to visit within " \
                             "the {}. Have a look!".format(self.obj.type)

        self.name = self.obj.name
        self.page_image = self.obj.type.lower() + '.jpg'


"""
Allow for locations to connect to other locations.

This is done through a in/out path architecture and
is horrifically complex. See:
http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#self-referential-many-to-many-relationship
NOTE: The docs might be wrong? I'll have to test and see if this works ...
but I tried making both columns primary keys and it didn't work.
But reading the normal association_table info no primary keys are used at all.
"""
adjacent_location_association = Table(
    "adjacent_location_association",
    Base.metadata,
    # Column("id", Integer, primary_key=True),
    Column("out_adjacent_id", Integer,
           ForeignKey("location.id",
                      ondelete="SET NULL")),
    Column("in_adjacent_id", Integer,
           ForeignKey("location.id",
                      ondelete="SET NULL"))
)


class Location(Base):
    """A place that the hero can travel to or interact with.

    The main hierarchy is parent -> child, where children with
    the same parent are called 'siblings'
    General order is:
    map -> town -> blacksmith
                -> marketplace
                -> gate
                -> arena
        -> cave
        -> explorable/generic location
    """

    ALL_TYPES = [
        'map', 'explorable', 'town',
        'blacksmith', 'merchant', 'house', 'store', 'barracks', 'marketplace',
        'tavern', 'gate', 'combat', 'spar', 'arena',
        'building',
        'dungeon', 'dungeon_entrance', 'explore_dungeon'
    ]

    # http://docs.sqlalchemy.org/en/latest/orm/extensions/
    # declarative/table_config.html
    # __table_args__ = (
    #     UniqueConstraint(
    #         'parent', 'children', 'siblings', name='non_circular')
    # )
    # Need validators for children - child can't be parent or sibling
    # Need validator for parent - parent can't be child or sibling
    # Need validator for siblings - can't be parent or child, max of 6?
    # Think a hex grid

    # What does this do? ... I have no idea (marlen)
    # Parent foreign key has the ondelete="CASCADE"
    parent_id = Column(Integer, ForeignKey('location.id', ondelete="CASCADE"))
    name = Column(String(50), nullable=False, unique=True)
    url = Column(String(50))   # What does this do?
    type = Column(String(50))   # What does this do?

    terrain = Column(String(50)) # Tells the game what monsters to generate

    # Children relationship has the cascade="all, delete-orphan"
    children = relationship("Location", back_populates="parent",
                            foreign_keys="[Location.parent_id]",
                            cascade="all, delete-orphan")
    parent = relationship("Location", remote_side="[Location.id]",
                          back_populates="children",
                          foreign_keys="[Location.parent_id]")
    locations = orm.synonym('children')   # What does this do?
    encompassing_location = orm.synonym('parent')   # What does this do?

    # I have no clue about how to deal with deletes for many to many...
    _out_adjacent = relationship(
        "Location",
        secondary="adjacent_location_association",
        primaryjoin="Location.id==adjacent_location_association.c.out_adjacent_id",
        secondaryjoin="Location.id==adjacent_location_association.c.in_adjacent_id",
        backref="_in_adjacent",
        foreign_keys='[adjacent_location_association.c.out_adjacent_id, '
                     'adjacent_location_association.c.in_adjacent_id]')

    # External relationships
    # Many heroes -> one map/world. (bidirectional)
    # Don't cascade the delete for Heroes!
    heroes = relationship("Hero", back_populates='current_world',
                          foreign_keys='[Hero.map_id]')
    # Each current_location -> can be held by Many Heroes (bidirectional)
    heroes_by_current_location = relationship(
        "Hero", back_populates="current_location",
        foreign_keys='[Hero.current_location_id]')
    # Each current_city -> can be held by Many Heroes (bidirectional)
    # Current_city may be: (town, cave)
    heroes_by_city = relationship(
        "Hero", back_populates="current_city",
        foreign_keys='[Hero.city_id]')
    heroes_by_last_city = relationship(
        "Hero", back_populates="last_city",
        foreign_keys='[Hero.last_city_id]'
    )

    # One location -> one display (bi)
    display = relationship("Display", back_populates='_location',
                           uselist=False, cascade="all, delete-orphan")

    # @orm.validates('adjacent')
    # def build_adjacency(self, key, sibling):
    #     if isinstance(sibling, int):
    #         raise Exception("Use Database method add_sibling_by_id")
    #     if sibling in self.parent.children:
    #         return sibling
    #     raise Exception("Not all of these are valid siblings.")

    @hybrid_property
    def adjacent(self):
        """A list of siblings that can be traveled to.

        This is bidirectional by default but can be changed without
        too much trouble .. I think.
        """
        return set(self._out_adjacent + self._in_adjacent)

    @adjacent.setter
    def adjacent(self, values):
        """Build a path between sibling locations.

        Raise and error if the potential adjacent locations are not siblings
        of this location.
        """
        for value in values:
            if value in self.siblings:
                self._out_adjacent = values
            else:
                raise Exception(
                    "Location.name='{}' is not a valid sibling of this "
                    "location. Try checking the parents of both objects."
                    "".format(value.name)
                )

    # @orm.validates('parent', 'children')
    # def update_siblings(self, key, value):
    #     if key == 'children':
    #         value.update_sibilings()
    #     else:
    #         self.update_siblings()

    @hybrid_property
    def siblings(self):
        """The children of the parent of this location, less this location.

        NOTE: this object is not returned.
        Definition: A sibling is an object with the same parent.
        """
        siblings = []
        if self.parent:
            siblings = list(self.parent.children)
            siblings.remove(self)
        return siblings

    def get_sibling_ids(self):
        """A list of all ids of the siblings of this object.

        """
        return [sibling.id for sibling in self.siblings]

    # @update_after_validate
    @orm.validates('type')
    # @update_after_validate
    def validate_type(self, key, value):
        """Make sure that the programmer doesn't create arbitrary types.

        If you need a new type, add it to Location attribute ALL_TYPES
        """
        if value in Location.ALL_TYPES:
            return value
        else:
            raise Exception(
                "Location type '{}' doesn't exist. "
                "Valid types are: {}".format(
                    value,
                    Location.ALL_TYPES
                )
            )

    def __init__(self, name, location_type, parent=None, children=None):
        """Create a new location object that the hero can explore.

        :param location_type: e.g. map, town, store
        :param parent: the place this place is inside of
        :param children: places inside this place

        NOTE: if you set the parent attribute ... the siblings
        attribute should be populated automatically.

        NOTE2: the url is populated automatically from the parent url
        and this location's type and name.

        NOTE3: the Display is populated automatically as well but can have
        extra information added to it.

        NOTE4: Currently you can't set siblings!

        NOTE5: You need to run 'update' after changing name or type!
        """
        children = [] if children is None else children  # Prevent default argument mutation.

        self.name = name
        self.type = location_type
        self.parent = parent
        self.children = children
        self.terrain = "none"
        self.update()

    # @orm.reconstructor  # I uncommented this. I don't know why it was here.
    # I imagine it was important? But I guess not ...
    def update(self):
        """Update the derived attributes to reflect changes to the main ones.

        !IMPORTANT! This could overwrite custom attribute values incorrectly.

        ONLY RUN THIS if you change the location's:
            name or
            type
        after creation.
        e.g.
            USE update()
        cave = node_grid[2]
        cave.name = "Outside Creepy cave"
        cave.type = 'cave'
        cave.update()
        cave.display.page_heading = "You are outside a cave called {}".format(cave.name)
        cave.display.page_image = "generic_cave_entrance.jpg"
        cave.display.paragraph = "There are many scary places to die within the cave. Have a look!"
            DON'T USE update()
        old_mans_hut = Location("Old Man's Hut", 'house')
        old_mans_hut.display.page_heading = "Old Man's Hut"
        old_mans_hut.display.page_image = 'hut.jpg'
        old_mans_hut.display.paragraph = "Nice to see you again kid. What do you need?"
        """
        self.url = self.build_url()
        if self.display is None:
            self.display = Display(self)
        else:
            self.display.update()

    def build_url(self):
        """Create a url for this object with its type and name.

        Old: Create a url for this location based on the parent's url.
        """
        url_name = self.name.replace(" ", "%20")
        if self.type == "explore_dungeon":
            url_name += "/False"
        return "/{}/{}".format(self.type, url_name)
        # if self.parent is None:
        #     return "/{}/{}".format(self.type, self.name)
        # else:
        #     return self.parent.url + "/{}/{}".format(
        #         self.type, self.name)

    @hybrid_property
    def places_of_interest(self):
        """The places that are directly connected to this place.

        This is a dictionary of objects lists.
        The children are those places enclosed by this place.
        The parent is the place this place encloses.
        The adjacent is the locations that you can travel to from here.
            They are on the same relative level as this place.
        """
        places = {'children': [],
                  'adjacent': [],
                  'siblings': [],
                  'parent': None}
        children = sorted(self.children, key=lambda x: x.name)
        places['children'] = sorted(children, key=lambda x: x.type)
        places['adjacent'] = sorted(self.adjacent, key=lambda x: x.name)
        places['siblings'] = sorted(self.siblings, key=lambda x: x.name)

        if self.parent:
            places['parent'] = self.parent
        return places
