from rsstools.feed_manager import FeedManager

def add_entry(title, link, description):
    fm = FeedManager()
    fe = fm.fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.description(description)
    fm.save_feed()

def remove_entry(title):
    fm = FeedManager()
    entries = fm.fg._FeedGenerator__entries
    fm.fg._FeedGenerator__entries = [e for e in entries if e['title']['value'] != title]
    fm.save_feed()

def show_feed():
    fm = FeedManager()
    for entry in fm.fg.entries():
        print(f"Title: {entry.title}, Link: {entry.link}, Description: {entry.description}")
