import kivy
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
import time
from kivy.uix.label import Label
from kivy.uix.button import Button


kivy.require("1.9.1")

class ClockLabel(Label):
    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        self.text = str(time.asctime())
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = str(time.asctime())

class SleepButton(Button):
    def __init__(self, **kwargs):
        super(SleepButton, self).__init__(**kwargs)
        self.text = "Good Night"

    def on_press(self):
        if self.text == "Good Night":
            os.system("echo 55 > /sys/class/backlight/rpi_backlight/brightness")
            self.text = "Good Morning"
        else:
            self.text = "Good Night"
            os.system("echo 255 > /sys/class/backlight/rpi_backlight/brightness")

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
        sleeper = SleepButton()
        return app

if __name__ == '__main__':
    MezaApp().run()
