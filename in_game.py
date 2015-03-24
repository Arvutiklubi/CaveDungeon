import pygame, map_gen, game_classes, main

map_size = 100
block_size = 16

mm_block_size, mm_surface_size = 2, 150

def fps_counter(screen, ms):
    fps_text = 'FPS: ' + str(1//(ms/1000))
    fps_surface = std_font.render(fps_text, False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))


def draw_minimap(block_size, surface_size):
    global minimap_surface
    row, column = 0, 0

    # v2rvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
        0 : (25, 25, 25),
        1 : (65, 65, 65),
        2 : (75, 75, 75),
        3 : (30,  0,  0),
        4 : (10, 100, 100),
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
    global map_surface

    # abistavad muutujad
    row = 0
    colomn = 0

    # värvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
        0 : (10, 10, 10),
        1 : (70, 70, 70),
        2 : (80, 80, 80),
        3 : (30,  0,  0),
        4 : (10, 100, 100),
    }

    # pind kuhu joonistatakse kaart
    map_surface = pygame.Surface((map_size*block_size, map_size*block_size))

    # kaardi joonistamine ridade kaupa
    for i in range(0, len(map_list)):
        for j in map_list[i]:
            map_surface.fill(colors[j], (block_size*colomn, block_size*row, block_size, block_size))
            colomn += 1
        row +=1
        colomn = 0


def init():
    global map_list, camera_pos, player1, World_map, std_font, enemy,enemyGroup, bullet, bulletGroup
    # init funktsioon kutsutakse mängu alguses korra, kõik muutujad mida kasutakatse üle mooduli või üle mängu peaksid olema deklareeritud siin

    # genereerib kaardi
    World_map = map_gen.Whole_map(map_size)

    # list mis sisaldab kaarti, y koord on esimene index x koord on teine index
    # esialgne map_list on world_mapi (0, 0) element. See juhtub olema Map objekt. Map objektist tahame map listi.
    map_list = World_map.map_dict[(0, 0)].map

    camera_pos = [0, 0]
    player1 = game_classes.player([10, 10])
    enemy = game_classes.Enemy()
    enemyGroup = pygame.sprite.Group()
    enemyGroup.add(enemy)
    bulletGroup = pygame.sprite.Group()

    # pind kuhu on joonistatud kaart
    draw_map_surface(block_size)
    draw_minimap(mm_block_size, mm_surface_size)

    # pygame'i standartne font
    std_font = pygame.font.Font(None, 16)


def on_event(event):
    global player1, mouse_click_pos
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

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click_pos = [(mouse_pos[0]-camera_pos[0])//block_size, (mouse_pos[1]-camera_pos[1])//block_size]
        if event.button == 1:
            player1.mine_block(mouse_click_pos)
        elif event.button == 3:
            #bullet = game_classes.ShootBullet(player1.pos, mouse_click_pos)
            #bulletGroup.add(bullet)
            player1.shoot(mouse_click_pos)

def draw(screen, ms):
    global camera_pos, World_map

    # kaamera asukoht on vaateakna üleval vasak nurk
    # kaamera asukoha arvutamine mängja asukoha järgi
    # x-suund : pool ekraanist + pool ruudu suurusest - mängja asukoht + 1 * ruudu suurus
    # y-suund : pool ekraanist - mängja asukoht * ruudu suurus
    # imelikud liitmised ja lahutamised on imeliku, sest.
    camera_pos = [main.screen_width//2 + block_size//2 - (player1.pos[0]+1) * block_size, main.screen_height//2 - (player1.pos[1]) * block_size]
    screen.blit(map_surface, camera_pos)

    # uuendame minimapi iga kaader
    screen.blit(minimap_update(mm_block_size, mm_surface_size, player1.pos), (main.screen_width - mm_surface_size, main.screen_height - mm_surface_size))

    # joonistab minimap'i indikaatori
    screen.fill((255, 0, 0), (main.screen_width - mm_surface_size//2 - 1, main.screen_height - mm_surface_size//2, mm_surface_size//50, mm_surface_size//50))



    player1.update(screen)
    enemyGroup.update(screen)
    enemyGroup.draw(screen)
    bulletGroup.update(screen)
    bulletGroup.draw(screen)


    # Kui lähed 10 sammu kaugusele mapi äärest genereeri sinna äärde uus map
    if map_gen.get_map_gen_direction(player1.pos, 10, map_size) != (0, 0):
        World_map.add_map((0, 0), map_gen.get_map_gen_direction(player1.pos, 10, map_size), map_size)


    fps_counter(screen, ms)