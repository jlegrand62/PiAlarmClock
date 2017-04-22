import kivy
import os
import signal
import subprocess
import pyowm
import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
import time
from time import gmtime, strftime
import datetime
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from functools import partial
import re
import newspaper
from newspaper import Article, Source, Config
from time import sleep


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
npr_paper = newspaper.build('http://npr.org/sections/technology' , memoize_articles=False)
bbc_paper = newspaper.build('http://bbc.com/news/technology' , memoize_articles=False)
wsj_paper = newspaper.build('http://wsj.com/news/technology' , memoize_articles=False)

#status labels for Settings page which update based on state of their corresponding checkbox
class WeatherStatusLabel(Label):
    def __init__(self, **kwargs):
        super(WeatherStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup=True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global weather_stat
        if(weather_stat == 0):
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"

class SmartSleepStatusLabel(Label):
    def __init__(self, **kwargs):
        super(SmartSleepStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup=True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global smart_sleep
        if(smart_sleep == 0):
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"

class NewsStatusLabel(Label):
    def __init__(self, **kwargs):
        super(NewsStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup=True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global news_stat
        if(news_stat == 0):
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"

#buttons to set news/smartsleep/weather mdoules as active/inactive
class WeatherStatButton(Button):
    def __init__(self, **kwargs):
        super(WeatherStatButton, self).__init__(**kwargs)
        self.text = "Weather Module"

        if store.exists('weather_stat'):
            global weather_stat
            weather_stat = store.get('weather_stat')['status']

    def updateWeather(self):
        global weather_stat
        if(weather_stat == 0):
            store.put('weather_stat', status=1)
            weather_stat = 1
        else:
            store.put('weather_stat', status=0)
            weather_stat = 0

class NewsStatButton(Button):
    def __init__(self, **kwargs):
        super(NewsStatButton, self).__init__(**kwargs)
        self.text = "News Module"

        if store.exists('news_stat'):
            global weather_stat
            weather_stat = store.get('news_stat')['status']

    def updateNews(self):
        global news_stat
        if(news_stat == 0):
            store.put('news_stat', status=1)
            news_stat = 1
        else:
            store.put('news_stat', status=0)
            news_stat = 0

class SmartSleepStatButton(Button):
    def __init__(self, **kwargs):
        super(SmartSleepStatButton, self).__init__(**kwargs)
        self.text = "SmartSleep \n   Module"

    def updateSmartSleep(self):
        global smart_sleep
        if(smart_sleep == 0):
            store.put('smart_sleep', status=1)
            smart_sleep = 1
        else:
            store.put('smart_sleep', status=0)
            smart_sleep = 0

class NewsArticleNum(Button):
    def __init__(self, **kwargs):
        super(NewsArticleNum, self).__init__(**kwargs)
        self.text = "News Articles:"

    def updateArticleNum(self):
        global news_article_num
        if(news_article_num == 1):
            store.put('news_article_num', status = 3)
            news_article_num = 3

        elif(news_article_num == 3):
            store.put('news_article_num', status = 5)
            news_article_num = 5

        elif(news_article_num == 5):
            store.put('news_article_num', status = 1)
            news_article_num = 1
        
class NewsArticleNumLabel(Label):
    def __init__(self, **kwargs):
        super(NewsArticleNumLabel, self).__init__(**kwargs)
        global news_article_num
        self.markup = True
        self.text = "[color=000000]{}[/color]".format(news_article_num)
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global news_article_num
        self.text = "[color=000000]{}[/color]".format(news_article_num)

class NewsSourceButton(Button):
    def __init__(self, **kwargs):
        super(NewsSourceButton, self).__init__(**kwargs)
        self.text = "News Source:"

    def updateNewsSource(self):
        global paper_name
        global paper
        if(paper_name == 'NPR'):
            paper_name = 'BBC'

        elif(paper_name == 'BBC'):
            paper_name = 'WSJ'

        elif(paper_name == 'WSJ'):
            paper_name = 'NPR'

class NewsSourceLabel(Label):
    def __init__(self, **kwargs):
        super(NewsSourceLabel, self).__init__(**kwargs)
        global paper_name
        self.markup = True
        self.text = "{}".format(paper_name)
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global paper_name
        self.text = "[color=000000]{}[/color]".format(paper_name)

#special button added to the popup to ensure user selects and alarm and then saves it 
class PopupDismissButton(Button):
    def __init__(self, **kwargs):
        super(PopupDismissButton, self).__init__(**kwargs)
        self.text = "Set Alarm"
        self.size_hint=(.2,.2);
        self.pos_hint={'x':.4, 'y':.2}

    def dismissPopup(self, instance, button1, button2, button3):
        global alarm_hour
        global alarm_minute

        if(button1.text != "Select Hour" and button2.text != "Select Minute"):
            alarm_hour = int(button1.text)
            alarm_minute = int(button2.text)
            currentDay = time.strftime("%A")
            store.put(currentDay, alarm_hour = alarm_hour, alarm_minute = alarm_minute)
            
        instance.dismiss()

#alarm picker button class and methods
class SetAlarmButton(Button):
    def __init__(self, **kwargs):
        super(SetAlarmButton, self).__init__(**kwargs)
        self.text = "Press To Set Alarm"
        #schedule this button to continually look to update it's text to reflect the current alarm
        Clock.schedule_interval(self.update, 1)

    def on_press(self):
        Clock.schedule_once(self.alarmPopup)

    def alarmPopup(self, *args):
        #content of the popup to be sorted in this float layout
        box = FloatLayout()

        #hour selector
        hourbutton = Button(text='Select Hour', size_hint=(.2,.2),
                            pos_hint={'x':.2, 'y':.5})
        #dropdown menu which drops down from the hourbutton
        hourdropdown = DropDown()
        for i in range(24):
            if(i<10):
                btn=Button(text = '0%r' % i, size_hint_y=None, height =70)
            else:
                btn=Button(text = '%r' % i, size_hint_y=None, height =70)
            btn.bind(on_release=lambda btn: hourdropdown.select(btn.text))
            hourdropdown.add_widget(btn)

        hourbutton.bind(on_release=hourdropdown.open)
        hourdropdown.bind(on_select=lambda instance, x: setattr(hourbutton, 'text', x))
        #add widgets to the popup's float layout
        box.add_widget(hourbutton)
        box.add_widget(hourdropdown)

        #minute selector
        minutebutton = Button(text='Select Minute', size_hint=(.2,.2),
                            pos_hint={'x':.6, 'y':.5})
        #dopdown menu which drops down from the minutebutton
        minutedropdown = DropDown()
        for i in range(60):
            if(i<10):
                btn=Button(text = '0%r' % i, size_hint_y=None, height =70)
            else:
                btn=Button(text = '%r' % i, size_hint_y=None, height =70)
            btn.bind(on_release=lambda btn: minutedropdown.select(btn.text))
            minutedropdown.add_widget(btn)
        
        minutebutton.bind(on_release=minutedropdown.open)
        minutedropdown.bind(on_select=lambda instance, x: setattr(minutebutton, 'text', x))
        #add widgets to the popup's float layout
        box.add_widget(minutebutton)
        box.add_widget(minutedropdown)

        #button to dismiss alarm selector and set alarm once user has chosen alarm
        dismissButton = PopupDismissButton()
        box.add_widget(dismissButton)
        
        currentDay = time.strftime("%A")
        alarmPopup = Popup(title='Set Your Alarm for {}:'.format(currentDay), content=box, size_hint=(.8, .8))
        dismissButton.bind(on_press=partial(dismissButton.dismissPopup, alarmPopup, hourbutton, minutebutton))
        alarmPopup.open()

    def update(self, *args):
        global alarm_hour
        global alarm_minute
        currentDay = time.strftime("%A")
        self.valign = 'middle'
        self.halign = 'center'
        
        if store.exists(currentDay):
            alarm_hour = store.get(currentDay)['alarm_hour']
            alarm_minute = store.get(currentDay)['alarm_minute']

        #default state of alarm button before any alarms are set
        if(alarm_hour == 0 and alarm_minute == 0):
            self.text = "    Set Alarm\n Alarm Not Set".format(alarm_hour, alarm_minute)

        #text formatting to properly display the current alarm
        else:
            if(alarm_hour < 10 and alarm_minute < 10):
                self.text = "Set Alarm\n Currently 0{}:0{}".format(alarm_hour, alarm_minute)
            elif(alarm_minute < 10):
                self.text = "Set Alarm\n Currently {}:0{}".format(alarm_hour, alarm_minute)
            elif(alarm_hour < 10):
                self.text = "Set Alarm\n Currently 0{}:{}".format(alarm_hour, alarm_minute)
            else:
                self.text = "Set Alarm\n Currently {}:{}".format(alarm_hour, alarm_minute)
            
#self-updating clock label used on the home screen to tell time and check the user-set alarms
class ClockLabel(Label):
    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        self.valign = 'middle'
        self.halign = 'center'
        time_string = time.strftime("%H:%M")
        date_string = time.strftime("%A, %b %d")
        self.markup = True
        self.text ="[size=100]{}[/size] \n[size=25]{}[/size]".format(time_string, date_string)
        #schedule text update and alarm checking functions
        Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.checkAlarm, 1)
    
    #updates the label's text to properly reflect the current time
    def update(self, *args):
        time_string = time.strftime("%H:%M")
        date_string = time.strftime("%A, %b %d")        
        self.text ="[color=#8ac640][size=100]{}[/size] \n[size=25]{}[/size][/color]".format(time_string, date_string)
      
    #checks the alarm set by the user and calls the alarm function if the alarm occurs
    def checkAlarm(self, *args):
        global alarm_hour
        global alarm_minute
        now = datetime.datetime.now()
        local_hour = int(now.hour)
        local_minute = int(now.minute)
        global wait_next_minute 

        #logic to ensure alarm function only fires once when it is the alarm time
        if(wait_next_minute!=0 and local_minute!=alarm_minute):
            wait_next_minute = 0
        elif((local_hour == alarm_hour and local_minute == alarm_minute) and wait_next_minute == 0):
            self.alarm_func()
            wait_next_minute = 1
    #function called when the alarm fires, will execute different commands based on user settings
    def alarm_func(self, *args):
        global smart_sleep
        global weather_stat
        global news_stat
        import time
        weather = ''
        news = ''

        if(weather_stat == 1):
            observation = owm.weather_at_place('06106')
            w = observation.get_weather()
            status = w.get_status()
            string_status = "{}".format(status)
            if(string_status == "Rain"):
                stat = " Bring an umbrella or rain coat with you."
            elif(string_status == "Snow" or string_status == "Hail"):
                stat = " Warm clothing and boots advised."
            else:
                stat = ""
    
            temp_fetch = w.get_temperature('fahrenheit')
            temp_read = temp_fetch["temp"]
            if(temp_read <= 32.00):
                temp = "It is very cold today. Bring a heavy jacket with you and wear layers. "
            elif(temp_read <= 43.00):
                temp = "It is cold today.  Wear warm clothing and bring a jacket. "
            elif (temp_read <=60.00):
                temp = "It is temperate outside today.  A light jacket or sweatshirt would be a good idea. "
            elif(temp_read <= 72.00):
                temp = "It is warm outside today. Long pants are not necessary.  Bring a light jacket if it is windy. "
            else:
                temp = "It is hot outside today.  Make sure to bring water with you and wear something light. "
                    
            wind_fetch = w.get_wind()
            wind_read = wind_fetch["speed"]
            if(wind_read >= 4.00):
                wind = "It is windy today."
            else:
                wind = ""
            
            weather = ' The weather right now is, {}. {}.  It is currently {} degrees Farenheit. {} {}'.format(status, stat, temp_read, wind, temp)

        if(news_stat == 1):
            global news_article_num
            global paper_name
            
            if (paper_name == 'NPR'):
                paper = npr_paper
            if(paper_name == 'BBC'):
                paper = bbc_paper
            if (paper_name == 'WSJ'):
                paper = wsj_paper
                
            if(news_article_num == 1):
                first_article = paper.articles[2]
                first_article.download()
                first_article.parse()
                first_article.nlp()
                title = first_article.title.encode('ascii', 'ignore').decode('ascii')
                summary = first_article.summary.encode('ascii', 'ignore').decode('ascii')
                escaped_summary = summary.replace('"', '')
                print(title)
                print(escaped_summary)
                news = ' Now for daily news, Article 1: {} , {}'.format(title, escaped_summary)
                news = news.encode('ascii', 'ignore').decode('ascii')

            if(news_article_num == 3):   
                articles = []
                titles = []
                summary = []
                for i in range(3):
                    articles.append(paper.articles[i+2])
                    articles[i].download()
                    articles[i].parse()
                    articles[i].nlp()
                    print(articles[i].url)
                    titles.append(articles[i].title.encode('ascii', 'ignore').decode('ascii'))
                    summary.append((articles[i].summary).replace('"', '').encode('ascii', 'ignore').decode('ascii'))

                news = ' Now for daily news, Article 1: {} , {}. Article 2: {} , {}. Article 3: {} , {}. '.format(titles[0], summary[0], titles[1], summary[1], titles[2], summary[2]).encode('ascii', 'ignore').decode('ascii')
                

            if(news_article_num == 5):
                global paper
                articles = []
                titles = []
                summary = []
                for i in range(5):
                    articles.append(paper.articles[i+2])
                    articles[i].download()
                    articles[i].parse()
                    articles[i].nlp()
                    titles.append(articles[i].title.encode('ascii', 'ignore').decode('ascii'))
                    summary.append((articles[i].summary).replace('"', '').encode('ascii', 'ignore').decode('ascii'))

                news = ' Now for daily news, Article 1: {} , {}. Article 2: {} , {}. Article 3: {} , {}. Article 4: {} , {}. Article 5: {} , {}. '.format(titles[0], summary[0], titles[1], summary[1], titles[2], summary[2], titles[3], summary[3], titles[4], summary[4])
                news = news.encode('ascii', 'ignore').decode('ascii')
            
        currentDay = time.strftime("%A")
        currentDayNum = time.strftime("%d")
        currentMonth = time.strftime("%B")
        currentYear = time.strftime("%Y")
        time = 'Today is {}, {} {} {},'.format(currentDay, currentMonth, currentDayNum, currentYear)
        cmd = "pico2wave -w alarm.wav \"Good Morning! This is your alarm clock speaking! Time to wake up! {} {} {}\" && aplay alarm.wav".format(time, weather, news)
        sub = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, preexec_fn=os.setsid)
        global alarm_pid
        alarm_pid = os.getpgid(sub.pid)
        
        #os.system("pico2wave -w alarm.wav \"Good Morning! This is your alarm clock speaking! Time to wake up! {} {} {}\" && aplay alarm.wav".format(time, weather, news))

        
#class to dim and brighten the backlight of the RPI when the user reports they are going to sleep/waking up         
class SleepButton(Button):
    def __init__(self, **kwargs):
        super(SleepButton, self).__init__(**kwargs)
        self.text = "Good Night"

    def on_press(self):
        if self.text == "Good Night":
            os.system("echo 55 > /sys/class/backlight/rpi_backlight/brightness")
            now = datetime.datetime.now()
            self.text = "Good Morning"
        else:
            os.system("echo 255 > /sys/class/backlight/rpi_backlight/brightness")
            global smart_sleep
            if(smart_sleep == 1):
                if store.exists('smart_sleep_count'):
                    global smart_sleep_count
                    smart_sleep_count = store.get('smart_sleep_count')['count']

                global smart_sleep_count

                if(smart_sleep_count == 7):
                    smart_sleep_count = 0
                    store.put('smart_sleep_count', count = 0)
                    smart_sleep = 0
                    store.put('smart_sleep', status=0)
                    
                    
                    average = 0
                    for i in xrange(1, 8):
                        day = 'Day{}'.format(i)
                        temp = store.get(day)['total_time']
                        average = average + temp

                    average = average/7

                    counter = 0
                    while(average >=60):
                        average = average - 60
                        counter = counter+1

                    store.put('Monday', alarm_hour = counter, alarm_minute = average)
                    store.put('Tuesday', alarm_hour = counter, alarm_minute = average)
                    store.put('Wednesday', alarm_hour = counter, alarm_minute = average)
                    store.put('Thursday', alarm_hour = counter, alarm_minute = average)
                    store.put('Friday', alarm_hour = counter, alarm_minute = average)
                    store.put('Saturday', alarm_hour = counter, alarm_minute = average)
                    store.put('Sunday', alarm_hour = counter, alarm_minute = average)
                    
                else:
                    smart_sleep_count = smart_sleep_count+1
                    store.put('smart_sleep_count', count = smart_sleep_count)

                    now = datetime.datetime.now()
                    wake_hour = int(now.hour)
                    wake_min = int(now.minute)
                    total_time = wake_hour*60 + wake_min
                    day = 'Day{}'.format(smart_sleep_count)
                    currentDay = time.strftime("%A")
                    if(currentDay == "Saturday" or currentDay == "Sunday"):
                        weekend = 1
                    else:
                        weekend = 0
                    store.put(day, total_time = total_time, isWeekend = weekend)
                
            self.text = "Good Night"

class AlarmStopButton(Button):
    def __init__(self, **kwargs):
        super(AlarmStopButton, self).__init__(**kwargs)
        self.text = "Stop Alarm"
    

    def on_press(self):
        global alarm_pid

        if(alarm_pid != 999999999999):
            os.killpg(alarm_pid, signal.SIGTERM)
            alarm_pid = 999999999999
            
#main screen of the app for use with screenmanager
class ClockScreen(Screen):
    pass

class SpecialFloatLayout(FloatLayout):
    pass

#settings screen for use with screenmanager
class SettingsScreen(Screen):
    #this allows for persistent storage to update the states of the labels in the settings
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

#screenmanager to allow for dynamic transitions between screens of the system
class ScreenHandler(ScreenManager):
    pass

#main loop which runs the app and populates the UI
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
            
        #app = Builder.load_file("meza.kv")
        crudeclock = ClockLabel()
        alarmButton = SetAlarmButton()
        sleeper = SleepButton()
        weatherStat = WeatherStatusLabel()
        
        #return app

if __name__ == '__main__':
    MezaApp().run()
