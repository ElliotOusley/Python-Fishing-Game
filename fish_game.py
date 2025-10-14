import pygame
import fish_generator # Used to generate a random fish
import fish_utils # Contains functions and classes for the game

## Initial code copied from pygame documentation

def fish_game():

    # pygame setup
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    running = True

    #generate initial fish, same color as background, no names or attributes
    current_fish = fish_generator.gameFish("", "black", "")

    #Initialize the player
    player = fish_utils.Player("Player", 0.0, 0, [])

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Draw the fish
        base_fish_size = 40
        fish_utils.draw_fish(current_fish, screen, base_fish_size)

        # Render text
        fish_utils.game_text(current_fish, screen, font, player)

        # Look for keyboard press, currently responsible for fish generation
        current_fish = fish_utils.manage_keyboard(current_fish, base_fish_size, player)


        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()





def main():
    fish_game()

if __name__ == "__main__":
    main()