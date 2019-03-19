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
        self.is_jump = False
        
    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def check_platform(self):
        for p in self.world.platforms:
            if p.left_most() <= self.x <= p.right_most() and self.y == p.y:
                self.is_jump = False
                self.vy = 0
                return True
        if self.x <= 0 or self.x >= self.world.width:
            return True
        return False
        
        
    def update(self,delta):
        self.x += DIR_OFFSET[self.direction] * self.vx
        if self.x < 0 or self.x > self.world.width:
            self.direction = DIR_STILL

        if self.is_jump or not self.check_platform():
            self.y += self.vy
            self.vy += GRAVITY

        self.check_platform()



class Platform:
    def __init__(self,world,x,y,width):
        self.x = x
        self.y = y
        self.width = width
        self.world = world
    
    def left_most(self):
        return self.x - 1
    
    def right_most(self):
        return self.x + self.width + 1


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self,50,100)
        self.platforms = [Platform(self,0,100,rint(100,500))]
    
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