import pygame, sys, in_game, vars

# Ehk oleks ilus teha tekstifail selliste globaalsete muutujate jaoks?
screen_width, screen_height = 1200, 800 

def quit_funct():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # setting up
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('CaveDungeon v0.002')

    clock = pygame.time.Clock()
    ms = clock.tick(90)

    state = in_game

    state.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_funct()

            else:
                # funktsioon mis k2sitleb nupuvajutusi in_game.py moodulis
                state.get_vars()
                state.on_event(event)

        ms = clock.tick(90)

        screen.fill((80, 80, 80))

        # funktsioon joonistab ekraani in_game.py moodulis
        state.draw(screen, ms)
        pygame.display.flip()
