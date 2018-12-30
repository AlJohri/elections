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

    elections = []
    for year in inclusive_range(2, 18):
        url = f'https://www.thegreenpapers.com/G{year:02}/events.phtml'
        response = requests.get(url)
        elections += parse_g_alphabetical(response.text, 2000+year)

    with open('elections.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=elections[0].keys())
        writer.writeheader()
        writer.writerows(elections)

    primaries = []

    for year in inclusive_range(4, 16, 4):
        url = f'https://www.thegreenpapers.com/P{year:02}/events.phtml?s=a&f=m'
        response = requests.get(url)
        primaries += parse_p_alphabetical(response.text, 2000+year)

    with open('primaries.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=primaries[0].keys())
        writer.writeheader()
        writer.writerows(primaries)
