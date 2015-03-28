import in_game, map_gen, main, game_classes, vars
import math, itertools, pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, mouse_click_pos, lifetime, explode_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([in_game.block_size/2,in_game.block_size/2])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = self.pos[0] * in_game.block_size - in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size - in_game.camera_pos[1]
        self.starttick = pygame.time.get_ticks()

        self.damage = 10
        self.lifetime = lifetime
        self.explode_size = explode_size
        self.speed = 0.5

        # how many blocks the bullet moves at a time
        self.angle = math.atan2(mouse_click_pos[1] - self.pos[1], mouse_click_pos[0] - self.pos[0])
        self.speed_x = self.speed*math.cos(self.angle)
        self.speed_y = self.speed*math.sin(self.angle)


    def update(self, screen):
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y
        self.rect.x = self.pos[0] * in_game.block_size + in_game.camera_pos[0]
        self.rect.y = self.pos[1] * in_game.block_size + in_game.camera_pos[1]
        self.collision_detect(screen)
        self.delete()

    def explode(self, radius):
        radius = int((radius - 1) / 2)
        try:
            if radius != 0:
                for dy, dx in itertools.product(range(-radius, radius+1), repeat=2):
                        # kustutab kivi map_list'ist, uuendab kaarti ja minimapi
                        game_classes.block_delete(round(self.pos[1] + self.speed_y + dy), round(self.pos[0] + self.speed_x + dx))
            else:
                game_classes.block_delete(round(self.pos[1] + self.speed_y + dy), round(self.pos[0] + self.speed_x + dx))

        except: pass

    def collision_detect(self, screen):
        global bulletGroup, map_list
        try:
            if in_game.map_list[round(self.pos[1] + self.speed_y)][round(self.pos[0] + self.speed_x)] != 0:
                #in_game.map_list[round(self.pos[1] + self.speed_y)][round(self.pos[0] + self.speed_y)] = 0
                self.explode(self.explode_size)

                in_game.draw_map_surface(in_game.block_size)
                in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)


                in_game.bulletGroup.remove(self)
        except: in_game.bulletGroup.remove(self)

    def delete(self):
        if pygame.time.get_ticks() - self.starttick >= self.lifetime:
            in_game.bulletGroup.remove(self)
