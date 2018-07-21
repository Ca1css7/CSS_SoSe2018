############
# author: Carina Blüm
############
# This code creates a .csv-file for the last FIFA world cup of women and a .csv-file for the last FIFA world cup of men, depending on the selected url. The data (information about the female and male soccer player) is extracted from two Wikipedia web pages which list all teams and their players.
############

import requests
from bs4 import BeautifulSoup
import io

# urls of last men and women world cup
############
# Women
############
url = "https://en.wikipedia.org/wiki/2015_FIFA_Women%27s_World_Cup_squads"
numberOfTeams = 24
fname = "wc_2015.csv"

############
# Men
############
#url = "https://en.wikipedia.org/wiki/2014_FIFA_World_Cup_squads"
#numberOfTeams = 32
#fname = "wc_2014.csv"

############
# class Player: for each player the following attributes are selected: name, position, age, wikipage (returns the urls of the individual soccer player) and number of matches; attributes are separated with a ";"
############
class Player:
    name = ""
    position = ""
    age = 0
    wikipage = ""
    numberOfMatches = 0

    def __init__(self, name=None, position=None, age=None, wikipage=None, numberOfMatches=None):
        self.name = name
        self.position = position
        self.age = age
        self.wikipage = wikipage
        self.numberOfMatches = numberOfMatches

    def setName(self, name):
        self.name = name

    def setWikipage(self, page):
        self.wikipage = page

    def setPosition(self, position):
        self.position = position

    def setAge(self, age):
        self.age = age

    def setNumberOfMatches(self, numberOfMatches):
        self.numberOfMatches = numberOfMatches

    def toString(self):
        return str(self.name) + ";" + str(self.age) + ";" + str(
            self.position) + ";" + "https://en.wikipedia.org" + str(self.wikipage) + ";" + str(
            self.numberOfMatches) + ";"

############
# class NationalTeam: returns the attributes name and a list of players for each nation
############
class NationalTeam:
    name = ""
    players = []

    def __init__(self):
        self.name = ""
        self.players = []

    def setName(self, name):
        self.name = name

    def addPlayer(self, player:Player):
        self.players.append(player)

    def toString(self):
        tmp = ""
        for player in self.players:
            tmp += self.name + ";" + player.toString() + "\n"
        return tmp

############
# getTeams() gets the nationality ( e.g. Brazil) for all teams
############
def getTeams(soup):
    spans = soup.find_all("span", {"class": "mw-headline"})

    for s in range(0, numberOfTeams + int(numberOfTeams / 4)):
        if not "Group_" in spans[s]["id"]:
            team = NationalTeam()
            team.setName(spans[s].text)
            teams.append(team)

############
# getPlayers() gets the information for each player (which is defined in class Player) from the respective url
############
def getPlayers(soup):

    tables = soup.find_all("table")
    for j in range(0,numberOfTeams):
        trs = tables[j].find_all("tr")
        for i in range(1,24):
            player = Player()
            tds = trs[i].find_all("td")
            th = trs[i].find("th")
            player.setPosition(tds[1].find("a").text.strip())
            player.setWikipage(th.find("a")["href"].strip())
            player.setName(str(th.find("a").text).strip())
            player.setAge(tds[2].text.split(" ")[4].replace(")","").strip()) # for men: player.setAge(tds[2].text.split(" ")[5].replace(")","").strip())
            player.setNumberOfMatches(tds[3].text.strip())
            teams[j].addPlayer(player)

############
# writeFile(): writes the .csv-files u(tf-8 encoding)
############
def writeFile():
    with io.open(fname, "w", encoding="utf-8") as f:
        f.write("Nation;Name;Age;Position;Wiki;Matches;\n")
        for t in teams:
            f.write(t.toString())

############
# calls the url and the previously defined functions
# content: team and for all players the name age position url and number of matches
############
if __name__ == "__main__":

    r = requests.get(url)
    teams = []
    soup = BeautifulSoup(r.content, 'html.parser')

    getTeams(soup)
    getPlayers(soup)

    writeFile()