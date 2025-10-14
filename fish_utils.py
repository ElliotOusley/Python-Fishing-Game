import pygame
import fish_generator
import time
import random
import math # Used in fish animation

class Player:
    def __init__(self, name, balance, fish_caught, inventory):
        self.name = name
        self.balance = balance
        self.fish_caught = fish_caught
        self.inventory = inventory

class InvItem:
    def __init__(self, name, count):
        self.name = name
        self.count = count

# Add an InvItem to the player's inventory, used for fish list currently,
# plans to add different functionality later
def add_inv_item(player, item):
    for inv_item in player.inventory:
        # If item already exists in player inventory, update its count and re-sort by quantity
        if(item.name == inv_item.name):
            inv_item.count += item.count
            player.inventory.sort(key=lambda x: x.count, reverse=True)
            return

    # If item does not yet exist, add to inventory and sort it to the bottom of the list
    player.inventory.append(InvItem(item.name, item.count))
    player.inventory.sort(key=lambda x: x.count, reverse=True)

# Render text for the inventory
def list_inventory(fish, screen, font, player):
    start_y = 150 # Start 150 pixels down from the screen
    start_x = 50 # 50 pixels away from the left side

    # Inventory title text
    title_text = font.render("Fish Caught:", True, "white")
    screen.blit(title_text,(start_x, start_y))
    start_y += 30

    # Display every item in the player's inventory
    for item in player.inventory:
        item_string = item.name + " (" + str(item.count) + ")"
        item_text = font.render(item_string, True, "gray")
        screen.blit(item_text, (start_x, start_y))
        start_y += 30

# Render the fish on the player's screen
def draw_fish(fish, screen, size):
    # Simple bobbing/swimming animation for the fish
    cycle = pygame.time.get_ticks()
    y_move = math.sin(cycle / 500) * 20
    x_move = math.cos(cycle / 2000) * 40

    # Get middle of screen, offset by animation numbers
    middle_posx = screen.get_width() / 2 + x_move
    middle_posy = screen.get_height() / 2 + y_move

    # Calculate the size of the fish to draw fish with modifiers
    size = calculate_size(fish, size)

    # Render the fish - Replace with tinted image of fish later
    pygame.draw.circle(screen, fish.color, (middle_posx, middle_posy), size)

# Calculate the size of a fish based on its attribute
def calculate_size(fish, size):
    match fish.attribute:
        case "Large":
            size = size * 1.5
        case "Massive":
            size = size * 4.0
        case "Small":
            size = size * 0.8
        case "Mini":
            size = size * 0.2
        case _:
            size = size
    return size

# Calculate monetary value of a fish
def calculate_value(fish, size):
    # Use fish attributes to calculate a size increase/decrease
    size = calculate_size(fish, size)

    # Use fish size, plus a random modifier to generate the fish price
    rand_price = random.randint(1, 10)
    price = round(size * rand_price / 20, 2)

    # For debug - Remove later
    print("Value:" + str(price))
    return price

# Render UI Text
def game_text(fish, screen, font, player):
    # Check if player has caught any fish yet, if so, render fish information
    if (player.fish_caught != 0):
        fishstring = "Recent Catch: " + fish.attribute + " " + fish.color + " " + fish.species
        text_fish_name = font.render(fishstring, True, "white")
        screen.blit(text_fish_name, (50, 50))

        balancestring = "Balance: " + str(int(player.balance)) + " coins"
        text_balance = font.render(balancestring, True, "gold")
        screen.blit(text_balance, (50, 100))

        list_inventory(fish, screen, font, player)

    else:
        fishstring = "press f to fish"
        text_fish_name = font.render(fishstring, True, "white")
        screen.blit(text_fish_name, (50, 50))

# Manage keyboard input
def manage_keyboard(current_fish, base_fish_size, player):
    keys = pygame.key.get_pressed()
    # If f key is pressed, generate fish
    if keys[pygame.K_f]:
        # Generate a random fish, update fish caught (for starting text)
        caught_fish = fish_generator.generate_fish(1)
        current_fish = caught_fish[0]
        player.fish_caught += 1

        # Calculate the value of the fish and add it to player balance
        fish_value = calculate_value(current_fish, base_fish_size)
        player.balance += fish_value

        # Add fish to player's inventory
        newitem = InvItem(current_fish.species, 1)
        add_inv_item(player, newitem)

        time.sleep(0.2) # Kinda hate that it freezes the whole program, find better cooldown

    return current_fish