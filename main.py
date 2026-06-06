from kivymd.app import MDApp
from kivy.lang import Builder

class MaxAIApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("chat_ui.kv")

if __name__ == '__main__':
    MaxAIApp().run()
