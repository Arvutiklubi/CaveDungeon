import pygame, in_game, map_gen

#siia tulevad classid mängu objektide jaoks
class player():
    def __init__(self, pos):
        #players position is the position of the block that the characters legs are on

        self.pos = pos
        self.size = [in_game.block_size, 2*in_game.block_size] #the character is 1x2 blocks
        self.pos_onscreen = [400-self.size[0]/2, 300-self.size[1]/2]

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

        self.pos = [self.pos[0]+self.speed_x, self.pos[1]+self.speed_y]

    def check_pos(self):
        global map1
        #esimene on vasakul;teine on paremal;kolmas on üleval;neljas on all
        kontroll=[0,0,0,0]
        c=[self.pos[0]*-1, self.pos[1]*-1]
        
        if map_gen.map1.map[c[1]][c[0]-1]==0:kontroll[0]=1
        if map_gen.map1.map[c[1]][c[0]+1]==0:kontroll[1]=1
        if map_gen.map1.map[c[1]-1][c[0]]==0:kontroll[2]=1
        if map_gen.map1.map[c[1]+1][c[0]]==0:kontroll[3]=1
        return kontroll
