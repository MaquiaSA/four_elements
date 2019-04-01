import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLATFORM_DRAW_THICKNESS = 10
PLATFORM_DRAW_Y_OFFSET = 24

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()

class BulletSprite:
    def __init__(self, bullet):
        self.bullet = bullet
        self.bullet_sprite = arcade.Sprite('images/coin.png')

    def draw(self):
        for b in self.bullet:
            self.bullet_sprite.set_position(b.x,b.y)
            self.bullet_sprite.draw()

class FourElementsRunWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.GRAY)

        self.world = World(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.player_sprite = ModelSprite('images/player.png',model=self.world.player,scale=0.24)
        self.bullet_sprite = BulletSprite(self.world.bullet)
        self.monster_bullet_sprite = BulletSprite(self.world.monster_bullet)
        
    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_rectangle_filled(p.x + (p.width//2),
                                         p.y - PLATFORM_DRAW_Y_OFFSET,
                                         p.width, PLATFORM_DRAW_THICKNESS,
                                         arcade.color.WHITE)
    
    def on_draw(self):
        arcade.start_render()
        self.player_sprite.draw()
        self.draw_platforms(self.world.platforms)
        for m in self.world.monster:
            ModelSprite('images/dot.png',model=m).draw()
        self.bullet_sprite.draw()
            
    def update(self, delta):
        self.world.update(delta)
        
    
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)


def main():
    window = FourElementsRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()