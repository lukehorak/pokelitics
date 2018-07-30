####################################################################################################################
## Preamble
####################################################################################################################

# LogParserLite.py
# Author: Lukas Horak
# Description: LogParserLite for Season 2

####################################################################################################################
## Import Modules
####################################################################################################################

from TrainerBattle import *
from Trainer import *
from bs4 import BeautifulSoup as bs
import json


####################################################################################################################
## Class, Method, and Variable Declaration
####################################################################################################################


def makeLogs(filepath):
    match_page = bs(open(filepath), "html.parser").find_all("script", class_="battle-log-data")[0].get_text()
    with open("data/temp.log", "w+") as f:
        f.write(match_page)


def parseLine(line):
    parsed = line.replace('\n', '')
    parsed = parsed.split('|')
    parsed.pop(0)
    return parsed

def switch(event):
    result = {
        "player" : event[1].split(":")[0][:-1],
        "mon_name" : event[1].split(":")[1].strip(),
        "mon_species" : event[2].split(",")[0].split('-')[0]
    }
    return result

def switch_in(line, results):
    switched = switch(line)
    for trainer in results:
        if results[trainer].player_number == switched["player"] and switched["mon_name"] != switched["mon_species"]:
            # If Species Equals mon in results, but not swich line, flip them
            try:
                results[trainer].team[switched["mon_species"]].used = True
                results[trainer].team[switched["mon_species"]].name = switched["mon_name"]
                results[trainer].team[switched["mon_name"]] = results[trainer].team.pop(switched["mon_species"])
            except:
                results[trainer].team[switched["mon_name"]].used = True
    # Print for testing
    print ("Switched", switched["player"], "to", switched["mon_name"] + "!")
    return switched["mon_name"]
####################################################################################################################
## Script Body
####################################################################################################################

# Testing FP
# fp = "data/BattleData2018-07-03.txt"
def main(fp):
    #####################
    # For keeping track of active 'mons for each player
    active_mons = {
    "p1" : None,
    "p2" : None
    }

    # Initial Line Parsing Start Point
    stopLine = -1
    ##########################
    makeLogs(fp)
    # Write Temp File for parsing
    battle = BattleLog("data/temp.log")

    # Set Lineups
    for line in battle.content:
        stopLine += 1
        event = parseLine(line)
        if event[0] == 'player':
            battle.results[event[1]] = Trainer(event[2], event[1])
        elif event[0] == 'poke':
            species = event[2].split(',')[0]
            if '-' in species:
                if species.lower() is not 'ho-oh' and species.lower() is not 'porygon-z' and 'rotom' not in species:
                    species = species.split('-')[0]
            for trainer in battle.results:
                if battle.results[trainer].player_number == event[1]:
                    battle.results[trainer].addMon(species)
        elif event[0] == 'start':
            stopLine +=1
            break

    # Set first 2 Active Mons
    for i in range (0, 2):
        lead_line = parseLine(battle.content[stopLine + i])
        current = switch_in(lead_line, battle.results)
        active_mons["p" + str(i+1)] = current
    stopLine += 2
    print(active_mons)

    # Parse for Faints and Switches
    for line in range (stopLine, len(battle.content)):
        event = parseLine(battle.content[line])
        if event[0] == 'faint':
            player = event[1].split(":")[0][:-1]
            battle.results[player].team[active_mons[player]].alive = False
            for other in active_mons:
                if other != player:
                    battle.results[other].team[active_mons[other]].kills += 1
                    # Log kill to console (with species in parentheses)
                    print (active_mons[other], "(" + battle.results[other].team[active_mons[other]].species + ")", "killed", active_mons[player], "(" + battle.results[player].team[active_mons[player]].species + ")")
        elif event[0] == 'switch':
            player = event[1].split(":")[0][:-1]
            active_mons[player] = switch_in(event, battle.results)
            print(active_mons)
        elif event[0] == 'win':
            print (event[1], "won the battle!")
            battle.winner = event[1]

    battle.results['battle_winner'] = battle.winner
    json_message = battle.toJSON()

    # Write out JSON Object for testing
    with open("data/test_results.json", "w+") as f:
        f.write(json_message)

    return json_message

#main("data/BattleData2018-07-03.txt")
