import math
import sys
from ingredientDictionary import (ingredients, durations, jarrin_root, river_betty, emperor_parasol_moss,
                                  nirnroot, crimson_nirnroot, deathbell, priorities)
from effectDictionary import effects

# TODO Test to ensure ingredient c is completely functional. Check every place where a and b are used.
#  Rewrite Magnitude and/or Duration logic as they are not 100% accurate to the game.

# LONG Global variable section.
# Generates a List of the keys shared between Dictionaries a and b (these are the common effects).
# Put your two ingredients in for a, b, and c. (c represents optional 3rd ingredient.)
# Format is ingredients["Ingredient Name"]
a = ingredients["Wheat"]
b = ingredients["Blisterwort"]
c = None
shared_effects = [effect for effect in a if effect in b]

# TODO trying to handle variable c. Currently throws TypeError.
#if c:
   #shared_effects += [effect for effect in [a, b] if effect in c]


# Prints text to indicate which effects the ingredients share in common. If none in common, quit program.
if c:
    shared_effects = [effect for effect in shared_effects if effect in c]
    valid_effects = ", ".join(shared_effects)
    print(f'The three Ingredients share {valid_effects}.')

if shared_effects:
    valid_effects = ", ".join(shared_effects)
    print(f'The two Ingredients share {valid_effects}.')

else:
    print('They share no effects.')
    sys.exit()

# ----------Defining Main/Side Effects----------
# Searches for any costs associated with effects in shared_effects and creates a list of tuple pairs.
effect_costs = {effect: effects[effect]["Base Cost"] for effect in shared_effects}

# Sort effects by descending cost
sorted_effects = sorted(effect_costs.items(), key=lambda x: x[1], reverse=True)

# Defining main and side effects by position in pair. Needed to determine whether certain perks are applied.
main_effect = sorted_effects[0][0]
side_effects = [effect for effect, _ in sorted_effects[1:]]

print(f'Primary Effect: {main_effect}')
print(f'Side Effect(s): {side_effects}')

# --------------Alchemy Formula------------------
# INITMULT is the initial multiplier in Result formula. INITMULT Always has a value of 4.
# alch_skill: Player Alchemy Skill Level.
# SKILLMULT: The Formula which governs how Alchemy Skill affects potion magnitude.
# total_enchants: Additive. Any fortify alchemy buffs go here. (+25% means +0.25).
# Also handles fortify restoration buffs, which stack multiplicatively with fortify alchemy.
# For the purposes of Alchemy, Fortify Restoration will only apply in-game if it buffs Spell Magnitude, not Spell Cost Reduction.
INITMULT = 4
alch_skill = 15
SKILLMULT = 1 + (1.5 - 1) * alch_skill/100
total_enchants = 1.0
fortify_restoration = 1.0
if total_enchants > 1.0:
    total_enchants = fortify_restoration * total_enchants

# Defining Perks the Player may have.
# Alchemist ranks 1 - 5. +20% each.
alchemist_rank1 = False
alchemist_rank2 = False
alchemist_rank3 = False
alchemist_rank4 = False
alchemist_rank5 = False
alchemist_perks = 1

# Physician (+25% Restore Potions), Benefactor (+25% Non-Poisons), Poisoner (+25% Poisons).
physician = False
physician_perk = 1

benefactor = False
benefactor_perk = 1

poisoner = False
poisoner_perk = 1

# Checking for Player Perks and adding them to the result formula accordingly.
# Staying as separate ifs for now, since the player may have multiple or all ranks.
if alchemist_rank1:
    alchemist_perks += 0.2
if alchemist_rank2:
    alchemist_perks += 0.2
if alchemist_rank3:
    alchemist_perks += 0.2
if alchemist_rank4:
    alchemist_perks += 0.2
if alchemist_rank5:
    alchemist_perks += 0.2

# Handling cases where Physician, Benefactor, and Poisoner perks should be applied.
if physician and shared_effects in ["Restore Health", "Restore Magicka", "Restore Stamina"]:
    physician_perk += 0.25

if benefactor and main_effect in ["Cure Disease", "Fortify Alteration", "Fortify Barter", "Fortify Block",
                                "Fortify Carry Weight", "Fortify Conjuration", "Fortify Destruction",
                                "Fortify Enchanting", "Fortify Health", "Fortify Heavy Armor",
                                "Fortify Illusion", "Fortify Light Armor", "Fortify Lockpicking",
                                "Fortify Magicka", "Fortify Marksman", "Fortify One-Handed", "Fortify Pickpocket",
                                "Fortify Restoration", "Fortify Smithing", "Fortify Sneak", "Fortify Stamina",
                                "Fortify Two-Handed", "Invisibility", "Regenerate Health", "Regenerate Magicka",
                                "Regenerate Stamina", "Resist Fire", "Resist Frost", "Resist Magic", "Resist Poison",
                                "Resist Shock", "Restore Health", "Restore Magicka", "Restore Stamina",
                                "Waterbreathing"]:
    benefactor_perk += 0.25

if poisoner and main_effect in ["Damage Health", "Damage Stamina", "Damage Magicka", "Damage Magicka Regen",
                                "Damage Stamina Regen", "Frenzy", "Lingering Damage Health",
                                "Lingering Damage Magicka", "Lingering Damage Stamina", "Paralysis",
                                "Ravage Health", "Ravage Magicka", "Ravage Stamina", "Slow", "Weakness to Fire",
                                "Weakness to Frost", "Weakness to Magic", "Weakness to Poison",
                                "Weakness to Shock"]:
    poisoner_perk += 0.25

# Seeker of Shadows. This is an Active Effect selectable from the Black Book, 'The Sallow Regent.'
seeker_of_shadows = False
seeker_of_shadows_pwr = 1
if seeker_of_shadows:
    seeker_of_shadows_pwr += 0.1

# Function starts here. For loop at bottom feeds input.
def calculate_potion(effect_name: str):
    global a, b, c, INITMULT, alch_skill, SKILLMULT, total_enchants, alchemist_perks, benefactor_perk, \
        physician_perk, poisoner_perk, seeker_of_shadows_pwr

    # Base multipliers for cost, magnitude, and duration assigned to a given effect.
    base_mag = effects[effect_name]["Base Magnitude"]
    base_dur = effects[effect_name]["Base Duration"]
    base_cost = effects[effect_name]["Base Cost"]

    #---------------MAGNITUDE------------------
    # Generates a list. Populates it with any ingredient-specific multipliers. Sets ingr_mult to the greatest one.
    magmults = []
    for ingr in [a, b, c] if c else [a, b]:
        if effect_name in ingr:
            magmults.append(ingr[effect_name])
    ingr_mult = max(magmults, default=1)

    # Handles cases where negative multipliers exist; lowest multiplier is taken instead.
    if magmults < [1]:
        ingr_mult = min(magmults)

    # Handling damage health. TODO there is def a better way to do this.
    if effect_name == "Damage Health" and a == jarrin_root or b == jarrin_root or c == jarrin_root:
        ingr_mult = 100
    elif effect_name == "Damage Health" and a == river_betty or b == river_betty or c == river_betty:
        ingr_mult = 2.5
    elif effect_name == "Damage Health" and a == emperor_parasol_moss or b == emperor_parasol_moss or c == emperor_parasol_moss:
        ingr_mult = 1.5
    elif effect_name == "Damage Health" and a == nirnroot or b == nirnroot or c == nirnroot:
        ingr_mult = 1
    elif effect_name == "Damage Health" and a == crimson_nirnroot or b == crimson_nirnroot or c == crimson_nirnroot:
        ingr_mult = 3
    elif effect_name == "Damage Health" and a == deathbell or b == deathbell or c == deathbell:
        ingr_mult = 1.5
    else:
        pass


    # Finally, rounds the end result according to Skyrim's Alchemy formula.
    result = round(INITMULT * (base_mag * ingr_mult) * SKILLMULT * alchemist_perks * physician_perk * benefactor_perk
                   * poisoner_perk * total_enchants * seeker_of_shadows_pwr)

    # Handles fixed magnitude effects
    if effect_name in ["Damage Magicka Regen", "Damage Stamina Regen"]:
        result = 100
    elif effect_name in ["Slow"]:
        result = 50
    else:
        pass

    # Handles cases where final potion magnitude is less than 0
    if result < 0:
        result = round(base_mag * ingr_mult)

    # Prints Resulting potion magnitude. Different print statements to further contextualize each effect.
    if effect_name in ["Waterbreathing", "Invisibility", "Paralysis", "Cure Disease"]:
        print(f'You created {effect_name}.')

    elif effect_name in ["Fortify Alteration", "Fortify Conjuration"]:
        print(f'You created {effect_name}: spells last for {result}% longer.')

    elif effect_name in ["Fortify Destruction", "Fortify Restoration", "Fortify Illusion"]:
        print(f'You created {effect_name}: spells are {result}% stronger.')

    elif effect_name in ["Fortify Heavy Armor", "Fortify Light Armor"]:
        print(f'You created {effect_name}: skill increased by {result} points.')

    elif effect_name in ["Fortify Marksman", "Fortify One-Handed", "Fortify Two-Handed"]:
        print(f'You created {effect_name}: deal {result}% more damage.')

    elif effect_name in ["Fortify Lockpicking", "Fortify Pickpocket"]:
        print(f'You created {effect_name}: {result}% easier.')

    elif effect_name in ["Fortify Sneak", "Regenerate Health", "Regenerate Magicka", "Regenerate Stamina",
                         "Resist Frost", "Resist Fire", "Resist Shock", "Resist Poison", "Resist Magic",
                         "Weakness to Fire", "Weakness to Frost", "Weakness to Shock", "Weakness to Magic",
                         "Weakness to Poison", "Damage Stamina Regen", "Damage Magicka Regen", "Fortify Block",
                         "Fortify Barter", "Fortify Smithing", "Fortify Enchanting", "Slow"]:
        print(f'You created {effect_name}: {result}%.')

    else:
        print(f'You created {effect_name}: {result} points.')

    #---------------DURATION------------------
    # Creates a list. If this finds any Duration multiplier among ingredients, it is added to list.
    # If any value exists within list, multiply base_dur by that amount.
    dur_mult = [
        durations[(ingr_name, effect_name)]
        for ingr_name, ingr_dict in ingredients.items()
        if ingr_dict in ([a, b, c] if c else [a, b])
        if (ingr_name, effect_name) in durations
    ]

    # Unlike magnitude, duration will multiply regardless of greatest multiplier.
    if dur_mult:
        base_dur = round(base_dur * dur_mult[0])
    else:
        base_dur = base_dur

    # TODO: FINISH DURATION LOGIC; SOME EFFECTS HAVE ODD OR VARIATE DURAITONS.
    # Naming var true_dur so variable names make more sense below.

    true_dur = 0

    # Handles cases for duration-only potions where duration is affected by magnitude buffs.
    # Potions with fixed mag, variate durations
    if effect_name in ["Invisibility", "Waterbreathing"]:
        true_dur = round((INITMULT * base_dur) * SKILLMULT * alchemist_perks * benefactor_perk \
                         * total_enchants * seeker_of_shadows_pwr)
    # Poisons with fixed mag, variate durations
    elif effect_name in ["Paralysis", "Slow", "Damage Magicka Regen", "Damage Stamina Regen"]:
        true_dur = round((INITMULT * base_dur) * SKILLMULT * alchemist_perks * poisoner_perk \
                         * total_enchants * seeker_of_shadows_pwr)
    # Poisons with variate mag, fixed duraions
    elif effect_name in ["Frenzy", "Lingering Damage Health", "Lingering Damage Magicka", "Lingering Damage Stamina"]:
        true_dur = 10

    # Effects with 0 duration.
    elif effect_name in ["Restore Health", "Restore Magicka", "Restore Stamina", "Cure Disease",
                    "Damage Stamina", "Damage Magicka"]:
        true_dur = 0

    # TODO rewrite this since true_dur only matters for the print statement here. Also, fix c.
    elif effect_name in ["Damage Health"] and a == river_betty or b == river_betty or c == river_betty:
        true_dur = 0
    elif effect_name in ["Damage Health"] and a == emperor_parasol_moss or b == emperor_parasol_moss or c == emperor_parasol_moss:
        true_dur = 0
    elif effect_name in ["Damage Health"] and a == nirnroot or b == nirnroot or c == nirnroot:
        true_dur = 0
    else:
        true_dur = base_dur

    print(f'Lasts for {true_dur} seconds.')

    # ---------------COST------------------
    # TODO SEE DAMAGE HEALTH ON WIKI FOR COST CALC; SOME INGREDIENTS HAVE DUR=0 BUT WILL CALCULATE COST AS IF
    #   DUR=10
    # Naming true_cost so variable names make more sense.
    # Checking if either duration or magnitude equal 0 and selecting formulae accordingly.

    true_cost = float

    # This should now handle Damage Health cost properly.
    # Attempting to handle non-standard behavior for certain Damage Health ingredients. TODO again, fix c here.
    if effect_name in "Damage Health" and a == river_betty or b == river_betty or c == river_betty:
        true_dur = 10
    elif effect_name in "Damage Health" and a == emperor_parasol_moss or b == emperor_parasol_moss or c == emperor_parasol_moss:
        true_dur = 10
    elif effect_name in "Damage Health" and a == nirnroot or b == nirnroot or c == nirnroot:
        true_dur = 10
    else:
        pass

    if effect_name in ["Slow"]:
        true_cost = math.floor((base_cost * max(50 ** 1.1, 1) * ((true_dur / 10) ** 1.1)))
    elif true_dur > 0 and result > 0:
        true_cost = math.floor((base_cost * max(result ** 1.1, 1) * ((true_dur / 10) ** 1.1)))
    elif true_dur == 0:
        true_cost = math.floor(base_cost * max(result ** 1.1, 1) * 1)
    elif result == 0 and effect_name not in ["Slow"]:
        true_cost = math.floor(base_cost * max((true_dur/10)**1.1, 1))
    else:
        true_cost = math.floor(base_cost * max(result ** 1.1, 1) * ((true_dur/10)**1.1))

    print(f'Sells for {true_cost} Gold.')
    return true_cost

# Searches shared_effects for a string to be used as the input to functions. Also, sums the total potion cost in gold.
total_cost = 0
for effect in shared_effects:
    effect_cost = calculate_potion(effect)
    total_cost += effect_cost
print(f'Sells for {total_cost} Gold in Total.')