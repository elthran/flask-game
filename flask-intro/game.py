#//////////////////////////////////////////////////////////////////////////////#
#                                                                              #
#  Author: Elthran B, Jimmy Zhang                                              #
#  Email : jimmy.gnahz@gmail.com                                               #
#                                                                              #
#//////////////////////////////////////////////////////////////////////////////#

import math
from flask import request
from items import *
from bestiary import *
from abilities import *

# function used in '/level_up'
def convert_input(x):
    try:
        x = int(x)
    except:
        x = 0
    return x

class Game(object):
    def __init__(self, hero):
        self.hero = hero
        self.has_enemy = False

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.has_enemy = True

class Hero(object):
    def __init__(self, user_name="Unknown"):
        self.user_name = user_name
        self.name = "Unknown"
        self.starting_class = "None"
        self.current_exp = 0
        self.max_exp = 10
        self.level = 1
        self.attribute_points = 0
        self.strength = 1
        self.endurance = 1
        self.vitality = 1
        self.agility = 1
        self.dexterity = 1
        self.devotion = 1
        self.resistance = 1
        self.wisdom = 1
        self.charm = 1
        self.instinct = 1
        self.equipped_items = []
        self.inventory = []
        self.abilities = []
        self.gold = 500
        
    # Sets damage
    def update_secondary_attributes(self):
        self.min_damage = self.strength + self.dexterity
        self.max_damage = (2 * self.strength) + self.dexterity
        self.attack_speed = ((2 * self.agility) + self.dexterity) / 5
        self.attack_accuracy = round(((5 * self.dexterity) + (3 * self.agility)) ** 1.5, 2)
        self.defence_modifier = (2 * self.resistance + self.endurance)/ 2
        self.dodge_chance = (self.agility + self.dexterity) / 2
        self.max_hp = (5 * self.vitality) + self.endurance
        self.max_mp = self.wisdom + self.devotion
        self.current_mp = self.max_mp
        self.carrying_capacity = (3 * self.endurance) + (2 * self.strength)
        for ability in self.abilities:
            ability.update_stats()
        for item in self.equipped_items:
            item.update_stats()
        self.current_hp = self.max_hp

    # updates field variables when hero levels up
    def level_up(self, attribute_points, current_exp, max_exp):
        if self.current_exp < self.max_exp:
            return
        self.current_exp = 0
        self.max_exp = math.floor(1.5 * self.max_exp)
        self.attribute_points += 3
        self.level += 1
        self.update_secondary_attributes()

    def __repr__(self):
        return "\nName: %s" % (self.name)

# Temporary Function to create a random hero
def create_random_hero():
    myHero = Hero()
    clothes = [Garment("Ripped Tunic", myHero, 25, 35), Garment("Medium Tunic", myHero, 25, 35), Garment("Strong Tunic", myHero, 25, 35)]
    weapons = [Weapon("Broken Axe", myHero, 10, 15), Weapon("Medium Axe", myHero, 10, 15), Weapon("Strong Axe", myHero, 10, 15)]
    myHero.update_secondary_attributes
    
    # Abilities & Items (Temporary)
    test_ability = Ability("Stone Skin", myHero, skin_adjective)
    myHero.abilities.append(test_ability)
    myHero.inventory.append(clothes[0])
    myHero.inventory.append(weapons[0])
    
    # Refresh Hero
    myHero.update_secondary_attributes
    return myHero
# End of temporary functions


# initialization
myHero = create_random_hero()
game = Game(myHero)
enemy = monster_generator(myHero.level)


	


