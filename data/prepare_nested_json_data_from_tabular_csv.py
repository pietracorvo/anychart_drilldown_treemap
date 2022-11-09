import pandas as pd
import json



INPUT_CSV_FILE_PATH = r"data.csv"
OUTPUT_JSON_FILE_PATH = r"data.json"


# 1. Load input .csv to pandas DataFrame
df = pd.read_csv(INPUT_CSV_FILE_PATH, sep=";")
# NOTE NaN values (like "#N/A" in data.ods) get an empty NaN node below -> TODO QSTN should this be like this?

# 2. Build hierarchically nested python dict from DataFrame
res = [{
    "name": "World",
    "children": []
}]
for k1 in df['Continent'].unique():   # level: Continent
    tmp1 = {
        "name": k1,
        "children": [],
    }
    res[-1]["children"].append(tmp1)
    for k2 in df[df['Continent']==k1]['Country (or dependency)'].unique():   # level: Country -> leaf
        # print(k1, k2, df[(df['Continent']==k1) & (df['Country (or dependency)']==k2)]['Population (2020)'].iloc[0])
        population_count = df[(df['Continent']==k1) & (df['Country (or dependency)']==k2)]['Population (2020)'].iloc[0]
        tmp2 = {
        "name": k2,
        "value": int(population_count),
        }
        res[-1]["children"][-1]["children"].append(tmp2)
    # I think I just have to ask for "children" in keys of dict and if not it is a leaf


# 3. Export python dict as nested .json
with open(OUTPUT_JSON_FILE_PATH, 'w+') as f:
    json.dump(res, f, indent=4)

print(f'Successfully generated new data file: {OUTPUT_JSON_FILE_PATH}')
