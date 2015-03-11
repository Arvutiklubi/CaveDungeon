import pygame, in_game, map_gen, main, random, math, itertools

#siia tulevad classid mängu objektide jaoks
class player():
    def __init__(self, pos):
        #players position is the position of the block that the characters legs are on

        self.pos = self.create_player()
        self.size = [in_game.block_size, 2*in_game.block_size] #the character is 1x2 blocks
        self.pos_onscreen = [main.screen_width//2 - self.size[0]/2, main.screen_height//2 - self.size[1]/2]

        self.health = 100
        self.max_health = 100
        self.block_mine_range = 5.5

        #how many blocks the character moves at a time
        self.speed_x = 0
        self.speed_y = 0

        self.color = [255, 10, 10]

    def update(self, screen):
        #esimene: kolmnurga alus; teine: vasak haar; kolmas: parem haar
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), 3)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)
        pygame.draw.line(screen, self.color, (self.pos_onscreen[0]+self.size[0], self.pos_onscreen[1]+self.size[1]), (self.pos_onscreen[0]+self.size[0]/2, self.pos_onscreen[1]), 2)

        if self.collision_detect():
            self.pos = [self.pos[0]+self.speed_x, self.pos[1]+self.speed_y]

    def collision_detect(self):
        # True kui liigutav koordinaat on legaalne
        # Hendrik, mida kuradit?! Paneme paar and'i veel? :D
        # Tegin natuke paremaks, aga ainult selle pärast, et see tööle hakkaks. See rida oli väga ilus !

        if self.pos[0]+self.speed_x >= 0 and self.pos[1]+self.speed_y >= 0 and self.pos[0]+self.speed_x < in_game.map_size and self.pos[1]+self.speed_y < in_game.map_size:
            if in_game.map_list[self.pos[1]+self.speed_y][self.pos[0]+self.speed_x] == 0:
                return True
            else:
                return False
        else:
            return False

    def mine_block(self, mouse_click_pos):
        if in_game.map_list[mouse_click_pos[1]][mouse_click_pos[0]] != 0:
            if (((mouse_click_pos[0] - self.pos[0])**2 + (mouse_click_pos[1] - self.pos[1])**2)**(0.5)) <= self.block_mine_range:
                try:
                    for dy, dx in itertools.product(range(-1, 2), repeat=2):
                        # kustutab kivi map_list'ist, uuendab kaarti ja minimapi
                        in_game.map_list[mouse_click_pos[1] + dy][mouse_click_pos[0] + dx] = 0

                        in_game.draw_map_surface(in_game.block_size)
                        in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)
                        in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)
                except: pass

    def create_player(self):
        thatWillDo = False
        while not thatWillDo:
            pos = [random.randint(30, in_game.map_size-30), random.randint(30, in_game.map_size-30)]
            if in_game.map_list[pos[1]][pos[0]] == 0:
                thatWillDo = True
        return pos

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([in_game.block_size,2*in_game.block_size])
        self.image.fill((0,255,255))
        self.rect = self.image.get_rect()
        self.pos = self.create_enemy()
        self.rect.x = self.pos[0] * in_game.block_size - in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size - in_game.camera_pos[1]

        self.health = 100
        self.max_health = 100

        #how many blocks the character moves at a time
        self.speed_x = 0
        self.speed_y = 0

    def update(self, screen):
        self.rect.x = self.pos[0] * in_game.block_size + in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size + in_game.camera_pos[1]

    def collision_detect(self):
        # True kui liigutav koordinaat on legaalne
        # Hendrik, mida kuradit?! Paneme paar and'i veel? :D
        # Tegin natuke paremaks, aga ainult selle pärast, et see tööle hakkaks. See rida oli väga ilus !

        if self.pos[0]+self.speed_x >= 0 and self.pos[1]+self.speed_y >= 0 and self.pos[0]+self.speed_x < in_game.map_size and self.pos[1]+self.speed_y < in_game.map_size:
            if in_game.map_list[self.pos[1]+self.speed_y][self.pos[0]+self.speed_x] == 0:
                return True
            else:
                return False
        else:
            return False

    def mine_block(self, mouse_click_pos):
        if in_game.map_list[mouse_click_pos[1]][mouse_click_pos[0]] == 1 or in_game.map_list[mouse_click_pos[1]][mouse_click_pos[0]] == 2:
            #kustutab kivi map_list'ist, uuendab kaarti ja minimapi
            in_game.map_list[mouse_click_pos[1]][mouse_click_pos[0]] = 0

            in_game.draw_map_surface(in_game.block_size)
            in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)

    def create_enemy(self):
        thatWillDo = False
        while not thatWillDo:
            pos = [random.randint(30, in_game.map_size-30), random.randint(30, in_game.map_size-30)]
            if in_game.map_list[pos[1]][pos[0]] == 0:
                thatWillDo = True
        return pos
