import arcade.key

GRAVITY = -1
JUMP_VY = 15

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
        self.is_jump = True
        self.vy = JUMP_VY
        
    def update(self,delta):
        self.x += DIR_OFFSET[self.direction] * self.vx
        if self.x < 0:
            self.x = 0
        if self.x > self.world.width:
            self.x = self.world.width
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY



class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self,50,100)
    
    def update(self,delta):
        self.player.update(delta)
    
    def on_key_press(self,key,key_modifiers):
        if key == arcade.key.LEFT:
            self.player.direction = DIR_LEFT
        elif key == arcade.key.RIGHT:
            self.player.direction = DIR_RIGHT
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.direction = DIR_STILL