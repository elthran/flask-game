import pdb
from pprint import pprint

from functools import wraps
from flask import render_template_string, jsonify


def set_notification_active(f):
    """Tack data onto a response that activates the notification button.

    This is a decorator that will be used to un-hide the
    globalNotificationButton.

    Add the isNotice=true/false into any response.
    If the response is a json type then it adds it to the JSON object
        (at the front, but as this is a dictionary it isn't that important).
    If the response is a string it tacks it on the end as a
        keyword=variable pair.
    """

    @wraps(f)
    def wrap_set_notice_active(hero, *args, **kwargs):
        response = f(hero, *args, **kwargs)
        print("Using the set notification active code!")
        notice = str(bool(hero.journal.notification)).lower()
        try:
            new_data = b'\n  "isNotice": ' + notice.encode() + b', '
            response.data = b"{" + new_data + response.data[1:]
        except AttributeError:
            # Convert the string from binary.
            response += "&&isNotice={}".format(notice)
        return response
    return wrap_set_notice_active


# TODO: update documentation!
class Command:
    """Run a list of html update commands based on the string cmd.
    
    Usage:
    # 'app.py'
    from commands import Command
    NEW STYLE
    @app.route('/command/<cmd>')
    command_function = Command.cmd_functions(cmd)
        if request.method == 'POST' and request.is_json:
            data = request.get_json()
            response = command_function(hero, database, data=data,
                                            engine=engine)
        return response

    # 'commands.py'
    @staticmethod
    def buy(hero, database, data, engine):
        item_id = data['id']
        location = data['location']
        item = database.create_item(item_id)
        if hero.gold >= item.buy_price:
            hero.inventory.add_item(item)
            hero.gold -= item.buy_price
            engine.spawn(
                'buy_event',
                hero,
                description="{} buys a/an {}.".format(hero.name, item.name)
            )
            return jsonify(
                message="Purchased: {}: id={}".format(item.name, item.id),
                heroGold=hero.gold)
        return jsonify(error="Not enough gold to buy '{}'!".format(item.name))

    # 'store.html'
    <button onclick="sendToPy(
        event,
        itemPurchasedPopup, 'buy', {'id': {{ item.id }}});">Buy</button>
    NOTE: the data is sent as JSON

    # 'script.js'
    See:
    function sendToPy(event, callback, cmd, data, preProcess, url) {
    "use strict";
    var element = event.target;
    ...
    if (cmd) {
        url = "/command/" + cmd;
    } else if (!cmd && !url) {
        // if url is blank use url of page
        url = window.location.pathname;
    }

    // Normal data processing is object form.
    // Must return a JSON object - no I can't check for this.
    if (preProcess) {
        data = preProcess(element);
    }

    // If you send a simple string location won't be added.
    // If you send (hopefully) some JSON the location parameter will be added.
    if (typeof data !== "string") {
        // If there is some (JSON type data) add in the location variable.
        data.location = window.location.pathname;
    }

    postJSON(url, data, callback);
    ...
    }

    #NOTES:
        Go to the real code for most up to date documentation and examples.

    -preProcess is the name of whatever JS function you want to use
    to extract the data from the HTML. See 'scripts.js > getIdsFromCheckboxes'
    See: 'inbox.html'
    <input type="submit" name="delete" form="messageForm" value="DELETE"
    onclick="return sendToPy(
        event, updateMessageTable, null, null, getIdsFromCheckboxes);"/>



    OLD STYLE
    @app.route('/command/<cmd>')
    def command(cmd=None):
        try:
            # command_function = getattr(Command, <cmd>)
            # response = command_function(hero, database,
            #   javascript_kwargs_from_html)
            command_function = Command.cmd_functions(cmd)
            try:
                response = command_function(hero, database=database,
                                            arg_dict=request.args)
                # pdb.set_trace()
                return response
            except Exception as ex:
                raise ex
        except AttributeError:
            print("Warning: Using old code for command: '{}'".format(cmd))
            print("You need to write a static function called '{}' in "
                  "commands.py in the Command class.".format(cmd))
            # Look in the not yet refactored list of if statements ...

    This should call the function and execute it in the Command class.

    The format for a button is:
    -<button data-py-function="consume" data="{{ item.id }}"
    data-js-callback="javascript_consume"></button>
    -Where data-py-function means this object runs command code.
    -Where data is the python object's database id. Or any other data necessary.
    -Where data-py-function="consume" is the name of the Python
        method/function to run (in commands.py).
    -Where data-js-callback="javascript_consume" is the name of a JavaScript
        function that accepts data as a return value from the Python
        function defined in data-py-function="..".
        NOTE: This function runs after the python code returns a response.
        "onClick" does not. It runs first/or independently?

    Usage:
        Use the python functions if you need to change the database or hero
        object.
        Use the JS functions if you need to update the website data.
            e.g. buy and item ... send it to the python code with the item's id
        Drop hero's gold ... add item to inventory.
        Then send back the confirmation to the JS function and update the hero's
        gold value on the website and some kind of visual feedback for the purchase.

    **Alternative JavaScript function call:
    -<button data-py-function="consume" data="{{ item.id }}"
        onClick="remove(this)"></button>
    -Where onClick is a local function to run. "this" is the button object itself.


    NOTES:
        1. The data attribute can be used to send more complex data.
        2. The onClick function could be called by the XHTTP script at the bottom of static/layout.html
            it could then respond to changes in the database. It may need to.
        3. data-* can be anything for any specific values. Might be needed in the
            future for expansions.
    """

    @staticmethod
    @set_notification_active
    def buy(hero, database, data, engine):
        """Allow the user to buy items from the Blacksmith.

        Returns an error if the character doesn't have enough gold.
        """
        item_id = data['id']
        location = data['location']
        item = database.create_item(item_id)
        if hero.gold >= item.buy_price:
            hero.inventory.add_item(item)
            hero.gold -= item.buy_price
            engine.spawn(
                'buy_event',
                hero,
                description="{} buys a/an {}.".format(hero.name, item.name)
            )
            return jsonify(
                message="Purchased: {}: id={}".format(item.name, item.id),
                heroGold=hero.gold)
        return jsonify(error="Not enough gold to buy '{}'!".format(item.name))

    @staticmethod
    def consume(hero, database, arg_dict, **kwargs):
        """Apply the effect of a potion when the hero consumes it.

        NOTE: the item is then deleted from the hero's inventory and the database.
        """
        item_id = arg_dict.get('data', None, type=int)
        item = database.get_item_by_id(item_id)
        item.apply_effect(hero)
        database.delete_item(item_id)
        return "success"

    @staticmethod
    @set_notification_active
    def toggle_equip(hero, database, data, engine):
        item_id = data['id']
        item = database.get_item_by_id(item_id)
        len_rings = None
        if item.type == "Ring":
            lowest_empty_slot = hero.inventory.get_lowest_empty_ring_pos()
            primary_slot_type = "finger-{}".format(lowest_empty_slot)
        else:
            primary_slot_type = hero.inventory.\
                js_slots_used_by_item_type[item.type][0]
        if item.equipped:
            hero.inventory.unequip(item)
            hero.refresh_character()
            engine.spawn(
                'unequip_event',
                hero,
                description="{} unequips a/an {}.".format(hero.name, item.name)
            )
            return jsonify(primarySlotType=primary_slot_type,
                           command="unequip")
        else:
            ids_to_unequip = hero.inventory.equip(item)
            hero.refresh_character()
            engine.spawn(
                'equip_event',
                hero,
                description="{} equips a/an {}.".format(hero.name, item.name)
            )
            return jsonify(primarySlotType=primary_slot_type,
                           command="equip", idsToUnequip=ids_to_unequip)

    @staticmethod
    def cast_spell(hero, database, arg_dict, **kwargs):
        ability_id = arg_dict.get('data', None, type=int)
        ability = database.get_ability_by_id(ability_id)
        ability.cast(hero)
        return "success"

    @staticmethod
    def change_attribute_tooltip(hero, database, arg_dict, **kwargs):
        # I want to pass in the actual attribute here instead of the description. That way I can assign the attribute name and description to the tooltip.
        # Unfortunately, I don't know how to pull the attribute object from the database. I need a get_attribute_by_name() function in database.py
        tooltip = arg_dict.get('data', None, type=str)
        return "{}".format(tooltip)

    @staticmethod
    def update_attribute(hero, database, arg_dict, **kwargs):
        attribute_id = arg_dict.get('data', None, type=int)
        if hero.attribute_points <= 0:
            return "error: no attribute points"
        for attribute in hero.attributes:
            if attribute.id == attribute_id:
                attribute.level += 1
        hero.attribute_points -= 1
        if hero.attribute_points == 0:
            return "hide_all".format()
        return "success".format()

    @staticmethod
    def update_proficiency(hero, database, data, **kwargs):
        """Raise proficiency level, decrement proficiency_points.

        Return status of: success, hide_all, hide_this.
        "success" means hide none ... maybe I should call it that instead?
        """
        proficiency_id = data['id']
        proficiency = database.get_proficiency_by_id(proficiency_id)

        # Defensive coding: command buttons should be hidden by JavaScript
        # when no longer valid due to the return values of this function.
        # If for some reason they are still clickable return error to
        # JS console.
        if hero.proficiency_points <= 0 or proficiency.is_max_level:
            return "error: no proficiency_points or proficiency is at max level."

        hero.proficiency_points -= 1
        proficiency.level_up()
        return jsonify(tooltip=proficiency.tooltip,
                       pointsRemaining=hero.proficiency_points,
                       level=proficiency.level)

    @staticmethod
    def change_proficiency_tooltip(hero, database, data, **kwargs):
        tooltip_id = data['id']
        proficiency = database.get_proficiency_by_id(tooltip_id)
        return jsonify(tooltip=proficiency.tooltip)

    @staticmethod
    def change_ability_tooltip(hero, database, data, **kwargs):
        tooltip_id = data['id']
        ability = database.get_ability_by_id(tooltip_id)
        return jsonify(tooltip=ability.tooltip)

    @staticmethod
    def update_ability(hero, database, data, **kwargs):
        ability_id = data['id']
        ability = database.get_ability_by_id(ability_id)
        if hero.basic_ability_points <= 0 or ability.is_max_level():
            return "error: no ability_points or ability is at max level."
        hero.basic_ability_points -= 1
        ability.level += 1 # Should be a level_up() function instead?
        return jsonify(tooltip=ability.tooltip,
                       pointsRemaining=hero.basic_ability_points,
                       level=ability.level)

    @staticmethod
    def update_specialization(hero, database, data, **kwargs):
        choice = data['name']
        spec = data['spec']
        print("The hero's " + spec + " should be " + choice)
        # PLEASE MAKE THE ABOVE PRINT STATEMENT TRUE!!!!!!!!!!!!!!!!!!!!!!!
        #specialization = database.get_object_by_name("Specialization", choice)
        #setattr(hero.specializations, choice, specialization)
        return jsonify(tooltip="Temp", pointsRemaining=0, level=0)

    # This should be combined with function below when I know how to pass a path.id
    @staticmethod
    def change_path_tooltip(hero, database, arg_dict, **kwargs):
        choice = arg_dict.get('data', None, type=str)
        return "{}&&{}".format(choice, "50gold")

    @staticmethod
    def change_quest_tooltip(hero, database, arg_dict, **kwargs):
        quest_id = arg_dict.get('data', None, type=int)
        quest = database.get_object_by_id("Quest", quest_id)
        return "{}&&{}".format(quest.description, quest.reward_experience)

    @staticmethod
    def choose_background(hero, database, arg_dict, **kwargs):
        background = arg_dict.get('data', None, type=str)
        hero.background = background
        if hero.background == "Barbarian":
            hero.attributes.brawn.level += 1
        elif hero.background == "Missionary":
            hero.attributes.intellect.level += 1
        return "success".format()

    @staticmethod
    def get_message_content_and_sender_by_id(hero, database, arg_dict, **kwargs):
        """Return the content of a message based on its id."""
        id = arg_dict.get('data', None, type=int)
        message = database.get_object_by_id("Message", id)
        message.unread = False #Marks the message as having been seen by the receiver
        return "{}&&{}".format(message.content, message.sender.user.username)

    @staticmethod
    def send_notification_data(hero, database, data, *args, **kwargs):
        """Return the quest notification data as a JSON

        Maybe this should be a decorator?
        It would wrap any function and tack the "activate notification button"
        function and data on the end of any Json capable response?
        """

        header_template = """
            {% if quest_notification.total_reward %}
                <h1>{{ quest_notification.name }}</h1>
            {% else %}
                <h1>{{ quest_notification.name }}</h1>
                <h2>Stage: {{ quest_notification.stage }} / {{ quest_notification.stages }}</h2>
            {% endif %}
        """
        body_template = """
            {% if quest_notification.total_reward %}
                <h2>Completed!</h2>
            {% else %}
                <h2>Current Step:</h2>
                <h3>{{ quest_notification.current_quest.name }}</h3>
            {% endif %}
        """
        footer_template = """
            {% if quest_notification.total_reward %}
                <h3>Total reward: {{ quest_notification.total_reward }}xp</h3>
            {% else %}
                <h3>Reward: {{ quest_notification.current_quest.reward }}xp</h3>
            {% endif %}
        """

        # notice = hero.journal.quest_notification
        notice = hero.journal.notification.get_description()

        header = render_template_string(header_template,
                                        quest_notification=notice)
        body = render_template_string(body_template,
                                      quest_notification=notice)
        footer = render_template_string(footer_template,
                                        quest_notification=notice)

        data = jsonify(header=header, body=body, footer=footer)

        print("Sending Notice content to JS.")
        pprint(data)

        # Clear quest notification
        hero.journal.notification = None
        return data

    # @staticmethod
    # def clear_quest_notification(hero, database, arg_dict, **kwargs):
    #     id = arg_dict.get('data', None, type=int)
    #     hero.journal.quest_notification = None
    #     return "success"

    @staticmethod
    def temp_temp(hero, database, arg_dict, **kwargs):
        """Jacobs function which does nothing. I seem to need to have A function, so sometimes I run this blank function."""
        return "success"

    # @staticmethod
    # def send_message_to_user_by_username(hero, database, arg_dict, **kwargs):
    #     """Return the content of a message based on its id."""
    #     username = arg_dict.get('data', None, type=str)
    #     print ("username is: ", username)
    #     print("Attempting to generate a reply. Getting user now.")
    #     receiver = database.get_user_by_username(username)
    #     print("Generating reply to user: ", receiver.username)
    #     hero.user.inbox.send_message(receiver, "TEST REPLY!", "55:55:55")
    #     print ("Reply is successful. Message sent.")
    #     print("Sending message content back to JS.")
    #     return "message replied to successfully"

    @staticmethod
    def cmd_functions(name):
        """Use to refer to return a function from string of its name.
        
        Getattr wrapper ...
        """
        return getattr(Command, name)
