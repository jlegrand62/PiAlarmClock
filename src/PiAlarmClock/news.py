from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label

from main import store


class NewsStatButton(Button):
    def __init__(self, **kwargs):
        super(NewsStatButton, self).__init__(**kwargs)
        self.text = "News Module"

        if store.exists('news_stat'):
            global weather_stat
            weather_stat = store.get('news_stat')['status']

    def updateNews(self):
        global news_stat
        if news_stat == 0:
            store.put('news_stat', status=1)
            news_stat = 1
        else:
            store.put('news_stat', status=0)
            news_stat = 0


class NewsArticleNum(Button):
    def __init__(self, **kwargs):
        super(NewsArticleNum, self).__init__(**kwargs)
        self.text = "News Articles:"

    def updateArticleNum(self):
        global news_article_num
        if news_article_num == 1:
            store.put('news_article_num', status=3)
            news_article_num = 3

        elif news_article_num == 3:
            store.put('news_article_num', status=5)
            news_article_num = 5

        elif news_article_num == 5:
            store.put('news_article_num', status=1)
            news_article_num = 1


class NewsStatusLabel(Label):
    def __init__(self, **kwargs):
        super(NewsStatusLabel, self).__init__(**kwargs)
        self.text = "[color=f44253]Disabled[/color]"
        self.markup = True
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):
        global news_stat
        if news_stat == 0:
            self.text = "[color=f44253]Disabled[/color]"
        else:
            self.text = "[color=42f445]Enabled[/color]"


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
        if paper_name == 'NPR':
            paper_name = 'BBC'

        elif paper_name == 'BBC':
            paper_name = 'WSJ'

        elif paper_name == 'WSJ':
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