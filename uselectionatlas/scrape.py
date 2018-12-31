import csv
import requests
import lxml.html
import pendulum

def inclusive_range(start, end, step=1):
    return range(start, end+step, step)

def parse_date(month_day, year):
    if ',' in month_day:
        month_day = month_day.split(',')[0]
    date = month_day + ' ' + str(year)
    try:
        return pendulum.from_format(date, 'MMM D YYYY').date().isoformat()
    except Exception:
        return pendulum.from_format(date, 'MMMM D YYYY').date().isoformat()

if __name__ == "__main__":

    primaries = []

    p_type_map = {
        '(C)': 'caucus',
        '(SC)': 'SC??',
        '(CC)': 'CC??'
    }

    non_a_tag_states = ['DC (C)', 'ID (C)']

    for year in inclusive_range(2000, 2016, 4):
        for party in ['D', 'R']:
            url = f'https://uselectionatlas.org/USPRESIDENT/PRIMARY/MENU_STATETXT/statemenutxt{year}{party}.html'
            response = requests.get(url)
            doc = lxml.html.fromstring(response.text)

            current_date = None
            for tr in doc.cssselect('table tr')[3:]:
                td = tr.cssselect('td')[0]
                
                if len(td.getchildren()) == 0:
                    if not td.text.strip():
                        continue
                    if td.text not in non_a_tag_states:
                        current_date = parse_date(td.text, str(year))
                        continue
                
                if td.text in non_a_tag_states:
                    state = td.text
                    p_type = 'primary'
                    if ' ' in state:
                        state, p_type = state.split(' ')
                        p_type = p_type_map[p_type]
                    primary = {'year': year, 'party': party, 'state': state, 'date': current_date, 'type': p_type}
                    primaries.append(primary)
                elif td.cssselect('a'):
                    if not current_date:
                        raise Exception('no date currently set?')
                    state = td.cssselect('a')[0].text
                    p_type = 'primary'
                    if ' ' in state:
                        state, p_type = state.split(' ')
                        p_type = p_type_map[p_type]
                    primary = {'year': year, 'party': party, 'state': state, 'date': current_date, 'type': p_type}
                    print(primary)
                    primaries.append(primary)

    with open('primaries.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=primaries[0].keys())
        writer.writerows(primaries)
