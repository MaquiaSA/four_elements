import arcade
from gameplay import Gameplay

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class FourElementsRunWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.gameplay = Gameplay()

    def on_draw(self):
        arcade.start_render()
        self.gameplay.on_draw()
            
    def update(self, delta):
        self.gameplay.update(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.gameplay.on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.gameplay.on_key_release(key, key_modifiers)


def main():
    window = FourElementsRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()