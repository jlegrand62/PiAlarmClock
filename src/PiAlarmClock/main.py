#!/home/jonathan/venv/alarmclock/bin/python

import kivy
import pyowm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
import newspaper

from PiAlarmClock.components.buttons import SetAlarmButton, SleepButton
from PiAlarmClock.components.clock import ClockLabel
from PiAlarmClock.components.weather import WeatherStatusLabel

kivy.require("1.9.1")
owm = pyowm.OWM('f8ad5034578b3193450b67823d91f5bf')
STORE = JsonStore('../../config/settings.json')
SMART_SLEEP = 0
WEATHER_STAT = 0
NEWS_STAT = 0
NEWS_ARTICLE_NUM = 1
ALARM_HOUR = 0
ALARM_MINUTE = 0
ALARM_CHANGED = 0
WAIT_NEXT_MINUTE = 0
SMART_SLEEP_COUNT = 0
ALARM_PID = 999999999999
SUB_PROCESS = 0
WEATHER_ZIP = '69007'
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
    if STORE.exists('weather_stat'):
        global WEATHER_STAT
        WEATHER_STAT = STORE.get('weather_stat')['status']

    if STORE.exists('news_stat'):
        global NEWS_STAT
        NEWS_STAT = STORE.get('news_stat')['status']

    if STORE.exists('smart_sleep'):
        global SMART_SLEEP
        SMART_SLEEP = STORE.get('smart_sleep')['status']

    if STORE.exists('news_article_num'):
        global NEWS_ARTICLE_NUM
        NEWS_ARTICLE_NUM = STORE.get('news_article_num')['status']


# screenmanager to allow for dynamic transitions between screens of the system
class ScreenHandler(ScreenManager):
    pass


# main loop which runs the app and populates the UI
class PyAlarmClockApp(App):

    def build(self):
        if STORE.exists('weather_stat'):
            global WEATHER_STAT
            WEATHER_STAT = STORE.get('weather_stat')['status']

        if STORE.exists('news_stat'):
            global NEWS_STAT
            NEWS_STAT = STORE.get('news_stat')['status']

        if STORE.exists('smart_sleep'):
            global SMART_SLEEP
            SMART_SLEEP = STORE.get('smart_sleep')['status']

        if STORE.exists('news_article_num'):
            global NEWS_ARTICLE_NUM
            NEWS_ARTICLE_NUM = STORE.get('news_article_num')['status']

        # app = Builder.load_file("meza.kv")
        crudeclock = ClockLabel()
        alarmButton = SetAlarmButton()
        sleeper = SleepButton()
        weatherStat = WeatherStatusLabel()

        # return app


if __name__ == '__main__':
    PyAlarmClockApp().run()
