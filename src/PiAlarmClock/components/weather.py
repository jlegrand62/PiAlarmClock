from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label

import PiAlarmClock.config.config as cfg


class WeatherStatButton(Button):
    def __init__(self, **kwargs):
        super(WeatherStatButton, self).__init__(**kwargs)
        self.text = "Weather Module"

        if cfg.STORE.exists('weather_stat'):
            cfg.WEATHER_STAT = cfg.STORE.get('weather_stat')['status']

    def updateWeather(self):
        if cfg.WEATHER_STAT == 0:
            cfg.STORE.put('weather_stat', status=1)
            cfg.WEATHER_STAT = 1
        else:
            cfg.STORE.put('weather_stat', status=0)
            cfg.WEATHER_STAT = 0


#status labels for Settings page which update based on state of their corresponding checkbox
class WeatherStatusLabel(Label):
    def __init__(self, **kwargs):
        super(WeatherStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup = True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        if cfg.WEATHER_STAT == 0:
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"