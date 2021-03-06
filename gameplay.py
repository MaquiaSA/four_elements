import arcade
import arcade.key
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

class Sound:
    def __init__(self):
        self.health_play = 0
        self.floor_play = 0
        self.power_play = 0
        self.power_full_sound = arcade.load_sound("sounds/gameplay/power_full.wav")
        self.power_proc_sound = arcade.load_sound("sounds/gameplay/power_proc.wav")
        self.low_health_sound = arcade.load_sound("sounds/gameplay/low_health.wav")
        self.next_floor_sound = arcade.load_sound("sounds/gameplay/next.wav")
        self.melee_sound = arcade.load_sound("sounds/gameplay/melee.wav")
        self.range_sound = arcade.load_sound("sounds/gameplay/range.wav")

    def play_pw_full(self):
        if self.power_play == 0:
            arcade.play_sound(self.power_full_sound)
            self.power_play += 1
    
    def play_pw_proc(self):
        if self.power_play == 1:
            arcade.play_sound(self.power_proc_sound)
            self.power_play += 1
    
    def play_low_hp(self):
        if self.health_play == 0:
            arcade.play_sound(self.low_health_sound)
            self.health_play += 1

    def play_next_floor(self):
        if self.floor_play == 0:
            arcade.play_sound(self.next_floor_sound)
            self.floor_play += 1

    def play_melee(self):
        arcade.play_sound(self.melee_sound)
    
    def play_range(self):
        arcade.play_sound(self.range_sound)

    def reset_health_play(self):
        self.health_play = 0
        
    def reset_power_play(self):
        self.power_play = 0
        
    def reset_floor_play(self):
        self.floor_play = 0


class Gameplay:
    def __init__(self):
        self.world = None
        self.player_sprite = None
        self.bullet_sprite = None
        self.monster_bullet_sprite = None
        self.game_over_cover = False
        self.enable_sound = False
        self.sound = Sound()

    def set_up(self):
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
            arcade.draw_triangle_outline(50,130,40,147.3,60,147.3,arcade.color.WHITE,border_width=2)
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
            self.draw_number(f'{self.world.player.health:.0f}'+'/100',90,SCREEN_HEIGHT-45)
        elif 0 < self.world.player.health < (1000/11):
            arcade.draw_polygon_filled([[75,SCREEN_HEIGHT-25],
                                            [75+(self.world.player.health)*2.75,SCREEN_HEIGHT-25],
                                            [75+(self.world.player.health)*2.75,SCREEN_HEIGHT-50],
                                            [75,SCREEN_HEIGHT-50]],color)
            self.draw_number(f'{self.world.player.health:.0f}'+'/100',90,SCREEN_HEIGHT-45)
        else:
            self.draw_number('0/100',90,SCREEN_HEIGHT-45)

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
                                            [310,SCREEN_HEIGHT-65],
                                            [75,SCREEN_HEIGHT-65]],
                                            color)
        elif 0 < self.world.player.power < (4700/49):
            arcade.draw_polygon_filled([[75,SCREEN_HEIGHT-55],
                                            [75+(self.world.player.power)*2.45,SCREEN_HEIGHT-55],
                                            [75+(self.world.player.power)*2.45,SCREEN_HEIGHT-65],
                                            [75,SCREEN_HEIGHT-65]],
                                            color)
        else:
            pass
    
    def bar_outline(self):
        arcade.draw_polygon_outline([[75,SCREEN_HEIGHT-25],
                                     [350,SCREEN_HEIGHT-25],
                                     [325,SCREEN_HEIGHT-50],
                                     [75,SCREEN_HEIGHT-50]],arcade.color.BLACK,line_width=2)
        arcade.draw_polygon_outline([[75,SCREEN_HEIGHT-55],
                                     [320,SCREEN_HEIGHT-55],
                                     [310,SCREEN_HEIGHT-65],
                                     [75,SCREEN_HEIGHT-65]],arcade.color.BLACK,line_width=2)
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

    def floor(self,x,y,size):
        arcade.draw_xywh_rectangle_textured(x,y,size*3,size,
            arcade.load_texture('images/char/floor.png'))
        self.draw_number(str(self.world.floor),x+size*3.1,y,size)
    
    def score(self,x,y,size):
        arcade.draw_xywh_rectangle_textured(x,y,size*3,size,
            arcade.load_texture('images/char/score.png'))
        self.draw_number(str(self.world.score),x+size*3.1,y,size)

    def gui(self):
        self.hp_bar()
        self.power_bar()
        self.bar_outline()
        self.floor(SCREEN_WIDTH-135,SCREEN_HEIGHT-45,20)
        self.score(SCREEN_WIDTH-135,SCREEN_HEIGHT-70,20)

    def game_over(self):
        if self.world.player.is_dead:
            arcade.draw_xywh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                arcade.load_texture("images/game_over/game_over.png"))
            self.floor(200,SCREEN_HEIGHT//2 - 50,40)
            self.score(SCREEN_WIDTH//2+30,SCREEN_HEIGHT//2 - 50,40)

    def draw_gameplay(self):
        self.draw_melee().draw()
        self.draw_platforms(self.world.platforms)
        self.draw_idle()
        if not self.world.player.is_dead:
            self.bullet_sprite.draw()
            self.player_sprite.draw()
            if self.world.player.is_hit:
                self.player_sprite_hit().draw()
            self.monster_bullet_sprite.draw()
        for m in self.world.monster:
            self.monster_sprite(m).draw()
            if m.is_hit:
                self.monster_sprite_hit(m).draw()

    def draw_gameplay_update(self):
        self.player_sprite = self.player()
    
    def sound_fx(self):
        if self.world.player.health <= 30 and not self.world.player.is_dead:
            self.sound.play_low_hp()
        else:
            self.sound.reset_health_play()
        if not self.world.monster:
            self.sound.play_next_floor()
        else:
            self.sound.reset_floor_play()
        if self.world.player.power == 100:
            self.sound.play_pw_full()
        elif self.world.player.shield:
            self.sound.play_pw_proc()
        else:
            self.sound.reset_power_play()
    
    def sound_on_key_press(self, key, key_modifiers):
        if key == arcade.key.J:
            self.sound.play_melee()
        if key == arcade.key.K:
            self.sound.play_range()

    def on_draw(self):
        self.background()
        self.draw_gameplay()
        self.gui()
        self.game_over()
            
    def update(self, delta):
        self.draw_gameplay_update()
        if self.enable_sound:
            self.sound_fx()
        self.world.update(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if self.enable_sound:
            self.sound_on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)
