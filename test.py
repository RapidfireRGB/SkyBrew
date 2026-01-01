from main import shared_effects, calculate_potion

from ingredientDictionary import ingredients

#from effectDictionary import effects

# Helper function to set values for skill and perks.
def check_perks() -> None:


    command = input("Do you want to manually set your Alchemy Skill values and Perks (y/n)?\n"
                    "If not, the calculator will assume an Alchemy Skill of 15 and no perks.").strip().lower()
    if command in ["n", "no"]:
        # Re declaring values here for clarity.
        alch_skill = 15
        total_enchants = 1.0
        fortify_restoration = 1.0

        alchemist_rank1 = False
        alchemist_rank2 = False
        alchemist_rank3 = False
        alchemist_rank4 = False
        alchemist_rank5 = False
        alchemist_perks = 1

        physician = False
        physician_perk = 1

        benefactor = False
        benefactor_perk = 1

        poisoner = False
        poisoner_perk = 1

        seeker_of_shadows = False
        seeker_of_shadows_pwr = 1

    elif command in ["y", "yes"]:
        # TODO add validation to this block.
        command = int(input("Input your skill level (1-100):\n").strip().lower())
        alch_skill = command
        command = float(input("Input the sum of your Fortify Alchemy Enchantments (EX: +25% -> 1.25. Defaults to 1.0)\n"))
        total_enchants = command
        command = float(input("Input the sum of your Fortify Restoration buffs, if you have any. (EX: +25% -> 1.25. Defaults to 1.0)\n"))
        fortify_restoration = command

        command = int(input("How many ranks of the Alchemist Perk do you have (0-5)?\n").strip().lower())
        if command == 1:
            alchemist_rank1 = True
        elif command == 2:
            alchemist_rank1 = True
            alchemist_rank2 = True
        elif command == 3:
            alchemist_rank1 = True
            alchemist_rank2 = True
            alchemist_rank3 = True
        elif command == 4:
            alchemist_rank1 = True
            alchemist_rank2 = True
            alchemist_rank3 = True
            alchemist_rank4 = True
        elif command == 5:
            alchemist_rank1 = True
            alchemist_rank2 = True
            alchemist_rank3 = True
            alchemist_rank4 = True
            alchemist_rank5 = True

        command = input("Do you have the Physician Perk (y/n)?\n").strip().lower()
        if command in ["y", "yes"]:
            physician = True

        command = input("Do you have the Benefactor Perk (y/n)?\n").strip().lower()
        if command in ["y", "yes"]:
            benefactor = True

        command = input("Do you have the Poisoner Perk (y/n)?\n").strip().lower()
        if command in ["y", "yes"]:
            poisoner = True

        command = input("Do you have the Seeker of Shadows Power (y/n)?\n").strip().lower()
        if command in ["y", "yes"]:
            seeker_of_shadows = True

# This should return values for a, b, c
def check_ingredients() -> dict[str, dict]:
    name = input("Input the name of an ingredient.\n"
                 "Make sure to capitalize the ingredients (EX: 'Giant's Toe')")
    return ingredients[name]

# Trying to implement an entry point function for ease of use.
def main():
    check_perks()

    command = input("Do you want to combine 2 ingredients, or 3 ingredients (2/3)?").strip().lower()
    main.a = check_ingredients()
    main.b = check_ingredients()
    if command in ["3", "three"]:
        main.c = check_ingredients()

    # Extracts effect_name string from shared_effects and inputs the string to the function. Also, sums the total potion cost in gold.
    total_cost = 0
    for effect_name_string in shared_effects:
        effect_cost = calculate_potion(effect_name_string)
        total_cost += effect_cost
    print(f'Sells for {total_cost} Gold in Total.')

main()
def test_values():
    return