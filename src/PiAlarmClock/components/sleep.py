from kivy.clock import Clock
from kivy.uix.label import Label

import PiAlarmClock.config.config as cfg


#status labels for Settings page which update based on state of their corresponding checkbox
class SmartSleepStatusLabel(Label):
    def __init__(self, **kwargs):
        super(SmartSleepStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup = True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        if cfg.SMART_SLEEP == 0:
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"


