import sys, os
import urllib.request, urllib.parse
import requests
import pandas as pd
import bs4 as bs
from datetime import date
import matplotlib.pyplot as plt
from matplotlib import style
import numpy
import json

pd.options.display.max_columns = 8

scoringPeriodId = (date.today() - date(2016, 10, 24)).days

class League(object):
    """Initiate Custom League Profile based on leagueId"""
    def __init__(self, leagueid):
        self.leagueid = leagueid
        self.name = self.get_name()
        self.settings = self.get_league_settings()
        self.teams = self.get_teams()
        self.teamids = self.get_teamids()        
        
    def get_name(self):        
        address = 'http://games.espn.com/fba/leagueoffice?leagueId={}&seasonId=2017'.format(self.leagueid)
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        for div in soup.find_all('div', {'class':'league-team-names'}):
            name = div.text
            
        return name

#### --------DEVELOP-----------####
    def get_league_settings(self):
        settings = {}

        categories = []
        subcategories = []
        values = []

        div_list = ['basic','roster', 'scoring', 'teaminfo', 'rules', 'schedule', 'draft']
        address = 'http://games.espn.com/fba/leaguesetup/settings?leagueId={}'.format(self.leagueid)
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        #divs = soup.find_all('div', {'id':'settings-content'})
        #print ('divs:{}'.format(len(divs)))
        divs = soup.find_all('div', {'name':div_list})
        print ('divs:{}'.format(len(divs)))
        
        for i,div in enumerate(divs):
            print ('\ndiv'+str(i))
            trs = div.find_all('tr', {'class':'tableHead'})
            for n,tr in enumerate(trs):
                categories.append(tr.text)
            trs = div.find_all('tr')
            for n,tr in enumerate(trs):
                print ('\ttr{}'.format(n))
                td = tr.find_all('td')
                for m,d in enumerate(td):
                    #if d.text not in categories:
                    print ('\t\ttd{}'.format(m),'-',d.text)
            
            '''
            table_rows = div.find_all('tr')
            print ('tr: {}'.format(len(table_rows)))
            for i,tr in enumerate(table_rows):
                print (i, '-', tr.text)
                td = tr.find_all('td', {'class':'settingLabel'})
                for d in td:
                    print (d.text)
                    categories.append(d.text)
                print (categories)

                td = tr.find_all('td')
                print ('td length:',len(td))
                for d in td[:10]:
                    print (d.text)
                sys.exit()
                
                if len(td) == 1:
                    for d in td:
                        values.append(d.text)
                else:
                    content = ''
                    for d in td:
                        content += ' | {}'.format(content)
                    values.append(content)

        values = [ v for v in values if v not in categories]
        print (len(categories), '\n', categories)
        print (len(values), '\n', values)
                
        tables = soup.find('table', {'class':'leagueSettingsTable tableBody'})
        print ('tables:', len(tables))
        table_rows = soup.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td', {'class':'settingLabel'})
            for d in td:
                print (d.text)               
            for div in soup.find_all('div', {'class':'leagueSettingsSection viewing'}):
            for d in div:
                print (d.text)
          
        tables = soup.find('table', {'class' : 'leagueSettingsTable tableBody viewable'})
        for table in tables:
            settings[table.name] = []
            table_rows = table.find_all('tr')  #, {'class' : 'leagueSettingsTable tableBody viewable'})
            for table_row in table_rows:
                td = table_row.find_all('td')
                text = [d.text for d in td]
                settings[table.name].append(text)

        return settings'''


    def get_teams(self):
        teams = []
        
        address = 'http://games.espn.com/fba/leagueoffice?leagueId={}&seasonId=2017'.format(self.leagueid)
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for ul in soup.find_all('ul', {'id': 'games-tabs1'}):
            for li in ul.find_all('li'):
                teams.append(li.text)

        return teams


    def get_teamids(self):
        teamids = []
        
        address = 'http://games.espn.com/fba/leagueoffice?leagueId={}&seasonId=2017'.format(self.leagueid)
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for ul in soup.find_all('ul', {'id': 'games-tabs1'}):
            for li in ul:
                for a in li.find_all('a'):
                    teamids.append(a['href'].split("teamId=")[1].split("&")[0])

        return teamids

class Team(object):
    """Team Object | contains team level information for your fantasy league"""
    def __init__(self, teamid):
        self.teamid = teamid
        self.name = self.get_name()
        self.roster = self.get_roster()
        self.schedule = self.get_schedule()
        self.scoring = self.get_scoring_stats()

    def teamid(self):
        return self.teamid

    def get_name(self):
        address = 'http://games.espn.com/fba/clubhouse?leagueId={}&teamId={}&seasonId=2017'.format(leagueid, self.teamid)
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        for div in soup.find_all('div', {'class':'games-univ-mod3'}):
            name = div.text

        return name

    def get_roster(self):
        roster = []
        
        address = 'http://games.espn.com/fba/clubhouse?leagueId={}&teamId={}&seasonId=2017&scoringPeriodId={}&view=stats&context=clubhouse&ajaxPath=playertable/prebuilt/manageroster&managingIr=false&droppingPlayers=false&asLM=false'.format(leagueid, self.teamid, str(scoringPeriodId))
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        table = soup.find('table', {'id' : 'playertable_0'})
        table_rows = table.find_all('tr', {'class' : 'pncPlayerRow'})
        for table_row in table_rows:
            td = table_row.find_all('td')
            playername = td[1].text.split(",")[0]
            if '\xa0' not in playername:
                roster.append(playername.replace("*",""))

        return roster

    def get_schedule(self):
        schedule = []
        intable = []

        address = 'http://games.espn.com/fba/schedule?leagueId={}&teamId={}'.format(leagueid, self.teamid)
        sauce = urllib.request.urlopen(address).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        table = soup.find('table',{'class':'tableBody'})
        table_rows = table.find_all('tr')

        for tr in table_rows[2:]:
            td = tr.find_all('td')
            row = [0,0,0.0]
            row.extend([d.text for d in td])
            intable.append(row)
                    
        headers = ['WINS', 'LOSSES', 'WIN%', 'MATCHUP', 'RESULT', 'TRASH', 'OPPONENT', 'OWNER']
        df = pd.DataFrame(intable, columns = headers)

        return df
    
    def get_scoring_stats(self):
        stats = []
        version_dict = {}
        unique_ids = ['S', '7', '15', '30']
        versions = ['currSeason', 'last7', 'last15', 'last30']
        
        for i in range(len(versions)):
            try:
                roster = []
                intable = []
                version_dict[i] = {}

                address = 'http://games.espn.com/fba/clubhouse?leagueId={}&teamId={}&seasonId=2017&scoringPeriodId={}&view=stats&context=clubhouse&ajaxPath=playertable/prebuilt/manageroster&managingIr=false&droppingPlayers=false&asLM=false&version={}'.format(leagueid, self.teamid, str(scoringPeriodId), versions[i])
                sauce = urllib.request.urlopen(address).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')                
                
                table = soup.find('table', {'id' : 'playertable_0'})
                table_rows = table.find_all('tr', {'class' : 'playerTableBgRowSubhead'})
                for table_row in table_rows:
                    td = table_row.find_all('td')
                    headers = [d.text.replace("\xa0","") if d.text.replace("\xa0","") not in ['AVG', 'TOT'] else d.text.replace("\xa0","") + unique_ids[i] for d in td ]
                table_rows = table.find_all('tr', {'class' : 'pncPlayerRow'})
                for table_row in table_rows:
                    row = []
                    td = table_row.find_all('td')
                    playername = td[1].text.split(",")[0].replace("*","")
                    roster.append(playername)
                    try:
                        avg = float(td[-4].text)
                    except:
                        pass
                    
                    version_dict[i][playername] = avg

                    for d in td:
                        try:
                            row.append(float(d.text))
                        except:
                            row.append(d.text)
                    intable.append(row)
                    
                if i == 0:
                    df1 = pd.DataFrame(intable, index = [i for i in range(len(roster))], columns = headers)
                elif i ==1:
                    df2 = pd.DataFrame(intable, index = [i for i in range(len(roster))], columns = headers)
                elif i ==2:
                    df3 = pd.DataFrame(intable, index = [i for i in range(len(roster))], columns = headers)
                elif i == 3:
                    df4 = pd.DataFrame(intable, index = [i for i in range(len(roster))], columns = headers)
        
            except Exception as e:
                print ('\t', e, '\n')

        df5 = pd.merge(df1, df2, left_index=True, right_index=True, how='inner', suffixes=('Seas','Last7')).merge(df3,left_index=True, right_index=True, how='inner', suffixes=('Season','Last15')).merge(df4,left_index=True, right_index=True, how='inner', suffixes=('Season','Last30'))
        df5['PLAYERNAME'] = [ x.split(",")[0].replace("*","") for x in df5['PLAYER, TEAM POSSeas'] ]

        try:
            return df5[df5['PLAYERNAME'] != "\xa0" ][['PLAYERNAME', 'AVGS', 'AVG7','AVG15','AVG30']].sort_values('AVGS',ascending=False)
        except:
            return df5[df5['PLAYERNAME'] != "\xa0" ][['PLAYERNAME', 'AVGS', 'AVG7','AVG15','AVG30']]

try:
    leagueid = input('Please input your leagueid | ')
    l = League(leagueid)
except Exception as e:
    print (repr(e))
    leagueid = input('\nPlease input your leagueid | ')
    l = League(leagueid)
finally:
    leagueid = input('\nPlease input your leagueid | ')
    l = League(leagueid)

