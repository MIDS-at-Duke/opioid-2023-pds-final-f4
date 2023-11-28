import pandas as pd
import numpy as np

# Specify the file paths
file_path_population = r'C:\\Users\\19l20\\Desktop\\mids_study\\pds_final_project\\opioid-2023-pds-final-f4\\20_intermediate_files\\population.csv'
file_path_vs_dataset = r'C:\\Users\\19l20\\Desktop\\mids_study\\pds_final_project\\opioid-2023-pds-final-f4\\20_intermediate_files\\vs_dataset.csv'

# Read the CSV files into pandas DataFrames
df_population = pd.read_csv(file_path_population)
df_vs_dataset = pd.read_csv(file_path_vs_dataset)

# Merge the two columns and create a new column named "County_Code" in the population DataFrame
df_population['County_Code'] = df_population['STUSAB'] + '-' + df_population['County Code'].astype(str)

df_population = df_population[df_population['_merge'] == 'both']


# Merge the two datasets on the "County_Code" column
merged_df = pd.merge(df_population, df_vs_dataset, on="County_Code", how="inner")

# print("the merged dataframe is:", merged_df.head())

# Initialize a list of columns for the final DataFrame
final_columns = ['County_Code']

# Calculate deaths per capita for each year (2003-2015)
years = [str(year) for year in range(2003, 2016)]

for year in years:
    
    death_column = f"{year}_y"  # Adjust if the column name has a suffix in the vs_dataset
    population_column = f"{year}_x"
    deaths_per_capita_column = year
    
    # Convert columns to float, handling non-numeric values
    merged_df[death_column] = pd.to_numeric(merged_df[death_column], errors='coerce').astype(float)
    merged_df[population_column] = pd.to_numeric(merged_df[population_column], errors='coerce').astype(float)
    
    # Calculate deaths per capita, handling potential division by zero
    merged_df[deaths_per_capita_column] = np.where(merged_df[population_column] != 0, merged_df[death_column] / merged_df[population_column], 0)
    
    # Add the deaths per capita to the final DataFrame
    final_columns.append(deaths_per_capita_column)

# Create the final DataFrame with selected columns
final_df = merged_df[final_columns]

# Display the final dataset
print(final_df.head())




