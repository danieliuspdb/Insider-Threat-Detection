import pandas as pd
import os

SCRIPT_DIR = 'Path'
INPUT_FILE = 'Path'
INSIDERS_FILE = 'Path'
OUTPUT_FILE = 'Path'

df = pd.read_excel(INPUT_FILE)
insiders = set(pd.read_csv(INSIDERS_FILE)['user'].unique())

insiders.add('TIH0348')

print(f"Total rows: {len(df)}")
print(f"Insiders/excluded users: {len(insiders)}")

df = df[~df['user'].isin(insiders)]
print(f"Rows after removing insiders: {len(df)}")

df = df.drop(columns=['user'])

df.to_excel(OUTPUT_FILE, index=False)