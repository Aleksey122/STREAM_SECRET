from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import threading, requests
from auth_mobile import get_token

Window.clearcolor = (0.05, 0.05, 0.05, 1)

class ChatApp(App):
    def build(self):
        self.history = []
        root = BoxLayout(orientation='vertical', padding=8, spacing=6)
        title = Label(text='MAX AI', size_hint_y=None, height=40,
                     color=(0.4,1,0.4,1), font_size=20, bold=True)
        root.add_widget(title)
        self.scroll = ScrollView()
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4, padding=4)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll.add_widget(self.chat_box)
        root.add_widget(self.scroll)
        row = BoxLayout(size_hint_y=None, height=50, spacing=6)
        self.inp = TextInput(hint_text='Сообщение...', multiline=False,
                            background_color=(0.1,0.1,0.1,1), foreground_color=(1,1,1,1))
        self.inp.bind(on_text_validate=self.send)
        btn = Button(text='➤', size_hint_x=None, width=50, background_color=(0.4,1,0.4,1))
        btn.bind(on_press=self.send)
        row.add_widget(self.inp)
        row.add_widget(btn)
        root.add_widget(row)
        self.msg('MAX', 'Привет! Я MAX. Чем помочь?', (0.4,1,0.4,1))
        return root

    def msg(self, who, text, color):
        lbl = Label(text=f'[b]{who}:[/b] {text}', markup=True,
                   size_hint_y=None, color=color,
                   text_size=(Window.width-20, None), halign='left', valign='top')
        lbl.bind(texture_size=lbl.setter('size'))
        self.chat_box.add_widget(lbl)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def send(self, *a):
        text = self.inp.text.strip()
        if not text: return
        self.inp.text = ''
        self.history.append({'role': 'user', 'content': text})
        self.msg('Вы', text, (0.7,0.9,1,1))
        self.msg('MAX', '⏳ думаю...', (0.6,0.6,0.6,1))
        threading.Thread(target=self.giga, args=(text,), daemon=True).start()

    def giga(self, text):
        try:
            token = get_token()
            r = requests.post(
                'https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
                headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                json={'model': 'GigaChat', 'messages': self.history},
                verify=False, timeout=30)
            reply = r.json()['choices'][0]['message']['content']
            self.history.append({'role': 'assistant', 'content': reply})
        except Exception as e:
            reply = f'Ошибка: {e}'
        Clock.schedule_once(lambda dt: self.update(reply), 0)

    def update(self, reply):
        if self.chat_box.children:
            self.chat_box.remove_widget(self.chat_box.children[0])
        self.msg('MAX', reply, (0.4,1,0.4,1))

if __name__ == '__main__':
    ChatApp().run()
