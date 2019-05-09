import arcade
from gameplay import Gameplay

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "4 Elements"

MENU = 0
GAMEPLAY = 1
HOWTOPLAY = 2


class Sound:
    def __init__(self):
        self.sound_play = 0
        self.hover_sound = arcade.load_sound("sounds/menu/hover.wav")
        self.select_sound = arcade.load_sound("sounds/menu/select.wav")
        self.flip_sound = arcade.load_sound("sounds/menu/flip.wav")
        self.close_sound = arcade.load_sound("sounds/menu/close.wav")
        self.main_menu_sound = arcade.load_sound("sounds/gameplay/main_menu.wav")

    def play_hover(self):
        if self.sound_play == 0:
            arcade.play_sound(self.hover_sound)
            self.sound_play += 1
    
    def play_select(self):
        if self.sound_play == 1:
            arcade.play_sound(self.select_sound)
            self.sound_play += 1
    
    def play_flip(self):
        if self.sound_play >= 1:
            arcade.play_sound(self.flip_sound)
            self.sound_play += 1
    
    def play_close(self):
        if self.sound_play >= 1:
            arcade.play_sound(self.close_sound)
            self.sound_play += 1

    def play_main_menu(self):
        if self.sound_play >= 1:
            arcade.play_sound(self.main_menu_sound)
            self.sound_play += 1
    
    def reset_sound_play(self):
        self.sound_play = 0


class FourElementsRunWindow(arcade.Window):
    def __init__(self, width, height, window_title):
        super().__init__(width, height, window_title)
        self.stage = MENU
        self.all_check_cover()
        self.howto_page = 1
        self.gameplay = Gameplay()
        self.sound_fx = Sound()
    
    def all_check_cover(self):
        self.start_cover = False
        self.how_cover = False
        self.howto_left = False
        self.howto_right = False
        self.game_over_cover = False
        self.sound_onoff_cover = False
        self.howto_gui_cover()

    def howto_gui_cover(self):
        self.player = False
        self.range = False
        self.melee = False
        self.hp = False
        self.power = False
        self.floor = False
        self.score = False
        self.platform = False
        self.monster = False

    def all_howto_interface(self,x,y):
        self.howto_interface_player(x,y)
        self.howto_interface_range(x,y)
        self.howto_interface_melee(x,y)
        self.howto_interface_hp(x,y)
        self.howto_interface_power(x,y)
        self.howto_interface_floor(x,y)
        self.howto_interface_score(x,y)
        self.howto_interface_platform(x,y)
        self.howto_interface_monster(x,y)

    def howto_interface_player(self,x,y):
        if x in range(127,178) and y in range(121,187):
            self.player = True
        else:
            self.player = False
    
    def howto_interface_range(self,x,y):
        if x in range(206,323) and y in range(159,208):
            self.range = True
        else:
            self.range = False
            
    def howto_interface_melee(self,x,y):
        if x in range(206,271) and y in range(102,150):
            self.melee = True
        else:
            self.melee = False
            
    def howto_interface_hp(self,x,y):
        if x in range(166,367) and y in range(462,483):
            self.hp = True
        else:
            self.hp = False
            
    def howto_interface_power(self,x,y):
        if x in range(166,347) and y in range(451,461):
            self.power = True
        else:
            self.power = False
            
    def howto_interface_floor(self,x,y):
        if x in range(581,640) and y in range(466,483):
            self.floor = True
        else:
            self.floor = False
            
    def howto_interface_score(self,x,y):
        if x in range(581,640) and y in range(448,465):
            self.score = True
        else:
            self.score = False
            
    def howto_interface_platform(self,x,y):
        if x in range(501,680) and y in range(332,349):
            self.platform = True
        else:
            self.platform = False
            
    def howto_interface_monster(self,x,y):
        if x in range(561,620) and y in range(192,242):
            self.monster = True
        else:
            self.monster = False

    def menu_hover(self,x,y):
        self.game_over_cover = False
        if x in range(274,526) and y in range(151,204):
            self.start_cover = True
        else:
            self.start_cover = False
        if x in range(382,418) and y in range(87,124):
            self.how_cover = True
        else:
            self.how_cover = False
        if x in range(750,785) and y in range(15,50):
            self.sound_onoff_cover = True
        else:
            self.sound_onoff_cover = False

        
    def menu_press(self,x,y):
        if x in range(274,526) and y in range(151,204):
            self.stage = GAMEPLAY
            self.gameplay.set_up()
        elif x in range(382,418) and y in range(87,124):
            self.stage = HOWTOPLAY
        elif x in range(750,785) and y in range(15,50):
            self.gameplay.enable_sound = not self.gameplay.enable_sound
        
    def game_over_press(self,x,y):
        if self.gameplay.world.player.is_dead:
            if x in range(312,489) and y in range(50,100):
                self.stage = MENU

    def game_over_hover(self,x,y):
        if self.gameplay.world.player.is_dead:
            if x in range(312,489) and y in range(50,100):
                self.game_over_cover = True
            else:
                self.game_over_cover = False

    def howto_press(self,x,y):
        if 1 <= self.howto_page <= 3:
            if x in range(22,96) and y in range(274,325):
                self.howto_page -= 1
            elif x in range(707,781) and y in range(274,325):
                self.howto_page += 1
        
    def howto_arrow_hover(self,x,y):
        if x in range(22,96) and y in range(274,325):
            self.howto_left = True
        else:
            self.howto_left = False
        if x in range(707,781) and y in range(274,325):
            self.howto_right = True
        else:
            self.howto_right = False

    def draw_sprite(self, condition, location):
        if condition:
            sprite = arcade.Sprite(location,scale=0.24)
            sprite.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            sprite.draw()

    def draw_menu(self):
        arcade.draw_xywh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,
            arcade.load_texture('images/menu/menu.png'))
        self.draw_sprite(self.gameplay.enable_sound,'images/menu/sound_on.png')
        self.draw_sprite(not self.gameplay.enable_sound,'images/menu/sound_off.png')
        self.draw_sprite(self.gameplay.enable_sound and self.sound_onoff_cover,'images/menu/sound_on_cover.png')
        self.draw_sprite(not self.gameplay.enable_sound and self.sound_onoff_cover,'images/menu/sound_off_cover.png')
        self.draw_sprite(self.start_cover,'images/menu/start_cover.png')
        self.draw_sprite(self.how_cover,'images/menu/how_cover.png')
        
    def draw_howto(self):
        arcade.draw_xywh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,
            arcade.load_texture('images/how_to/menu_bg.png'))
        if 1 <= self.howto_page <= 3:
            arcade.draw_xywh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,
                arcade.load_texture('images/how_to/howto_'+str(self.howto_page)+'.png'))
            self.draw_sprite(self.howto_left,'images/how_to/arrow_left.png')
            self.draw_sprite(self.howto_right,'images/how_to/arrow_right.png')
            if self.howto_page == 2:
                self.draw_howto_interface()
        else:
            self.stage = MENU
            self.howto_page = 1
    
    def draw_game_over_hover(self):
        if self.game_over_cover:
            over = arcade.Sprite('images/game_over/game_over_cover.png',scale=0.24)
            over.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            over.draw()

    def draw_howto_interface(self):
        self.draw_sprite(self.player,'images/how_to/howto_2-1.png')
        self.draw_sprite(self.range,'images/how_to/howto_2-2.png')
        self.draw_sprite(self.melee,'images/how_to/howto_2-3.png')
        self.draw_sprite(self.hp,'images/how_to/howto_2-4.png')
        self.draw_sprite(self.floor,'images/how_to/howto_2-5.png')
        self.draw_sprite(self.score,'images/how_to/howto_2-6.png')
        self.draw_sprite(self.power,'images/how_to/howto_2-7.png')
        self.draw_sprite(self.platform,'images/how_to/howto_2-8.png')
        self.draw_sprite(self.monster,'images/how_to/howto_2-9.png')

    def sound_on_mouse_motion(self,x,y,dx,dy):
        if self.stage == MENU:
            if x in range(274,526) and y in range(151,204):
                self.sound_fx.play_hover()
            elif x in range(382,418) and y in range(87,124):
                self.sound_fx.play_hover()
            else:
                self.sound_fx.reset_sound_play()
        elif self.stage == GAMEPLAY and self.gameplay.world.player.is_dead:
            if x in range(312,489) and y in range(50,100):
                self.sound_fx.play_hover()
            else:
                self.sound_fx.reset_sound_play()
        elif self.stage == HOWTOPLAY:
            if x in range(22,96) and y in range(274,325):
                self.sound_fx.play_hover()
            elif x in range(707,781) and y in range(274,325):
                self.sound_fx.play_hover()
            else:
                self.sound_fx.reset_sound_play()
    
    def sound_on_mouse_press(self,x,y):
        if self.stage == MENU:
            if x in range(274,526) and y in range(151,204):
                self.sound_fx.play_select()
                self.sound_fx.reset_sound_play()
            elif x in range(382,418) and y in range(87,124):
                self.sound_fx.play_select()
                self.sound_fx.reset_sound_play()
        elif self.stage == GAMEPLAY and self.gameplay.world.player.is_dead:
            if x in range(312,489) and y in range(50,100):
                self.sound_fx.play_main_menu()
            else:
                self.sound_fx.reset_sound_play()
        elif self.stage == HOWTOPLAY:
            if 1 <= self.howto_page <= 3:
                if x in range(22,96) and y in range(274,325):
                    self.sound_fx.play_flip()
                elif x in range(707,781) and y in range(274,325):
                    self.sound_fx.play_flip()
                else:
                    self.sound_fx.reset_sound_play()
            else:
                if x in range(22,96) and y in range(274,325):
                    self.sound_fx.play_close()
                elif x in range(707,781) and y in range(274,325):
                    self.sound_fx.play_close()
                else:
                    self.sound_fx.reset_sound_play()

    def on_draw(self):
        arcade.start_render()
        if self.stage == MENU:
            self.draw_menu()
        elif self.stage == GAMEPLAY:
            self.gameplay.on_draw()
            self.draw_game_over_hover()
        elif self.stage == HOWTOPLAY:
            self.draw_howto()
            
    def update(self, delta):
        self.set_update_rate(1/70)
        if self.stage == GAMEPLAY:
            self.gameplay.update(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.gameplay.on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.gameplay.on_key_release(key, key_modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.gameplay.enable_sound:
            self.sound_on_mouse_motion(x,y,dx,dy)
        if self.stage == MENU:
            self.menu_hover(x, y)
        elif self.stage == GAMEPLAY:
            self.game_over_hover(x, y)
        elif self.stage == HOWTOPLAY:
            self.howto_arrow_hover(x, y)
            if self.howto_page == 2:
                self.all_howto_interface(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.gameplay.enable_sound:
            self.sound_on_mouse_press(x,y)
        if self.stage == MENU:
            self.menu_press(x,y)
        if self.stage == GAMEPLAY:
            self.game_over_press(x,y)
        if self.stage == HOWTOPLAY:
            self.howto_press(x,y)


def main():
    window = FourElementsRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()
