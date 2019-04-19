import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLATFORM_DRAW_THICKNESS = 10
PLATFORM_DRAW_Y_OFFSET = 28

MELEE_UPDATE = 3


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

    def draw(self):
        for b in self.bullet:
            if b.direction == 2:
                self.bullet_sprite = arcade.Sprite('images/bullet/bullet-'+str(b.element)+'_left.png',scale=0.5)
            else:
                self.bullet_sprite = arcade.Sprite('images/bullet/bullet-'+str(b.element)+'_right.png',scale=0.5)
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
            player_sprite = ModelSprite('images/player/player-'+str(self.world.player.element)+'_left.png',
                                        model=self.world.player,scale=0.24)
        else:
            player_sprite = ModelSprite('images//player/player-'+str(self.world.player.element)+'_right.png',
                                        model=self.world.player,scale=0.24)
        return player_sprite

    def draw_melee(self):
        melee_sprite = ModelSprite('images/melee/melee.png',model=self.world.player,scale=0.24)
        if 0 <= self.world.player_melee.frame <= MELEE_UPDATE:
            if self.world.player.current_direction == 2:
                melee_sprite = ModelSprite('images/melee/left/melee-0'+\
                    # str(self.world.player.element)+\
                        str(self.world.player_melee.melee_update)+'.png',
                    model=self.world.player,scale=0.24)
            else:
                melee_sprite = ModelSprite('images/melee/right/melee-0'+\
                    # str(self.world.player.element)+\
                        str(self.world.player_melee.melee_update)+'.png',
                    model=self.world.player,scale=0.24)
        
        return melee_sprite
        



    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_xywh_rectangle_filled(p.x,
                                            p.y-PLATFORM_DRAW_Y_OFFSET,
                                            p.width, PLATFORM_DRAW_THICKNESS,
                                            arcade.color.WHITE)
    
    def monster_sprite(self,m):
        if m.current_direction == 2:
            monster_sprite = ModelSprite('images/monster/monster-'+str(m.element)+'_left.png',model=m,scale=0.35)
        else:
            monster_sprite = ModelSprite('images/monster/monster-'+str(m.element)+'_right.png',model=m,scale=0.35)
        return monster_sprite
    
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
    
    def floor(self):
        arcade.draw_text("Floor: "+str(self.world.floor),100,SCREEN_HEIGHT - 130, arcade.color.BLACK, 20)

    def dead_screen(self):
        if self.world.player.is_dead:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)
            arcade.draw_text("YOU  DIED",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT/2 + 10, arcade.color.RED, 90, width=SCREEN_WIDTH, align="center",
                         anchor_x="center", anchor_y="center")

    def on_draw(self):
        arcade.start_render()
        self.bullet_sprite.draw()
        self.monster_bullet_sprite.draw()
        self.player_sprite.draw()
        self.draw_melee().draw()
        for m in self.world.monster:
            self.monster_sprite(m).draw()
        self.draw_platforms(self.world.platforms)
        self.hp_bar()
        self.power_bar()
        self.floor()
        self.dead_screen()
            
    def update(self, delta):
        # self.set_update_rate(1/2)
        self.player_sprite = self.player()
        self.draw_melee().draw()
        for m in self.world.monster:
            self.monster_sprite(m).draw()
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