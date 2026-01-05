#from perkInfo import a bunch of shit
import math
from src.ingredientDictionary import (ingredients, durations, jarrin_root, river_betty, emperor_parasol_moss,
                                      nirnroot, crimson_nirnroot, deathbell)
from src.effectDictionary import effects
from src.perkInfo import physician_applies, benefactor_applies, poisoner_applies


# All relevant formulas for magnitude, duration and cost will be stored here.


# Helper function for returning a list of shared effects between ingredients
#def get_shared_effects(ingr_a: dict,
                       #ingr_b: dict,
                       #ingr_c: None) -> list:
    # Creates shared_effects list which contains common elements of a, b, c
    #if ingr_c:
        #shared_effects = [effect for effect in a if effect in b]
        #shared_effects += [effect for effect in a if effect in c]
        #shared_effects += [effect for effect in b if effect in c]
        #valid_effects = ", ".join(shared_effects)
        #print(f'The three Ingredients share {valid_effects}.')

    #elif ingr_a and ingr_b:
        #shared_effects = [effect for effect in a if effect in b]
        #valid_effects = ", ".join(shared_effects)
        #print(f'The two Ingredients share {valid_effects}.')

    #else:
        #print('They share no effects, or values for a and b were not found.')
        #quit()
    #print(shared_effects)
    #return shared_effects
    #pass

# Helper function to sort shared effects into a list in order of descending cost. it should return this list.
# TODO this sort also needs to be fixed after implementing.
def sort_effects(shared_effects: list) -> list:

    # Searches for any costs associated with effects in shared_effects.
    effect_costs = {effect: effects[effect]["Base Cost"] for effect in shared_effects}

    # Sort effects by descending cost
    sorted_effects = sorted(effect_costs.items(), key=lambda x: x[1], reverse=True)

    return sorted_effects


# takes list of sorted effects by cost.
def get_main_effect(sorted_effects: list) -> str:
    main_effect = sorted_effects[0][0]
    return main_effect


# takes list of sorted effects by cost. returns list or None if no side effects exist.
def get_side_effects(sorted_effects: list) -> list|None:
    side_effects = [effect for effect, cost in sorted_effects[1:]]
    return side_effects



# TODO these also needs access to perk/skill info
# TODO this needs to take a, b, and c to fetch multipliers
# Parameter 'constant' takes INITMULT; parameter 'skill' takes SKILLMULT; parameter 'enchants' takes TOTAL_ENCHANTS
def calculate_magnitude(ingr_a: dict,
                        ingr_b: dict,
                        ingr_c: None|dict,
                        effect_name: str,
                        main_effect: str,
                        INITMULT: int,
                        SKILLMULT: float,
                        TOTAL_ENCHANTS: float,
                        alchemist_perks: float,
                        physician_perk: float,
                        benefactor_perk: float,
                        poisoner_perk: float,
                        seeker: float) -> int:

    base_mag = effects[effect_name]["Base Magnitude"]
    magmults = []

    for mag in [ingr_a, ingr_b, ingr_c] if ingr_c else [ingr_a, ingr_b]:
        if effect_name in mag:
            magmults.append(mag[effect_name])
    ingr_mult = max(magmults, default=1)

    if (effect_name == "Damage Health" and ingr_a == jarrin_root
            or ingr_b == jarrin_root
            or ingr_c == jarrin_root):
        ingr_mult = 100
    elif (effect_name == "Damage Health" and ingr_a ==river_betty
          or ingr_b == river_betty
          or ingr_c == river_betty):
        ingr_mult = 2.5
    elif (effect_name == "Damage Health" and ingr_a == emperor_parasol_moss
          or ingr_b == emperor_parasol_moss
          or ingr_c == emperor_parasol_moss):
        ingr_mult = 1.5
    elif (effect_name == "Damage Health" and ingr_a == nirnroot
          or ingr_b == nirnroot
          or ingr_c == nirnroot):
        ingr_mult = 1
    elif (effect_name == "Damage Health" and ingr_a == crimson_nirnroot
          or ingr_b == crimson_nirnroot
          or ingr_c == crimson_nirnroot):
        ingr_mult = 3
    elif (effect_name == "Damage Health" and ingr_a == deathbell
          or ingr_b == deathbell
          or ingr_c == deathbell):
        ingr_mult = 1.5
    else:
        pass

# Finally, rounds the end result according to Skyrim's Alchemy formula.
    try:

        result = round(INITMULT * (base_mag * ingr_mult) * SKILLMULT * alchemist_perks * TOTAL_ENCHANTS * seeker)
        if physician_applies(effect_name):
            result *= physician_perk

        if benefactor_applies(effect_name, main_effect):
            result *= benefactor_perk

        if poisoner_applies(effect_name, main_effect):
            result *= poisoner_perk


        # Handles fixed magnitude effects
        if effect_name in ["Damage Magicka Regen", "Damage Stamina Regen"]:
            result = 100
        elif effect_name in ["Slow"]:
            result = 50
        elif effect_name in ["Waterbreathing", "Invisibility"]:
            result = 0
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

        elif effect_name in ["Regenerate Health", "Regenerate Magicka", "Regenerate Stamina"]:
            print(f'You created {effect_name}: {result}% faster regeneration.')

        elif effect_name in ["Fortify Sneak", "Resist Frost", "Resist Fire", "Resist Shock", "Resist Poison", "Resist Magic",
                             "Weakness to Fire", "Weakness to Frost", "Weakness to Shock", "Weakness to Magic",
                             "Weakness to Poison", "Damage Stamina Regen", "Damage Magicka Regen", "Fortify Block",
                             "Fortify Barter", "Fortify Smithing", "Fortify Enchanting", "Slow"]:
            print(f'You created {effect_name}: {result}%.')

        else:
            print(f'You created {effect_name}: {result} points.')

    except OverflowError or MemoryError:
        print("You attempted to create a potion that is too strong.")
        quit()
    return result

def calculate_duration(ingr_a: dict,
                       ingr_b: dict,
                       ingr_c: None|dict,
                       effect_name: str,
                       constant: int,
                       skill: float,
                       enchants: float,
                       alchemist_perks: float,
                       benefactor_perk: float,
                       poisoner_perk: float,
                       seeker: float) -> int:

    base_dur = effects[effect_name]["Base Duration"]

    dur_mult = [
        durations[(ingr_name, effect_name)]
        for ingr_name, ingr_dict in ingredients.items()
        if ingr_dict in ([ingr_a, ingr_b, ingr_c] if ingr_c else [ingr_a, ingr_b])
        if (ingr_name, effect_name) in durations
    ]

    # Unlike magnitude, duration will multiply regardless of greatest multiplier.
    if dur_mult:
        base_dur = round(base_dur * dur_mult[0])
    else:
        base_dur = 1.0

    # Naming var true_dur so variable names make more sense below.

    true_dur = 0

    # Handles cases for duration-only potions where duration is affected by magnitude buffs.
    # Potions with fixed mag, variate durations
    if effect_name in ["Invisibility", "Waterbreathing"]:
        true_dur = round((constant * base_dur) * skill * alchemist_perks * benefactor_perk * enchants * seeker)


    # Poisons with fixed mag, variate durations
    elif effect_name in ["Paralysis", "Slow", "Damage Magicka Regen", "Damage Stamina Regen"]:
        true_dur = round((constant * base_dur) * skill * alchemist_perks * poisoner_perk * enchants * seeker)


    # Poisons with variate mag, fixed duraions
    elif effect_name in ["Frenzy", "Lingering Damage Health", "Lingering Damage Magicka", "Lingering Damage Stamina"]:
        true_dur = 10

    # Effects with 0 duration.
    elif effect_name in ["Restore Health", "Restore Magicka", "Restore Stamina", "Cure Disease",
                    "Damage Stamina", "Damage Magicka"]:
        true_dur = 0

    # Handles print statements for the odd damage health ingredients.
    elif (effect_name in ["Damage Health"] and ingr_a == river_betty
          or ingr_b == river_betty
          or ingr_c == river_betty):
        true_dur = 0

    elif (effect_name in ["Damage Health"] and ingr_a == emperor_parasol_moss
          or ingr_b == emperor_parasol_moss
          or ingr_c == emperor_parasol_moss):
        true_dur = 0

    elif (effect_name in ["Damage Health"] and ingr_a == nirnroot
          or ingr_b == nirnroot
          or ingr_c == nirnroot):
        true_dur = 0
    else:
        true_dur = base_dur

    # Effects with no duration will not print their duration.
    if effect_name in ["Damage Health", "Damage Magicka", "Damage Stamina", "Cure Disease",
                       "Restore Health", "Restore Magicka", "Restore Stamina"]:
        pass
    elif true_dur == 0:
        pass
    else:
        print(f'Lasts for {true_dur} seconds.')

    return true_dur

# TODO this function needs magnitude and duration
def calculate_cost(ingr_a: dict,
                   ingr_b: dict,
                   ingr_c: None|dict,
                   effect_name: str,
                   magnitude: int,
                   duration: int) -> int:

    base_cost = effects[effect_name]["Base Cost"]

    # Attempting to handle non-standard behavior for certain Damage Health ingredients.
    if (effect_name in "Damage Health" and ingr_a == river_betty
            or ingr_b == river_betty
            or ingr_c == river_betty):
        duration = 10

    elif (effect_name in "Damage Health" and ingr_a == emperor_parasol_moss
          or ingr_b == emperor_parasol_moss
          or ingr_c == emperor_parasol_moss):
        duration = 10

    elif (effect_name in "Damage Health" and ingr_a == nirnroot
          or ingr_b == nirnroot
          or ingr_c == nirnroot):
        duration = 10
    else:
        pass

    true_cost = float
    # Checking if either duration or magnitude equal 0 and selecting formulae accordingly.
    if duration > 0 and magnitude > 0:
        true_cost = math.floor((base_cost * max(magnitude ** 1.1, 1) * ((duration / 10) ** 1.1)))

    elif duration == 0:
        true_cost = math.floor(base_cost * max(magnitude ** 1.1, 1) * 1)

    elif magnitude == 0:
        true_cost = math.floor(base_cost * max((duration/10)**1.1, 1))

    else:
        true_cost = math.floor(base_cost * max(magnitude ** 1.1, 1) * ((duration/10)**1.1))

    print(f'Sells for {true_cost} Gold.\n')
    return true_cost
