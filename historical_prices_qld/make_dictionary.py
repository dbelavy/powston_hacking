import pandas as pd

import pprint

# Specify the file path to the CSV
file_path = "average_rrp_with_sd.csv"

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print(df.head())


# Create the nested dictionary
lookup_table = {}
for _, row in df.iterrows():
    month = int(row["Month"])
    hour = int(row["Hour"])
    
    if month not in lookup_table:
        lookup_table[month] = {}
    
    lookup_table[month][hour] = {
        "Average_RRP": row["Average_RRP"],
        "SD_RRP": row["SD_RRP"]
    }


pprint.pp(lookup_table)

# Example: Access data
print(lookup_table[1][0])  # Output: {'Average_RRP': 98.94, 'SD_RRP': 36.99}