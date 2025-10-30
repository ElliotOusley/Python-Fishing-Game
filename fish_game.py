import pygame
import fish_generator # Used to generate a random fish
import fish_utils # Contains functions and classes for the game
import classes

## Initial code copied from pygame documentation

def fish_game():

    # pygame setup
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    fish_images = fish_utils.load_fish_images() # Loads the array of fish images
    background_images = fish_utils.load_background_images(screen) #Loads the array of background images

    running = True

    #generate initial fish, same color as background, no names or attributes
    current_fish = classes.gameFish("", "black", "", 0)

    #Initialize the player
    player = classes.Player("Player", 0.0, 0, [])

    #Initialize Settings
    settings = classes.Settings("FPS off", 0)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Draw the background
        fish_utils.draw_background(background_images, settings.background, screen)

        # Draw the fish
        base_fish_size = 100
        if player.fish_caught != 0:
            fish_utils.draw_fish(current_fish, screen, base_fish_size, fish_images)

        # Test out mouse movement
        #mousePos = pygame.mouse.get_pos()
        #print(str(mousePos))

        clock.tick(60)  # limits FPS to 60
        current_fps = clock.get_fps()

        # Render text
        fish_utils.game_text(current_fish, screen, font, player, current_fps, settings)

        # Look for keyboard press, currently responsible for fish generation
        current_fish = fish_utils.manage_keyboard(current_fish, base_fish_size, player, settings)


        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()


    pygame.quit()





def main():
    fish_game()

if __name__ == "__main__":
    main()