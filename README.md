# SkyBrew
Simulates the Alchemy system of 'The Elder Scrolls V: Skyrim' in Python. Work in Progress.


To use it, run main.py. To select your ingredient combo, you must manually type in values for a, b, or c in the format of ingredients["Ingredient Name"].
For example, 'a = ingredients["Wheat"]'


What it can do currently:
- Checks for valid combination of ingredients
- Prints Potion Magnitude, Duration, and total Gold Value of the Potion
- Adjusts Potion Calculations based on Player's Alchemy Skill and perks

I am working on:
- Getting optional third ingredient (variable c in code) to function fully
- Implementing Priority values for ingredients with Damage Health effect (this matters for magnitude, duration, and gold value calcs).
- Eventually implementing AE content. Currently, only ingredients and effects available in base Special Edition are implemented in my script.
