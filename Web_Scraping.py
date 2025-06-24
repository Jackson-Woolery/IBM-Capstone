import re
import pandas as pd

pd.set_option('display.max_columns', None)

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

tables = pd.read_html(static_url)
# select and combine tables
tables = tables[2:-4]
df = pd.concat(tables, ignore_index=True)

# remove duplicate rows
df = df.drop_duplicates(subset='Flight No.')
# remove unnecessary row and columns
df = df.iloc[:-1, :-6]
df.drop(columns='Payload[c]', inplace=True)

# combine booster columns to fill nan and get rid of duplicate column
df['Version, Booster [b]'] = df['Version, Booster [b]'].fillna(df['Version, Booster[b]'])
df = df.iloc[:, :-1]

# rename columns
df.columns = ['Flight No.', 'Date and time', 'Version Booster', 'Launch site', 'Payload mass', 'Orbit',
              'Customer', 'Launch outcome', 'Booster landing']

# remove everything in brackets and clean up whitespace
df = df.map(lambda x: re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}", "", x) if isinstance(x, str) else x)
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# create time and date columns and delete the combined column
df['Date'] = pd.to_datetime(df['Date and time'], format='mixed').dt.date
df['Time'] = pd.to_datetime(df['Date and time'], format='mixed').dt.strftime('%H:%M')
df.drop(columns='Date and time', inplace=True)

# remove launch complex from launch site
df['Launch site'] = df['Launch site'].str.split(',').str[0]

# remove unnecessary symbols
df['Payload mass'] = df['Payload mass'].str.replace('~', '')
df['Version Booster'] = df['Version Booster'].str.replace('♺ ', '')

print(df)
