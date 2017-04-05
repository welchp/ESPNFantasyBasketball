# ESPN FANTASY BASKETBALL

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



## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/welchp/ESPNFantasyBasketball/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/welchp/ESPNFantasyBasketball/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
