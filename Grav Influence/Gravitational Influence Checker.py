# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 17:29:04 2024

@author: abiga
"""
# Section with all the important data
names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn",
         "Uranus", "Neptune"]
masses_10_24kg = [0.330, 4.87, 5.97, 0.642, 1898, 568,
                  86.8, 102]
perihelions_10_6km = [46.0, 107.5, 147.1, 206.7, 740.6, 1357.6,
                      2732.7, 4471.1]
aphelions_10_6km = [69.8, 108.9, 152.1, 249.3, 816.4, 1506.5,
                    3001.4, 4558.9]


# creates a loop to keep asking until stop
while True:
    try:
        # Asks the user for the planet they want to study
        planet = input("What planet do you want to study?")
        # Formats the planet to avoid errors due to capital letters
        # or whitespace
        planet = planet.lower()
        planet = planet.capitalize()
        planet = planet.strip()
        # checks if user wants to stop
        if planet == "Stop":
            break
        else:
            # Finds the index of the planet
            index = names.index(planet)

# for loop to calculate the gravitational effect of each planet
# on the selected planet and see if it is detectable
        for i in range(8):
            if i != index:
                # calculates the maximum possible distance between the planet
                # i and chosen planet
                r_max = (aphelions_10_6km[index] + aphelions_10_6km[i]) \
                    * 1e9
                # calculates the acceleration due to gravity at maximum
                # distance
                a_max = (6.674e-11 * masses_10_24kg[i] * 1e24) / (r_max)**2
                # same for minimum possible distance
                # checks to see which planet is the inner of the two
                if i > index:
                    r_min = (-aphelions_10_6km[index] + perihelions_10_6km[i])\
                        * 1e9
                else:
                    r_min = (-aphelions_10_6km[i] + perihelions_10_6km[index])\
                        * 1e9
                a_min = (6.674e-11 * masses_10_24kg[i] * 1e24) / (r_min)**2
                # calculates the gravitation effect
                grav = a_min - a_max
                # compares it to the detectable amount and prints the
                # detectable planets
                if grav > 5.5e-8:
                    print(f"{names[i]} has a detectable gravitation influence on {names[index]}")
# if their is a value error, prints an custom error message
    except ValueError:
        print("Have you put the right value in?")
