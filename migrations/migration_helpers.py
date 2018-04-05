def truncate_table(name, engine):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("TRUNCATE TABLE `{}`;".format(name))
    engine.execute("SET FOREIGN_KEY_CHECKS=1;")


def set_all(old, new):
    """Migrate the data from one object to another."""
    for key in old.keys():
        try:
            setattr(new, key, getattr(old, key))
        except AttributeError:
            pass