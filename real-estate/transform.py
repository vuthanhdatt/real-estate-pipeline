import json
import pandas as pd
import os

#list all json files in folder aand subfolder
path = 'data/json/13000/'
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

df = pd.DataFrame()
for idx, file in enumerate(files):
    print(f'Processing {idx+1}/{len(files)}')
    with open(file, 'r') as f:
        data = json.load(f)
        current_df = pd.DataFrame(data['ads'])
    df = pd.concat([df, current_df], axis=0)


df.to_parquet('data/05-10-24.parquet', index=False)
pass