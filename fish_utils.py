import pygame
import fish_generator
import fish_data
import random
import math # Used in fish animation
import classes


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
    player.inventory.append(classes.InvItem(item.name, item.count))
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
def draw_fish(fish, screen, size, fish_images):
    # Simple bobbing/swimming animation for the fish
    cycle = pygame.time.get_ticks()
    y_move = math.sin(cycle / 500) * 20
    x_move = math.cos(cycle / 2000) * 40

    # Get middle of screen, offset by animation numbers
    middle_posx = screen.get_width() / 2 + x_move

    middle_posy = screen.get_height() / 2 + y_move

    # Calculate the size of the fish to draw fish with modifiers
    size = calculate_size(fish, size)

    fish_img = fish_images[fish.dex_number]

    # Render the fish as an actual image
    scale_size = size*2
    scaled_fish = pygame.transform.smoothscale(fish_img, (scale_size, scale_size))
    tinted_fish = tint(scaled_fish, fish.color, 1)

    screen.blit(tinted_fish, (middle_posx - scale_size //2, middle_posy - scale_size // 2))

## Adapted from pygame wiki
## https://www.pygame.org/wiki/Tint
def tint(image, tint_color, alpha):
    # Break named color into rgba values
    r, g, b, a = pygame.Color(tint_color)

    #Get surface, preserving transparency
    tint_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    tint_surface.fill((r, g, b, int(a * alpha)))

    tinted_image = image.copy()

    ## Render with a multiply layer
    tinted_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return tinted_image

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
def game_text(fish, screen, font, player, fps, settings):
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

    if(settings.fps == "FPS on"):
        fpsstring = str(int(fps))

        if fps >= 50:
            text_fps = font.render(fpsstring, True, "green")
        elif fps >= 30:
            text_fps = font.render(fpsstring, True, "yellow")
        elif fps <= 30:
            text_fps = font.render(fpsstring, True, "red")
        else:
            text_fps = font.render(fpsstring, True, "white")
        screen.blit(text_fps, (1200, 50))

# Manage keyboard input
def manage_keyboard(current_fish, base_fish_size, player, settings):
    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()
    cooldowns = fish_data.cooldowns
    # If f key is pressed, generate fish
    if keys[pygame.K_f] and now - cooldowns['f'] > 200:
        # Generate a random fish, update fish caught (for starting text)
        caught_fish = fish_generator.generate_fish(1)
        current_fish = caught_fish[0]
        player.fish_caught += 1

        # Calculate the value of the fish and add it to player balance
        fish_value = calculate_value(current_fish, base_fish_size)
        player.balance += fish_value

        # Add fish to player's inventory
        newitem = classes.InvItem(current_fish.species, 1)
        add_inv_item(player, newitem)

        cooldowns['f'] = now

    if keys[pygame.K_z] and now - cooldowns['z'] > 200:
        if settings.fps == "FPS on":
            settings.fps = "FPS off"
        else:
            settings.fps = "FPS on"
        cooldowns['z'] = now
        print(settings.fps)

    if keys[pygame.K_x] and now - cooldowns['x'] > 200:
        samebackground = True
        while(samebackground):
            newbackground = random.randint(0, len(fish_data.background_image) - 1)
            if newbackground == settings.background:
                samebackground = True

            else:
                samebackground = False
                settings.background = newbackground

        cooldowns['x'] = now

    return current_fish

# https://www.reddit.com/r/pygame/comments/dx2oja/i_was_trying_to_load_some_images_into_pygame_is

def load_fish_images():
    fish_images = {}
    for index, f in enumerate(fish_data.fish_image):
        image = pygame.image.load(f).convert_alpha()
        fish_images[index] = image
    return fish_images

def load_background_images(screen):
    screen_size = (screen.get_width(), screen.get_height())
    background_images = {}
    for index, f in enumerate(fish_data.background_image):
        image = pygame.image.load(f).convert_alpha()
        scaled_image = pygame.transform.scale(image, screen_size)
        background_images[index] = scaled_image
    return background_images

def draw_background(background_images, imgnum, screen):
    # Draw background
    screen.fill((50, 50, 50))  # Super dark gray
    screen.blit(background_images[imgnum], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Overlay dock image on gray background

