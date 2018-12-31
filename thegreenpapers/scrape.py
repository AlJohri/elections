import csv
import requests
import lxml.html
import pendulum

def inclusive_range(start, end, step=1):
    return range(start, end+step, step)

def parse_g_alphabetical(html, year):
    rows = []
    doc = lxml.html.fromstring(html)
    for row in doc.cssselect('table tbody tr'):

        try:
            state = row.cssselect('td')[0].cssselect('a')[1].text
        except Exception:
            state = row.cssselect('td')[0].cssselect('a')[0].text

        for x in row.cssselect('td')[1].cssselect('a'):
            text = x.text
            if not text:
                print(f'[{year} {state}] no events')
                continue
            if text.count(' - ') == 1:
                event, _, date_str = text.rpartition(' - ')
                date = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
            else:
                event, _, date_str = text.rpartition(' - ')
                date2 = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
                event, _, date_str = text.rpartition(' - ')
                date1 = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
                date = f'{date1} {date2}'
            output = {'year': year, 'date': date, 'state': state, 'event': event}
            print(output)
            rows.append(output)
    return rows

def parse_p_alphabetical(html, year):
    rows = []
    doc = lxml.html.fromstring(html)
    for row in doc.cssselect('table tbody tr'):

        try:
            state = row.cssselect('td')[0].cssselect('a')[1].text
        except Exception:
            state = row.cssselect('td')[0].cssselect('a')[0].text

        party = 'DEM'
        for x in row.cssselect('td')[1].cssselect('a span'):
            text = x.text
            if not text:
                print(f'[{year} {state}] no events')
                continue
            if text.count(' - ') == 1:
                event, _, date_str = text.rpartition(' - ')
                date = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
            else:
                event, _, date_str = text.rpartition(' - ')
                date2 = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
                event, _, date_str = text.rpartition(' - ')
                date1 = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
                date = f'{date1} {date2}'
            output = {'year': year, 'date': date, 'state': state, 'event': event, 'party': party, 'type': 'primary'}
            print(output)
            rows.append(output)
        
        party = 'REP'
        for x in row.cssselect('td')[2].cssselect('a span'):
            text = x.text
            if not text:
                print(f'[{year} {state}] no events')
                continue
            if text.count(' - ') == 1:
                event, _, date_str = text.rpartition(' - ')
                date = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
            else:
                event, _, date_str = text.rpartition(' - ')
                date2 = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
                event, _, date_str = text.rpartition(' - ')
                date1 = pendulum.from_format(date_str, 'dddd DD MMMM YYYY', tz=None).date().isoformat()
                date = f'{date1} {date2}'
            output = {'year': year, 'date': date, 'state': state, 'event': event, 'party': party, 'type': 'primary'}
            print(output)
            rows.append(output)

    return rows

if __name__ == "__main__":

    # GXX Pages

    g_pages = []
    for year in inclusive_range(2, 18):
        url = f'https://www.thegreenpapers.com/G{year:02}/events.phtml'
        response = requests.get(url)
        g_pages += parse_g_alphabetical(response.text, 2000+year)

    with open('g_pages.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=g_pages[0].keys())
        writer.writeheader()
        writer.writerows(g_pages)
    
    # PXX Pages

    p_pages = []

    for year in inclusive_range(4, 16, 4):
        url = f'https://www.thegreenpapers.com/P{year:02}/events.phtml?s=a&f=m'
        response = requests.get(url)
        p_pages += parse_p_alphabetical(response.text, 2000+year)

    with open('p_pages.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=p_pages[0].keys())
        writer.writeheader()
        writer.writerows(p_pages)
    
    # Data Download Pages

    for year in inclusive_range(12, 20, 4):
        url = f'https://www.thegreenpapers.com/P{year:02}/download.phtml'
        response = requests.get(url)
        link = lxml.html.fromstring(response.text).cssselect("a[target]")[0].get('href')
        link = link.replace('?dl=0', '?dl=1')
        print(url, link)

    for year in inclusive_range(12, 18):
        url = f'https://www.thegreenpapers.com/G{year:02}/download.phtml'
        response = requests.get(url)
        link = lxml.html.fromstring(response.text).cssselect("a[target]")[0].get('href')
        link = link.replace('?dl=0', '?dl=1')
        print(url, link)
