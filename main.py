from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1

        MDTopAppBar:
            title: "MAX AI"
            elevation: 2

        ScrollView:
            MDList:
                id: chat_list
                padding: "12dp"

        MDBoxLayout:
            adaptive_height: True
            padding: "8dp"
            spacing: "8dp"

            MDTextField:
                id: msg_input
                hint_text: "Сообщение..."
                mode: "round"
                size_hint_x: 1

            MDIconButton:
                icon: "send"
                on_release: app.send_message()
'''

class MAXApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def send_message(self):
        from kivymd.uix.label import MDLabel
        text = self.root.ids.msg_input.text.strip()
        if text:
            self.root.ids.chat_list.add_widget(
                MDLabel(text=f"Вы: {text}", adaptive_height=True)
            )
            self.root.ids.msg_input.text = ""

if __name__ == '__main__':
    MAXApp().run()
