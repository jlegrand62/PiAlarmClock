from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label

from PiAlarmClock.main import STORE


class WeatherStatButton(Button):
    def __init__(self, **kwargs):
        super(WeatherStatButton, self).__init__(**kwargs)
        self.text = "Weather Module"

        if STORE.exists('weather_stat'):
            global weather_stat
            weather_stat = STORE.get('weather_stat')['status']

    def updateWeather(self):
        global weather_stat
        if weather_stat == 0:
            STORE.put('weather_stat', status=1)
            weather_stat = 1
        else:
            STORE.put('weather_stat', status=0)
            weather_stat = 0


#status labels for Settings page which update based on state of their corresponding checkbox
class WeatherStatusLabel(Label):
    def __init__(self, **kwargs):
        super(WeatherStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup = True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global weather_stat
        if weather_stat == 0:
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"