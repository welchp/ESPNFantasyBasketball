# GENERAL 

This project provides a python interface to visit ESPN's fantasy basketball site. Fantasy league and team data is scraped and summarized to provide insights not available by defualt.

Many of these tools are still in development and the entire scope of functionality has yet to be determined.

## THE PROCESS
1. Begin by creating a League object with leagueid as the only parameter:
    l = League(__yourleagueid__)
    
2. With your League object created as 'l', you can loop through the League attribute 'teamids' and create a Team object for each team in your league.
    for teamid in l.teamids:
      team = Team(teamid)
      print (team.teamid, '|', team.name)

## OBJECT CLASSES
### League
leagueid, name, settings, teams, teamids
### Team
teamid, name, roster, scoring, schedule
