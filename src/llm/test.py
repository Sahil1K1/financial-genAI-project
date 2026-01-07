from pathlib import Path
import pandas as pd
import os
import json

csv_path = os.path.join(Path().resolve(), 'data', 'processed', 'KPI_summary.csv')

print(csv_path)

df = pd.read_csv(csv_path)

# df = pd.read_excel(excel_path)
# print(df)
df = df.iloc[:100, :].to_json()

json_file = os.path.join(Path().resolve(), 'data', 'outputs')
json_file_output = os.path.join(json_file, 'llm_output.json')
print(json_file_output)

with open(json_file_output, 'w') as file:
    json.dump(df, file, indent=4)
