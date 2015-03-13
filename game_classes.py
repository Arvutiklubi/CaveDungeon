import pygame, in_game, map_gen, main, random, math, itertools

# Omadused, mida k6ik characterid peaksid omama
class Character:
    def __init__(self, pos, health=100, max_health=100):
        self.pos = pos
        self.speed_x = 0
        self.speed_y = 0
        self.health = health
        self.max_health = max_health

    def collision_detect(self):
        self.dir = ""
        if self.pos[0]+self.speed_x >= 0 and self.pos[1]+self.speed_y >= 0 and self.pos[0]+self.speed_x < in_game.map_size and self.pos[1]+self.speed_y < in_game.map_size:
            if in_game.map_list[self.pos[1]+self.speed_y][self.pos[0]+self.speed_x] == 0:
                return True
            elif in_game.map_list[self.pos[1]][self.pos[0]+self.speed_x] != 0 and in_game.map_list[self.pos[1]+self.speed_y][self.pos[0]] == 0:
                self.dir = "y"
            elif in_game.map_list[self.pos[1]+self.speed_y][self.pos[0]] != 0 and in_game.map_list[self.pos[1]][self.pos[0]+self.speed_x] == 0:
                self.dir = "x"
            else:
                return False
        else:
            return False

    def rand_create_character(self):
        thatWillDo = False
        while not thatWillDo:
            pos = [random.randint(30, in_game.map_size-30), random.randint(30, in_game.map_size-30)]
            if in_game.map_list[pos[1]][pos[0]] == 0:
                thatWillDo = True
        return pos

# Omadused, mis on iseloomulikud vastastele
class Enemy(Character, pygame.sprite.Sprite):
    def __init__(self, pos=None):
        pygame.sprite.Sprite.__init__(self)
        # if no position is given generate randomly, else generate with the position given
        if pos is None:
            Character.__init__(self, Character.rand_create_character(self))
        else:
            Character.__init__(self, self.pos)

        self.image = pygame.Surface([in_game.block_size, 2*in_game.block_size])
        self.image.fill((0,255,255))
        self.rect = self.image.get_rect()

        self.rect.x = self.pos[0] * in_game.block_size - in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size - in_game.camera_pos[1]

    def update(self, screen):
        self.rect.x = self.pos[0] * in_game.block_size + in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size + in_game.camera_pos[1]

# Omadused, mis on iseloomulikud playerile
class player(Character):
    def __init__(self, pos):
        # players position is the position of the block that the player legs are on
        Character.__init__(self, self.rand_create_character())
        self.size = [in_game.block_size, 2*in_game.block_size] # the player is 1x2 blocks
        self.pos_onscreen = [main.screen_width//2 - self.size[0]/2, main.screen_height//2 - self.size[1]/2]
        self.color = [255, 10, 10]

        self.block_mine_range = 5.5

    def update(self, screen):
        # esimene: kolmnurga alus; teine: vasak haar; kolmas: parem haar
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), 3)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)

        if self.collision_detect():
            self.pos = [self.pos[0]+self.speed_x, self.pos[1]+self.speed_y]
        elif self.dir == "y":
            self.pos = [self.pos[0], self.pos[1]+self.speed_y]
        elif self.dir == "x":
            self.pos = [self.pos[0]+self.speed_x, self.pos[1]]

    def mine_block(self, mouse_click_pos):
                try:
                    if (((mouse_click_pos[0] - self.pos[0])**2 + (mouse_click_pos[1] - self.pos[1])**2)**(0.5)) <= self.block_mine_range:
                        for dy, dx in itertools.product(range(-1, 2), repeat=2):
                            # kustutab kivi map_list'ist, uuendab kaarti ja minimapi
                            in_game.map_list[mouse_click_pos[1] + dy][mouse_click_pos[0] + dx] = 0
                except: pass

                in_game.draw_map_surface(in_game.block_size)
                in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)
                in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)

    def shoot(self, mouse_click_pos):
        global bulletGroup
        bullet = ShootBullet(self.pos, mouse_click_pos)
        bulletGroup.add(bullet)

class ShootBullet(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_click_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([in_game.block_size/2,in_game.block_size/2])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.pos = player_pos
        self.mouse_click_pos = mouse_click_pos
        self.rect.x = self.pos[0] * in_game.block_size - in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size - in_game.camera_pos[1]

        # how many blocks the bullet moves at a time
        self.speed_x = 0.5
        self.speed_y = 0.5
        self.angle = math.atan2(self.mouse_click_pos[1] - self.pos[1], self.mouse_click_pos[0] - self.pos[0])

        self.damage = 10

    def update(self, screen):
        self.pos[0] += self.speed_x * math.cos(self.angle)
        self.pos[1] += self.speed_y * math.sin(self.angle)
        self.rect.x = self.pos[0] * in_game.block_size + in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size + in_game.camera_pos[1]

    def collision_detect(self):
        if self.pos[0]+self.speed_x*math.cos(self.angle) >= 0 and self.pos[1]+self.speed_y*math.sin(self.angle) >= 0 and self.pos[0]+self.speed_x*math.cos(self.angle) < in_game.map_size and self.pos[1]+self.speed_y*math.sin(self.angle) < in_game.map_size:
            if in_game.map_list[self.pos[1]+self.speed_y*math.sin(self.angle)][self.pos[0]+self.speed_x** math.sin(self.angle)] == 1:
                try:
                    for dy, dx in itertools.product(range(-1, 2), repeat=2):
                        # kustutab kivi map_list'ist, uuendab kaarti ja minimapi
                            in_game.map_list[self.mouse_click_pos[1] + dy][self.mouse_click_pos[0] + dx] = 0
                except: pass


            else:
                return False
        else:
            return False

        in_game.draw_map_surface(in_game.block_size)
        in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)
        in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)