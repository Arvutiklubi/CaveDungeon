import pygame, map_gen, game_classes, main

map_size = 200
block_size = 13

mm_block_size, mm_surface_size = 2, 150

def fps_counter(screen, ms):
    fps_text = 'FPS: ' + str(1//(ms/1000))
    fps_surface = std_font.render(fps_text, False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))

def draw_minimap(block_size, surface_size, player_pos):
    global minimap_surface
    row, column = 0, 0

    #värvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
        0 : (25, 25, 25),
        1 : (65, 65, 65),
        2 : (75, 75, 75),
        'red' : (255, 0, 0)
    }

    # Pind, kuhu joonistatkase kaart
    minimap_surface = pygame.Surface((surface_size, surface_size))
    # Kaardi joonistamine ridade kaupa
    for i in range(0, len(map_list)):
        for j in map_list[i]:
            minimap_surface.fill(colors[j], (block_size * (column - player_pos[0]) + surface_size//2, block_size*(row - player_pos[1]) + surface_size //2, block_size, block_size))
            column += 1
        row +=1
        column = 0
    minimap_surface.fill(colors['red'], (surface_size//2 - 1, surface_size//2, surface_size//50, surface_size//50))

def draw_map_surface(block_size):
    global map_surface

    #abistavad muutujad
    row = 0
    colomn = 0

    #värvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
        0 : (10, 10, 10),
        1 : (70, 70, 70),
        2 : (80, 80, 80),
    }

    #pind kuhu joonistatakse kaart
    map_surface = pygame.Surface((map_size*block_size, map_size*block_size))

    #kaardi joonistamine ridade kaupa
    for i in range(0, len(map_list)):
        for j in map_list[i]:
            map_surface.fill(colors[j], (block_size*colomn, block_size*row, block_size, block_size))
            colomn += 1
        row +=1
        colomn = 0

def init():
    global map_list, camera_pos, player1, std_font

    #genereerib kaardi
    map_gen.generate_map(map_size, map_size)

    #list mis sisaldab kaarti, y koord on esimene index x koord on teine index
    map_list = map_gen.map1.map

    camera_pos = [0, 0]
    player1 = game_classes.player([10, 10])

    #pind kuhu on joonistatud kaart
    draw_map_surface(block_size)
    draw_minimap(mm_block_size, mm_surface_size, player1.pos)

    std_font = pygame.font.Font(None, 16)


def on_event(event):
    global player1
    global map1

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player1.speed_y = -1

        elif event.key == pygame.K_DOWN:
            player1.speed_y = 1

        elif event.key == pygame.K_LEFT:
            player1.speed_x = -1

        elif event.key == pygame.K_RIGHT:
            player1.speed_x = 1

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            player1.speed_y = 0

        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            player1.speed_x = 0

def draw(screen, ms):
    global camera_pos

    camera_pos = [main.screen_width//2 + block_size//2 - (player1.pos[0]+1) * block_size, main.screen_height//2 - (player1.pos[1]) * block_size]
    screen.blit(map_surface, camera_pos)

    # uuendame minimapi iga kaader
    draw_minimap(mm_block_size, mm_surface_size, player1.pos)
    screen.blit(minimap_surface, (main.screen_width - mm_surface_size, main.screen_height - mm_surface_size))

    player1.update(screen)

    fps_counter(screen, ms)
