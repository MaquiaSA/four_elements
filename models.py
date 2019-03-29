import arcade.key
import time
from random import randint as rint
from random import choice,randrange
from copy import deepcopy

PLATFORM_THICKNESS = 30
GROUND_THICKNESS = 100
MAP_GRID = 50

PLAYER_RADIUS = 10
GRAVITY = -1
MIN_VY = -20
JUMP_VY = 15
PLAYER_VX = 7

MONSTER_VX = 2
MONSTER_RADIUS = 40

BULLET_VX = 10
BULLET_RADIUS = 32
BULLET_RANGE = 250

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

DIR_OFFSET = {DIR_STILL: 0,
              DIR_RIGHT: 1,
              DIR_LEFT: -1}

MONSTER_DIR_OFFSET = {DIR_RIGHT: 1,
                      DIR_LEFT: -1}

GROUND_PLATFORM = 2

class Model:
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0
        self.direction = DIR_STILL

class Player(Model):
    def __init__(self,world,x,y):
        super().__init__(world,x,y)
        self.vx = PLAYER_VX
        self.current_direction = DIR_RIGHT
        self.is_jump = False
        self.count_jump = 0
    
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
        if self.x <= PLAYER_RADIUS or self.x - PLAYER_RADIUS >= self.world.width:
            self.direction = DIR_STILL
            if self.player_left() <= 0:
                self.x = PLAYER_RADIUS
            if self.player_right() >= self.world.width:
                self.x = self.world.width - PLAYER_RADIUS
    
    def check_floating(self,platforms):
        if self.is_jump or not self.check_platform(platforms):
            self.y += self.vy
            self.vy += GRAVITY
        if self.vy < MIN_VY:
            self.vy = MIN_VY

    def update(self,delta):
        self.x += DIR_OFFSET[self.direction] * self.vx
        self.check_out_of_world()
        self.set_current_direction()

        platforms = self.closest_platform()
        self.check_floating(platforms)
        
        self.check_platform(platforms)


class Bullet:
    def __init__(self,world,x,y):
        self.world = world
        self.init_x = x
        self.x = deepcopy(self.init_x)
        self.y = y
        self.direction = None
    
    def move(self):
        prev_direction = self.world.player.current_direction
        if not prev_direction == self.world.player.current_direction or self.direction is None:
            self.direction = prev_direction
        self.x += BULLET_VX * DIR_OFFSET[self.direction]
    
    def hit(self,monster):
        if self.y - BULLET_RADIUS <= monster.y <= self.y + BULLET_RADIUS and \
            self.x - BULLET_RADIUS <= monster.x <= self.x + BULLET_RADIUS:
            return True
    
    def out_of_world(self):
        if self.x + BULLET_RADIUS < 0 or self.x - BULLET_RADIUS > self.world.width:
            return True
    
    def update(self,delta):
        self.move()
        for m in self.world.monster:
            if self.hit(m):
                self.world.monster.remove(m)
                self.world.bullet.remove(self)
        if self.out_of_world() and not self.world.bullet:
            self.world.bullet.remove(self)
        if abs(self.x - self.init_x) >= BULLET_RANGE:
            self.world.bullet.remove(self)


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
    def __init__(self,world,x,y,platforms):
        super().__init__(world,x,y)
        self.platforms = platforms
        self.vx = MONSTER_VX
        self.direction = None
        self.current_direction = DIR_STILL
        self.update_tick = 60*choice([0.5,1,2])
    
    def random_direction(self):
        self.direction = choice(list(MONSTER_DIR_OFFSET))
    
    def move(self):
        if self.direction != DIR_STILL:
            self.current_direction = self.direction
        self.x += self.vx * DIR_OFFSET[self.direction]

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
            
    
    def update(self,delta):
        if self.direction is None:
            self.random_direction()
        self.move()
        self.monster_boarder()
        self.random_moving()
        pass


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self,50,100)
        self.platforms = self.platform_top() + \
            self.platform_mid() + self.platform_bot()
        self.monster = self.generate_monster()
        self.bullet = []
    
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
    
    def generate_monster(self):
        monster = []
        for p in self.platforms:
            monster_x1 = rint(p.platform_leftmost(),p.platform_rightmost())
            monster.append(Monster(self,monster_x1,p.y,p))
            # if p.width > 250:
            #     monster_x2 = rint(p.platform_leftmost(),p.platform_rightmost())
            #     monster.append(Monster(self,monster_x2,p.y))
        return monster


    def update(self,delta):
        self.player.update(delta)
        for m in self.monster:
            m.update(delta)
        for b in self.bullet:
            b.update(delta)

    
    def on_key_press(self,key,key_modifiers):
        if key == arcade.key.A:
            self.player.direction = DIR_LEFT
        elif key == arcade.key.D:
            self.player.direction = DIR_RIGHT
        elif key == arcade.key.SPACE and self.player.check_platform:
            self.player.jump()
        elif key == arcade.key.L:
            bullet = Bullet(self, self.player.x, self.player.y)
            self.bullet.append(bullet)
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.player.direction = DIR_STILL
