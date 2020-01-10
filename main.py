#!/home/jonathan/venc/alarmclock/bin/python

import kivy
import pyowm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
import newspaper

from Meza.buttons import SetAlarmButton, SleepButton
from Meza.clock import ClockLabel
from Meza.weather import WeatherStatusLabel

kivy.require("1.9.1")
owm = pyowm.OWM('f8ad5034578b3193450b67823d91f5bf')
store = JsonStore('settings.json')
smart_sleep = 0
weather_stat = 0
news_stat = 0
news_article_num = 1
alarm_hour = 0
alarm_minute = 0
alarm_changed = 0
wait_next_minute = 0
smart_sleep_count = 0
alarm_pid = 999999999999
sub_process = 0
weather_zip = '06106'
paper_name = 'NPR'
npr_paper = newspaper.build('http://npr.org/sections/technology', memoize_articles=False)
bbc_paper = newspaper.build('http://bbc.com/news/technology', memoize_articles=False)
wsj_paper = newspaper.build('http://wsj.com/news/technology', memoize_articles=False)


# special button added to the popup to ensure user selects and alarm and then saves it


# alarm picker button class and methods


# self-updating clock label used on the home screen to tell time and check the user-set alarms

# class to dim and brighten the backlight of the RPI when the user reports they are going to sleep/waking up


# main screen of the app for use with screenmanager


class SpecialFloatLayout(FloatLayout):
    pass


# settings screen for use with screenmanager
class SettingsScreen(Screen):
    # this allows for persistent storage to update the states of the labels in the settings
    if store.exists('weather_stat'):
        global weather_stat
        weather_stat = store.get('weather_stat')['status']

    if store.exists('news_stat'):
        global news_stat
        news_stat = store.get('news_stat')['status']

    if store.exists('smart_sleep'):
        global smart_sleep
        smart_sleep = store.get('smart_sleep')['status']

    if store.exists('news_article_num'):
        global news_article_num
        news_article_num = store.get('news_article_num')['status']


# screenmanager to allow for dynamic transitions between screens of the system
class ScreenHandler(ScreenManager):
    pass


# main loop which runs the app and populates the UI
class MezaApp(App):

    def build(self):
        if store.exists('weather_stat'):
            global weather_stat
            weather_stat = store.get('weather_stat')['status']

        if store.exists('news_stat'):
            global news_stat
            news_stat = store.get('news_stat')['status']

        if store.exists('smart_sleep'):
            global smart_sleep
            smart_sleep = store.get('smart_sleep')['status']

        if store.exists('news_article_num'):
            global news_article_num
            news_article_num = store.get('news_article_num')['status']

        # app = Builder.load_file("meza.kv")
        crudeclock = ClockLabel()
        alarmButton = SetAlarmButton()
        sleeper = SleepButton()
        weatherStat = WeatherStatusLabel()

        # return app


if __name__ == '__main__':
    MezaApp().run()
