from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "TrollBox"
        MDLabel:
            text: "Система готова"
            halign: "center"
'''

class TrollBoxApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    TrollBoxApp().run()
