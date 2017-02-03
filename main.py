import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time
from kivy.uix.label import Label

kivy.require("1.9.1")

class ClockLabel(Label):
    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        self.text = str(time.asctime())
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = str(time.asctime())
        

class ClockScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ScreenHandler(ScreenManager):
    pass

class MezaApp(App):

    def build(self):
        app = Builder.load_file("meza.kv")
        crudeclock = ClockLabel()
        return app

if __name__ == '__main__':
    MezaApp().run()
