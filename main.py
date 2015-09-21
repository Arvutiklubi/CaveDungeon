import pygame, sys, in_game, vars, map_gen
import multiprocessing

# Ehk oleks ilus teha tekstifail selliste globaalsete muutujate jaoks?
screen_width, screen_height = 1080, 720

def main():
    # setting up
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('CaveDungeon v0.002')

    clock = pygame.time.Clock()
    ms = clock.tick(50)

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

        ms = clock.tick(50)

        screen.fill((80, 80, 80))

        # funktsioon joonistab ekraani in_game.py moodulis
        state.draw(screen, ms)
        pygame.display.flip()

def quit_funct():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main_thread = multiprocessing.Process(target=main)
    main_thread.start()
