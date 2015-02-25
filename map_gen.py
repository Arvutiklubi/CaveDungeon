import pygame
import random
import itertools


class Map:
    # Generates map with height and width
    #	 0 representing walkable area, 1 stone wall,
    #	 numbers onward different types of minerals.
    #	 mineral generation needs to be explicit.

    #   Todo flood fill to find cave-system size
    #   More optimal way to represent the map than Rect objects.
    #   Ability to create maps on different scales
    #   Ability to merge two maps into one.
    #   generate maps with different characteristics
    def __init__(self, width, height):
        self.height, self.width = height, width
        self.map = [[random.randint(0, 1) for i in range(self.width)] for j in range(self.height)]
        self.Rect_map = []
        self.Mineral_map = []
        self.Mineral_map2 = []
        self.Mineral_map3 = []

    def print_map(self):
        # Help function to visualise map from command line.
        print_dictionary = {
            0: ' ',  # Walkable area
            1: '#',  # Stone wall
            2: 'x',  # mineral 1
            3: '+',  # mineral 2
            4: '*'   # mineral 3
        }
        display_map = [[0 for i in range(self.width)] for j in range(self.height)]
        for x, y in itertools.product(range(self.width), range(self.height)):
            # Get print value from print_dictionary
            display_map[y][x] = print_dictionary[self.map[y][x]]
        # Hard work of printing it out
        for item in display_map:
            print(item[0], ' '.join(map(str, item[1:])))
        print('\n')
        return

    def map_iter(self, iter_rule):
        # single step of iteration to iterate through the map
        #self.print_map()
        new_map = [[0 for i in range(self.width)] for j in range(self.height)]
        for x, y in itertools.product(range(self.width), range(self.height)):
            new_map[y][x] = iter_rule(x, y)
        self.map = new_map
        return

    # Returns the number of adjacent blocks that are not empty
    def count_blocks(self, x, y, grid_sz):
        # magic constant making it more intuitive to use.
        a = int((grid_sz - 1) / 2)
        count = 0
        # iterates through all the blocks in grid_sz x grid_sz box.
        for dx, dy in itertools.product(range(-a, a + 1), repeat=2):
            # Don't count the square we are on.
            if not (dx == dy == 0):
                # ignore going outside of the map
                try:
                    if self.map[y + dy][x + dx]:
                        count += 1
                except: pass
        return count

    # Magical function that generates aesthetic (smooth) maps. Nobody knows why. Shouldn't work.
    def count_blocks2(self, x, y, grid_sz=3):
        # coverting grid_sz
        a = int((grid_sz - 1) / 2)
        count = 0
        # iterates through all the blocks in grid_sz x grid_sz box.
        for dx, dy in itertools.product(range(-1, a + 1), repeat=2):
            # Don't count the square we are on.
            if not (dx == dy == 0):
                # ignore going outside of the map
                try:
                    if self.map[x + dx][y + dy]:
                        count += 1
                except: pass
        return count

    def iter_rule(self, x, y):
        # Defines what happens to cell on iteration.
        grid_sz = 3
        count = self.count_blocks2(x, y, grid_sz)
        if count >= 4 and self.map[x][y]:
            return 1
        elif count >= 5 and not self.map[x][y]:
            return 1
        else:
            return 0

    def iter_rule2(self, x, y):
        grid_sz = 5
        count = self.count_blocks2(x, y, grid_sz)
        if count <= 6 and self.map[x][y]:
            return 1
        elif count <= 7 and not self.map[x][y]:
            return 1
        else:
            return 0

    # Generates pygame.Rect objects list of the map
    # Does not currently include minerals being different
    def convert_Rect(self, box_sz):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 1:
                    self.Rect_map.append(pygame.Rect(box_sz * x, box_sz * y, box_sz, box_sz))
                if self.map[y][x] == 2:
                    self.Mineral_map.append(pygame.Rect(box_sz * x, box_sz * y, box_sz, box_sz))
                if self.map[y][x] == 3:
                    self.Mineral_map2.append(pygame.Rect(box_sz * x, box_sz * y, box_sz, box_sz))
                if self.map[y][x] == 4:
                    self.Mineral_map3.append(pygame.Rect(box_sz * x, box_sz * y, box_sz, box_sz))

    def generate_minerals(self, probability, probability2, grid_sz, id):
        # Iterates through all the tiles and if it is stone wall, makes it mineral "id" with some probability.
        # Probability2 denotes the amount of cells not empty around. a
        for y in range(self.height):
            for x in range(self.width):
                # gives the probability that mineral spawns at possible spawn locations
                if self.map[y][x] and probability >= random.random():
                    # defines the possible spawn locations regarding what is around the spawn location.
                    # if the tile has so and so many stone tiles around it.
                    # making possible to make some minerals spawn deep within walls
                    # and some near cave walls.
                    if self.count_blocks(x, y, grid_sz) >= probability2:
                        self.map[y][x] = id
        self.print_map()
        return

    def enlarge_map(self):
        # makes the map bigger by generating new map from the old but enlarging each pixel to enlarging_coe**2 pixels
        enlarging_coe = 2  # should be <type int>
        new_map = [[0 for i in range(enlarging_coe * self.width)] for j in range(enlarging_coe * self.height)]
        # Iterates through the whole map if it finds a block that is not empty, copies it to new_map
        # After copying the original block also makes blocks next to it filled in.
        for x, y in itertools.product(range(self.width), range(self.height)):
            for dx, dy in itertools.product(range(enlarging_coe), repeat=2):
                if self.map[y][x]:
                    new_map[enlarging_coe * y + dy][enlarging_coe * x + dx] = self.map[y][x]
        self.map = [[0 for i in range(enlarging_coe * self.width)] for j in range(enlarging_coe * self.height)]
        self.width, self.height = enlarging_coe * self.width, enlarging_coe * self.height
        self.map = new_map
        self.print_map()


def generate_map(width, height):
    global map_surface, map1

    background = pygame.Surface((800, 600))
    background = background.convert()
    background.fill((0, 0, 0))

    # Generating the map
    map_color = (100, 100, 100)
    mineral_color = (75, 75, 75)
    mineral_color2 = (50, 50, 50)
    mineral_color3 = (25, 25, 25)
    box_sz = 20
    map1 = Map(width, height)
    # iterates map according to the iteration rule defined. Allows for different iteration schemes
    # making it possible to develop more complex maps and regions with different characteristics
    for i in range(7): map1.map_iter(map1.iter_rule2)
    map1.generate_minerals(probability=1, id=2, probability2=3**2-1, grid_sz=3)
    #map1.generate_minerals(probability=1, id=3, probability2=5**2-1, grid_sz=5)
    #map1.generate_minerals(probability=1, id=4, probability2=7**2-1, grid_sz=7)

    map1.convert_Rect(box_sz)

    map_surface = pygame.Surface((width, height))

        # Drawing part
    map_surface.blit(background, (0, 0))
    for rect in map1.Rect_map:
        pygame.draw.rect(map_surface, map_color, rect)
    for mineral in map1.Mineral_map:
        pygame.draw.rect(map_surface, mineral_color, mineral)
    for mineral2 in map1.Mineral_map2:
        pygame.draw.rect(map_surface, mineral_color2, mineral2)
    for mineral3 in map1.Mineral_map3:
        pygame.draw.rect(map_surface, mineral_color3, mineral3)
