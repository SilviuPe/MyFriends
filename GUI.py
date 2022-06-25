from kivy.clock import  mainthread
from kivy.config import Config
import kivy
from time import sleep
Config.set('graphics', 'width', 1580)
Config.set('graphics', 'height', 820)

from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from client import Client
from kivy.core.window import Window
import threading


client = Client()
t = threading.Thread(target=client.recv)

class ManageScreens(ScreenManager):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.transition = kivy.uix.screenmanager.NoTransition()

class Main(MDApp):
    def build(self) -> None:
        self.theme_cls.theme_style = 'Dark'
        self.title = "myFriends"
        kv = Builder.load_file('my.kv')
        return kv

class LogInWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        return client.login(self.username.text, self.password.text)
                

    def clear_text_fields(self):
        self.username.text = str()
        self.password.text = str()

class RegisterWindow(Screen):

    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def register(self):
        return client.register(self.username.text,self.password.text)

    def clear_text_fields(self):
        self.username.text = str()
        self.password.text = str()


class CustomLabel(MDLabel):
    pass


class MainScreen(Screen):

    messages = ObjectProperty(None)
    text = ObjectProperty(None)
    def __init__(self, **kw):
        super(MainScreen,self).__init__(**kw)
        Window.bind(on_key_down=self._on_keyboard_down)


    @mainthread
    def add_message(self, username: str, message: str):
        self.messages.add_widget(CustomLabel(text="[size=17][i][b]" + username + ":[/b][/i][/size]  " + message))

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.text.focus and keycode == 40:
            self.send()
            self.text.text = str()

    def on_pre_enter(self, *args):
        sleep(1)
        threading.Thread(target = self.receive_messages).start()
        print(True)

    def receive_messages(self):
        while True:
            if client.recv() == "message_done":
                self.add_message(client.username,client.message)

    def send(self) -> None:
        client.send(self.text.text)



main = Main().run()
client.server.close()
