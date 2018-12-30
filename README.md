# elections

Scrape http://www.thegreenpapers.com/ to get a list of all elections from 2002+.

#### General Events Page Parameters

Goes back to `G02`.

- Alphabetically: http://www.thegreenpapers.com/G14/events.phtml
- Alphabetically with Filing Deadlines: http://www.thegreenpapers.com/G14/events.phtml?type=ef
- Chronologically: http://www.thegreenpapers.com/G14/events.phtml?format=chronological
- Chronologically with Filing Deadlines: http://www.thegreenpapers.com/G14/events.phtml?format=chronological&type=ef

#### Primary Events Page Parameters

Goes back to `P04`.

- Alphabetically: https://www.thegreenpapers.com/P16/events.phtml?s=a
- Chronologically: https://www.thegreenpapers.com/P16/events.phtml?s=c
- Major Events Alphabetically: https://www.thegreenpapers.com/P16/events.phtml?s=a&f=m
- Major Events Chronologically: https://www.thegreenpapers.com/P16/events.phtml?s=c&f=m
- "First Determining Step" Alphabetically: https://www.thegreenpapers.com/P16/events.phtml?s=a&f=1
- "First Determining Step" Chronologically: https://www.thegreenpapers.com/P04/events.phtml?s=c&f=1

#### Primaries at a Glance Page

- https://www.thegreenpapers.com/P04/paag.phtml
- https://www.thegreenpapers.com/P08/paag.phtml
- https://www.thegreenpapers.com/P16/paag.phtml

#### Data Download

TODO: look into this later

Folder newer elections (2012+), thegreenpapers provides downloadable spreadsheets with events and politicians.

```
import requests, lxml.html

for year in range(12, 18+1):
    url = f'https://www.thegreenpapers.com/G{year:02}/download.phtml'
    response = requests.get(url)
    link = lxml.html.fromstring(response.text).cssselect("a[target]")[0].get('href')
    link = link.replace('?dl=0', '?dl=1')
    print(url, link)
````

```
https://www.thegreenpapers.com/G12/download.phtml https://docs.google.com/spreadsheet/ccc?key=0AlQjpIwl8_VIdDBVcllyMVliOFRGRGQwLWs4N2ZiVlE&usp=sharing
https://www.thegreenpapers.com/G13/download.phtml https://docs.google.com/spreadsheet/ccc?key=0AlQjpIwl8_VIdFlzV05uWE9FdV9tdGhfQ1lBUEJoNXc&usp=sharing
https://www.thegreenpapers.com/G14/download.phtml https://docs.google.com/spreadsheet/ccc?key=1H1OzOoezvbez14w5gGnJUvX3XKuL1MGk8jVYzkHLfJc&usp=sharing
https://www.thegreenpapers.com/G15/download.phtml https://www.dropbox.com/sh/hs1ayhb3va5bgim/AAAEhF5vRJX1k9htGVM8AblJa?dl=1
https://www.thegreenpapers.com/G16/download.phtml https://www.dropbox.com/sh/56bivg1qh8n2uun/AAB6mFM_aPgQtuRnTW2cl6Qqa?dl=1
https://www.thegreenpapers.com/G17/download.phtml https://www.dropbox.com/sh/zvdov7jknysriws/AABAT03pqk-tCVkfml9dhHlBa?dl=1
https://www.thegreenpapers.com/G18/download.phtml https://www.dropbox.com/sh/b2rs5xc2owrm6j4/AABLFDH-liF2Hc8abetTlnwOa?dl=1
```

#### Presidential Primaries Dates Page

May want to scrape this page later too. It has primary dates going back to 1900s.

https://www.thegreenpapers.com/Hx/PresidentialPrimariesDates.phtml

