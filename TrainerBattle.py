from bs4 import BeautifulSoup as bs
from Trainer import *

def makeLogs(filepath):
    match_page = bs(open(filepath), "html.parser").find_all("script", class_="battle-log-data")[0].get_text()
    with open("temp.log", "w+") as f:
        f.write(match_page)


def parseLine(line):
    parsed = line.replace('\n', '')
    parsed = parsed.split('|')
    parsed.pop(0)
    return parsed



class BattleLog:

    def __init__(self, filepath):
        with open(filepath, "r") as f:
            self.content = f.readlines()
        self.winner = None
        self.results = {}

    def toJSON(self):
        return json.dumps(self.results, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
