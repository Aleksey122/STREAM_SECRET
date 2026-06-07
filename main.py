from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
import threading, requests

SERVER = "http://138.124.102.128:8000"

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1

        MDTopAppBar:
            title: "MAX AI"
            elevation: 2
            md_bg_color: 0.118, 0.118, 0.118, 1
            specific_text_color: 1, 1, 1, 1

        ScrollView:
            id: scroll
            MDList:
                id: chat_list
                padding: "12dp"
                spacing: "6dp"

        MDBoxLayout:
            adaptive_height: True
            padding: "6dp"
            spacing: "4dp"
            md_bg_color: 0.96, 0.96, 0.96, 1

            MDIconButton:
                icon: "paperclip"
                theme_icon_color: "Custom"
                icon_color: 0.4, 0.4, 0.4, 1

            MDIconButton:
                icon: "camera"
                theme_icon_color: "Custom"
                icon_color: 0.4, 0.4, 0.4, 1

            MDIconButton:
                icon: "microphone"
                theme_icon_color: "Custom"
                icon_color: 0.4, 0.4, 0.4, 1

            MDTextField:
                id: msg_input
                hint_text: "Сообщение..."
                mode: "round"
                size_hint_x: 1
                on_text_validate: app.send_message()

            MDFloatingActionButton:
                icon: "send"
                elevation: 0
                md_bg_color: 0.118, 0.118, 0.118, 1
                on_release: app.send_message()
'''

class MAXApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def add_message(self, text, align="left"):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        card = MDCard(
            padding="12dp",
            radius=[18, 18, 4, 18] if align == "right" else [18, 18, 18, 4],
            size_hint_x=0.78,
            adaptive_height=True,
            pos_hint={"right": 0.97} if align == "right" else {"x": 0.03},
            md_bg_color=(0.118, 0.118, 0.118, 1) if align == "right" else (0.93, 0.93, 0.93, 1)
        )
        label = MDLabel(
            text=text,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1) if align == "right" else (0.1, 0.1, 0.1, 1)
        )
        card.add_widget(label)
        self.root.ids.chat_list.add_widget(card)
        Clock.schedule_once(lambda dt: setattr(self.root.ids.scroll, 'scroll_y', 0), 0.1)

    def send_message(self):
        text = self.root.ids.msg_input.text.strip()
        if not text:
            return
        self.root.ids.msg_input.text = ""
        self.add_message(text, align="right")
        self.add_message("...", align="left")
        threading.Thread(target=self.get_reply, args=(text,), daemon=True).start()

    def get_reply(self, text):
        try:
            r = requests.post(f"{SERVER}/chat", json={"text": text}, timeout=30)
            reply = r.json().get("reply", "Нет ответа")
        except Exception as e:
            reply = f"Нет соединения с сервером"
        def update(dt):
            lst = self.root.ids.chat_list
            if lst.children:
                lst.remove_widget(lst.children[0])
            self.add_message(reply, align="left")
        Clock.schedule_once(update, 0)

if __name__ == '__main__':
    MAXApp().run()
