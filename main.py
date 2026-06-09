import os
import sys
sys.path.append(os.getcwd())

from ui_controller import UIController
from kivy.app import App
from kivy.uix.label import Label

class TrollBoxApp(App):
    def build(self):
        ctrl = UIController()
        return Label(text=f"Статус контроллера: {type(ctrl).__name__}")

if __name__ == '__main__':
    TrollBoxApp().run()
