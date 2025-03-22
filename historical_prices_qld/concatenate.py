import pandas as pd
import os

# Specify the folder where the CSV files are located
folder_path = "/Users/davidbelavy/Library/CloudStorage/OneDrive-Personal/Development/powston_hacking/historical_prices_qld/"

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Create an empty list to store DataFrames
dataframes = []

# Loop through each CSV file and read it into a DataFrame
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the result to a new CSV file
combined_df.to_csv("combined_output.csv", index=False)

print(f"Successfully combined {len(csv_files)} CSV files into 'combined_output.csv'.")