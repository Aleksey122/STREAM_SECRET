from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
import threading
import requests
import os

SERVER_URL = "http://138.124.102.128:8000"

class BubbleLabel(Label):
    def __init__(self, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.is_user = is_user
        self.size_hint_y = None
        self.text_size = (Window.width * 0.72, None)
        self.halign = 'left'
        self.valign = 'top'
        self.padding = [dp(12), dp(10)]
        self.color = (1,1,1,1) if is_user else (0.1,0.1,0.1,1)
        self.bind(texture_size=self._update_height)
        self.bind(pos=self._redraw, size=self._redraw)

    def _update_height(self, inst, val):
        self.height = val[1] + dp(20)

    def _redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_user:
                Color(0.24, 0.52, 0.98, 1)
            else:
                Color(0.93, 0.93, 0.93, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])


class MessageRow(BoxLayout):
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(10), dp(4), dp(10), dp(4)]
        bubble = BubbleLabel(text=text, is_user=is_user, size_hint_x=0.8)
        spacer = BoxLayout(size_hint_x=0.2)
        if is_user:
            self.add_widget(spacer)
            self.add_widget(bubble)
        else:
            self.add_widget(bubble)
            self.add_widget(spacer)
        bubble.bind(height=lambda i,v: setattr(self, 'height', v + dp(8)))


class MAXAIApp(App):
    def build(self):
        Window.softinput_mode = 'below_target'
        self.title = 'MAX AI'
        root = BoxLayout(orientation='vertical')
        appbar = BoxLayout(size_hint_y=None, height=dp(56), padding=[dp(16), dp(8)])
        with appbar.canvas.before:
            Color(1,1,1,1)
            self._ab = RoundedRectangle(pos=appbar.pos, size=appbar.size)
        appbar.bind(pos=lambda i,v: setattr(self._ab,'pos',v))
        appbar.bind(size=lambda i,v: setattr(self._ab,'size',v))
        appbar.add_widget(Label(text='MAX AI', font_size=dp(22), bold=True, color=(0.1,0.1,0.1,1)))
        root.add_widget(appbar)
        div = BoxLayout(size_hint_y=None, height=dp(1))
        with div.canvas.before:
            Color(0.85,0.85,0.85,1)
            RoundedRectangle(pos=div.pos, size=div.size)
        root.add_widget(div)
        self.scroll = ScrollView(do_scroll_x=False)
        self.msg_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(4), padding=[0,dp(8),0,dp(8)])
        self.msg_box.bind(minimum_height=self.msg_box.setter('height'))
        self.scroll.add_widget(self.msg_box)
        root.add_widget(self.scroll)
        input_area = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(58))
        with input_area.canvas.before:
            Color(1,1,1,1)
            self._ia = RoundedRectangle(pos=input_area.pos, size=input_area.size)
        input_area.bind(pos=lambda i,v: setattr(self._ia,'pos',v))
        input_area.bind(size=lambda i,v: setattr(self._ia,'size',v))
        div2 = BoxLayout(size_hint_y=None, height=dp(1))
        with div2.canvas.before:
            Color(0.85,0.85,0.85,1)
            RoundedRectangle(pos=div2.pos, size=div2.size)
        input_area.add_widget(div2)
        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56), padding=[dp(6),dp(6)], spacing=dp(4))
        def mkbtn(text, cb):
            b = Button(text=text,size_hint=(None,None),size=(dp(40),dp(44)),background_normal='',background_color=(0.95,0.95,0.95,1),color=(0.2,0.2,0.2,1),font_size=dp(16),bold=True)
            b.bind(on_press=cb)
            return b
        btn_row.add_widget(mkbtn('[A]',self.on_attach))
        btn_row.add_widget(mkbtn('[P]',self.on_photo))
        btn_row.add_widget(mkbtn('[V]',self.on_video))
        btn_row.add_widget(mkbtn('[M]',self.on_mic))
        self.txt = TextInput(hint_text='Сообщение...',multiline=False,size_hint=(1,None),height=dp(44),font_size=dp(16),background_normal='',background_active='',background_color=(0.97,0.97,0.97,1),foreground_color=(0.1,0.1,0.1,1),cursor_color=(0.24,0.52,0.98,1),padding=[dp(10),dp(10)])
        self.txt.bind(on_text_validate=self.send_message)
        btn_row.add_widget(self.txt)
        send = Button(text='>',size_hint=(None,None),size=(dp(44),dp(44)),background_normal='',background_color=(0.24,0.52,0.98,1),color=(1,1,1,1),font_size=dp(20),bold=True)
        send.bind(on_press=self.send_message)
        btn_row.add_widget(send)
        input_area.add_widget(btn_row)
        root.add_widget(input_area)
        Clock.schedule_once(lambda dt: self.add_message('Privet! Ja MAX AI.',False),0.4)
        return root
    def on_attach(self,*a):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self._file_selected)
        except Exception as e: self.add_message(f'Err: {e}',False)
    def _file_selected(self,selection):
        if not selection: return
        path=selection[0]; name=os.path.basename(path)
        self.add_message(f'File: {name}',True)
        threading.Thread(target=self._upload,args=(path,),daemon=True).start()
    def _upload(self,path):
        try:
            with open(path,'rb') as f:
                r=requests.post(f'{SERVER_URL}/upload',files={'file':(os.path.basename(path),f)},timeout=60)
                reply=r.json().get('response','OK')
        except Exception as e: reply=f'Err: {e}'
        Clock.schedule_once(lambda dt:self.add_message(reply,False))
    def on_photo(self,*a):
        try:
            from plyer import camera
            camera.take_picture(filename='/sdcard/maxai.jpg',on_complete=self._photo_done)
        except Exception as e: self.add_message(f'Err: {e}',False)
    def _photo_done(self,path):
        if path and os.path.exists(path):
            self.add_message('Photo OK',True)
            threading.Thread(target=self._upload,args=(path,),daemon=True).start()
        else: self.add_message('No photo',False)
    def on_video(self,*a): self.add_message('Video soon',False)
    def on_mic(self,*a): self.add_message('Mic soon',False)
    def send_message(self,*a):
        text=self.txt.text.strip()
        if not text: return
        self.txt.text=''
        self.add_message(text,True)
        self._t=MessageRow(text='...',is_user=False)
        self.msg_box.add_widget(self._t)
        Clock.schedule_once(lambda dt:setattr(self.scroll,'scroll_y',0),0.1)
        threading.Thread(target=self._api,args=(text,),daemon=True).start()
    def _api(self,text):
        try:
            r=requests.post(f'{SERVER_URL}/chat',json={'message':text},timeout=30)
            reply=r.json().get('response','no resp')
        except Exception as e: reply=f'Err: {e}'
        Clock.schedule_once(lambda dt:self._show(reply))
    def _show(self,text):
        if hasattr(self,'_t') and self._t in self.msg_box.children:
            self.msg_box.remove_widget(self._t)
        self.add_message(text,False)
    def add_message(self,text,is_user=True):
        row=MessageRow(text=text,is_user=is_user)
        self.msg_box.add_widget(row)
        Clock.schedule_once(lambda dt:setattr(self.scroll,'scroll_y',0),0.15)
if __name__=='__main__':
    MAXAIApp().run()
