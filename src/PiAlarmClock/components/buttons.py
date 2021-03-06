#!/home/jonathan/venc/alarmclock/bin/python

"""
Buttons to set news/smartsleep/weather mdoules as active/inactive
"""

import datetime
import os
import signal
import time
from functools import partial

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

import PiAlarmClock.config.config as cfg


class PopupDismissButton(Button):
    # special button added to the popup to ensure user selects and alarm and then saves it
    def __init__(self, **kwargs):
        super(PopupDismissButton, self).__init__(**kwargs)
        self.text = "Set Alarm"
        self.size_hint = (.2, .2)
        self.pos_hint = {'x': .4, 'y': .2}

    def dismissPopup(self, instance, button1, button2, button3):
        if button1.text != "Select Hour" and button2.text != "Select Minute":
            cfg.ALARM_HOUR = int(button1.text)
            cfg.ALARM_MINUTE = int(button2.text)
            currentDay = time.strftime("%A")
            cfg.STORE.put(currentDay, alarm_hour=cfg.ALARM_HOUR, alarm_minute=cfg.ALARM_MINUTE)

        instance.dismiss()


class SetAlarmButton(Button):
    def __init__(self, **kwargs):
        super(SetAlarmButton, self).__init__(**kwargs)
        self.text = "Press To Set Alarm"
        # schedule this button to continually look to update it's text to reflect the current alarm
        Clock.schedule_interval(self.update, 1)

    def on_press(self):
        Clock.schedule_once(self.alarmPopup)

    def alarmPopup(self, *args):
        # content of the popup to be sorted in this float layout
        box = FloatLayout()

        # hour selector
        hourbutton = Button(text='Select Hour', size_hint=(.2, .2),
                            pos_hint={'x': .2, 'y': .5})
        # dropdown menu which drops down from the hourbutton
        hourdropdown = DropDown()
        for i in range(24):
            if i < 10:
                btn = Button(text='0%r' % i, size_hint_y=None, height=70)
            else:
                btn = Button(text='%r' % i, size_hint_y=None, height=70)
            btn.bind(on_release=lambda btn: hourdropdown.select(btn.text))
            hourdropdown.add_widget(btn)

        hourbutton.bind(on_release=hourdropdown.open)
        hourdropdown.bind(on_select=lambda instance, x: setattr(hourbutton, 'text', x))
        # add widgets to the popup's float layout
        box.add_widget(hourbutton)
        box.add_widget(hourdropdown)

        # minute selector
        minutebutton = Button(text='Select Minute', size_hint=(.2, .2),
                              pos_hint={'x': .6, 'y': .5})
        # dopdown menu which drops down from the minutebutton
        minutedropdown = DropDown()
        for i in range(60):
            if i < 10:
                btn = Button(text='0%r' % i, size_hint_y=None, height=70)
            else:
                btn = Button(text='%r' % i, size_hint_y=None, height=70)
            btn.bind(on_release=lambda btn: minutedropdown.select(btn.text))
            minutedropdown.add_widget(btn)

        minutebutton.bind(on_release=minutedropdown.open)
        minutedropdown.bind(on_select=lambda instance, x: setattr(minutebutton, 'text', x))
        # add widgets to the popup's float layout
        box.add_widget(minutebutton)
        box.add_widget(minutedropdown)

        # button to dismiss alarm selector and set alarm once user has chosen alarm
        dismissButton = PopupDismissButton()
        box.add_widget(dismissButton)

        currentDay = time.strftime("%A")
        alarmPopup = Popup(title='Set Your Alarm for {}:'.format(currentDay), content=box, size_hint=(.8, .8))
        dismissButton.bind(on_press=partial(dismissButton.dismissPopup, alarmPopup, hourbutton, minutebutton))
        alarmPopup.open()

    def update(self, *args):
        currentDay = time.strftime("%A")
        self.valign = 'middle'
        self.halign = 'center'

        if cfg.STORE.exists(currentDay):
            cfg.ALARM_HOUR = cfg.STORE.get(currentDay)['alarm_hour']
            cfg.ALARM_MINUTE = cfg.STORE.get(currentDay)['alarm_minute']

        # default state of alarm button before any alarms are set
        if cfg.ALARM_HOUR == 0 and cfg.ALARM_MINUTE == 0:
            self.text = "    Set Alarm\n Alarm Not Set".format(cfg.ALARM_HOUR, cfg.ALARM_MINUTE)

        # text formatting to properly display the current alarm
        else:
            if cfg.ALARM_HOUR < 10 and cfg.ALARM_MINUTE < 10:
                self.text = "Set Alarm\n Currently 0{}:0{}".format(cfg.ALARM_HOUR, cfg.ALARM_MINUTE)
            elif cfg.ALARM_MINUTE < 10:
                self.text = "Set Alarm\n Currently {}:0{}".format(cfg.ALARM_HOUR, cfg.ALARM_MINUTE)
            elif cfg.ALARM_HOUR < 10:
                self.text = "Set Alarm\n Currently 0{}:{}".format(cfg.ALARM_HOUR, cfg.ALARM_MINUTE)
            else:
                self.text = "Set Alarm\n Currently {}:{}".format(cfg.ALARM_HOUR, cfg.ALARM_MINUTE)


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
            if cfg.SMART_SLEEP == 1:
                if cfg.STORE.exists('smart_sleep_count'):
                    cfg.SMART_SLEEP_COUNT = cfg.STORE.get('smart_sleep_count')['count']
                else:
                    cfg.SMART_SLEEP_COUNT = 0

                if cfg.SMART_SLEEP_COUNT == 7:
                    cfg.SMART_SLEEP_COUNT = 0
                    cfg.STORE.put('smart_sleep_count', count=0)
                    cfg.SMART_SLEEP = 0
                    cfg.STORE.put('smart_sleep', status=0)

                    average = 0
                    for i in range(1, 8):
                        day = 'Day{}'.format(i)
                        temp = cfg.STORE.get(day)['total_time']
                        average = average + temp

                    average = average / 7

                    counter = 0
                    while average >= 60:
                        average = average - 60
                        counter = counter + 1

                    cfg.STORE.put('Monday', alarm_hour=counter, alarm_minute=average)
                    cfg.STORE.put('Tuesday', alarm_hour=counter, alarm_minute=average)
                    cfg.STORE.put('Wednesday', alarm_hour=counter, alarm_minute=average)
                    cfg.STORE.put('Thursday', alarm_hour=counter, alarm_minute=average)
                    cfg.STORE.put('Friday', alarm_hour=counter, alarm_minute=average)
                    cfg.STORE.put('Saturday', alarm_hour=counter, alarm_minute=average)
                    cfg.STORE.put('Sunday', alarm_hour=counter, alarm_minute=average)

                else:
                    cfg.SMART_SLEEP_COUNT = cfg.SMART_SLEEP_COUNT + 1
                    cfg.STORE.put('smart_sleep_count', count=cfg.SMART_SLEEP_COUNT)

                    now = datetime.datetime.now()
                    wake_hour = int(now.hour)
                    wake_min = int(now.minute)
                    total_time = wake_hour * 60 + wake_min
                    day = 'Day{}'.format(cfg.SMART_SLEEP_COUNT)
                    currentDay = time.strftime("%A")
                    if currentDay == "Saturday" or currentDay == "Sunday":
                        weekend = 1
                    else:
                        weekend = 0
                    cfg.STORE.put(day, total_time=total_time, isWeekend=weekend)

            self.text = "Good Night"


class AlarmStopButton(Button):
    def __init__(self, **kwargs):
        super(AlarmStopButton, self).__init__(**kwargs)
        self.text = "Stop Alarm"

    def on_press(self):
        if cfg.ALARM_PID != 999999999999:
            os.killpg(cfg.ALARM_PID, signal.SIGTERM)
            cfg.ALARM_PID = 999999999999


class SmartSleepStatButton(Button):
    def __init__(self, **kwargs):
        super(SmartSleepStatButton, self).__init__(**kwargs)
        self.text = "SmartSleep \n   Module"

    def updateSmartSleep(self):
        if cfg.SMART_SLEEP == 0:
            cfg.STORE.put('smart_sleep', status=1)
            cfg.SMART_SLEEP = 1
        else:
            cfg.STORE.put('smart_sleep', status=0)
            cfg.SMART_SLEEP = 0
