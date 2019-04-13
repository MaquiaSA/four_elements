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
 
        self.setup()
    
    def setup(self):
        arcade.set_background_color(arcade.color.GRAY)

        self.world = World(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.player_sprite = self.player()
        self.bullet_sprite = BulletSprite(self.world.bullet)
        self.monster_bullet_sprite = BulletSprite(self.world.monster_bullet)

    def player(self):
        if self.world.player.current_direction == 2:
            player_sprite = ModelSprite('images/player-'+str(self.world.player.element)+'_left.png',
                                        model=self.world.player,scale=0.24)
        else:
            player_sprite = ModelSprite('images/player-'+str(self.world.player.element)+'_right.png',
                                        model=self.world.player,scale=0.24)
        return player_sprite

    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_rectangle_filled(p.x + (p.width//2),
                                         p.y - PLATFORM_DRAW_Y_OFFSET,
                                         p.width, PLATFORM_DRAW_THICKNESS,
                                         arcade.color.WHITE)
    
    def draw_monster(self):
        for m in self.world.monster:
            if m.current_direction == -1:
                ModelSprite('images/dot.png',model=m,mirrored=True).draw()
            else:
                ModelSprite('images/dot.png',model=m).draw()
    
    def hp_bar(self):
        arcade.draw_xywh_rectangle_filled(75, SCREEN_HEIGHT - 50,
                                            self.world.player.health * 2.5,
                                            20,arcade.color.RED)
        arcade.draw_xywh_rectangle_outline(75, SCREEN_HEIGHT - 50,
                                            250,20,arcade.color.BLACK)

    def power_bar(self):
        arcade.draw_xywh_rectangle_filled(75, SCREEN_HEIGHT - 70,
                                            self.world.player.power * 2.5,
                                            10,arcade.color.BLUE)
        arcade.draw_xywh_rectangle_outline(75, SCREEN_HEIGHT - 70,
                                            250,10,arcade.color.BLACK)

    def dead_screen(self):
        if self.world.player.is_dead:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)
            arcade.draw_text("YOU  DIED",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT/2 + 10, arcade.color.RED, 90, width=SCREEN_WIDTH, align="center",
                         anchor_x="center", anchor_y="center")

    def on_draw(self):
        arcade.start_render()
        self.player_sprite.draw()
        self.draw_platforms(self.world.platforms)
        self.draw_monster()
        self.bullet_sprite.draw()
        self.monster_bullet_sprite.draw()
        self.hp_bar()
        self.power_bar()
        arcade.draw_text(str(self.world.floor),100,SCREEN_HEIGHT - 130, arcade.color.BLACK, 20)
        self.dead_screen()

            
    def update(self, delta):
        self.player_sprite = self.player()
        self.hp_bar()
        self.power_bar()
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