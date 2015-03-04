import pygame, sys, in_game

def quit_funct():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    #setting up
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Cave')
    pygame.display.set_caption('CaveDungeon v0.001')

    clock = pygame.time.Clock()
    ms = clock.tick(40)

    state = in_game

    state.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_funct()

            else:
                #funktsioon mis käsitleb nupuvajutusi in_game.py moodulis
                state.on_event(event)

        ms = clock.tick(30)

        screen.fill((80, 80, 80))

        #funktsioon joonistab ekraani in_game.py moodulis
        state.draw(screen, ms)
        pygame.display.flip()
