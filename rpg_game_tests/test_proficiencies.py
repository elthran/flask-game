from . import GenericTestCase

# from hero import Hero

from models.proficiencies import Proficiency, Health, Regeneration

"""
To add current directory to sys.path run like this:
NOTE: cls is an alias in .bash_alias cls="clear && printf '\033[3J'"

$ cls;python3 -m pytest -x -vv -l -s rpg_game_tests/test_ProficiencyContainer.py

s - no output capture (shows print statement output)
x - exit after first failed test
v - verbose
vv - show full length output
l - show local vars during traceback (when a test fails)
"""


class TestProficiency(GenericTestCase):
    @classmethod
    def setup_class(cls):
        db = super().setup_class()
        # Might be better for testing? To allow post mortem analysis.
        db.engine.execute("DROP TABLE `proficiency`;")
        db = super().setup_class()

        health = Health()
        regen = Regeneration()
        db.session.add(health)
        db.session.add(regen)
        db.update()

    @classmethod
    def teardown_class(cls, delete=True):
        db = super().teardown_class(delete=False)

    def setup(self):
        super().setup()
        self.profs_query = self.db.session.query(Proficiency)
        self.health_query = self.db.session.query(Health)

    def test_health_init(self):
        """Check if object is created, storeable and retrievable.
        """

        health = self.health_query.one()
        str_health = health.pretty

        self.rebuild_instance()
        health2 = self.health_query.one()
        assert str_health == health2.pretty is not None

    def test_regeneration_init(self):
        """Check if object is created, storeable and retrievable.
        """

        regeneration = self.profs_query.filter_by(type_='Regeneration').one()
        str_regeneration = regeneration.pretty
        # print("regeneration", str_regeneration)

        self.rebuild_instance()
        regeneration2 = self.profs_query.filter_by(type_='Regeneration').one()
        # print(regeneration2.pretty)
        assert str_regeneration == regeneration2.pretty is not None
