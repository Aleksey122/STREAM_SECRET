from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MAXAIApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20)
        label = Label(text="MAX AI Initialized\nReady for input")
        layout.add_widget(label)
        return layout

if __name__ == '__main__':
    MAXAIApp().run()
