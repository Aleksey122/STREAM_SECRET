from kivy.lang import Builder
from kivy.app import App

class ChatApp(App):
    def build(self):
        return Builder.load_file("chat_ui.kv")

if __name__ == '__main__':
    ChatApp().run()
