import datetime

class Article:
    def __init__(self, headline, link, date = datetime.datetime(1970, 1, 1), source = ""):
        self.headline = headline
        self.link = link
        self.date = date
        self.source = source
    
    def __str__(self):
        return f"{self.headline}, {self.date}, {self.link}, {self.source}"
    
    #getters and setters
    def getHeadline(self):
        return self.headline
    def getLink(self):
        return self.link
    def getDate(self):
        return self.date
    def getSource(self):
        return self.source
    
    def setHeadline(self, headline):
        self.headline = headline
    def setLink(self, link):
        self.link = link
    def setDate(self, date):
        self.date = date
    def setSource(self, source):
        self.source = source