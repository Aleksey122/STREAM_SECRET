from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
import threading
import requests
SERVER = "http://138.124.102.128:8000"
KV = '''
MDScreen:
MDBoxLayout:
orientation: 'vertical'
MDTopAppBar:
        title: "MAX AI"
        md_bg_color: 1, 1, 1, 1
        specific_text_color: 0.1, 0.1, 0.1, 1
        elevation: 1
        left_action_items: [["robot-happy-outline", lambda x: None]]

    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.98, 0.98, 0.98, 1

        ScrollView:
            id: scroll
            do_scroll_x: False
            bar_width: 0

            MDList:
                id: chat_list
                padding: "12dp"
                spacing: "8dp"

    MDBoxLayout:
        id: input_bar
        orientation: 'horizontal'
        size_hint_y: None
        height: "64dp"
        padding: "8dp", "6dp"
        spacing: "6dp"
        md_bg_color: 1, 1, 1, 1
        elevation: 4

        MDIconButton:
            icon: "microphone-outline"
            theme_text_color: "Custom"
            text_color: 0.3, 0.3, 0.3, 1
            on_release: app.toggle_voice()

        MDTextField:
            id: msg_input
            hint_text: "Напишите сообщение..."
            mode: "round"
            size_hint_x: 1
            fill_color: 0.94, 0.94, 0.94, 1
            on_text_validate: app.send_message()

        MDIconButton:
            id: send_btn
            icon: "send"
            theme_text_color: "Custom"
            text_color: 0.2, 0.6, 1, 1
            on_release: app.send_message()
'''
class MAXApp(MDApp):
def build(self):
self.theme_cls.theme_style = "Light"
self.theme_cls.primary_palette = "Blue"
Window.softinput_mode = "below_target"
return Builder.load_string(KV)
def on_start(self):
    self.add_message("👋 Привет! Я MAX AI. Чем могу помочь?", "left")

def add_message(self, text, align="left"):
    from kivymd.uix.card import MDCard
    from kivymd.uix.label import MDLabel
    is_user = align == "right"
    bg = (0.2, 0.6, 1, 1) if is_user else (1, 1, 1, 1)
    txt = (1, 1, 1, 1) if is_user else (0.1, 0.1, 0.1, 1)
    radius = [18, 18, 4, 18] if is_user else [18, 18, 18, 4]
    pos = {"right": 0.98} if is_user else {"x": 0.02}
    card = MDCard(
        padding="14dp",
        radius=radius,
        size_hint_x=0.78,
        adaptive_height=True,
        pos_hint=pos,
        md_bg_color=bg,
        elevation=1,
    )
    card.add_widget(MDLabel(
        text=text,
        adaptive_height=True,
        theme_text_color="Custom",
        text_color=txt,
    ))
    self.root.ids.chat_list.add_widget(card)
    Clock.schedule_once(lambda dt: setattr(self.root.ids.scroll, "scroll_y", 0), 0.15)

def send_message(self):
    text = self.root.ids.msg_input.text.strip()
    if not text:
        return
    self.root.ids.msg_input.text = ""
    self.root.ids.send_btn.disabled = True
    self.add_message(text, "right")
    self.add_message("⏳ ...", "left")
    threading.Thread(target=self._get, args=(text,), daemon=True).start()

def _get(self, text):
    try:
        r = requests.post(f"{SERVER}/chat", json={"text": text}, timeout=30)
        r.raise_for_status()
        reply = r.json().get("reply", "Нет ответа")
    except requests.exceptions.ConnectionError:
        reply = "❌ Нет соединения с сервером"
    except requests.exceptions.Timeout:
        reply = "⏱ Сервер не отвечает"
    except Exception as e:
        reply = f"⚠️ Ошибка: {str(e)[:80]}"
    def upd(dt):
        lst = self.root.ids.chat_list
        if lst.children:
            lst.remove_widget(lst.children[0])
        self.add_message(reply, "left")
        self.root.ids.send_btn.disabled = False
    Clock.schedule_once(upd, 0)

def toggle_voice(self):
    self.add_m
if name == "main":
MAXApp().run()
