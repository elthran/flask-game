"""
I have as of January 1st, 2017 come across a problem where I could not
store python objects conveniently in my version of the database.

To solve this I am rewriting the whole thing with SQLAlchemy ORM.
Mainly using the tutorial at:
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

This class is imported first and can be used to add generic methods to all
database objects. Like a __str__ function that I can actually read.
"""
import functools
import operator

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.orderinglist
import sqlalchemy.orm.collections
import sqlalchemy.ext.declarative

import services


def attribute_mapped_dict_hybrid(key):
    """A dictionary-based collection type with attribute-based keying.

    See http://docs.sqlalchemy.org/en/latest/orm/collections.html#sqlalchemy.orm.collections.attribute_mapped_collection
    Returns a MappedCollection factory with a keying based on the ‘attr_name’
    attribute of entities in the collection, where attr_name is the string
    name of the attribute.

    The key value must be immutable for the lifetime of the object.
    You can not, for example, map on foreign key values if those key values
    will change during the session, i.e. from None to a database-assigned
    integer after a session flush.

    As far as I can see ... this shouldn't work at all. Clearly it does.
    Wish I understood how.
    """
    return lambda: DictHybrid(key_attr=key)


class DictHybrid(sa.orm.collections.MappedCollection):
    """A Python object that acts like a JS one.

    You can assign values via attribute or via key.
    e.g.
        obj.foo = obj['foo'] all but really special keys :P

    The attribute_mapped_dict_hybrid
    allows me to build a factory for this class similar to
    sqlalchemy.orm.collections.attribute_mapped_collection(attr_name)

    Defaults to keying on object 'type'.
    """

    invalid_keys = {'__emulates__', 'id', 'keyfunc', '_sa_adapter'}

    def __init__(self, *args, key_attr='type', **kwargs):
        """Create a new DictHybrid with keying on 'type'.

        This is mostly cloned code I don't understand. I hope it doesn't
        break. I have a test suite so if it does break I should be able
        to come up with a solid fix.

        You can create a new internal dict by passing in a dict
        or by by passing tuples of key, value pairs.
        """
        super().__init__(operator.attrgetter(key_attr))
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    @sa.orm.collections.collection.internally_instrumented
    def __setitem__(self, key, value, _sa_initiator=None):
        """Instrumented version of dict setitem.

        I don't know how this works."""
        # noinspection PyArgumentList
        super().__setitem__(key, value, _sa_initiator)

    @sa.orm.collections.collection.internally_instrumented
    def __delitem__(self, key, _sa_initiator=None):
        """Instrumented version of dict delitem.

        I don't know how this works."""
        # noinspection PyArgumentList
        super().__delitem__(key, _sa_initiator)

    def __getattr__(self, attr):
        """Overloaded getattr method with custom handling.

        Any attribute that isn't in {'__emulates__', 'id', 'keyfunc'}
        gets called as a key to the dictionary.

        I'm not sure why these aren't ... how it works though is:

        self.id ... returns self.id like a normal object.
        self.some_key ... returns self[some_key] as though self was a dict.
        """
        if attr not in self.invalid_keys:
            return self[attr]
        return self.get(attr)

    @sa.orm.collections.collection.internally_instrumented
    def __setattr__(self, key, _sa_initiator=None):
        """Overloaded and Instrumented setattr method with custom handling.

        Any attribute that isn't in {'keyfunc', '_sa_adapter'}
        gets added as a key to the dictionary.

        I'm not sure why these aren't ... how it works though is:

        self.keyfunc = somefunc ... sets self.keyfunc like a normal object.
        self.some_key ... sets self[some_key] as though self was a dict.
        """
        if key not in self.invalid_keys:
            self.__setitem__(key, _sa_initiator)
        super().__setattr__(key, _sa_initiator)

    def __delattr__(self, item):
        """Makes object delatter act like dict delitem.

        del self.some_key ... does del self[some_key]
        as though self was a dict.
        """
        self.__delitem__(item)

    def sorted_keys(self):
        """Returns the the dictionary keys of self as a sorted frozenset.

        It is frozen so it can be used in a cache function.
        I don't really know how this works ... but it should allow repeated
        calls to sorted_keys to be very fast.
        """
        keys = self._key_sort(frozenset(self.keys()))
        return (x for x in sorted(keys))

    @staticmethod
    @functools.lru_cache(maxsize=16)
    def _key_sort(keys):
        """Cached sort method.

        Cache uses frozenset so it should be order independent?
        """
        return sorted(keys)

    def __iter__(self):
        """Return all the values (sorted by keys) of this dict as an iterator.

        If you want the normal dict method for __iter__ do:
        self.keys() instead. This will return unsorted keys.
        """

        return (self[key] for key in self.sorted_keys())

    def sorted_items(self):
        """Return the keys and values sorted by keys."""
        return ((k, self[k]) for k in self.sorted_keys())


class Base(object):
    def get_mro_till_base(self):
        """Return the MRO until you hit base."""

    def get_mro_keys(self):
        """Return all attributes of objects in MRO

        All non-base objects in inheritance path.
        Remove <class 'sqlalchemy.ext.declarative.api.Base'>,
        <class 'object'> as these are the last two objects in the MRO
        """
        hierarchy_keys = set()

        hierarchy = type(self).__mro__
        max_index = hierarchy.index(Base)
        hierarchy = hierarchy[1:max_index]

        for obj in hierarchy:
            if "Mixin" in obj.__name__:
                hierarchy_keys |= set(vars(obj).keys())
            else:
                hierarchy_keys |= set(vars(obj).keys()) \
                              - set(obj.__mapper__.relationships.keys())

        # Remove private variables and id keys to prevent weird recursion
        # and redundancy.
        hierarchy_keys -= set(
            [key for key in hierarchy_keys if key.startswith('_')]
        )  # ? or 'id' in key])

        return hierarchy_keys

    def get_all_atts(self):
        if self.__class__ == Base:
            return set()
        # noinspection PyUnresolvedReferences
        data = set(vars(self).keys()) | \
            set(self.__table__.columns.keys()) | \
            set(self.__mapper__.relationships.keys())

        data.discard('_sa_instance_state')

        hierarchy_keys = set()
        try:
            hierarchy_keys = self.get_mro_keys()
        except IndexError:
            pass  # This is the Base class and has no useful MRO.

        data |= hierarchy_keys

        # Remove special hoisted variable that I add in Mixin.
        # I don't know why it even exits in the MRO.
        data.discard('session')

        # Remove weird SQLAlchemy var available to higher class but no
        # lower ones.
        keys_to_remove = set()
        for key in data:
            try:
                getattr(self, key)
            except AttributeError:
                # Because of single table inheritance ... invalid attributes
                # can end up inside of the object hierarchy list.
                keys_to_remove.add(key)
        data -= keys_to_remove

        # Don't print the object's methods.
        data -= set([e for e in data
                     if "method" in repr(type(getattr(self, e)))])

        return data

    def data_to_string(self, data):
        for key in sorted(data):
            value = getattr(self, key)
            if value and (type(value) == sa.orm.collections.InstrumentedList or
                          type(value) ==
                          sa.ext.orderinglist.OrderingList):
                value = '[' + ', '.join(
                    "<{}(id={})>".format(e.__class__.__name__, e.id)
                    for e in value) + ']'
            elif value and type(value) == sa.orm.collections.MappedCollection:
                value = "{" + ', '.join(
                    "{}: <{}(id={})>".format(k, v.__class__.__name__, v.id)
                    for k, v in value.items()) + '}'
            # This if/try is a way to print ONE to ONE relationship objects
            # without infinite recursion.
            elif value:
                try:
                    # Dummy call to test if value is a Database object.
                    # value._sa_instance_state  # temporarily removed.
                    value = "<{}(id={})>".format(
                        value.__class__.__name__, value.id)
                except AttributeError:
                    pass  # The object is not a databse object.
            yield '{}={}'.format(key, repr(value))

    def __str__(self):
        """Return string data about a Database object.

        Note: prints lists as list of ids.
        Note2: key.lstrip('_') accesses _attributes as attributes due to my
        convention of using _value, @hybrid_property of value, @value.setter.

        I don't understand why I need all of these ... only that each one seems
        to hold slightly different data than the others with some overlap.

        Not3: super class variables like 'type' and 'name' don't exist in
        WorldMap until they are referenced as they are declared in Map...?
        I called super to fix this ... but it may only allow ONE level of
        superclassing. Multi-level superclasses will probably fail.
        """

        data = self.get_all_atts()
        data_str_gen = self.data_to_string(data)
        return "<{}({})>".format(
            self.__class__.__name__, ', '.join(data_str_gen))

    def pprint(self):
        """Multi-line print of a database object -> good for object diff.

        Basically a string_of clone but one variable per line.
        """

        data = self.get_all_atts()

        print("\n\n<{}(".format(self.__class__.__name__))
        for line in self.data_to_string(data):
                print(line)
        print(")>\n")

    @property
    def pretty(self):
        data = self.get_all_atts()

        lines = (line for line in self.data_to_string(data))
        return "\n<{}(\n{}\n)>\n".format(
            self.__class__.__name__, '\n'.join(lines))

    @staticmethod
    def pretty_list(obj_list, key='id'):
        """Build a human readable string version of a list of objects.

        :param obj_list: The list of Base objects to print.
        :param key: and attribute of the each object to print by.
        :return: A nicely formatted string version of the list.

        Mainly used for print 'InstrumentedList' that most hated of objects.
        NOTE: the list is sorted! If the key can't be sorted then this will
        fail.
        """
        return '[' + ', '.join(
            '{}.{}={}'.format(
                obj.__class__.__name__,
                key,
                repr(getattr(obj, key))
            ) for obj in sorted(
                obj_list,
                key=lambda x, k=key: getattr(x, k))
        ) + ']'

    def is_equal(self, other):
        """Test if two database objects are equal.

        hero.is_equal(hero) vs. str(hero) == str(hero)
        is_equal is 0.3 seconds faster over 1000 iterations than str == str.
        So is_equal is not that useful. I would like it if it was 5-10 times
        faster.
        """
        data = self.get_all_atts()
        other_data = other.get_all_atts()

        if data != other_data:
            return False

        if self.__class__.__name__ != other.__class__.__name__:
            return False

        for key in data:
            value = getattr(self, key)
            other_value = getattr(other, key)
            if value != other_value:
                return False
        return True

    Session = None

    @classmethod
    def query(cls):
        with services.session_helpers.session_scope(cls.Session) as session:
            return session.query(cls)

    @classmethod
    def first(cls):
        return cls.query().first()

    @classmethod
    def get(cls, id_):
        return cls.query().get(id_)

    def save(self):
        session = self._sa_instance_state.session
        try:
            session.commit()
        except:
            session.rollback()
            raise


# Initialize SQLAlchemy base class.
convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(column_0_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}
metadata = sqlalchemy.MetaData(naming_convention=convention)
Base = sa.ext.declarative.declarative_base(cls=Base, metadata=metadata)
# This used a class factory to build a class called base in the local
# context. Why I can't just import Base I have no idea.
# And I know how to use it.


# class BaseListElement(Base):
#     """Stores list objects in database.
#
#     To implement:
#     1. add line in this class:
#         parent_table_name_id = Column(Integer,
#             ForeignKey('parent_table_name.id'))
#     2. add line in foreign class: _my_list = relationship("BaseListElement")
#     3. add method to foreign class:
#     @hybrid_property
#     def my_list(self):
#         '''Return a list of elements.
#         '''
#         return [element.value for element in self._my_list]
#
#     4. add method to foreign class:
#     @my_list.setter
#     def my_list(self, values):
#         '''Create list of BaseListElement objects.
#         '''
#         self._my_list = [BaseListElement(value) for value in values]
#
#     See Location class for example implementation.
#     5. Probably a better way using decorators ...?
#     """
#     __tablename__ = "base_list"
#     id = Column(Integer, primary_key=True)
#     int_value = Column(Integer)
#     str_value = Column(String(50))
#
#     # dict_id_keys = Column(Integer, ForeignKey('base_dict.id',
#     #                                           ondelete="CASCADE"))
#     # dict_id_values = Column(Integer, ForeignKey('base_dict.id',
#     #                                             ondelete="CASCADE"))
#
#     def __init__(self, value):
#         """Build BaseListElement from value.
#         """
#         self.value = value
#
#     @hybrid_property
#     def value(self):
#         """Return value of list element.
#
#         Can be string or integer.
#         """
#         return self.int_value or self.str_value
#
#     @value.setter
#     def value(self, value):
#         """Assign value to appropriate column.
#
#         Currently implements the strings and integers.
#         """
#         if isinstance(value, str):
#             self.str_value = value
#         elif isinstance(value, int):
#             self.int_value = value
#         else:
#             raise "TypeError: BaseListElement does not accept " \
#                 "type '{}':".format(type(value))
#
#     def __str__(self):
#         """Return pretty string version of data.
#         """
#         return repr(self.value)
            

# class BaseItem(Base):
#     __tablename__ = 'base_item'
#     id = Column(Integer, primary_key=True)
#     str_key = Column(String(50))
#     int_key = Column(Integer)
#     str_value = Column(String(50))
#     int_value = Column(Integer)
#
#     base_dict_id = Column(Integer, ForeignKey('base_dict.id',
#                                               ondelete="CASCADE"))
#     def __init__(self, key, value):
#         self.key = key
#         self.value = value
#
#     @hybrid_property
#     def key(self):
#         """Return key of appropriate type.
#
#         Can be string or integer.
#         """
#         return self.int_key or self.str_key
#
#
#     @key.setter
#     def key(self, key):
#         """Assign key to appropriate typed column.
#
#         Currently implements strings and integers.
#         """
#         if type(key) is type(str()):
#             self.str_key = key
#         elif type(key) is type(int()):
#             self.int_key = key
#         else:
#             raise "TypeError: BaseItem does not accept type '{}':".format(type(key))
#
#     @hybrid_property
#     def value(self):
#         """Return value of appropriate type.
#
#         Can be string or integer.
#         """
#         return self.int_value or self.str_value
#
#
#     @value.setter
#     def value(self, value):
#         """Assign value to appropriate typed column.
#
#         Currently implements strings and integers.
#         """
#         if type(value) is type(str()):
#             self.str_value = value
#         elif type(value) is type(int()):
#             self.int_value = value
#         else:
#             raise "TypeError: BaseItem does not accept type '{}':".format(type(value))
#
#
# class BaseDict(Base):
#     """Mimic a dictionary but be storable in a database.
#
#
#     """
#     __tablename__ = "base_dict"
#     id = Column(Integer, primary_key=True)
#
#     base_items = relationship("BaseItem", cascade="all, delete-orphan")
#
#     def __init__(self, d={}):
#         """Build a list of items and a matching dictionary.
#
#         The dictionary should act as a hash table/index for the list.
#         """
#         self.d_items = {}
#         for key in d:
#             self.d_items[key] = BaseItem(key, d[key])
#             self.base_items.append(self.d_items[key])
#             assert self.d_items[key] is self.base_items[-1]
#
#
#     @orm.reconstructor
#     def rebuild_d_items(self):
#         self.d_items = {}
#         for item in self.base_items:
#             self.d_items[item.key] = item
#
#
#     def remove(self, key):
#         base_item = self.d_items.pop(key, None)
#         if base_item:
#             self.base_items.remove(base_item)
#
#
#     def __getitem__(self, key):
#         """Get value of key using a dict key name or list index.
#         """
#
#         return self.d_items[key].value
#
#
#     def __setitem__(self, key, value):
#         """Change value at key or create key with value.
#         """
#         try:
#             self.d_items[key].value = value
#         except KeyError as ex:
#             self.add(key, value)
#
#     def add(self, key, value):
#         """Add an element to the end of the dictionary.
#
#         """
#         self.d_items[key] = BaseItem(key, value)
#         self.base_items.append(self.d_items[key])
#
#     def keys(self):
#         return (item.key for item in self.base_items)
#
#     def values(self):
#         return (item.value for item in self.base_items)
#
#     def items(self):
#         return ((item.key, item.value) for item in self.base_items)
#
#     # def __iter__(self):
#         # return (key for key in self.d_items)
#
#     def __str__(self):
#         """Return pretty string version of data.
#
#         """
#
#         data = ', '.join(['{}: {}'.format(repr(item.key), repr(item.value))
#             for item in self.base_items])
#         return "BaseDict{" + data + "}"


# class Map(dict):
#     """
#     Example:
#     m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
#
#     Should allow a dictionary to behave like an object.
#     So you can do either ->
#     map['some_key']
#     OR
#     map.some_key
#
#     NOTE: the iterator function is not normal for dictionaries.
#     It returns .values() (ordered) not .keys() (random)
#     """
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for arg in args:
#             if isinstance(arg, dict):
#                 for k, v in arg.items():
#                     self[k] = v
#
#         if kwargs:
#             for k, v in kwargs.items():
#                 self[k] = v
#
#         self.sorted_keys = sorted(self.keys())
#
#     def __getattr__(self, attr):
#         return self.get(attr)
#
#     def __setattr__(self, key, value):
#         self.__setitem__(key, value)
#
#     def __setitem__(self, key, value):
#         super(Map, self).__setitem__(key, value)
#         self.__dict__.update({key: value})
#
#     def __delattr__(self, item):
#         self.__delitem__(item)
#
#     def __delitem__(self, key):
#         super(Map, self).__delitem__(key)
#         del self.__dict__[key]
#
#     def __iter__(self):
#         """Return all the values (sorted by key) of this Map as an iterator.
#
#         Overrides default of returning .keys() (unsorted).
#         Now returns .values() (sorted by .keys())
#         """
#         if self.sorted_keys:
#             # pdb.set_trace()
#             return (self[key] for key in self.sorted_keys)
#         self.sorted_keys = sorted(self.keys())
#         return (self[key] for key in self.sorted_keys)