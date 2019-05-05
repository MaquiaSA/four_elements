import arcade
from gameplay import Gameplay

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MENU = 0
GAMEPLAY = 1
HOWTOPLAY = 2

class FourElementsRunWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.stage = MENU
        self.all_check_cover()
        self.howto_page = 1
        self.gameplay = Gameplay()
    
    def all_check_cover(self):
        self.start_cover = False
        self.how_cover = False
        self.howto_left = False
        self.howto_right = False
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

    def menu_cover(self,x,y):
        if x in range(274,526) and y in range(151,204):
            self.start_cover = True
        else:
            self.start_cover = False
        if x in range(382,418) and y in range(87,124):
            self.how_cover = True
        else:
            self.how_cover = False
    
    def menu_press(self,x,y):
        if x in range(274,526) and y in range(151,204):
            self.stage = GAMEPLAY
            self.gameplay.set_up()
        if x in range(382,418) and y in range(87,124):
            self.stage = HOWTOPLAY
    
    def howto_press(self,x,y):
        if 1 <= self.howto_page <= 3:
            if x in range(22,96) and y in range(274,325):
                self.howto_page -= 1
            if x in range(707,781) and y in range(274,325):
                self.howto_page += 1

    def howto_arrow_cover(self,x,y):
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



    def on_draw(self):
        arcade.start_render()
        if self.stage == MENU:
            self.draw_menu()
        elif self.stage == GAMEPLAY:
            self.gameplay.on_draw()
        elif self.stage == HOWTOPLAY:
            self.draw_howto()
            
    def update(self, delta):
        self.set_update_rate(1/80)
        if self.stage == GAMEPLAY:
            self.gameplay.update(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.gameplay.on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.gameplay.on_key_release(key, key_modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.stage == MENU:
            self.menu_cover(x, y)
        elif self.stage == GAMEPLAY:
            self.gameplay.on_mouse_motion(x, y, dx, dy)
        elif self.stage == HOWTOPLAY:
            self.howto_arrow_cover(x, y)
            if self.howto_page == 2:
                self.all_howto_interface(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.stage == MENU:
            self.menu_press(x,y)
        if self.stage == GAMEPLAY:
            if x in range(312,489) and y in range(50,100):
                self.stage = MENU
        if self.stage == HOWTOPLAY:
            self.howto_press(x,y)


            


def main():
    window = FourElementsRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()