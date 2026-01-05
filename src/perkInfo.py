# Storing the functions relevant to the player's perks/skill here.

# Return a multiplier based on user-input perk rank.
def check_alchemist_ranks() -> float:
    rank = input("How many ranks of the Alchemist Perk do you have (0-5)?\n").strip()
    if rank == "1":
        return 1.2
    elif rank == "2":
        return 1.4
    elif rank == "3":
        return 1.6
    elif rank == "4":
        return 1.8
    elif rank == "5":
        return 2.0
    else:
        return 1.0

# Return a multiplier based on whether user has Physician perk.
def check_physician() -> float:
    check = input("Do you have the Physician Perk (y/n)?\n").strip().lower()
    if check == "y":
        return 1.25
    else:
        return 1.0

# Return a multiplier based on whether user has Benefactor perk.
def check_benefactor() -> float:
    check = input("Do you have the Benefactor Perk (y/n)?\n").strip().lower()
    if check == "y":
        return 1.25
    else:
        return 1.0

# Return a multiplier based on whether user has Poisoner perk.
def check_poisoner() -> float:
    check = input("Do you have the Poisoner Perk (y/n)?\n").strip().lower()
    if check == "y":
        return 1.25
    else:
        return 1.0

# Return a multiplier based on whether user has Seeker of Shadows Active Effect.
def check_seeker_pwr() -> float:
    check = input("Do you have the Seeker of Shadows Active Effect (y/n)?\n").strip().lower()
    if check == "y":
        return 1.1
    else:
        return 1.0

# Returns the multiplier for fortify restoration based on user input.
def check_fortify_resto() -> float:
    try:
        # If conversion to float fails, raise ValueError
        fortify_resto_mult = float(input("Enter the sum of your Fortify Restoration buffs \n(EX: +25% -> 1.25):\n").strip())
        if fortify_resto_mult < 1:
            fortify_resto_mult = 1
        return fortify_resto_mult

    except OverflowError:
        print("You Fortified you Restoration a little too hard.")
        quit()

    except ValueError:
        print("You entered an invalid value for 'Fortify Restoration'.\n")
        quit()

# Returns the multiplier for fortify alchemy based on user input.
def check_fortify_alch() -> float:
    try:
        # If conversion to float fails, raise ValueError
        fortify_alch_mult = float(input("Enter the sum of your Fortify Alchemy buffs \n(EX: +25% -> 1.25):\n").strip())
        if fortify_alch_mult < 1:
            fortify_alch_mult = 1
        return fortify_alch_mult

    except OverflowError:
        print("You Fortified your Restoration a little too hard.")
        quit()
    except ValueError:
        print("You entered an invalid value for 'Fortify Alchemy'.\n")
        quit()

# Returns alchemy skill value based on user input.
def check_skill() -> int:
    try:
        # If conversion to int fails, raise ValueError
        alchemy_skill_val = int(input("Enter your Alchemy Skill (1-100):\n").strip())

        # Handling out of range values
        if alchemy_skill_val > 100:
            alchemy_skill_val = 100
        if alchemy_skill_val < 1:
            alchemy_skill_val = 15

    except ValueError:
        print("You entered an invalid value for 'Alchemy Skill',\n")
        quit()

    return alchemy_skill_val

# Check if a potion should have physician applied. returns bool.
def physician_applies(effect_name: str) -> bool:
    restore_potions = ["Restore Health", "Restore Magicka", "Restore Stamina"]
    if effect_name in restore_potions:
        return True
    else:
        return False

# Check if a potion should have benefactor applied. returns bool.
def benefactor_applies(effect_name: str, main_effect: str) -> bool:
    if (effect_name in ["Cure Disease", "Fortify Alteration", "Fortify Barter", "Fortify Block",
                                "Fortify Carry Weight", "Fortify Conjuration", "Fortify Destruction",
                                "Fortify Enchanting", "Fortify Health", "Fortify Heavy Armor",
                                "Fortify Illusion", "Fortify Light Armor", "Fortify Lockpicking",
                                "Fortify Magicka", "Fortify Marksman", "Fortify One-Handed", "Fortify Pickpocket",
                                "Fortify Restoration", "Fortify Smithing", "Fortify Sneak", "Fortify Stamina",
                                "Fortify Two-Handed", "Invisibility", "Regenerate Health", "Regenerate Magicka",
                                "Regenerate Stamina", "Resist Fire", "Resist Frost", "Resist Magic", "Resist Poison",
                                "Resist Shock", "Restore Health", "Restore Magicka", "Restore Stamina",
                                "Waterbreathing"]
        and main_effect == effect_name):

        return True
    else:
        return False

# Check if a potion should have poisoner applied. returns bool.
def poisoner_applies(effect_name: str, main_effect: str) -> bool:
    if (effect_name in ["Damage Health", "Damage Stamina", "Damage Magicka", "Damage Magicka Regen",
                                "Damage Stamina Regen", "Frenzy", "Lingering Damage Health",
                                "Lingering Damage Magicka", "Lingering Damage Stamina", "Paralysis",
                                "Ravage Health", "Ravage Magicka", "Ravage Stamina", "Slow", "Weakness to Fire",
                                "Weakness to Frost", "Weakness to Magic", "Weakness to Poison",
                                "Weakness to Shock"]
        and main_effect == effect_name):

        return True
    else:
        return False