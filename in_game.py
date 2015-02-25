import pygame, map_gen, game_classes

map_size = 200 #jäta mõlemad numbrid alati võrdseks
block_size = 15

def draw_map_surface():
    global map_surface

    #abistavad muutujad
    row = 0
    colomn = 0

    #värvid millega joonistatakse kõnnitava ala ja kivimid
    colors = {
        0 : (10, 10, 10),
        1 : (150, 150, 150),
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
    global map_list, camera_pos, camera_speed_x, camera_speed_y

    #genereerib kaardi
    map_gen.generate_map(map_size, map_size)

    #list mis sisaldab kaarti, y koord on esimene index x koord on teine index
    map_list = map_gen.map1.map
    #pind kuhu on joonistatud kaart

    draw_map_surface()

    camera_pos = [0, 0]
    camera_speed_x = 0
    camera_speed_y = 0

def on_event(event):
    global camera_speed_x, camera_speed_y

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            camera_speed_y = 6

        elif event.key == pygame.K_DOWN:
            camera_speed_y = -6

        elif event.key == pygame.K_LEFT:
            camera_speed_x = 6

        elif event.key == pygame.K_RIGHT:
            camera_speed_x = -6

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            camera_speed_y = 0

        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            camera_speed_x = 0




def draw(screen, ms):
    global camera_pos

    camera_pos = [camera_pos[0]+camera_speed_x, camera_pos[1]+camera_speed_y]
    screen.blit(map_surface, camera_pos)

