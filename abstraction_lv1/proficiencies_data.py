# Name, Description, Attribute_Type, Type, [(Values Name, Value type, (Modifiers of value), Decimal Places)]
# Linear: (Level multiplier), (Starting Value)
# Root: Not finished. Looks like square root function. Used for diminishing returns and things that get better the larger they are. (Starting value) [Currently approaches 100]

# Curvy: (larger "0" means it reaches the cap quicker) (smaller [1] means it reaxhes the cap quicker) ([2] is the cap or maximum possible value) ([3] is the negative amount)
# Sensitive: Like curvy but has decimals (larger [0] means it reaches the cap quicker) (smaller [1] means it reaches the cap quicker) ([2] is the cap or maximum possible value) ([3] is the negative amount)
# Modifier: (larger [0] means greater amplitude), (larger [1] means greater steepness andfaster increase), (greater [2]  means greater frequency of waves)
# Percent: ???
# Empty: Sets this value to take on the value of "maximum". Must be placed after "Maximum" in the list of variables
PROFICIENCY_INFORMATION = [
    ("Health", "How much you can take before you die", "Vitality", [("Maximum", "linear", (2, 5, 0)), ("Current", "empty")]),
    ("Regeneration", "How quickly your wounds heal", "Vitality", [("Speed", "root", (1, 2))]),
    ("Recovery", "How quickly you recover from poisons and negative effects", "Vitality",[("Efficiency", "root", (0, 0))]),
    ("Climbing", "Your ability to climb obstacles", "Agility", [("Ability", "linear", (0.5, 0.5, 1))]),
    ("Storage", "Your carrying capacity", "Brawn", [("Maximum", "linear", (2, 10, 0)), ("Current", "empty")]),
    ("Encumbrance", "How much your are slowed down in combat by your equipment", "Brawn", [("Amount", "root", (0, 0))]),
    ("Endurance", "Actions performed each day", "Resilience", [("Maximum", "linear", (1, 3, 0)), ("Current", "empty")]),
    ("Damage", "How much damage you do on each hit", "Brawn", [("Minimum", "linear", (1, 0, 0)), ("Maximum", "linear", (1, 1, 0)), ("Modifier", "linear", (.1, 1, 1))]),
    ("Speed", "How fast you attack", "Quickness", [("Speed", "linear", (0.03, 1, 2))]),
    ("Accuracy", "The chance of your attacks hitting their target.", "Agility", [("Accuracy", "root", (35, 0))]),
    ("First strike", "Chance to strike first", "Quickness", [("Chance", "root", (0, 0))]),
    ("Killshot", "Ability to hit enemies in their weak spot", "Agility", [("Chance", "root", (0, 0)), ("Modifier", "linear", (0.1, 1, 1))]),
    ("Defence", "Damage reduction", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Evade", "Chance to dodge", "Quickness", [("Chance", "root", (5, 0))]),
    ("Parry", "Chance to parry", "Quickness", [("Chance", "root", (2, 0))]),
    ("Flee", "Chance to run from a battle", "Quickness", [("Chance", "root", (7, 0))]),
    ("Riposte", "Chance to riposte an enrmy attack", "Agility", [("Chance", "root", (0, 0))]),
    ("Fatigue", "How quickly you tire in combat", "Resilience", [("Maximum", "linear", (1, 5, 0)), ("Current", "empty")]),
    ("Block", "Ability to block if a shield is equipped", "Resilience", [("Chance", "root", (0, 0)), ("Modifier", "root", (0, 0))]),
    ("Stealth", "Chance to avoid detection", "Agility", [("Chance", "root", (3, 0))]),
    ("Pickpocketing", "Skill at stealing from others", "Agility", [("Chance", "root", (1, 0))]),
    ("Faith", "Strength of spells you cast", "Divinity", [("Modifier", "linear", (0.1, 1, 0))]),
    ("Sanctity", "Amount of sanctity you can have", "Divinity", [("Maximum", "linear", (3, 0, 0)), ("Current", "empty")]),
    ("Resist holy", "Ability to resist holy damage", "Divinity", [("Modifier", "root", (0, 0))]),
    ("Bartering", "Discount from negotiating prices", "Charisma", [("Modifier", "linear", (-0.05, 1, 0))]),
    ("Oration", "Proficiency in speaking to others", "Charisma", [("Modifier", "root", (11, 0))]),
    ("Charm", "How quickly other people will like you", "Charisma", [("Modifier", "root", (3, 0))]),
    ("Trustworthiness", "How much other players trust you", "Charisma", [("Modifier", "root", (0, 0))]),
    ("Renown", "How much your actions affect your reputation", "Charisma", [("Modifier", "linear", (0.1, 1, 0))]),
    ("Knowledge", "Ability to understand", "Intellect", [("Modifier", "root", (6, 0))]),
    ("Literacy", "Ability to read", "Intellect", [("Modifier", "root", (0, 0))]),
    ("Understanding", "How quickly you level up", "Intellect", [("Modifier", "linear", (0.05, 1, 0))]),
    ("Luckiness", "Chance to have things turn your way against all odds", "Fortuity", [("Chance", "linear", (0.01, 0, 0))]),
    ("Adventuring", "Chance to discover treasure", "Fortuity", [("Chance", "root", (0, 0))]),
    ("Logistics",  "How far you can move on the map", "Pathfinding", [("Modifier", "linear", (0.2, 1, 0))]),
    ("Mountaineering", "Modifier for mountain movement", "Pathfinding", [("Modifier", "linear", (0.5, 1, 0))]),
    ("Woodsman", "Modifier for forest movement", "Pathfinding", [("Modifier", "linear", (.5, 1, 0))]),
    ("Navigator", "Modifier for water movement", "Pathfinding", [("Modifier", "linear", (.5, 1, 0))]),
    ("Detection", "Chance to discover enemy stealth and traps", "Survivalism", [("Chance", "root", (0, 0))]),
    ("Caution",  "See information about a new grid before going there", "Survivalism", [("Ability", "linear", (0.5, 0.5, 0))]),
    ("Explorer", "Additional options on the map, such as foraging", "Survivalism", [("Ability", "linear", (0.5, 0.5, 0))]),
    ("Huntsman", "Learn additional information about enemies", "Survivalism", [("Ability", "linear", (0.5, 0.5, 0))]),
    ("Survivalist", "Create bandages, tents, and other useful objects", "Survivalism", [("Ability", "linear", (0.5, 0.5, 0))]),
    ("Resist frost", "Ability to resist frost damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Resist flame", "Ability to resist flame damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Resist shadow", "Ability to resist shadow damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Resist poison", "Ability to resist poison damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Resist blunt", "Ability to resist blunt damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Resist slashing", "Ability to resist slashing damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Resist piercing", "Ability to resist piercing damage", "Resilience", [("Modifier", "root", (0, 0))]),
    ("Courage", "Your ability to overcome fears", "Willpower", [("Skill", "linear", (1, 0, 0))]),
    ("Sanity", "Your ability to resist mind altering affects", "Willpower", [("Skill", "linear", (1, 0, 0))]),
    ]



ALL_PROFICIENCIES = [attrib[0].lower().replace(" ", "_") for attrib in PROFICIENCY_INFORMATION]