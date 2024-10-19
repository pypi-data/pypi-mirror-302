from feedgen.feed import FeedGenerator
import os

FEED_PATH = 'rss_feed.xml'

class FeedManager:
    def __init__(self):
        self.fg = FeedGenerator()
        if os.path.exists(FEED_PATH):
            self.fg.load_extension(FEED_PATH)
    
    def create_feed(self, title, link, description):
        self.fg.title(title)
        self.fg.link(href=link)
        self.fg.description(description)
        self.fg.language('en')
        self.save_feed()
    
    def save_feed(self):
        self.fg.rss_file(FEED_PATH)
    
    def load_feed(self):
        if os.path.exists(FEED_PATH):
            self.fg.load_extension(FEED_PATH)
    
    def edit_metadata(self, new_title, new_link, new_description):
        self.fg.title(new_title)
        self.fg.link(href=new_link)
        self.fg.description(new_description)
        self.save_feed()
