import json

class pokemon:

    def __init__(self, name):
        self.name = name
        self.species = name
        self.alive = True
        self.kills = 0
        self.used = False

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class Trainer:

    def __init__(self, name, player_num):
        self.name = name
        self.player_number = player_num
        self.team = {}

    def addMon(self, mon):
        self.team[mon] = pokemon(mon)

    def setLineup(self, team):
        for mon in team:
            pkmn = pokemon(mon)
            self.team[mon] = pkmn

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __str__(self):
        return self.toJSON()
