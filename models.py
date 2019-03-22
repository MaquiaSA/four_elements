import arcade.key
from random import randint as rint

PLAYER_RADIUS = 10
PLATFORM_THICKNESS = 30
MAP_GRID = 20

GRAVITY = -1
MIN_VY = -20
JUMP_VY = 15

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

DIR_OFFSET = {DIR_STILL: 0,
              DIR_RIGHT: 1,
              DIR_LEFT: -1}

GROUND_PLATFORM = 5

class Model:
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y


class Player(Model):
    def __init__(self,world,x,y):
        super().__init__(world,x,y)
        self.vx = 8
        self.vy = 0
        self.direction = DIR_STILL
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
        platform = Platform(self.world,self.world.width,self.world.height,0)
        for p in self.world.platforms:
            if self.y >= p.y and self.y - p.y <= dy:
                if min(abs(self.x - p.p_left_most()), abs(self.x - p.p_right_most())) <= dx:
                    dx = min(abs(self.x - p.p_left_most()), abs(self.x - p.p_right_most()))
                    dy = self.y - p.y
                    platform = p
        return platform

    def stay_on_platform(self,platform):
        self.is_jump = False
        self.count_jump = 0
        self.vy = 0
        self.y = platform.y

    def check_player_boarder(self,player_boarder,platform):
        if platform.p_left_most() <= player_boarder <= platform.p_right_most() and \
            platform.p_bottom_most() <= self.y <= platform.y:
            if 0 < self.x < self.world.width:
                self.stay_on_platform(platform)
                return True


    def check_platform(self,platform):
        self.check_player_boarder(self.player_right(),platform)
        self.check_player_boarder(self.player_left(),platform)
        if not 0 < self.x < self.world.width:
            return True
        return False
    
    def check_out_of_world(self):
        if self.x <= PLAYER_RADIUS or self.x - PLAYER_RADIUS >= self.world.width:
            self.direction = DIR_STILL
            if self.x <= 0:
                self.x = PLAYER_RADIUS
            if self.x >= self.world.width:
                self.x = self.world.width - PLAYER_RADIUS
    
    def check_floating(self,platform):
        if self.is_jump or not self.check_platform(platform):
            self.y += self.vy
            self.vy += GRAVITY
        if self.vy < MIN_VY:
            self.vy = MIN_VY

    def update(self,delta):
        self.x += DIR_OFFSET[self.direction] * self.vx
        self.check_out_of_world()
        self.set_current_direction()

        platform = self.closest_platform()
        self.check_floating(platform)
        
        self.check_platform(platform)



class Platform:
    def __init__(self,world,x,y,width):
        self.x = x
        self.y = y
        self.width = width
        self.thick = PLATFORM_THICKNESS
        self.world = world
    
    def p_left_most(self):
        return self.x
    
    def p_right_most(self):
        return self.x + self.width
    
    def p_bottom_most(self):
        return self.y - self.thick


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self,50,100)
        self.platforms = self.platform_top() + \
            self.platform_mid() + self.platform_bot()
    
    def platform_top(self):
        x1,y1,width1 = rint(0,10),rint(20,22),rint(10,15)
        x2,y2,width2 = rint(26,30),rint(20,22),rint(10,15)
        return [self.platform_grid(x1,y1,width1),
                self.platform_grid(x2,y2,width2)]
    
    def platform_mid(self):
        x1,y1,width1 = rint(0,5),rint(12,15),rint(10,15)
        x2,y2,width2 = rint(25,30),rint(10,15),rint(10,15)
        x3,y3,width3 = rint(55,65),rint(12,15),rint(10,15)
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
        x1,width1 = 0,rint(5,15)
        x2,width2 = rint(10,20),rint(10,15)
        x3,width3 = rint(25,30),15
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

    def update(self,delta):
        self.player.update(delta)
    
    def on_key_press(self,key,key_modifiers):
        if key == arcade.key.LEFT:
            self.player.direction = DIR_LEFT
        elif key == arcade.key.RIGHT:
            self.player.direction = DIR_RIGHT
        elif key == arcade.key.SPACE and self.player.check_platform:
            self.player.jump()
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.direction = DIR_STILL