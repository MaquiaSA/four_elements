import arcade.key
from random import randint as rint

GRAVITY = -1
JUMP_VY = 20

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

DIR_OFFSET = {DIR_STILL: 0,
              DIR_RIGHT: 1,
              DIR_LEFT: -1}

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
    
    def bottom_y(self):
        return self.y - 0
    
    def set_current_direction(self):
        if not self.direction == DIR_STILL:
            self.current_direction = self.direction
        
    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY
    
    def closest_platform(self):
        dx,dy = self.world.width, self.world.height
        platform = Platform(self.world,0,0,0)
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
            self.vy = 0
            self.y = p.y
            return True
        if self.x <= 0 or self.x >= self.world.width:
            return True
        return False
    
    def check_out_of_world(self):
        if self.x <= 0 or self.x >= self.world.width:
            self.direction = DIR_STILL
            if self.x <= 0:
                self.x = 0
            if self.x >= self.world.width:
                self.x = self.world.width

        
    def update(self,delta):
        self.x += DIR_OFFSET[self.direction] * self.vx
        self.check_out_of_world()
        self.set_current_direction()

        platform = self.closest_platform()
        if self.is_jump or not self.check_platform(platform):
            self.y += self.vy
            self.vy += GRAVITY
            if self.vy > 40:
                self.vy = 40
            if self.vy < -40:
                self.vy = -40
        
        self.check_platform(platform)



class Platform:
    def __init__(self,world,x,y,width):
        self.x = x
        self.y = y
        self.width = width
        self.thick = 30
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
        self.platforms = [
            Platform(self,rint(0,200),rint(200,300),rint(100,300)), Platform(self,rint(250,500),rint(200,300),rint(100,300)), Platform(self,rint(550,800),rint(200,300),rint(100,300)),
            Platform(self,0,100,rint(100,300)), Platform(self,300,100,rint(100,300)), Platform(self,500,100,rint(100,300))
            ]
    
    def generate_platform_top(self):
        x1,y1,width1 = rint(200,300),rint(400,500),rint(100,300)
        x2,y2,width2 = rint(600,800),rint(400,500),rint(100,300)
        while x1 + width1 < x2:
            width1 = rint(100,300)
        self.platforms.append(Platform(self,x1,y1,width1))
        self.platforms.append(Platform(self,x2,y2,width2))

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