import  random
import fish_data
import classes

def generate_fish(amount):
    # Initialize an array of fish
    fish_array = []

    # Randomly generate fish species, color, and attribute
    for i in range(amount):
        choice = random.randint(0, len(fish_data.fish_type) - 1)
        f_species = fish_data.fish_type[choice]
        f_dex_number = choice

        choice = random.randint(0, len(fish_data.fish_color) - 1)
        f_color = fish_data.fish_color[choice]

        choice = random.randint(0, len(fish_data.fish_attribute) - 1)
        f_attribute = fish_data.fish_attribute[choice]

        f = classes.gameFish(f_species, f_color, f_attribute, f_dex_number)

        fish_array.append(f)
    # Print out the generated fish, done as a list so lots of fish can be made at once, for testing
    for fish in fish_array:
        print(fish.attribute + " " + fish.color + " " + fish.species + " - " + str(fish.dex_number))
    return fish_array


def main():
    generate_fish(5)

if __name__ == "__main__":
    main()