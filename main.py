from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

class ChatApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        self.chat_area = ScrollView()
        self.messages = BoxLayout(orientation='vertical', size_hint_y=None)
        self.messages.bind(minimum_height=self.messages.setter('height'))
        self.chat_area.add_widget(self.messages)
        
        input_layout = BoxLayout(size_hint_y=None, height='50dp')
        self.input_field = TextInput(hint_text="Сообщение...", multiline=False)
        send_button = Button(text=">", size_hint_x=None, width='50dp')
        
        input_layout.add_widget(self.input_field)
        input_layout.add_widget(send_button)
        
        root.add_widget(self.chat_area)
        root.add_widget(input_layout)
        return root

if __name__ == '__main__':
    ChatApp().run()
