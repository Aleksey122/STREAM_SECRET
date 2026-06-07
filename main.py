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
            md_bg_color: 0.259, 0.647, 0.961, 1

        ScrollView:
            id: scroll
            MDList:
                id: chat_list
                padding: "12dp", "12dp", "12dp", "12dp"
                spacing: "8dp"

        MDBoxLayout:
            adaptive_height: True
            padding: "8dp"
            spacing: "8dp"
            md_bg_color: 0.95, 0.95, 0.95, 1

            MDTextField:
                id: msg_input
                hint_text: "Сообщение..."
                mode: "round"
                size_hint_x: 1
                on_text_validate: app.send_message()

            MDIconButton:
                icon: "send"
                theme_icon_color: "Custom"
                icon_color: 0.259, 0.647, 0.961, 1
                on_release: app.send_message()
'''

class MAXApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def add_message(self, text, align="left"):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        card = MDCard(
            padding="12dp",
            radius=[12],
            size_hint_x=0.8,
            adaptive_height=True,
            pos_hint={"right": 0.98} if align == "right" else {"x": 0.02},
            md_bg_color=(0.259, 0.647, 0.961, 1) if align == "right" else (0.93, 0.93, 0.93, 1)
        )
        label = MDLabel(
            text=text,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=(1,1,1,1) if align == "right" else (0,0,0,1)
        )
        card.add_widget(label)
        self.root.ids.chat_list.add_widget(card)
        Clock.schedule_once(lambda dt: setattr(self.root.ids.scroll, 'scroll_y', 0), 0.1)

    def send_message(self):
        text = self.root.ids.msg_input.text.strip()
        if not text:
            return
        self.root.ids.msg_input.text = ""
        self.add_message(f"{text}", align="right")
        threading.Thread(target=self.get_reply, args=(text,), daemon=True).start()

    def get_reply(self, text):
        try:
            r = requests.post(f"{SERVER}/chat", json={"text": text}, timeout=30)
            reply = r.json().get("reply", "Нет ответа")
        except Exception as e:
            reply = f"Ошибка связи: {e}"
        Clock.schedule_once(lambda dt: self.add_message(reply, align="left"), 0)

if __name__ == '__main__':
    MAXApp().run()
