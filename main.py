from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
import threading, requests

SERVER = "http://138.124.102.128:8000"

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.97, 0.97, 0.97, 1

        MDTopAppBar:
            title: "MAX AI"
            elevation: 0
            md_bg_color: 1, 1, 1, 1
            specific_text_color: 0.1, 0.1, 0.1, 1

        ScrollView:
            id: scroll
            MDList:
                id: chat_list
                padding: "16dp"
                spacing: "8dp"

        MDBoxLayout:
            adaptive_height: True
            padding: "8dp"
            spacing: "6dp"
            md_bg_color: 1, 1, 1, 1

            MDIconButton:
                icon: "plus"
                theme_icon_color: "Custom"
                icon_color: 0.5, 0.5, 0.5, 1
                on_release: app.attach_file()

            MDIconButton:
                icon: "camera"
                theme_icon_color: "Custom"
                icon_color: 0.5, 0.5, 0.5, 1
                on_release: app.open_camera()

            MDTextField:
                id: msg_input
                hint_text: "Сообщение..."
                mode: "round"
                size_hint_x: 1
                on_text_validate: app.send_message()

            MDIconButton:
                icon: "microphone"
                theme_icon_color: "Custom"
                icon_color: 0.5, 0.5, 0.5, 1
                on_release: app.toggle_voice()

            MDFloatingActionButton:
                icon: "send"
                elevation: 1
                md_bg_color: 0.2, 0.6, 1, 1
                on_release: app.send_message()
'''

class MAXApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.RECORD_AUDIO, Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE])
        except:
            pass
        return Builder.load_string(KV)

    def add_message(self, text, align="left"):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        color = (0.2, 0.6, 1, 1) if align == "right" else (1, 1, 1, 1)
        txt = (1,1,1,1) if align == "right" else (0.1,0.1,0.1,1)
        card = MDCard(padding="14dp", radius=[18,18,4,18] if align=="right" else [4,18,18,18],
            size_hint_x=0.82, adaptive_height=True,
            pos_hint={"right":0.97} if align=="right" else {"x":0.03},
            md_bg_color=color, elevation=0)
        card.add_widget(MDLabel(text=text, adaptive_height=True, theme_text_color="Custom", text_color=txt))
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
            reply = "Нет соединения"
        def upd(dt):
            lst = self.root.ids.chat_list
            if lst.children:
                lst.remove_widget(lst.children[0])
            self.add_message(reply, "left")
        Clock.schedule_once(upd, 0)

    def toggle_voice(self):
        self.add_message("🎤 Голос — скоро", "left")

    def attach_file(self):
        self.add_message("📎 Файлы — скоро", "left")

    def open_camera(self):
        self.add_message("📷 Камера — скоро", "left")

if __name__ == '__main__':
    MAXApp().run()
