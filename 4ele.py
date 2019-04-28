import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLATFORM_THICKNESS = 30
GROUND_THICKNESS = 100
PLATFORM_DRAW_THICKNESS = 10
PLATFORM_DRAW_Y_OFFSET = 30

MELEE_FRAME_UPDATE = 3

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

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
            if b.direction == DIR_LEFT:
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

    def background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/background.png'))

    def player(self):
        if self.world.player.current_direction == DIR_LEFT:
            player_sprite = ModelSprite('images/player/player-'+str(self.world.player.element)+'_left.png',
                                        model=self.world.player,scale=0.24)
        else:
            player_sprite = ModelSprite('images//player/player-'+str(self.world.player.element)+'_right.png',
                                        model=self.world.player,scale=0.24)
        return player_sprite

    def draw_idle(self):
        if self.world.player.idle:
            arcade.draw_triangle_filled(50,130,40,147.3,60,147.3,arcade.color.LEMON_GLACIER)
        else:
            pass

    def draw_melee(self):
        melee_sprite = ModelSprite('images/melee/melee.png',model=self.world.player,scale=0.24)
        if 0 <= self.world.player_melee.frame <= MELEE_FRAME_UPDATE:
            if self.world.player.current_direction == DIR_LEFT:
                direction = 'left'
            else:
                direction = 'right'
            melee_sprite = ModelSprite('images/melee/'+ direction +'/melee-'+\
                    str(self.world.player.element) + str(self.world.player_melee.melee_update)+'.png',
                    model=self.world.player,scale=0.24)
        return melee_sprite
        
    def player_sprite_hit(self):
        if self.world.player.current_direction == DIR_LEFT:
            direction = 'left'
        else:
            direction = 'right'
        return ModelSprite('images/player/player-hit_'+ direction +'.png',model=self.world.player,scale=0.24)

    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_xywh_rectangle_textured(p.x,
                                            p.y-PLATFORM_DRAW_Y_OFFSET,
                                            p.width, PLATFORM_DRAW_THICKNESS,
                                            texture=arcade.load_texture('images/platform.png'))
    
    def monster_sprite(self,m):
        if m.current_direction == DIR_LEFT:
            monster_sprite = ModelSprite('images/monster/monster-'+str(m.element)+'_left.png',model=m,scale=0.35)
        else:
            monster_sprite = ModelSprite('images/monster/monster-'+str(m.element)+'_right.png',model=m,scale=0.35)
        return monster_sprite
    
    def monster_sprite_hit(self,m):
        if m.current_direction == DIR_LEFT:
            direction = 'left'
        else:
            direction = 'right'
        return ModelSprite('images/monster/monster-hit_'+ direction +'.png',model=m,scale=0.35)
    
    def element_icon(self):
        arcade.draw_xywh_rectangle_textured(15,SCREEN_HEIGHT-85,70,70,
            arcade.load_texture('images/icon/icon-'+str(self.world.player.element)+'.png'))

    def draw_shield(self):
        if self.world.player.shield:
            arcade.draw_xywh_rectangle_filled(20, SCREEN_HEIGHT - 50,
                                            50,
                                            50,arcade.color.GREEN)
        else:
            arcade.draw_xywh_rectangle_filled(20, SCREEN_HEIGHT - 50,
                                            50,
                                            50,arcade.color.YELLOW)
    
    def hp_bar(self):
        color = arcade.color.PANSY_PURPLE
        if self.world.player.element == 0:
            color = arcade.color.FIRE_ENGINE_RED
        elif self.world.player.element == 1:
            color = arcade.color.OCEAN_BOAT_BLUE
        elif self.world.player.element == 2:
            color = arcade.color.WINDSOR_TAN
        elif self.world.player.element == 3:
            color = arcade.color.SHEEN_GREEN
        
        if self.world.player.health >= (1000/11):
            arcade.draw_polygon_filled([[75,SCREEN_HEIGHT-25],
                                            [75+(self.world.player.health)*2.75,SCREEN_HEIGHT-25],
                                            [75+(self.world.player.health)*2.75,
                                                SCREEN_HEIGHT-(25+(275-(self.world.player.health)*2.75))],
                                            [325,SCREEN_HEIGHT-50],
                                            [75,SCREEN_HEIGHT-50]],color)
        else:
            arcade.draw_polygon_filled([[75,SCREEN_HEIGHT-25],
                                            [75+(self.world.player.health)*2.75,SCREEN_HEIGHT-25],
                                            [75+(self.world.player.health)*2.75,SCREEN_HEIGHT-50],
                                            [75,SCREEN_HEIGHT-50]],color)
        self.draw_number(f'{self.world.player.health:.0f}'+'/100',90,SCREEN_HEIGHT-45)

    def power_bar(self):
        color = arcade.color.BLUE
        if self.world.player.power == 100 or self.world.player.shield:
            color = arcade.color.PUMPKIN
        else:
            color = arcade.color.LEMON
        if self.world.player.power >= (4700/49):
            arcade.draw_polygon_filled([[75,SCREEN_HEIGHT-55],
                                            [75+(self.world.player.power)*2.45,SCREEN_HEIGHT-55],
                                            [75+(self.world.player.power)*2.45,
                                                SCREEN_HEIGHT-(55+(245-(self.world.player.power)*2.45))],
                                            [305,SCREEN_HEIGHT-65],
                                            [75,SCREEN_HEIGHT-65]],color)
        else:
            arcade.draw_polygon_filled([[75,SCREEN_HEIGHT-55],
                                            [75+(self.world.player.power)*2.45,SCREEN_HEIGHT-55],
                                            [75+(self.world.player.power)*2.45,SCREEN_HEIGHT-65],
                                            [75,SCREEN_HEIGHT-65]],color)
    
    def bar_outline(self):
        arcade.draw_polygon_outline([[75,SCREEN_HEIGHT-25],
                                     [350,SCREEN_HEIGHT-25],
                                     [325,SCREEN_HEIGHT-50],
                                     [75,SCREEN_HEIGHT-50]],arcade.color.BLACK,border_width=2)
        arcade.draw_polygon_outline([[75,SCREEN_HEIGHT-55],
                                     [320,SCREEN_HEIGHT-55],
                                     [310,SCREEN_HEIGHT-65],
                                     [75,SCREEN_HEIGHT-65]],arcade.color.BLACK,border_width=2)
        # arcade.draw_circle_filled(50,SCREEN_HEIGHT-50,35,arcade.color.WHITE)
        # arcade.draw_circle_outline(50,SCREEN_HEIGHT-50,35,arcade.color.BLACK,border_width=2)
    
    def draw_number(self,string,x,y,size=16,color='white'):
        x0 = x
        for s in string:
            if s == '/':
                arcade.draw_xywh_rectangle_textured(x0,y,size/2,size,
                    arcade.load_texture('images/char/'+str(color)+'/slash.png'))
            else:
                arcade.draw_xywh_rectangle_textured(x0,y,size/2,size,
                    arcade.load_texture('images/char/'+str(color)+'/'+str(s)+'.png'))
            x0 += size/2

    def floor(self):
        arcade.draw_xywh_rectangle_textured(SCREEN_WIDTH-135,SCREEN_HEIGHT-45,60,20,
            arcade.load_texture('images/char/floor.png'))
        self.draw_number(str(self.world.floor),SCREEN_WIDTH-72,SCREEN_HEIGHT-45,20)
    
    def score(self):
        arcade.draw_xywh_rectangle_textured(SCREEN_WIDTH-135,SCREEN_HEIGHT-70,60,20,
            arcade.load_texture('images/char/score.png'))
        self.draw_number(str(self.world.score),SCREEN_WIDTH-72,SCREEN_HEIGHT-70,20)

    def gui(self):
        # self.draw_shield()
        self.hp_bar()
        self.power_bar()
        self.bar_outline()
        # self.element_icon()
        self.floor()
        self.score()

    def dead_screen(self):
        if self.world.player.is_dead:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)
            arcade.draw_text("YOU  DIED",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT/2 + 10, arcade.color.RED, 90, width=SCREEN_WIDTH, align="center",
                         anchor_x="center", anchor_y="center")

    def on_draw(self):
        arcade.start_render()
        self.background()
        self.bullet_sprite.draw()
        self.monster_bullet_sprite.draw()
        if self.world.player.is_hit:
            self.player_sprite_hit().draw()
        self.draw_melee().draw()
        for m in self.world.monster:
            self.monster_sprite(m).draw()
            if m.is_hit:
                self.monster_sprite_hit(m).draw()
        self.draw_platforms(self.world.platforms)
        self.draw_idle()
        self.player_sprite.draw()
        self.gui()
        self.dead_screen()
            
    def update(self, delta):
        self.draw_idle()
        self.player_sprite = self.player()
        self.player_sprite_hit().draw()
        self.draw_melee().draw()
        for m in self.world.monster:
            self.monster_sprite(m).draw()
            if m.is_hit:
                self.monster_sprite_hit(m).draw()
        self.gui()
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