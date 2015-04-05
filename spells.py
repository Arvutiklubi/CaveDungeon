import in_game, map_gen, main, game_classes, vars
import math, itertools, pygame, random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, mouse_click_pos, lifetime, explode_size, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([in_game.block_size/2,in_game.block_size/2])
        self.image.fill(color)
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

        self.particle_type = "fire"

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

        except: pass

    def collision_detect(self, screen):
        global bulletGroup, map_list
        try:
            if in_game.map_list[round(self.pos[1] + self.speed_y)][round(self.pos[0] + self.speed_x)] != 0:
                #in_game.map_list[round(self.pos[1] + self.speed_y)][round(self.pos[0] + self.speed_y)] = 0
                self.explode(self.explode_size)

                in_game.draw_minimap(in_game.mm_block_size, in_game.mm_surface_size)


                in_game.bulletGroup.remove(self)
        except: in_game.bulletGroup.remove(self)

    def delete(self):
        if pygame.time.get_ticks() - self.starttick >= self.lifetime:
            in_game.bulletGroup.remove(self)

class Fireparticle(Bullet):
    def __init__(self, pos, mouse_click_pos, lifetime, explode_size, color=(255, 10, 10)):
        Bullet.__init__(self, pos, mouse_click_pos, lifetime, explode_size, color)

    def update(self, screen):
        Bullet.update(self, screen)
        self.change_color()

    def change_color(self):
        time = pygame.time.get_ticks() - self.starttick
        _life_time = time / self.lifetime
        # prevent time imprecision errors
        if not _life_time * 255 < 255: _life_time = 1
        # make color change magic happen.
        rand = random.randint(1, 50)
        self.image.fill((255, int(255 - (_life_time * (255 - rand))), 50 - rand))

class Buff():
    def __init__(self, character, lifetime=1000):
        self.start_time = pygame.time.get_ticks()
        self.lifetime = lifetime
        character.add_buffs(self)


    def check_buff_timers(self, character):
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            character.rm_buffs(self)


class FireDamage(Buff):
    def __init__(self, character, damage=5):
        Buff.__init__(self, character, lifetime=500)
        self.damage = damage
        self.type = "fire"

    def Buff_effect(self, character):
        character.health -= self.damage


class SlowEffect(Buff):
    def __init__(self, character, slow=0.3):
        Buff.__init__(self, lifetime=500)
        self.slow = slow
        character.speed_x *= self.slow
        character.speed_y *= self.slow


    def Buff_effect(self, character):
        pass
