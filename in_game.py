import pygame, map_gen, game_classes, main, vars
from math import trunc

map_size = 75
block_size = 16

mm_block_size, mm_surface_size = 2, 150

def get_vars():
    global mouse_pos, mouse_index
    mouse_pos = pygame.mouse.get_pos()
    mouse_index = [(mouse_pos[0]-camera_pos[0])//block_size, (mouse_pos[1]-camera_pos[1])//block_size]

def fps_counter(screen, ms):
    fps_text = 'FPS: ' + str(1//(ms/1000))
    fps_surface = std_font.render(fps_text, False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))
    print(str(1//(ms/1000)))

def draw_minimap(block_size, surface_size):
    global minimap_surface
    row, column = 0, 0

    # v2rvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
         0 : ( 25,  25,  25),
         1 : ( 65,  65,  65),
         2 : ( 75,  75,  75),
         3 : ( 45,   0,   0),
         4 : (100,   0, 100),
        11 : ( 50, 100,   0),
        12 : ( 10, 100, 100),
        13 : (  0,  45,   0),

    }

    # Pind, kuhu joonistatkase kaart
    minimap_surface = pygame.Surface((map_size*block_size+surface_size, map_size*block_size+surface_size))
    minimap_surface.fill((0, 0, 0))

    for i in range(len(map_list)):
        for j in map_list[i]:
            minimap_surface.fill(colors[j], (block_size*column + surface_size//2, block_size*row + surface_size//2, block_size, block_size))
            column += 1
        row += 1
        column = 0

def minimap_update(block_size, surface_size, player_pos):
    minimap_seqment = minimap_surface.subsurface((block_size * player_pos[0], block_size * player_pos[1], surface_size, surface_size))
    return minimap_seqment

def draw_map_surface(block_size):
    global map_surface_dict

    # abistavad muutujad
    row = 0
    colomn = 0

    # värvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
         0 : ( 10,  10,  10),
         1 : ( 70,  70,  70),
         2 : ( 80,  80,  80),
         3 : ( 45,   0,   0),
         4 : (100,   0, 100),
        11 : (100, 100,  10),
        12 : ( 10, 100, 100),
        13 : (  0,  45,   0),
    }

    # pind kuhu joonistatakse kaart
    map_surface_dict = {}

    # kaardi joonistamine ridade kaupa
    for x in World_map.map_dict:
        #print(len(World_map.map_dict[x].map), len(World_map.map_dict[x].map[0]))
        map_surface_dict[x] = pygame.Surface((map_size*block_size, map_size*block_size))
        for i in range(len(World_map.map_dict[x].map)):
            for j in World_map.map_dict[x].map[i]:
                if j in terrain_textures:
                    map_surface_dict[x].blit(terrain_textures[j], (block_size*colomn, block_size*row))
                else:
                    map_surface_dict[x].fill(colors[j], (block_size*colomn, block_size*row, block_size, block_size))
                colomn += 1
            row +=1
            colomn = 0

        row = 0
        column = 0

def update_map():
    global whole_map_surface , map_surface_dict, map_update_queue, World_map
    #võtab listist kordinaadid ja blocki id ning muudab need map_surface'ilt ja map_listist
    colors = {
             0 : ( 10,  10,  10),
             1 : ( 70,  70,  70),
             2 : ( 80,  80,  80),
             3 : ( 45,   0,   0),
             4 : (100,   0, 100),
            11 : (100, 100,  10),
            12 : ( 10, 100, 100),
            13 : (  0,  45,   0),
        }

    greatest_positive_x1 = 0
    greatest_negative_x1 = 0
    greatest_positive_y1 = 0
    greatest_negative_y1 = 0

    for i in map_surface_dict:
        if i[0] > greatest_positive_x1 and i[0] > 0:
            greatest_positive_x1 = i[0]
        if i[0] < greatest_negative_x1 and i[0] < 0:
            greatest_negative_x1 = i[0]
        if i[1] > greatest_positive_y1 and i[1] > 0:
            greatest_positive_y1 = i[1]
        if i[1] < greatest_negative_y1 and i[1] < 0:
            greatest_negative_y1 = i[1]

    if len(map_update_queue) != 0:
        for i in range(len(map_update_queue)):
            map_chunk = []

            cord_y = map_update_queue[i][0] / 100
            if cord_y < 0:
                cord_y -= 1
            map_chunk.append(trunc(cord_y))

            cord_x = map_update_queue[i][1] / 100
            if cord_x < 0:
                cord_x -= 1
            map_chunk.append(trunc(cord_x))

            World_map.map_dict[tuple(map_chunk)].map[map_update_queue[i][0]][map_update_queue[i][1]] = map_update_queue[i][2]


            if map_update_queue[i][2] in terrain_textures:
                map_surface_dict[tuple(map_chunk)].blit(terrain_textures[map_update_queue[i][2]], (map_update_queue[i][1]*block_size, map_update_queue[i][0]*block_size))
                whole_map_surface.blit(terrain_textures[map_update_queue[i][2]], (((abs(greatest_negative_x1) + map_chunk[0])*map_size + map_update_queue[i][1])*block_size, ((greatest_positive_y1 - map_chunk[1])*map_size + map_update_queue[i][0])*block_size))

            else:
                map_surface_dict[tuple(map_chunk)].fill(colors[map_update_queue[i][2]], (map_update_queue[i][1]*block_size, map_update_queue[i][0]*block_size, block_size, block_size))
                whole_map_surface.fill(colors[map_update_queue[i][2]], (((abs(greatest_negative_x1) + map_chunk[0])*map_size + map_update_queue[i][1])*block_size, ((greatest_positive_y1 - map_chunk[1])*map_size + map_update_queue[i][0])*block_size, block_size, block_size))

    for j in World_map.map_dict:
        for i in World_map.map_dict[tuple(j)].dropped_items:

            map_surface_dict[j].fill(colors[4], (i[1]*block_size, i[0]*block_size, block_size, block_size))
            whole_map_surface.fill(colors[4], (((abs(greatest_negative_x1) + j[0])*map_size + i[1])*block_size, ((greatest_positive_y1 - j[1])*map_size + i[0])*block_size, block_size, block_size))

    map_update_queue = []

def join_maps():
    global World_map, map_surface_dict, whole_map_surface, greatest_negative_x, greatest_positive_y, greatest_positive_x, greatest_negative_y

    whole_map_size_x = 0
    whole_map_size_y = 0

    greatest_positive_x = 0
    greatest_negative_x = 0
    greatest_positive_y = 0
    greatest_negative_y = 0

    for i in map_surface_dict:
        if i[0] > greatest_positive_x and i[0] > 0:
            greatest_positive_x = i[0]
        if i[0] < greatest_negative_x and i[0] < 0:
            greatest_negative_x = i[0]
        if i[1] > greatest_positive_y and i[1] > 0:
            greatest_positive_y = i[1]
        if i[1] < greatest_negative_y and i[1] < 0:
            greatest_negative_y = i[1]

    whole_map_size_x = greatest_positive_x + abs(greatest_negative_x) + 1
    whole_map_size_y = greatest_positive_y + abs(greatest_negative_y) + 1

    whole_map_surface = pygame.Surface((whole_map_size_x*map_size*block_size, whole_map_size_y*map_size*block_size))

    for i in map_surface_dict:
        whole_map_surface.blit(map_surface_dict[i], ((abs(greatest_negative_x) + i[0]) * map_size * block_size, (greatest_positive_y - i[1]) * map_size * block_size))

def init():
    global map_list, camera_pos, player1, World_map, std_font, enemy,enemyGroup, bullet, bulletGroup, map_update_queue, whole_map_surface, terrain_textures
    # init funktsioon kutsutakse mängu alguses korra, kõik muutujad mida kasutakatse üle mooduli või üle mängu peaksid olema deklareeritud siin

    terrain_textures = {
        2: pygame.image.load('generic_rock.png')
    }

    for i in terrain_textures:
        pygame.transform.scale(terrain_textures[i], (block_size, block_size))

    # genereerib kaardi
    World_map = map_gen.Whole_map(map_size)

    # list mis sisaldab kaarti. y koord on esimene index, x koord on teine index
    # esialgne map_list on world_mapi (0, 0) element. See juhtub olema Map objekt. Map objektist tahame map listi.
    map_list = World_map.map_dict[(0, 0)].map

    #list kuhu lähevad kaardi muudatused, vorm = [y, x, block_ID]
    map_update_queue = []

    camera_pos = [0, 0]
    player1 = game_classes.player([10, 10])
    enemy = game_classes.Enemy()
    enemyGroup = pygame.sprite.Group()
    enemyGroup.add(enemy)
    bulletGroup = pygame.sprite.Group()

    # pind kuhu on joonistatud kaart
    draw_map_surface(block_size)
    join_maps()
    draw_minimap(mm_block_size, mm_surface_size)

    # pygame'i standartne font
    std_font = pygame.font.Font(None, 16)

def on_event(event):
    global player1, mouse_click_pos, map_surface_dict
    global map1

    if event.type == pygame.MOUSEMOTION and player1.flamethrower:
        mouse_click_pos = [(event.pos[0]-camera_pos[0])//block_size, (event.pos[1]-camera_pos[1])//block_size]

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player1.speed_y = -1

        elif event.key == pygame.K_DOWN:
            player1.speed_y = 1

        elif event.key == pygame.K_LEFT:
            player1.speed_x = -1

        elif event.key == pygame.K_RIGHT:
            player1.speed_x = 1

        elif event.key == pygame.K_e:
            player1.display_inventory()

        elif event.key == pygame.K_p:
            pygame.image.save(whole_map_surface, 'pic.jpeg')

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            player1.speed_y = 0

        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            player1.speed_x = 0

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_click_pos = [(mouse_pos[0]-camera_pos[0])//block_size, (mouse_pos[1]-camera_pos[1])//block_size]
        if event.button == 1:
            player1.mine_block(mouse_click_pos)
        elif event.button == 3:
            #bullet = game_classes.Bullet(player1.pos, mouse_click_pos)
            #bulletGroup.add(bullet)
            player1.shoot(mouse_click_pos)
        elif event.button == 2:
            #player1.flip()
            player1.flamethrower = True

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 2:
            #player1.flip()
            player1.flamethrower = False

def draw(screen, ms):
    global camera_pos, World_map

    # kaamera asukoht on vaateakna üleval vasak nurk
    # kaamera asukoha arvutamine mängja asukoha järgi
    # x-suund : pool ekraanist + pool ruudu suurusest - mängja asukoht + 1 * ruudu suurus
    # y-suund : pool ekraanist - mängja asukoht * ruudu suurus
    # imelikud liitmised ja lahutamised on imeliku, sest.

    camera_pos = [main.screen_width//2 + block_size//2 - (player1.pos[0]+1) * block_size, main.screen_height//2 - (player1.pos[1]) * block_size]

    round(camera_pos[0], -1)
    round(camera_pos[1], -1)

    update_map()

    screen.blit(whole_map_surface, (camera_pos[0]-abs(greatest_negative_x)*map_size*block_size, camera_pos[1]-greatest_positive_y*map_size*block_size))

    player1.update(screen, mouse_index)

    enemyGroup.update(screen)
    enemyGroup.draw(screen)
    bulletGroup.update(screen)
    bulletGroup.draw(screen)

    # uuendame minimapi iga kaader
    screen.blit(minimap_update(mm_block_size, mm_surface_size, player1.pos), (main.screen_width - mm_surface_size, main.screen_height - mm_surface_size))

    # joonistab minimap'i indikaatori
    screen.fill((255, 0, 0), (main.screen_width - mm_surface_size//2 - 1, main.screen_height - mm_surface_size//2, mm_surface_size//50, mm_surface_size//50))

    # Kui lähed 10 sammu kaugusele mapi äärest genereeri sinna äärde uus map
    if map_gen.get_map_gen_direction(player1.pos, 10, map_size) != (0, 0):
        current_map = (0, 0)
        map_gen_dir = map_gen.get_map_gen_direction(player1.pos, 10, map_size)
        World_map.add_map((0, 0), map_gen_dir, map_size)
        x, y = map_gen_dir
        # Kui liigume diagonaalis, magic
        if abs(x) + abs(y) == 2:
            World_map.add_map(current_map, (x, 0), map_size)
            World_map.add_map(current_map, (0, y), map_size)



    fps_counter(screen, ms)