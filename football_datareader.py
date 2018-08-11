from html.parser import HTMLParser
import urllib.request
import pandas as pd

PFR = 'https://www.pro-football-reference.com/{}.htm'

class MyHTMLParser(HTMLParser):
    data_sources = []
    parse_data = False
    def handle_starttag(self, tag, attrs):
        if tag=='h1' and attrs and attrs[0][1]=="name":
            self.parse_data = True

    def handle_data(self, data):
        if self.parse_data:
            self.data_sources.append(data.strip())
            self.parse_data = False

def pull_hist_stats_by_name(name):
    first_last = name.split()
    plr_stng = "players/"+first_last[1][0]+"/"+first_last[1][0:4]+first_last[0][0:2]
    num=find_player(name, plr_stng)
    return pd.read_html(PFR.format(plr_stng+num), skiprows=1, header=0)[0]

def find_player(name, plr_stng):
    plr_name = ""
    num = 0
    while plr_name != name:
        num_st = str(num)
        if num < 10:
            num_st = '0' + num_st
        fp = urllib.request.urlopen(PFR.format(plr_stng + num_st))
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        parser = MyHTMLParser()
        parser.feed(mystr)
        if parser.data_sources:
            plr_name = parser.data_sources[-1]
        num += 1
    return num_st