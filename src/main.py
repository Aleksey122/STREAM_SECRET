from kivy.app import App
from kivy.uix.webview import WebView
import logging

class LinkNodeAdmin(App):
    def build(self):
        logging.info("Admin Mode: Active")
        return WebView(url="https://lk.megafon.ru")

if __name__ == '__main__':
    LinkNodeAdmin().run()
