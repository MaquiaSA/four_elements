import arcade.key
from random import randint as rint

PLAYER_RADIUS = 20
PLATFORM_THICKNESS = 30

GRAVITY = -1
MIN_VY = -20
JUMP_VY = 20

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

DIR_OFFSET = {DIR_STILL: 0,
              DIR_RIGHT: 1,
              DIR_LEFT: -1}

GROUND_LEVEL = 100

class Model:
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y


class Player(Model):
    def __init__(self,world,x,y):
        super().__init__(world,x,y)
        self.vx = 10
        self.vy = 0
        self.direction = DIR_STILL
        self.current_direction = DIR_RIGHT
        self.is_jump = False
    
    def set_current_direction(self):
        if not self.direction == DIR_STILL:
            self.current_direction = self.direction
        
    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY
    
    def closest_platform(self):
        dx,dy = self.world.width, self.world.height
        platform = Platform(self.world,self.world.width,self.world.height,0)
        for p in self.world.platforms:
            if self.y >= p.y and self.y - p.y <= dy:
                if min(abs(self.x - p.left_most()), abs(self.x - p.right_most())) <= dx:
                    dx = min(abs(self.x - p.left_most()), abs(self.x - p.right_most()))
                    dy = self.y - p.y
                    platform = p
        return platform


    def check_platform(self,p):
        if p.left_most() <= self.x <= p.right_most() and p.bottom_most() <= self.y <= p.y:
            self.is_jump = False
            if 0 < self.x < self.world.width:
                self.vy = 0
                self.y = p.y
                return True
        if self.x <= 0 or self.x >= self.world.width:
            return True
        return False
    
    def check_out_of_world(self):
        if self.x <= PLAYER_RADIUS or self.x - PLAYER_RADIUS>= self.world.width:
            self.direction = DIR_STILL
            if self.x <= 0:
                self.x = PLAYER_RADIUS
            if self.x >= self.world.width:
                self.x = self.world.width - PLAYER_RADIUS

        
    def update(self,delta):
        self.x += DIR_OFFSET[self.direction] * self.vx
        self.check_out_of_world()
        self.set_current_direction()

        platform = self.closest_platform()
        if self.is_jump or not self.check_platform(platform):
            self.y += self.vy
            self.vy += GRAVITY
        if self.vy < MIN_VY:
            self.vy = MIN_VY
        
        self.check_platform(platform)



class Platform:
    def __init__(self,world,x,y,width):
        self.x = x
        self.y = y
        self.width = width
        self.thick = PLATFORM_THICKNESS
        self.world = world
    
    def left_most(self):
        return self.x
    
    def right_most(self):
        return self.x + self.width
    
    def bottom_most(self):
        return self.y - self.thick


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self,50,100)
        self.platforms = self.platform_top() + self.platform_mid() + self.platform_bot()
    
    def platform_top(self):
        x1,y1,width1 = rint(0,250),rint(400,500),rint(200,300)
        x2,y2,width2 = rint(400,600),rint(400,500),rint(200,300)
        return [Platform(self,x1,y1,width1),Platform(self,x2,y2,width2)]
    
    def platform_mid(self):
        x1,y1,width1 = rint(50,100),rint(250,300),rint(200,300)
        x2,y2,width2 = rint(250,300),rint(250,300),rint(200,300)
        x3,y3,width3 = rint(550,650),rint(250,300),rint(200,300)
        if x1 + width1 >= x2:
            return [Platform(self,x1,y1,x2 + width2 - x1),Platform(self,x3,y3,width3)]
        if x2 + width2 >= x3:
            return [Platform(self,x2,y2,x3 + width3 - x2),Platform(self,x1,y1,width1)]
        return [Platform(self,x1,y1,width1),Platform(self,x2,y2,width2),Platform(self,x3,y3,width3)]
    
    def platform_bot(self):
        x1,width1 = 0,rint(100,300)
        x2,width2 = rint(200,400),rint(200,300)
        x3,width3 = rint(500,600),300
        if x1 + width1 >= x2:
            if x2 + width2 >= x3:
                return [Platform(self,0,GROUND_LEVEL,self.width)]
            else:
                return [Platform(self,x1,GROUND_LEVEL,x2 + width2 - x1),Platform(self,x3,GROUND_LEVEL,width3)]
        if x2 + width2 >= x3:
            return [Platform(self,x2,GROUND_LEVEL,x3 + width3 - x2),Platform(self,x1,GROUND_LEVEL,width1)]
        return [Platform(self,x1,GROUND_LEVEL,width1),Platform(self,x2,GROUND_LEVEL,width2),Platform(self,x3,GROUND_LEVEL,width3)]
    

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