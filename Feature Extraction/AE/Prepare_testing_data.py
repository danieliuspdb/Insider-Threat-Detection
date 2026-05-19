import pandas as pd
import os

SCRIPT_DIR = 'Path'
INPUT_FILE = 'Path'
OUTPUT_FILE = 'Path'

df = pd.read_excel(INPUT_FILE)
print(f"Total rows: {len(df)}")

df = df.drop(columns=['user'])

df.to_excel(OUTPUT_FILE, index=False)
