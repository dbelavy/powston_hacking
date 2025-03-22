import pandas as pd

# Load the data into a DataFrame (replace 'data.csv' with your file path)
data = pd.read_csv("historical_prices_qld/combined_output.csv")

# Ensure SETTLEMENTDATE is treated as a datetime
data['SETTLEMENTDATE'] = pd.to_datetime(data['SETTLEMENTDATE'])

# Extract 'Month' and 'Hour' from the SETTLEMENTDATE
data['Month'] = data['SETTLEMENTDATE'].dt.month
data['Hour'] = data['SETTLEMENTDATE'].dt.hour

# Group by Month and Hour, and calculate the average RRP and standard deviation
stats = (
    data.groupby(['Month', 'Hour'])['RRP']
    .agg(Average_RRP='mean', SD_RRP='std')  # Calculate both mean and SD
    .reset_index()
)

# Sort data by Month and Hour for proper analysis
stats = stats.sort_values(['Month', 'Hour']).reset_index(drop=True)

# Calculate RRP changes between consecutive hours
# stats['RRP_Change'] = stats['Average_RRP'].diff()

# Define a threshold for "big shifts" and flag them
# threshold = 20  # Adjust this threshold as needed
# stats['Big_Shift'] = (stats['RRP_Change'].abs() > threshold)

# Round the numeric columns to 2 decimal places
stats = stats.round({'Average_RRP': 2, 'SD_RRP': 2})

# Save the result to a CSV file or display it
stats.to_csv("historical_prices_qld/average_rrp_with_sd.csv", index=False)
print(stats)
