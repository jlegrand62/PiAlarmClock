from os.path import dirname, abspath, join
from kivy.storage.jsonstore import JsonStore

_ROOT = abspath(dirname(__file__))

STORE = JsonStore(join(_ROOT, 'settings.json'))

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
PAPER_NAME = 'NPR'
