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
        self.start_cover = False
        self.how_cover = False
        self.gameplay = Gameplay()

    def check_cover(self,x,y):
        if x in range(75,226) and y in range(48,92):
            self.start_cover = True
        else:
            self.start_cover = False
        if x in range(278,429) and y in range(48,92):
            self.how_cover = True
        else:
            self.how_cover = False
    
    def menu_press(self,x,y):
        if x in range(75,226) and y in range(48,92):
            self.stage = GAMEPLAY
            self.gameplay.set_up()
        if x in range(278,429) and y in range(48,92):
            self.stage = HOWTOPLAY

    def draw_menu(self):
        arcade.draw_xywh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,
            arcade.load_texture('images/menu/menu.png'))
        if self.start_cover:
            start = arcade.Sprite('images/menu/start_cover.png',scale=0.24)
            start.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            start.draw()
        if self.how_cover:
            how = arcade.Sprite('images/menu/how_cover.png',scale=0.24)
            how.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            how.draw()

    def on_draw(self):
        arcade.start_render()
        if self.stage == MENU:
            self.draw_menu()
        elif self.stage == GAMEPLAY:
            self.gameplay.on_draw()
            
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
            self.check_cover(x, y)
        elif self.stage == GAMEPLAY:
            self.gameplay.on_mouse_motion(x, y, dx, dy)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.stage == MENU:
            self.menu_press(x,y)
        if self.stage == GAMEPLAY:
            if x in range(312,489) and y in range(50,100):
                self.stage = MENU


            


def main():
    window = FourElementsRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()