from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.webview import WebView

class BrowserCore(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wv = WebView(url="https://lk.megafon.ru")
        self.add_widget(self.wv)

class PandaApp(App):
    def build(self):
        return BrowserCore()

if __name__ == '__main__':
    PandaApp().run()
