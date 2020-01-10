from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label

from PiAlarmClock.main import cfg.STORE


class NewsStatButton(Button):
    def __init__(self, **kwargs):
        super(NewsStatButton, self).__init__(**kwargs)
        self.text = "News Module"

        if cfg.STORE.exists('news_stat'):
            cfg.WEATHER_STAT = cfg.STORE.get('news_stat')['status']

    def updateNews(self):
        if cfg.NEWS_STAT == 0:
            cfg.STORE.put('news_stat', status=1)
            cfg.NEWS_STAT = 1
        else:
            cfg.STORE.put('news_stat', status=0)
            cfg.NEWS_STAT = 0


class NewsArticleNum(Button):
    def __init__(self, **kwargs):
        super(NewsArticleNum, self).__init__(**kwargs)
        self.text = "News Articles:"

    def updateArticleNum(self):
        if cfg.NEWS_ARTICLE_NUM == 1:
            cfg.STORE.put('news_article_num', status=3)
            cfg.NEWS_ARTICLE_NUM = 3

        elif cfg.NEWS_ARTICLE_NUM == 3:
            cfg.STORE.put('news_article_num', status=5)
            cfg.NEWS_ARTICLE_NUM = 5

        elif cfg.NEWS_ARTICLE_NUM == 5:
            cfg.STORE.put('news_article_num', status=1)
            cfg.NEWS_ARTICLE_NUM = 1


class NewsStatusLabel(Label):
    def __init__(self, **kwargs):
        super(NewsStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup = True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        if cfg.NEWS_STAT == 0:
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"


class NewsArticleNumLabel(Label):
    def __init__(self, **kwargs):
        super(NewsArticleNumLabel, self).__init__(**kwargs)
        self.markup = True
        self.text = "[color=000000]{}[/color]".format(cfg.NEWS_ARTICLE_NUM)
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        self.text = "[color=000000]{}[/color]".format(cfg.NEWS_ARTICLE_NUM)


class NewsSourceButton(Button):
    def __init__(self, **kwargs):
        super(NewsSourceButton, self).__init__(**kwargs)
        self.text = "News Source:"

    def updateNewsSource(self):
        if cfg.PAPER_NAME == 'NPR':
            cfg.PAPER_NAME = 'BBC'

        elif cfg.PAPER_NAME == 'BBC':
            cfg.PAPER_NAME = 'WSJ'

        elif cfg.PAPER_NAME == 'WSJ':
            cfg.PAPER_NAME = 'NPR'


class NewsSourceLabel(Label):
    def __init__(self, **kwargs):
        super(NewsSourceLabel, self).__init__(**kwargs)
        self.markup = True
        self.text = "{}".format(cfg.PAPER_NAME)
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        self.text = "[color=000000]{}[/color]".format(cfg.PAPER_NAME)