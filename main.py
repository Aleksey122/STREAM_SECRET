from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
import threading, requests

SERVER = "http://138.124.102.128:8000"

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "MAX AI"
            md_bg_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 1, 1, 1, 1

        ScrollView:
            id: scroll
            MDList:
                id: chat_list
                padding: "12dp"
                spacing: "6dp"

        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: "6dp"
            spacing: "6dp"
            md_bg_color: 0.95, 0.95, 0.95, 1

            MDIconButton:
                icon: "microphone"
                on_release: app.toggle_voice()

            MDTextField:
                id: msg_input
                hint_text: "Сообщение..."
                mode: "round"
                size_hint_x: 1

            MDRaisedButton:
                text: ">"
                on_release: app.send_message()
                md_bg_color: 0.2, 0.6, 1, 1
'''

class MAXApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def add_message(self, text, align="left"):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        color = (0.2,0.6,1,1) if align=="right" else (1,1,1,1)
        txt = (1,1,1,1) if align=="right" else (0.1,0.1,0.1,1)
        card = MDCard(
            padding="12dp",
            radius=[16,16,4,16] if align=="right" else [4,16,16,16],
            size_hint_x=0.8, adaptive_height=True,
            pos_hint={"right":0.97} if align=="right" else {"x":0.03},
            md_bg_color=color, elevation=0)
        card.add_widget(MDLabel(text=text, adaptive_height=True,
            theme_text_color="Custom", text_color=txt))
        self.root.ids.chat_list.add_widget(card)
        Clock.schedule_once(lambda dt: setattr(self.root.ids.scroll,'scroll_y',0), 0.1)

    def send_message(self):
        text = self.root.ids.msg_input.text.strip()
        if not text:
            return
        self.root.ids.msg_input.text = ""
        self.add_message(text, "right")
        self.add_message("...", "left")
        threading.Thread(target=self._get, args=(text,), daemon=True).start()

    def _get(self, text):
        try:
            r = requests.post(f"{SERVER}/chat", json={"text": text}, timeout=30)
            reply = r.json().get("reply", "Нет ответа")
        except:
            reply = "Нет соединения с сервером"
        def upd(dt):
            lst = self.root.ids.chat_list
            if lst.children:
                lst.remove_widget(lst.children[0])
            self.add_message(reply, "left")
        Clock.schedule_once(upd, 0)

    def toggle_voice(self):
        self.add_message("🎤 Голос в разработке", "left")

if __name__ == '__main__':
    MAXApp().run()
