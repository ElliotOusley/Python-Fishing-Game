import pygame
import math
import fish_utils

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
    size = fish_utils.calculate_size(fish, size)

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


def draw_background(background_images, imgnum, screen):
    # Draw background
    screen.fill((50, 50, 50))  # Super dark gray
    screen.blit(background_images[imgnum], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Overlay dock image on gray background

