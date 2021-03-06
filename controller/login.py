import services.time
import services.validation
import models


def login_account(username, password, session):
    """Log the account in if the password matches.

    This updates the session variable.
    NOTE:
        The validate method runs a password migration script internally.
    Check for data_migration 'reset_key' ... if exists use old style
    password validation ... then convert password to new style.
    Otherwise, we are just logging in normally
    """
    if services.validation.validate(username, password):
        session['logged_in'] = True
        session['id'] = models.Account.filter_by(username=username).one().id


def login_hero(hero, session):
    check_daily_login_reward(hero)
    # End of daily login reward code (Elthran)
    session['hero_id'] = hero.id
    if not hero.game:
        hero.game = models.Game()


def check_daily_login_reward(hero):
    """Daily login reward.

    It's temporary as I am just trying to play with and learn about timestamps and whatnot.
    """
    time = str(services.time.now().date())
    if hero.last_login == "":
        hero.login_alerts += "First time logging in!"
    elif hero.last_login != time:
        reward = 3
        hero.login_alerts += "Thanks for logging in today! You earn " + str(
            reward) + " experience."
        hero.gain_experience(reward)
    hero.last_login = time
