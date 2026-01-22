from src.ingredientDictionary import ingredients
from src.perkInfo import (check_alchemist_ranks, check_physician, check_benefactor, check_poisoner, check_seeker_pwr,
                          check_fortify_alch, check_fortify_resto, check_skill)
from src.logic import calculate_magnitude, calculate_duration, calculate_cost, sort_effects, get_main_effect, \
    get_side_effects
from src.inputValidation import corrections

# Global perk multipliers. modified in function scope.
alchemist_perks = 1
physician_perk = 1
benefactor_perk = 1
poisoner_perk = 1
seeker_of_shadows_pwr = 1

# This should return values for a, b, c
def check_ingredients() -> dict[str, dict]:
    try:
        name = input("Input the name of an ingredient (EX: 'Giant's Toe'):\n").title()
        temp = ingredients[name]

    # If text input is not a valid key, search corrections dictionary to spellcheck. If a valid string
    # is not found, call the function again.
    except KeyError:

        try:
            temp = corrections[name]
            confirm = input(f"Did you mean '{temp}' (y/n)?\n").strip().lower()

            if confirm in ["y", "yes"]:
                print(f"You have selected: '{temp}'.\n")
                return ingredients[corrections[name]]

            else:
                print(f"'{name}' is not a valid ingredient. Please try again.\n")
                check_ingredients()

        except KeyError:
            print(f"'{name}' is not a valid ingredient. Please try again.\n")
            check_ingredients()

    print(f"You have selected '{name}'.\n")
    return ingredients[name]

# Trying to implement an entry point function for ease of use.
def main():
    global alchemist_perks, physician_perk, benefactor_perk, poisoner_perk, seeker_of_shadows_pwr

    # Checking perks.
    user_wants_perks = input("Do you want to manually set your Perks?\n"
                             "If not, the script will assume that you do not have any Perks. (y/n)\n").strip()
    if user_wants_perks in ["y", "yes"]:
        alchemist_perks = check_alchemist_ranks()
        physician_perk = check_physician()
        benefactor_perk = check_benefactor()
        poisoner_perk = check_poisoner()
        seeker_of_shadows_pwr = check_seeker_pwr()
    else:
        pass

    quantity = input("How many ingredients are you using (2/3)?\n").strip()
    INGR_A = check_ingredients()
    INGR_B = check_ingredients()
    if quantity == '3':
        INGR_C = check_ingredients()
    else:
        INGR_C = None

    if INGR_C:
        SHARED_EFFECTS = [effect for effect in INGR_A if effect in INGR_B]
        SHARED_EFFECTS += [effect for effect in INGR_A if effect in INGR_C]
        SHARED_EFFECTS += [effect for effect in INGR_B if effect in INGR_C]
    elif INGR_A and INGR_B:
        SHARED_EFFECTS = [effect for effect in INGR_A if effect in INGR_B]
    else:
        print("They share no effects, or values for Ingredients A and B were not found.\n")
        quit()

    # Defining constants needed in the alchemy formula.
    INITMULT = 4
    ALCH_SKILL = 15
    TOTAL_ENCHANTS = 1.0
    FORTIFY_RESTORATION = 1.0

    user_wants_skills = input("Do you want to manually set values for your Alchemy Skill and Fortify Alchemy enchantments? (y/n)\n"
                              "If not, the script will assume an Alchemy Skill of 15 with no Enchantments.\n").strip().lower()
    if user_wants_skills in ["y", "yes"]:
        ALCH_SKILL = check_skill()
        TOTAL_ENCHANTS = check_fortify_alch()
        FORTIFY_RESTORATION = check_fortify_resto()
    else:
        pass

    SKILLMULT = 1 + (1.5 - 1) * ALCH_SKILL / 100

    if TOTAL_ENCHANTS > 1.0:
        TOTAL_ENCHANTS = FORTIFY_RESTORATION * TOTAL_ENCHANTS

    # Distinguishing between main and side effects matters for potion name, and whether benefactor/poisoner should be applied.
    # Note that the sort_effects() function only half works and is in need of revision.
    sorted_effects = sort_effects(SHARED_EFFECTS)
    main_effect = get_main_effect(sorted_effects)
    side_effects = get_side_effects(sorted_effects)
    print(f'Main effect: {main_effect}\n')
    if side_effects:
        print(f'Side effects: {side_effects}\n')

    # for loop to get multiple effects in one potion
    # Extracts effect_name string from unique shared effects and inputs the string to the functions. Also, sums the total potion cost in gold.
    total_cost = 0
    unique_effects = set(SHARED_EFFECTS)
    for effect_name_string in unique_effects:

    # Should have enough info at this point to get relevant potion info. Stores magnitude and duration as variables to input to cost function.
        magnitude = calculate_magnitude(INGR_A, INGR_B, INGR_C, effect_name_string, main_effect, INITMULT, SKILLMULT, TOTAL_ENCHANTS,
                                        alchemist_perks, physician_perk, benefactor_perk, poisoner_perk, seeker_of_shadows_pwr)

        duration = calculate_duration(INGR_A, INGR_B, INGR_C, effect_name_string, INITMULT, SKILLMULT, TOTAL_ENCHANTS,
                                      alchemist_perks, benefactor_perk, poisoner_perk, seeker_of_shadows_pwr)

        # Increments total_cost by output of cost function.
        total_cost += calculate_cost(INGR_A, INGR_B, INGR_C, effect_name_string, magnitude, duration)

    print(f'Sells for {total_cost} Gold in Total.\n\n')

    user_wants_another = input("Do you want to try another Potion(y/n)?\n").strip().lower()
    if user_wants_another in ["y", "yes"]:
        main()
    else:
        return

main()