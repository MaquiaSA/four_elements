import arcade.key
import time
from random import randint as rint
from random import choice,randrange
from copy import deepcopy

PLATFORM_THICKNESS = 30
GROUND_THICKNESS = 100
MAP_GRID = 50

PLAYER_RADIUS = 15
GRAVITY = -1
MIN_VY = -20
JUMP_VY = 15
PLAYER_VX = 7
PLAYER_STARTX = 50
PLAYER_STARTY = 100
HEALTH = 100
MELEE_RANGE = 60
MELEE_UPDATE = 3

MONSTER_VX = 2
MONSTER_RADIUS = 40
DETECT_PLAYER_X = 250
DETECT_PLAYER_Y = 30
M_BULLET_VX = 10
MONSTER_DMG = 5

BULLET_VX = 20
BULLET_RADIUS = 32
BULLET_RANGE = 300
BULLET_DMG = 60
RANGE_START = 30

SCORE_WIN = 1500
SCORE_DRAW = 1000
SCORE_LOSE = 750
SCORE_MELEE = 1800


DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

DIR_OFFSET = {DIR_STILL: 0,
              DIR_RIGHT: 1,
              DIR_LEFT: -1}

MONSTER_DIR_OFFSET = {DIR_RIGHT: 1,
                      DIR_LEFT: -1}

FIRE = 0
WATER = 1
EARTH = 2
WIND = 3
NORMAL = 4
#               dmg vs ->   Fi    Wa    Ea    Wi    N
ELEMENT_OFFSET = {FIRE:   (1.00, 0.75, 1.00, 1.25, 1.00), #    FIRE>WIND>EARTH>WATER>FIRE
                  WATER:  (0.75, 1.00, 1.25, 1.00, 1.00),
                  EARTH:  (1.00, 1.25, 1.00, 0.75, 1.00),
                  WIND:   (1.25, 1.00, 0.75, 1.00, 1.00),
                  NORMAL: (1.00, 1.00, 1.00, 1.00, 1.00)}

SHIELD_OFFSET = {FIRE:   (0.5, 0.8, 0.5, 0.0, 0.5),
                 WATER:  (0.0, 0.5, 0.8, 0.5, 0.5),
                 EARTH:  (0.5, 0.0, 0.5, 0.8, 0.5),
                 WIND:   (0.8, 0.5, 0.0, 0.5, 0.5),
                 NORMAL: (0.5, 0.5, 0.5, 0.5, 0.5)}

M_ELEMENT_LIST = [FIRE, WATER, EARTH, WIND]

GROUND_PLATFORM = 2

class Model:
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0
        self.direction = DIR_STILL
        self.is_hit = False
        self.is_dead = False
        self.health = None
    
    def check_dead(self):
        if self.health <= 0:
            self.is_dead = True
        if self.is_dead:
            self.health = 0

class Player(Model):
    def __init__(self,world,x,y):
        super().__init__(world,x,y)
        self.idle = True

        self.vx = PLAYER_VX
        self.current_direction = DIR_RIGHT

        self.count_jump = 0
        self.is_jump = False

        self.health = HEALTH
        self.prev_health = HEALTH
        
        self.element = NORMAL
        self.melee_frame = 0

        self.power = 0
        self.dmg_reduce = 1
        self.shield = False

    def move(self):
        self.x += DIR_OFFSET[self.direction] * self.vx
    
    def set_current_direction(self):
        if not self.direction == DIR_STILL:
            self.current_direction = self.direction
        
    def jump(self):
        if self.count_jump <= 1:
            self.is_jump = True
            self.vy = JUMP_VY
            self.count_jump += 1
        
    def player_left(self):
        return self.x - PLAYER_RADIUS
    
    def player_right(self):
        return self.x + PLAYER_RADIUS
        
    def player_top(self):
        return self.y + PLAYER_RADIUS
        
    def player_bot(self):
        return self.y - PLAYER_RADIUS
    
    def closest_platform(self):
        dx,dy = self.world.width, self.world.height
        platforms = Platform(self.world,self.world.width,self.world.height,0)
        for p in self.world.platforms:
            if self.y >= p.y and self.y - p.y <= dy:
                if min(abs(self.x - p.platform_leftmost()),
                    abs(self.x - p.platform_rightmost())) <= dx:
                    dx = min(abs(self.x - p.platform_leftmost()), 
                        abs(self.x - p.platform_rightmost()))
                    dy = self.y - p.y
                    platforms = p
        return platforms

    def stay_on_platform(self,platforms):
        self.is_jump = False
        self.count_jump = 0
        self.vy = 0
        self.y = platforms.y

    def check_player_boarder(self,player_boarder,platforms):
        if platforms.platform_leftmost() <= player_boarder <= platforms.platform_rightmost() and \
            platforms.platform_bottommost() <= self.y <= platforms.y:
            if 0 < self.x < self.world.width:
                self.stay_on_platform(platforms)
                return True

    def check_platform(self,platforms):
        self.check_player_boarder(self.player_right(),platforms)
        self.check_player_boarder(self.player_left(),platforms)
        if not 0 < self.x < self.world.width:
            return True
        return False
    
    def check_out_of_world(self):
        if self.player_left() <= 0 or self.player_right() >= self.world.width:
            self.direction = DIR_STILL
            if self.player_left() <= 0:
                self.x = PLAYER_RADIUS
            if self.player_right() >= self.world.width:
                self.x = self.world.width - PLAYER_RADIUS
        if self.y < 0:
            self.health = 0
    
    def check_floating(self,platforms):
        if self.is_jump or not self.check_platform(platforms):
            self.y += self.vy
            self.vy += GRAVITY
        if self.vy < MIN_VY:
            self.vy = MIN_VY
    
    def check_is_hit(self):
        if self.prev_health > self.health:
            self.is_hit = True
            self.prev_health = self.health
        else:
            self.is_hit = False
    
    def check_shield(self):
        if self.power >= 100:
            self.power = 100
        # if self.power == 100 or self.shield:
        #     self.shield = True
        if self.power <= 0:
            self.shield = False
            self.power = 0
        if self.shield:
            self.power -= 0.2 * self.world.floor
            if self.health <= 100:
                self.health += 0.1
            else:
                self.health = 100

    def update(self,delta):
        self.move()
        self.check_out_of_world()
        self.set_current_direction()

        platforms = self.closest_platform()
        self.check_floating(platforms)
        
        self.check_platform(platforms)
        self.check_is_hit()
        self.check_shield()
        self.check_dead()


class Bullet:
    def __init__(self,world,x,y):
        self.world = world
        self.init_x = x
        self.x = deepcopy(self.init_x)
        self.y = y
        self.direction = None
    
    def out_of_world(self):
        if self.x + BULLET_RADIUS < 0 or self.x - BULLET_RADIUS > self.world.width:
            return True


class PlayerBullet(Bullet):
    def __init__(self,world,x,y):
        super().__init__(world,x,y)
        self.element = self.world.player.element
    
    def move(self):
        prev_direction = self.world.player.current_direction
        if not prev_direction == self.world.player.current_direction or \
            self.direction is None:
            self.direction = prev_direction
        self.x += BULLET_VX * DIR_OFFSET[self.direction]
    
    def hit(self,monster):
        if self.y - BULLET_RADIUS <= monster.y <= self.y + BULLET_RADIUS and \
            self.x - BULLET_RADIUS <= monster.x <= self.x + BULLET_RADIUS:
            return True
    
    def increase_power(self, power):
        if self.world.player.power < 100:
            self.world.player.power += power

    def increase_world_score(self, m):
        dmg_modifier = ELEMENT_OFFSET[self.world.player.element][m.element]
        if dmg_modifier == 1.25:
            self.world.score += SCORE_WIN
        elif dmg_modifier == 1.00:
            self.world.score += SCORE_DRAW
        elif dmg_modifier == 0.75:
            self.world.score += SCORE_LOSE

    def update(self,delta):
        self.move()
        if self.out_of_world():
            if self.world.bullet != []:
                self.world.bullet.remove(self)
        elif self.x - self.init_x > BULLET_RANGE or self.init_x - self.x > BULLET_RANGE:
            if self.world.bullet != []:
                self.world.bullet.remove(self)
        for m in self.world.monster:
            if self.hit(m):
                m.health -= BULLET_DMG * ELEMENT_OFFSET[self.world.player.element][m.element]
                if not self.world.player.shield:
                    self.increase_power(2)
                    if m.health <= 0:
                        self.increase_power(3)
                if m.health <= 0:
                    self.world.monster.remove(m)
                    self.increase_world_score(m)
                if self in self.world.bullet:
                    self.world.bullet.remove(self)

class MonsterBullet(Bullet):
    def __init__(self,world,x,y,monster):
        super().__init__(world,x,y)
        self.monster = monster
        self.element = monster.element
    
    def move(self):
        prev_direction = self.monster.current_direction
        if not prev_direction == self.monster.current_direction or self.direction is None:
            self.direction = prev_direction
        self.x += M_BULLET_VX * DIR_OFFSET[self.direction]
        # self.direction = self.monster.current_direction
        # self.x += M_BULLET_VX * DIR_OFFSET[self.direction]
    
    def hit(self):
        if self.y - BULLET_RADIUS <= self.world.player.y <= self.y + BULLET_RADIUS and \
            self.x - BULLET_RADIUS <= self.world.player.x <= self.x + BULLET_RADIUS:
            return True
    
    def update(self,delta):
        self.move()
        if self.hit():
            self.world.monster_bullet.remove(self)
            if self.world.player.power == 100:
                self.world.player.shield = True
            if self.world.player.shield:
                self.world.player.dmg_reduce = SHIELD_OFFSET[self.world.player.element][self.element]
            else:
                self.world.player.dmg_reduce = 1
            self.world.player.health -= \
                (self.world.floor/2) *\
                    ELEMENT_OFFSET[self.monster.element][self.world.player.element] *\
                    self.world.player.dmg_reduce
        elif abs(self.x - self.init_x) >= BULLET_RANGE:
            self.world.monster_bullet.remove(self)
        elif self.out_of_world() and self.world.monster_bullet != []:
            self.world.monster_bullet.remove(self)


class Melee:
    def __init__(self,world):
        self.world = world
        self.x = self.world.player.x
        self.y = self.world.player.y
        self.frame = -1
        self.melee_update = 1
    
    def update(self,delta):
        if self.frame != -1:
            self.frame += 1
        if self.frame == MELEE_UPDATE:
            self.melee_update += 1
            self.frame = 0
        if self.melee_update > 3:
            self.frame = -1
            self.melee_update = 1



class Platform:
    def __init__(self,world,x,y,width):
        self.x = x
        self.y = y
        self.width = width
        if self.y == GROUND_PLATFORM * MAP_GRID:
            self.thick = GROUND_THICKNESS
        else:
            self.thick = PLATFORM_THICKNESS
        self.world = world
    
    def platform_leftmost(self):
        return self.x
    
    def platform_rightmost(self):
        return self.x + self.width
    
    def platform_bottommost(self):
        return self.y - self.thick


class Monster(Model):
    TICK = 0
    def __init__(self,world,x,y,platforms,health):
        super().__init__(world,x,y)
        self.platforms = platforms
        self.vx = MONSTER_VX
        self.direction = None
        self.current_direction = DIR_STILL
        self.update_tick = 60*choice([0.5,1,2])
        self.health = health
        self.prev_health = health
        self.element = choice(M_ELEMENT_LIST)
    
    def random_direction(self):
        self.direction = choice(list(MONSTER_DIR_OFFSET))
    
    def dead(self):
        if self.health <= 0:
            self.is_dead = True
        
    def check_is_hit(self):
        if self.health != self.prev_health:
            self.is_hit = True
            self.prev_health = self.health
        else:
            self.is_hit = False

    def move(self):
        if self.direction != DIR_STILL:
            self.current_direction = self.direction
        self.x += self.vx * DIR_OFFSET[self.direction]
        self.monster_boarder()
        self.random_moving()

    def random_moving(self):
        self.TICK += 1
        if self.TICK % self.update_tick == 0:
            if self.direction == DIR_STILL:
                self.vx = MONSTER_VX
                if self.x <= self.platforms.platform_leftmost() or\
                    self.x <= 10:
                    self.direction = DIR_RIGHT
                if self.x >= self.platforms.platform_rightmost() or\
                    self.x >= self.world.width - 10:
                    self.direction = DIR_LEFT
                else:
                    self.random_direction()
            else:
                self.direction = DIR_STILL
    
    def check_monster_boarder(self):
        if self.x <= 10 or \
            self.x >= self.world.width - 10 or \
            self.x <= self.platforms.platform_leftmost() or \
            self.x >= self.platforms.platform_rightmost():
            return False
        return True
    
    def monster_boarder(self):
        if not self.check_monster_boarder():
            if self.x <= 10:
                self.x = 10
            if self.x >= self.world.width - 10:
                self.x = self.world.width - 10
            if self.x <= self.platforms.platform_leftmost():
                self.x = self.platforms.platform_leftmost()
            if self.x >= self.platforms.platform_rightmost():
                self.x = self.platforms.platform_rightmost()
            self.vx = 0
            self.direction = DIR_STILL
    
    def detect_player(self):
        if self.y - DETECT_PLAYER_Y <= self.world.player.y <= self.y + DETECT_PLAYER_Y:
            if self.x - DETECT_PLAYER_X <= self.world.player.x <= self.x:
                self.direction = DIR_STILL
                self.current_direction = DIR_LEFT
                return True
            elif self.x <= self.world.player.x <= self.x + DETECT_PLAYER_X:
                self.direction = DIR_STILL
                self.current_direction = DIR_RIGHT
                return True
            return False
        return False
    
    def update(self,delta):
        if self.direction is None:
            self.random_direction()
        self.move()
        self.check_is_hit()
        self.check_dead()
        if self.is_dead:
            self.world.monster.remove(self)


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self,PLAYER_STARTX,PLAYER_STARTY)
        self.player_melee = Melee(self)
        self.bullet = []
        self.monster_bullet = []
        self.monster_health = 100
        self.floor = 0
        self.score = 0
        self.floor_delay = 0
        self.setup()
    
    def setup(self):
        self.floor += 1
        self.player.x = PLAYER_STARTX
        self.player.y = PLAYER_STARTY
        self.player.idle = True
        self.player.current_direction = DIR_RIGHT
        self.player.is_dead = False
        self.platforms = self.platform_top() + \
            self.platform_mid() + self.platform_bot()
        self.monster = self.generate_monster()

    
    def platform_top(self):
        x1,y1,width1 = rint(0,4),rint(8,9),rint(4,6)
        x2,y2,width2 = rint(10,12),rint(8,9),rint(4,6)
        return [self.platform_grid(x1,y1,width1),
                self.platform_grid(x2,y2,width2)]
    
    def platform_mid(self):
        x1,y1,width1 = rint(0,2),rint(5,6),rint(4,6)
        x2,y2,width2 = rint(10,12),rint(4,6),rint(4,6)
        x3,y3,width3 = rint(22,26),rint(5,6),rint(4,6)
        if x1 + width1 >= x2:
            return [self.platform_grid(x1,y1,x2 + width2 - x1),
                    self.platform_grid(x3,y3,width3)]
        if x2 + width2 >= x3:
            return [self.platform_grid(x2,y2,x3 + width3 - x2),
                    self.platform_grid(x1,y1,width1)]
        return [self.platform_grid(x1,y1,width1),
                self.platform_grid(x2,y2,width2),
                self.platform_grid(x3,y3,width3)]
    
    def platform_bot(self):
        x1,width1 = 0,rint(2,6)
        x2,width2 = rint(5,8),rint(4,6)
        x3,width3 = rint(10,12),6
        if x1 + width1 >= x2:
            if x2 + width2 >= x3:
                return [self.platform_grid(0,GROUND_PLATFORM,self.width)]
            else:
                return [self.platform_grid(x1,GROUND_PLATFORM,x2 + width2 - x1),
                        self.platform_grid(x3,GROUND_PLATFORM,width3)]
        if x2 + width2 >= x3:
            return [self.platform_grid(x2,GROUND_PLATFORM,x3 + width3 - x2),
                    self.platform_grid(x1,GROUND_PLATFORM,width1)]
        return [self.platform_grid(x1,GROUND_PLATFORM,width1),
                self.platform_grid(x2,GROUND_PLATFORM,width2),
                self.platform_grid(x3,GROUND_PLATFORM,width3)]
    
    def platform_grid(self,x,y,width):
        return Platform(self,x*MAP_GRID,y*MAP_GRID,width*MAP_GRID)
    
    def mon_health(self):
        return self.monster_health + (self.floor*10)
    
    def generate_monster(self):
        monster = []
        for p in self.platforms:
            monster_x1 = rint(p.platform_leftmost(),p.platform_rightmost())
            if 0 <= monster_x1 <= self.width:
                if p.y == GROUND_PLATFORM*MAP_GRID and \
                    abs(monster_x1-self.player.x) > BULLET_RANGE:
                    monster.append(Monster(self,monster_x1,p.y,p,self.mon_health()))
                elif p.y != GROUND_PLATFORM*MAP_GRID:
                    monster.append(Monster(self,monster_x1,p.y,p,self.mon_health()))
            if p.width > 250:
                monster_x2 = rint(p.platform_leftmost(),p.platform_rightmost())
                if 0 <= monster_x2 <= self.width:
                    if p.y == GROUND_PLATFORM*MAP_GRID and \
                        abs(monster_x2-self.player.x) > BULLET_RANGE:
                        monster.append(Monster(self,monster_x2,p.y,p,self.mon_health()))
                    elif p.y != GROUND_PLATFORM*MAP_GRID:
                        monster.append(Monster(self,monster_x2,p.y,p,self.mon_health()))
        return monster

    def monster_detect_player(self,monster):
        if monster.detect_player() and monster.TICK % (62-(2*self.floor)) == 0:
            m_bullet = MonsterBullet(self,
                monster.x,
                monster.y,
                monster)
            self.monster_bullet.append(m_bullet)
    
    def melee_attack(self):
        self.player.melee_frame = 0
        for m in self.monster:
            if m.x in range(self.player.player_left(), self.player.player_right() + MELEE_RANGE) and \
                m.y in range(self.player.player_bot(), self.player.player_top()) and \
                self.player.current_direction == DIR_RIGHT:
                self.player.element = m.element
                m.health = 0
                self.score += SCORE_MELEE
            elif m.x in range(self.player.player_left() - MELEE_RANGE, self.player.player_right()) and \
                m.y in range(self.player.player_bot(), self.player.player_top()) and \
                self.player.current_direction == DIR_LEFT:
                self.player.element = m.element
                m.health = 0
                self.score += SCORE_MELEE

    def update(self,delta):
        self.player.update(delta)
        self.player_melee.update(delta)
        for m in self.monster:
            m.update(delta)
            self.monster_detect_player(m)
        for b in self.bullet:
            b.update(delta)
        for mb in self.monster_bullet:
            mb.update(delta)
        if not self.monster:
            self.floor_delay += 1
            if self.floor_delay == 20:
                self.setup()
                self.floor_delay = 0

    
    def on_key_press(self,key,key_modifiers):
        if key == arcade.key.A:
            self.player.direction = DIR_LEFT
            self.player.idle = False
        elif key == arcade.key.D:
            self.player.direction = DIR_RIGHT
            self.player.idle = False
        elif key == arcade.key.SPACE and self.player.check_platform:
            self.player.jump()
            self.player.idle = False
        elif key == arcade.key.K:
            bullet = PlayerBullet(self,
                self.player.x,
                self.player.y)
            self.bullet.append(bullet)
            self.player.idle = False
        elif key == arcade.key.J:
            self.player_melee.frame = 0
            self.melee_attack()
            self.player.idle = False
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.A and self.player.direction == DIR_LEFT:
            self.player.direction = DIR_STILL
            self.player.idle = False
        if key == arcade.key.D and self.player.direction == DIR_RIGHT:
            self.player.direction = DIR_STILL
            self.player.idle = False
