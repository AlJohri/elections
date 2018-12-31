import pandas as pd

df = pd.read_csv('p_pages.csv')

df = df[~df.date.str.contains(' ')] # remove all multi-day events (usually the State Convention)

df = df[~df.event.str.contains('State Convention')]
df = df[~df.event.str.contains('Meeting')]
df = df[~df.event.str.contains('Assembly')]
df = df[~df.event.str.contains('Committee')]
df = df[~df.event.str.contains('District Caucus')]
df = df[~df.event.str.contains('Ward Caucus')]
df = df[~df.event.str.contains('District Conventions: CDs')]

df = df[~df.state.str.contains('Northern Marianas')]
df = df[~df.state.str.contains('American Samoa')]
df = df[~df.state.str.contains('Puerto Rico')]
df = df[~df.state.str.contains('Guam')]
df = df[~df.state.str.contains('Virgin Islands')]
df = df[~df.state.str.contains('Unassigned')]
df = df[~df.state.str.contains('Democrats Abroad')]

presidential_primaries = []

for (year, party, state), group in df.groupby(by=['year', 'party', 'state']):

    if year == 2016 and party == "REP" and state in ['Colorado', 'North Dakota', 'Wyoming']:
        """
        2016
        On the Republican side, American Samoa, Colorado, Guam, North Dakota, the U.S. Virgin Islands
        and Wyoming will not select delegates via caucuses or primaries. In Wyoming, delegates will be
        selected at county and state conventions; no winner has been called yet.
        """
        continue

    if group.event.count() == 1:
        row = group.iloc[0]
        presidential_primaries.append(row)
    else:
        if state == 'Iowa' and group.event.str.contains('Caucus').sum() == 1:
            row = group[group.event.str.contains('Caucus')].iloc[0]
            presidential_primaries.append(row)
        else:
            print(group)
            raise Exception('must filter down group to the main event')
            # for i, row in group.iterrows():
            #     presidential_primaries.append(row)

df = pd.DataFrame(presidential_primaries)

grouped_df = df.groupby(by=['year', 'party', 'state']).count()
more_than_one_event = grouped_df[grouped_df.date > 1]
# print(more_than_one_event)

grouped_df2 = df.groupby(by=['year', 'party']).count()
# print(grouped_df2)

df.sort_values(by='date').to_csv('presidential_primaries.csv', index=False)

def test(group):
    return pd.Series({
        'DEM': (group[group.party == 'DEM'].event + ' ' + group[group.party == 'DEM'].date).tolist(),
        'REP': (group[group.party == 'REP'].event + ' ' + group[group.party == 'REP'].date).tolist(),
    })

print('-----------------------')

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
    print(df.groupby(by=['year', 'state', 'date'], as_index=False).apply(test).loc[2016].sort_values(by=['date', 'state']))

print('-----------------------')

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
    print(df.groupby(by=['year', 'state'], as_index=False).apply(test).loc[2016].sort_values(by=['state']))
