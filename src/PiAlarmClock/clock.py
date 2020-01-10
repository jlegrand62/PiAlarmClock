import datetime
import os
import subprocess
import time

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from PiAlarmClock.src.PiAlarmClock.main import owm, npr_paper, bbc_paper, wsj_paper


#status labels for Settings page which update based on state of their corresponding checkbox
class ClockLabel(Label):
    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        self.valign = 'middle'
        self.halign = 'center'
        time_string = time.strftime("%H:%M")
        date_string = time.strftime("%A, %b %d")
        self.markup = True
        self.text = "[size=100]{}[/size] \n[size=25]{}[/size]".format(time_string, date_string)
        # schedule text update and alarm checking functions
        Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.checkAlarm, 1)

    # updates the label's text to properly reflect the current time
    def update(self, *args):
        time_string = time.strftime("%H:%M")
        date_string = time.strftime("%A, %b %d")
        self.text = "[color=#8ac640][size=100]{}[/size] \n[size=25]{}[/size][/color]".format(time_string, date_string)

    # checks the alarm set by the user and calls the alarm function if the alarm occurs
    def checkAlarm(self, *args):
        global alarm_hour
        global alarm_minute
        now = datetime.datetime.now()
        local_hour = int(now.hour)
        local_minute = int(now.minute)
        global wait_next_minute

        # logic to ensure alarm function only fires once when it is the alarm time
        if wait_next_minute != 0 and local_minute != alarm_minute:
            wait_next_minute = 0
        elif (local_hour == alarm_hour and local_minute == alarm_minute) and wait_next_minute == 0:
            self.alarm_func()
            wait_next_minute = 1

    # function called when the alarm fires, will execute different commands based on user settings
    def alarm_func(self, *args):
        global smart_sleep
        global weather_stat
        global news_stat
        import time
        weather = ''
        news = ''

        if weather_stat == 1:
            observation = owm.weather_at_place('06106')
            w = observation.get_weather()
            status = w.get_status()
            string_status = "{}".format(status)
            if string_status == "Rain":
                stat = " Bring an umbrella or rain coat with you."
            elif string_status == "Snow" or string_status == "Hail":
                stat = " Warm clothing and boots advised."
            else:
                stat = ""

            temp_fetch = w.get_temperature('fahrenheit')
            temp_read = temp_fetch["temp"]
            if temp_read <= 32.00:
                temp = "It is very cold today. Bring a heavy jacket with you and wear layers. "
            elif temp_read <= 43.00:
                temp = "It is cold today.  Wear warm clothing and bring a jacket. "
            elif temp_read <= 60.00:
                temp = "It is temperate outside today.  A light jacket or sweatshirt would be a good idea. "
            elif temp_read <= 72.00:
                temp = "It is warm outside today. Long pants are not necessary.  Bring a light jacket if it is windy. "
            else:
                temp = "It is hot outside today.  Make sure to bring water with you and wear something light. "

            wind_fetch = w.get_wind()
            wind_read = wind_fetch["speed"]
            if wind_read >= 4.00:
                wind = "It is windy today."
            else:
                wind = ""

            weather = f" The weather right now is, {status}."
            weather += f" {stat}"
            weather += f" It is currently {temp_read} degrees Farenheit."
            weather += " {wind} {temp}"

        if news_stat == 1:
            global news_article_num
            global paper_name

            if paper_name == 'NPR':
                paper = npr_paper
            elif paper_name == 'BBC':
                paper = bbc_paper
            elif paper_name == 'WSJ':
                paper = wsj_paper
            else:
                raise ValueError(f"Unknown paper name: {paper_name}!")

            if news_article_num == 1:
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

            if news_article_num == 3:
                articles = []
                titles = []
                summary = []
                for i in range(3):
                    articles.append(paper.articles[i + 2])
                    articles[i].download()
                    articles[i].parse()
                    articles[i].nlp()
                    print(articles[i].url)
                    titles.append(articles[i].title.encode('ascii', 'ignore').decode('ascii'))
                    summary.append(articles[i].summary.replace('"', '').encode('ascii', 'ignore').decode('ascii'))

                news = ' Now for daily news, Article 1: {} , {}. Article 2: {} , {}. Article 3: {} , {}. '.format(
                    titles[0], summary[0], titles[1], summary[1], titles[2], summary[2]).encode('ascii',
                                                                                                'ignore').decode(
                    'ascii')

            if news_article_num == 5:
                articles = []
                titles = []
                summary = []
                for i in range(5):
                    articles.append(paper.articles[i + 2])
                    articles[i].download()
                    articles[i].parse()
                    articles[i].nlp()
                    titles.append(articles[i].title.encode('ascii', 'ignore').decode('ascii'))
                    summary.append(articles[i].summary.replace('"', '').encode('ascii', 'ignore').decode('ascii'))

                news = ' Now for daily news, Article 1: {} , {}. Article 2: {} , {}. Article 3: {} , {}. Article 4: {} , {}. Article 5: {} , {}. '.format(
                    titles[0], summary[0], titles[1], summary[1], titles[2], summary[2], titles[3], summary[3],
                    titles[4], summary[4])
                news = news.encode('ascii', 'ignore').decode('ascii')

        currentDay = time.strftime("%A")
        currentDayNum = time.strftime("%d")
        currentMonth = time.strftime("%B")
        currentYear = time.strftime("%Y")
        time = 'Today is {}, {} {} {},'.format(currentDay, currentMonth, currentDayNum, currentYear)
        cmd = "pico2wave -w alarm.wav \"Good Morning! This is your alarm clock speaking! Time to wake up! {} {} {}\" && aplay alarm.wav".format(
            time, weather, news)
        sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        global alarm_pid
        alarm_pid = os.getpgid(sub.pid)
        # cmd = "pico2wave -w alarm.wav \"Good Morning! This is your alarm clock speaking! Time to wake up! {} {} {}\" && aplay alarm.wav".format(
        #     time, weather, news)
        # sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        # global alarm_pid
        # alarm_pid = os.getpgid(sub.pid)
        cmd = "python /home/jonathan/Projects/alarmclock/PiAlarmClock/alarm.py"
        sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        global alarm_pid
        alarm_pid = os.getpgid(sub.pid)

        # os.system("pico2wave -w alarm.wav \"Good Morning! This is your alarm clock speaking! Time to wake up! {} {} {}\" && aplay alarm.wav".format(time, weather, news))


class ClockScreen(Screen):
    pass