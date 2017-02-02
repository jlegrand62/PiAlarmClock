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

class ClockScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ScreenHandler(ScreenManager):
    pass

app = Builder.load_file("meza.kv")

class MezaApp(App):

    def build(self):
        return app

if __name__ == '__main__':
    MezaApp().run()
