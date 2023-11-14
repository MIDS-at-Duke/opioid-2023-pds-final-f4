import pandas as pd
import os

# Create an empty DataFrame to store the final result
result_df = pd.DataFrame()

# List of state codes to filter (FL, WA, TX)
state_codes = ['FL', 'WA', 'TX']

# Set the path to the directory containing the files
directory_path = r'C:\Users\19l20\Desktop\mids_study\vitality_stats_data'

# Loop through each year
for year in range(2003, 2016):
    # Generate the file name for the current year
    file_path = os.path.join(directory_path, f"Underlying cause of death, {year}.txt")

    # Check if the file exists
    if os.path.exists(file_path):
        
        # Read the current file into a DataFrame
        df = pd.read_csv(file_path, sep=' ')

        # Filter rows based on the specified conditions
        filtered_df = df[(df['Drug/Alcohol Induced Cause'] == 'Drug poisonings (overdose) Unintentional (X40-X44)') & 
                         (df['Year Code'] == year) & 
                         (df['County'].isin(state_codes))]

        # Append the filtered data to the result DataFrame
        result_df = result_df._append(filtered_df, ignore_index=True)

# Save the result DataFrame to a new CSV file
result_df.to_csv(os.path.join(directory_path, 'filtered_data.csv'), index=False)