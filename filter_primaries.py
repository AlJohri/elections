import pandas as pd

df = pd.read_csv('primaries.csv')

df = df[~df.date.str.contains(' ')]

df = df[~df.event.str.contains('Meeting')]
df = df[~df.event.str.contains('Convention')]
df = df[~df.event.str.contains('Assembly')]
df = df[~df.event.str.contains('Committee')]
df = df[~df.event.str.contains('District Caucus')]
df = df[~df.event.str.contains('Ward Caucus')]

df = df[~df.state.str.contains('Northern Marina')]
df = df[~df.state.str.contains('American Samoa')]
df = df[~df.state.str.contains('Puerto Rico')]
df = df[~df.state.str.contains('Guam')]
df = df[~df.state.str.contains('Virgin Islands')]
df = df[~df.state.str.contains('Unassigned')]

grouped_df = df.groupby(by=['year', 'party', 'state']).count()
more_than_one_event = grouped_df[grouped_df.date > 1]
print(more_than_one_event)

df.query("year == 2004 and party == 'REP' and state == 'Washington'")
df.to_csv('presidential_primaries.csv', index=False)
