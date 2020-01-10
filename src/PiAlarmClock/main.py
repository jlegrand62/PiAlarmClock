#!/home/jonathan/venv/alarmclock/bin/python

import kivy
import pyowm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
import newspaper

import PiAlarmClock.config.config as cfg

kivy.require("1.9.1")
owm = pyowm.OWM('f8ad5034578b3193450b67823d91f5bf')

npr_paper = newspaper.build('http://npr.org/sections/technology', memoize_articles=False)
bbc_paper = newspaper.build('http://bbc.com/news/technology', memoize_articles=False)
wsj_paper = newspaper.build('http://wsj.com/news/technology', memoize_articles=False)


class SpecialFloatLayout(FloatLayout):
    pass


# settings screen for use with screenmanager
class SettingsScreen(Screen):
    # this allows for persistent storage to update the states of the labels in the settings
    if cfg.STORE.exists('weather_stat'):
        cfg.WEATHER_STAT = cfg.STORE.get('weather_stat')['status']

    if cfg.STORE.exists('news_stat'):
        cfg.NEWS_STAT = cfg.STORE.get('news_stat')['status']

    if cfg.STORE.exists('smart_sleep'):
        cfg.SMART_SLEEP = cfg.STORE.get('smart_sleep')['status']

    if cfg.STORE.exists('news_article_num'):
        cfg.NEWS_ARTICLE_NUM = cfg.STORE.get('news_article_num')['status']


# screenmanager to allow for dynamic transitions between screens of the system
class ScreenHandler(ScreenManager):
    pass


# main loop which runs the app and populates the UI
class PyAlarmClockApp(App):

    def build(self):
        from PiAlarmClock.components.buttons import SetAlarmButton, SleepButton
        from PiAlarmClock.components.clock import ClockLabel
        from PiAlarmClock.components.weather import WeatherStatusLabel

        if cfg.STORE.exists('weather_stat'):
            cfg.WEATHER_STAT = cfg.STORE.get('weather_stat')['status']

        if cfg.STORE.exists('news_stat'):
            cfg.NEWS_STAT = cfg.STORE.get('news_stat')['status']

        if cfg.STORE.exists('smart_sleep'):
            cfg.SMART_SLEEP = cfg.STORE.get('smart_sleep')['status']

        if cfg.STORE.exists('news_article_num'):
            cfg.NEWS_ARTICLE_NUM = cfg.STORE.get('news_article_num')['status']

        # app = Builder.load_file("PyAlarmClock.kv")
        crudeclock = ClockLabel()
        alarmButton = SetAlarmButton()
        sleeper = SleepButton()
        weatherStat = WeatherStatusLabel()

        # return app


if __name__ == '__main__':
    PyAlarmClockApp().run()
