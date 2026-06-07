from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from android.permissions import request_permissions, Permission
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
            right_action_items: [["dots-vertical", lambda x: None]]

        MDDivider:

        ScrollView:
            id: scroll
            MDList:
                id: chat_list
                padding: "16dp"
                spacing: "8dp"

        MDBoxLayout:
            adaptive_height: True
            padding: "8dp", "8dp"
            spacing: "8dp"
            md_bg_color: 1, 1, 1, 1

            MDIconButton:
                icon: "plus"
                theme_icon_color: "Custom"
                icon_color: 0.4, 0.4, 0.4, 1
                on_release: app.attach_file()

            MDIconButton:
                icon: "camera"
                theme_icon_color: "Custom"
                icon_color: 0.4, 0.4, 0.4, 1
                on_release: app.open_camera()

            MDTextField:
                id: msg_input
                hint_text: "Напишите сообщение..."
                mode: "round"
                size_hint_x: 1
                on_text_validate: app.send_message()

            MDIconButton:
                id: mic_btn
                icon: "microphone"
                theme_icon_color: "Custom"
                icon_color: 0.4, 0.4, 0.4, 1
                on_release: app.toggle_voice()

            MDFloatingActionButton:
                icon: "send"
                elevation: 1
                md_bg_color: 0.2, 0.6, 1, 1
                on_release: app.send_message()
'''

class MAXApp(MDApp):
    recording = False

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        try:
            request_permissions([Permission.RECORD_AUDIO, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA])
        except:
            pass
        return Builder.load_string(KV)

    def add_message(self, text, align="left", color=None):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.boxlayout import MDBoxLayout

        if color is None:
            color = (0.2, 0.6, 1, 1) if align == "right" else (1, 1, 1, 1)
        txt_color = (1,1,1,1) if align == "right" else (0.1,0.1,0.1,1)

        card = MDCard(
            padding="14dp",
            radius=[18, 18, 4, 18] if align == "right" else [4, 18, 18, 18],
            size_hint_x=0.82,
            adaptive_height=True,
            pos_hint={"right": 0.98} if align == "right" else {"x": 0.02},
            md_bg_color=color,
            elevation=0
        )
        label = MDLabel(
            text=text,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=txt_color
        )
        card.add_widget(label)
        self.root.ids.chat_list.add_widget(card)
        Clock.schedule_once(lambda dt: setattr(self.root.ids.scroll, 'scroll_y', 0), 0.1)

    def send_message(self, text=None):
        if text is None:
            text = self.root.ids.msg_input.text.strip()
        if not text:
            return
        self.root.ids.msg_input.text = ""
        self.add_message(text, align="right")
        self._show_typing()
        threading.Thread(target=self.get_reply, args=(text,), daemon=True).start()

    def _show_typing(self):
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        card = MDCard(
            padding="14dp", radius=[4,18,18,18],
            size_hint_x=0.3, adaptive_height=True,
            pos_hint={"x": 0.02},
            md_bg_color=(1,1,1,1), elevation=0
        )
        card.add_widget(MDLabel(text="...", adaptive_height=True, theme_text_color="Custom", text_color=(0.5,0.5,0.5,1)))
        self._typing_card = card
        self.root.ids.chat_list.add_widget(card)

    def get_reply(self, text):
        try:
            r = requests.post(f"{SERVER}/chat", json={"text": text}, timeout=30)
            reply = r.json().get("reply", "Нет ответа")
        except:
            reply = "Нет соединения с сервером"
        def update(dt):
            if hasattr(self, '_typing_card'):
                try:
                    self.root.ids.chat_list.remove_widget(self._typing_card)
                except:
                    pass
            self.add_message(reply, align="left")
        Clock.schedule_once(update, 0)

    def toggle_voice(self):
        try:
            from android.permissions import check_permission, Permission
            from jnius import autoclass
            SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')
            Intent = autoclass('android.content.Intent')
            RecognizerIntent = autoclass('android.speech.RecognizerIntent')
            from kivymd.uix.snackbar import MDSnackbar
            MDSnackbar(text="Голосовой ввод активирован").open()
        except Exception as e:
            self.add_message(f"Голосовой ввод: {e}", align="left", color=(1,0.9,0.9,1))

    def attach_file(self):
        self.add_message("📎 Прикрепление файлов — скоро", align="left", color=(0.95,0.95,1,1))

    def open_camera(self):
        self.add_message("📷 Камера — скоро", align="left", color=(0.95,0.95,1,1))

if __name__ == '__main__':
    MAXApp().run()
