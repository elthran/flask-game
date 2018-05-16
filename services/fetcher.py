import pdb

import sqlalchemy as sa

import models


def get_user_id(username):
    """Return the id of the user by username from the User's table.

    """
    user = models.Account.filter_by(username=username).first()
    if user is None:
        return None
    return user.id


def fetch_sorted_heroes(attribute, descending=False):
    """Return a list of all heroes sorted by attribute.

    :param attribute: an attribute of the Hero object.
    :param descending: the desired direction for the sorted list
        ascending/descending
    :return: list sorted by attribute.

    NOTE: this code is not very flexible. If you tried to access
    hero.inventory.id it would not work.

    A more generic function might do:
    extended_attr, attr = attribute.split('.')
    join_attr = getattr(Hero, extended_attr)?
    self.session.query(Hero).join(join_attr).order_by(attr).all()

    NOTE: to order by descending:
    order_by(attribute + " desc")
    or
    order_by(desc(attribute))

    Former does not work for numbers

    https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
    """
    query = models.Hero.query()
    if '.' not in attribute:
        if descending:
            return query.order_by(sa.desc(attribute)).all()
        return query.order_by(attribute).all()

    all_attrs = attribute.split('.')
    sort_attr = all_attrs.pop()  # Remove last value for use as sort key
    try:
        join_attr = getattr(models.Hero, all_attrs.pop(0))  # remove first attr
        for extended_attr in all_attrs:
            join_attr = getattr(join_attr, extended_attr)
    except AttributeError:
        raise Exception("Trying to access an attribute that this code"
                        " does not accommodate.")
    joined_query = query.join(join_attr)
    heroes = []
    if descending:
        heroes = joined_query.order_by(sa.desc(sort_attr)).all()
    else:
        heroes = joined_query.order_by(sort_attr).all()
    return heroes if heroes else models.Hero.all()


def fetch_hero_by_username(username, character_name=None):
    """Return hero objected based on username_or_id and character_name.

    If no character_name is passed just return first hero.
    Note: Providing a username when you have the hero/character id is
    redundant.
    """
    user = models.Account.filter_by(username=username)
    if character_name is not None:
        return models.Hero.filter_by(
            user_id=user.id, character_name=character_name).one()
    return user.heroes[0]
