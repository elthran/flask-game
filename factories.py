from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from pprint import pprint


def non_synchronous_relationship_mixin_factory(container_name, cls_name,
                                               attribute_and_class_names):
    """Build a mixin of relationships with varying class names.

    Example:
        scholar = relationship(
        "AuraAbility",
        primaryjoin="and_(Abilities.id==Ability.abilities_id, "
                    "Ability.name=='scholar')",
        back_populates="abilities", uselist=False)

    NOTE: the attribute name != relationship name
    i.e. 'scholar' != "AuraAbility"

    names = [('scholar', 'AuraAbility'), (...)]
    """

    dct = {}
    for name, relationship_cls_name in attribute_and_class_names:
        dct[name] = lambda cls: relationship(
            relationship_cls_name,
            primaryjoin="and_({}.id=={}.{}_id, {}.name=='{}')".format(
                container_name, cls_name, container_name.lower(),
                relationship_cls_name, name),
            back_populates=container_name.lower(), uselist=False)

        dct[name] = declared_attr(dct[name])

    return type('RelationshipMixin', (), dct)


def synchronous_relationship_mixin_factory(container_name, cls_name, names):
    """Build a Mixin of relationships for the container class.

    Example:
        health = relationship(
        "Health",
        primaryjoin="and_(Proficiencies.id==Proficiency.proficiencies_id, "
                    "Proficiency.name=='Heath')",
        back_populates="proficiencies", uselist=False)

    NOTE: the attribute name == relationship name capitalized
    i.e. 'health' -> "Heath"
    """
    dct = {}
    for false_name in names:
        attr_name = false_name.lower().replace(" ", "_")
        name = false_name.title().replace(" ", '')
        dct[attr_name] = lambda cls: relationship(
                name,
                primaryjoin="and_({}.id=={}.{}_id, {}.name=='{}')".format(
                    container_name, cls_name, container_name.lower(),
                    cls_name, name),
                back_populates=container_name.lower(), uselist=False)

        dct[attr_name] = declared_attr(dct[attr_name])

    return type('RelationshipMixin', (), dct)


def container_factory(cls_name, cls_name_singular, supers, names, namespace):
    """Build a container object that pretends to be a normal python class
    but is really a Database object.

    Example init looks like:
        def __init__(self):
            self.health = Health()
            self.sanctity = Sanctity()
    """
    dct = {
        '__tablename__': cls_name.lower(),
        'id': Column(Integer, primary_key=True),

        # Relationships
        # Hero class, One -> One
        'hero': relationship("Hero", back_populates=cls_name.lower(),
                             uselist=False)
    }

    def setup_init(self):
        """Create a generic init function with a bunch of objects.

        self.health = Health()
        self.sanctity = Sanctity()

        This may not work.
        """
        for false_name in names:
            attrib_name = false_name.lower().replace(" ", "_")
            name = false_name.title().replace(" ", '')
            setattr(self, attrib_name, namespace[name]())
    dct['__init__'] = setup_init

    RelationshipMixin = synchronous_relationship_mixin_factory(
        cls_name, cls_name_singular, names)
    attrib_names = [name.lower().replace(" ", "_") for name in names]
    IterItemsExtension = iter_items_factory(attrib_names)
    supers += (RelationshipMixin, IterItemsExtension)
    return type(cls_name, supers, dct)


def iter_items_factory(attrib_names):
    dct = {}

    def items(self):
        """Returns a list of 2-tuples

        Basically a dict.items() clone that looks like
        [(key, value), (key, value), ...]
        """
        return ((key, getattr(self, key)) for key in attrib_names)
    dct['items'] = items

    def __iter__(self):
        """Return all the attributes of this function as a list."""
        return (getattr(self, key) for key in attrib_names)
    dct['__iter__'] = __iter__

    return type("IterItemsExtension", (), dct)


class PolymorphicIdentityOnClassNameMixin:
    """Set the polymorphic identity of an object to its class name."""
    @declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__}