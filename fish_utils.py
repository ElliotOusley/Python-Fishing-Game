import pygame
import fish_generator
import time
import random

class Player:
    def __init__(self, name, balance, fish_caught):
        self.name = name
        self.balance = balance
        self.fish_caught = fish_caught

def draw_fish(fish, screen, size):
    middle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    size = calculate_size(fish, size)

    pygame.draw.circle(screen, fish.color, middle_pos, size)

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

def calculate_value(fish, size):
    size = calculate_size(fish, size)

    rand_price = random.randint(1, 10)

    price = size * rand_price

    print("Value:" + str(price))
    return price

def game_text(fish, screen, font, player):
    if (player.fish_caught != 0):
        fishstring = fish.attribute + " " + fish.color + " " + fish.species
        text_fish_name = font.render(fishstring, True, "white")
        screen.blit(text_fish_name, (50, 50))

        balancestring = "Balance: " + str(player.balance) + " coins"
        text_balance = font.render(balancestring, True, "gold")
        screen.blit(text_balance, (50, 100))
    else:
        fishstring = "press f to fish"
        text_fish_name = font.render(fishstring, True, "white")
        screen.blit(text_fish_name, (50, 50))

def manage_keyboard(current_fish, base_fish_size, player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        caught_fish = fish_generator.generate_fish(1)
        current_fish = caught_fish[0]
        player.fish_caught += 1
        fish_value = calculate_value(current_fish, base_fish_size)
        player.balance += fish_value
        time.sleep(0.25)
    return current_fish