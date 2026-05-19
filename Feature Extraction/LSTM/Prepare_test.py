import pandas as pd
import os

SCRIPT_DIR = 'Path'
INPUT_FILE = 'Path'
OUTPUT_FILE = 'Path'

df = pd.read_excel(INPUT_FILE)
print(f"Total rows: {len(df)}")

print(f"Columns retained: {list(df.columns)}")
print(f"Features per timestep: {len(df.columns) - 2} (+ user + date)")

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_excel(OUTPUT_FILE, index=False)