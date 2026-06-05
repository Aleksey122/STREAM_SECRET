from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import threading
import sys
sys.path.insert(0, '/root')
from auth_manager import get_valid_token
import requests

Window.clearcolor = (0.05, 0.05, 0.05, 1)

class ChatApp(App):
    def build(self):
        self.history = []
        root = BoxLayout(orientation='vertical', padding=8, spacing=6)

        # Заголовок
        title = Label(text='MAX AI — GigaChat', size_hint_y=None,
                     height=40, color=(0.4,1,0.4,1), font_size=18, bold=True)
        root.add_widget(title)

        # Чат
        self.scroll = ScrollView()
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4, padding=4)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll.add_widget(self.chat_box)
        root.add_widget(self.scroll)

        # Поле ввода
        input_row = BoxLayout(size_hint_y=None, height=50, spacing=6)
        self.text_input = TextInput(hint_text='Сообщение...', multiline=False,
                                   background_color=(0.1,0.1,0.1,1),
                                   foreground_color=(1,1,1,1))
        self.text_input.bind(on_text_validate=self.send_message)
        send_btn = Button(text='➤', size_hint_x=None, width=50,
                         background_color=(0.4,1,0.4,1))
        send_btn.bind(on_press=self.send_message)
        input_row.add_widget(self.text_input)
        input_row.add_widget(send_btn)
        root.add_widget(input_row)

        self.add_message('MAX', 'Привет! Я MAX на базе GigaChat. Чем помочь?', (0.4,1,0.4,1))
        return root

    def add_message(self, sender, text, color):
        lbl = Label(text=f'[b]{sender}:[/b] {text}', markup=True,
                   size_hint_y=None, color=color, text_size=(Window.width-20, None),
                   halign='left', valign='top')
        lbl.bind(texture_size=lbl.setter('size'))
        self.chat_box.add_widget(lbl)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def send_message(self, *args):
        text = self.text_input.text.strip()
        if not text: return
        self.text_input.text = ''
        self.history.append({'role': 'user', 'content': text})
        self.add_message('Вы', text, (0.7,0.9,1,1))
        self.add_message('MAX', '...думаю...', (0.8,0.8,0.8,1))
        threading.Thread(target=self.ask_giga, args=(text,), daemon=True).start()

    def ask_giga(self, text):
        try:
            token = get_valid_token()
            if not token:
                reply = 'Ошибка авторизации GigaChat'
            else:
                url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
                headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
                payload = {'model': 'GigaChat', 'messages': self.history}
                r = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)
                reply = r.json()['choices'][0]['message']['content']
                self.history.append({'role': 'assistant', 'content': reply})
        except Exception as e:
            reply = f'Ошибка: {e}'
        Clock.schedule_once(lambda dt: self._update_reply(reply), 0)

    def _update_reply(self, reply):
        if self.chat_box.children:
            self.chat_box.remove_widget(self.chat_box.children[0])
        self.add_message('MAX', reply, (0.4,1,0.4,1))

if __name__ == '__main__':
    ChatApp().run()
