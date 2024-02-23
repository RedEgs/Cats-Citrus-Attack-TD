import kivy

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class RedEngine(App):
    def build(self):
        self.title = "Hello"


if __name__ == '__main__':
    engine = RedEngine()
    engine.run()
    
