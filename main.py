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
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from functools import partial


kivy.require("1.9.1")
smart_sleep = 0
weather_stat = 0
news_stat = 0
alarm_hour = 0
alarm_minute = 0

class WeatherStatusLabel(Label):
    def __init__(self, **kwargs):
        super(WeatherStatusLabel, self).__init__(**kwargs)
        self.text = "Disabled"

class SmartSleepStatusLabel(Label):
    def __init__(self, **kwargs):
        super(SmartSleepStatusLabel, self).__init__(**kwargs)
        self.text = "Disabled"

class NewsStatusLabel(Label):
    def __init__(self, **kwargs):
        super(NewsStatusLabel, self).__init__(**kwargs)
        self.text = "Disabled"

class SetAlarmButton(Button):
    def __init__(self, **kwargs):
        super(SetAlarmButton, self).__init__(**kwargs)
        self.text = "Press To Set Alarm"

    def alarmPopup(self):
        box = FloatLayout()

        #hour selector
        hourbutton = Button(text='Select Hour', size_hint=(.2,.2),
                            pos_hint={'x':.2, 'y':.5})
        hourdropdown = DropDown()
        for i in range(24):
            if(i<10):
                btn=Button(text = '0%r' % i, size_hint_y=None, height =30)
            else:
                btn=Button(text = '%r' % i, size_hint_y=None, height =30)
            btn.bind(on_release=lambda btn: hourdropdown.select(btn.text))
            hourdropdown.add_widget(btn)

        hourbutton.bind(on_release=hourdropdown.open)
        hourdropdown.bind(on_select=lambda instance, x: setattr(hourbutton, 'text', x))
        box.add_widget(hourbutton)
        box.add_widget(hourdropdown)

        #minute selector
        minutebutton = Button(text='Select Minute', size_hint=(.2,.2),
                            pos_hint={'x':.6, 'y':.5})
        minutedropdown = DropDown()
        for i in range(60):
            if(i<10):
                btn=Button(text = '0%r' % i, size_hint_y=None, height =30)
            else:
                btn=Button(text = '%r' % i, size_hint_y=None, height =30)
            btn.bind(on_release=lambda btn: minutedropdown.select(btn.text))
            minutedropdown.add_widget(btn)
        
        minutebutton.bind(on_release=minutedropdown.open)
        minutedropdown.bind(on_select=lambda instance, x: setattr(minutebutton, 'text', x))
        box.add_widget(minutebutton)
        box.add_widget(minutedropdown)

        dismissButton = PopupDismissButton()
        box.add_widget(dismissButton)
        
        
        alarmPopup = Popup(title='Set Your Alarm:', content=box, size_hint=(.9, .9))
        dismissButton.bind(on_press=partial(dismissButton.dismissPopup, alarmPopup, hourbutton, minutebutton))
        alarmPopup.open()

class PopupDismissButton(Button):
    def __init__(self, **kwargs):
        super(PopupDismissButton, self).__init__(**kwargs)
        self.text = "Set Alarm"
        self.size_hint=(.2,.2);
        self.pos_hint={'x':.5, 'y':.2}

    def dismissPopup(self, instance, button1, button2, button3):
        global alarm_hour
        global alarm_minute

        alarm_hour = button1.text
        alarm_minute = button2.text

        instance.dismiss()

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

class WeatherCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(WeatherCheckBox, self).__init__(**kwargs)

    def updateWeather(self):
        global weather_stat
        if(weather_stat == 0):
            weather_stat = 1
        else:
            weather_stat = 0

class SmartSleepCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(SmartSleepCheckBox, self).__init__(**kwargs)

    def updateSmartSleep(self):
        global smart_sleep
        if(smart_sleep == 0):
            smart_sleep = 1
        else:
            smart_sleep = 0

class NewsCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super(NewsCheckBox, self).__init__(**kwargs)

    def updateNews(self):
        global news_stat
        if(news_stat == 0):
            news_stat = 1
        else:
            news_stat = 0    
        
class SettingsScreen(Screen):
    pass

class ScreenHandler(ScreenManager):
    pass

class MezaApp(App):

    def build(self):
        app = Builder.load_file("meza.kv")
        crudeclock = ClockLabel()
        sleeper = SleepButton()
        weatherStat = WeatherStatusLabel()
        weatherBox = WeatherCheckBox()
        
        return app

if __name__ == '__main__':
    MezaApp().run()
