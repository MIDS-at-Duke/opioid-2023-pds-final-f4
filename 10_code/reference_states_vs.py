import pandas as pd
import matplotlib.pyplot as plt

file_path_vs_dataset = r'C:\Users\19l20\Desktop\mids_study\pds_final_project\vs_dataset.csv'
df_vs_dataset = pd.read_csv(file_path_vs_dataset)

# Extract state codes from County_Code using a modified regular expression
df_vs_dataset['State_Code'] = df_vs_dataset['County_Code'].str.extract(r'([A-Za-z]{2})-\d+')

# Filter rows based on selected states
selected_states = ['WA', 'AZ', 'CA', 'ID', 'IA', 'NE', 'OR']
selected_rows = df_vs_dataset[df_vs_dataset['State_Code'].isin(selected_states)]

# Initialize empty dictionaries to store the summed deaths for each state
summed_deaths_WA = {}
summed_deaths_AZ = {}
summed_deaths_CA = {}
summed_deaths_ID = {}
summed_deaths_IA = {}
summed_deaths_NE = {}
summed_deaths_OR = {}

# Iterate through the years and sum the deaths for each state
for year in range(2003, 2015):
    year_column = str(year)
    summed_deaths_WA[year] = selected_rows[selected_rows['State_Code'] == 'WA'][year_column].sum()
    summed_deaths_AZ[year] = selected_rows[selected_rows['State_Code'] == 'AZ'][year_column].sum()
    summed_deaths_CA[year] = selected_rows[selected_rows['State_Code'] == 'CA'][year_column].sum()
    summed_deaths_ID[year] = selected_rows[selected_rows['State_Code'] == 'ID'][year_column].sum()
    summed_deaths_IA[year] = selected_rows[selected_rows['State_Code'] == 'IA'][year_column].sum()
    summed_deaths_NE[year] = selected_rows[selected_rows['State_Code'] == 'NE'][year_column].sum()
    summed_deaths_OR[year] = selected_rows[selected_rows['State_Code'] == 'OR'][year_column].sum()

# Update the labels and markers accordingly
plt.plot(summed_deaths_WA.keys(), summed_deaths_WA.values(), marker='o', label='Washington')
plt.plot(summed_deaths_AZ.keys(), summed_deaths_AZ.values(), marker='x', label='Arizona')
plt.plot(summed_deaths_CA.keys(), summed_deaths_CA.values(), marker='*', label='California')
plt.plot(summed_deaths_ID.keys(), summed_deaths_ID.values(), marker='+', label='Idaho')
plt.plot(summed_deaths_IA.keys(), summed_deaths_IA.values(), marker='^', label='Iowa')
plt.plot(summed_deaths_NE.keys(), summed_deaths_NE.values(), marker='s', label='Nebraska')
plt.plot(summed_deaths_OR.keys(), summed_deaths_OR.values(), marker='D', label='Oregon')

plt.title('Opioid-Related Deaths Trend')
plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.legend()
plt.show()