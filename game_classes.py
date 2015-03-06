import pygame, in_game, map_gen, main

#siia tulevad classid mängu objektide jaoks
class player():
    def __init__(self, pos):
        #players position is the position of the block that the characters legs are on

        self.pos = pos
        self.size = [in_game.block_size, 2*in_game.block_size] #the character is 1x2 blocks
        self.pos_onscreen = [main.screen_width//2 - self.size[0]/2, main.screen_height//2 - self.size[1]/2]

        self.health = 100
        self.max_health = 100

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

        if in_game.map_list[self.pos[1]+self.speed_y][self.pos[0]+self.speed_x] == 0 and self.pos[0]+self.speed_x >= 0 and self.pos[1]+self.speed_y >= 0 and self.pos[0]+self.speed_x < in_game.map_size and self.pos[1]+self.speed_y < in_game.map_size:
            return True
        else:
            return False
