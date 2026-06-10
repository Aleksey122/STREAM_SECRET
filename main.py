from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

class TrollBoxApp(MDApp):
    def build(self):
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.text_input = MDTextField(hint_text="Введите текст сообщения")
        btn_action = MDRaisedButton(text="Прикрепить файл / Микрофон", pos_hint={"center_x": .5})
        btn_action.bind(on_release=self.on_action_click)
        layout.add_widget(self.text_input)
        layout.add_widget(btn_action)
        screen.add_widget(layout)
        return screen

    def on_action_click(self, instance):
        self.text_input.text = "Функция запущена!"

if __name__ == '__main__':
    TrollBoxApp().run()
