import pygame, map_gen, game_classes

def init():
    global map_list, map_surface

    #genereerib kaardi
    map_gen.generate_map(800, 800)

    #list mis sisaldab kaarti, y koord on esimene index x koord on teine index
    map_list = map_gen.map1.map
    #pind kuhu on joonistatud kaart
    map_surface = map_gen.map_surface

def on_event(event):
    pass

def draw(screen, ms):
    #joonistab kaardi ekraanile
    screen.blit(map_surface, (0, 0))

