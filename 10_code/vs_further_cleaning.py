import pandas as pd
import numpy as np

pd.set_option("mode.copy_on_write", True)

# Specify the file paths
file_path_pop = r"C:\\Users\\19l20\\Desktop\\mids_study\\pds_final_project\\opioid-2023-pds-final-f4\\20_intermediate_files\\population.csv"
file_path_vs = r"C:\\Users\\19l20\\Desktop\\mids_study\\pds_final_project\\opioid-2023-pds-final-f4\\20_intermediate_files\\vs_dataset.csv"
save_file_path = r"C:\\Users\\19l20\\Desktop\\mids_study\\pds_final_project\\opioid-2023-pds-final-f4\\20_intermediate_files\\"
report_file_path = r"C:\\Users\\19l20\\Desktop\\mids_study\\pds_final_project\\opioid-2023-pds-final-f4\\30_results\\"


# Read the CSV files into pandas DataFrames
df_population = pd.read_csv(file_path_pop)
df_vs_dataset = pd.read_csv(file_path_vs)
df_population.head()

# Reshape the vs dataset
reshaped_vs = df_vs_dataset.melt(
    id_vars=["County_Code"],
    value_vars=[
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
    ],
    var_name="Year",
    value_name="Total_Deaths",
)
reshaped_vs.head()

# Merge the two columns and create a new column named "County_Code" in the population DataFrame
df_population["County_Code"] = (
    df_population["STUSAB"] + "-" + df_population["County Code"].astype(str)
)

# print("the population code is", df_population.head())
df_population.head()

# Drop rows where COUNTY == 0
df_population = df_population[df_population["COUNTY"] != 0]
df_population.head()

# Drop columns from df_population
df_population.drop(
    columns=[
        "STATE",
        "COUNTY",
        "STNAME",
        "CTYNAME",
        "2000",
        "2001",
        "2002",
        "2016",
        "2017",
        "2018",
        "2019",
        "_merge",
        "STUSAB",
        "County Code",
        "BUYER_COUNTY",
    ],
    inplace=True,
)
df_population.head()

# Reshape the population dataset
pop_reshaped_df = df_population.melt(
    id_vars=["County_Code"],
    value_vars=[
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
    ],
    var_name="Year",
    value_name="Total_Pop",
)
pop_reshaped_df.head()

# Merge pop_resahped_df and reshaped_df on County_Code and Year
merged_df = pd.merge(
    reshaped_vs, pop_reshaped_df, how="left", on=["County_Code", "Year"]
)
merged_df.head()


# Get missing data rows
missing_data = merged_df[merged_df.isnull().any(axis=1)]
print(missing_data.count())

# View the missing data
missing_data

# Get count rows where County_Code starts with "VA-" to confirm
merged_df[merged_df["County_Code"].str.startswith("VA-")].count()


missing = ["VA-51560", "VA-51515"]
# Drop rows where County_Code is in missing
merged_df = merged_df[~merged_df["County_Code"].isin(missing)]

# Cast Total_pop and Year to int
merged_df["Year"] = merged_df["Year"].astype(int)
merged_df["Total_Pop"] = merged_df["Total_Pop"].astype(int)

# Get columns and their data types
merged_df.dtypes
    

# In this code, we're making sure not to fill zeros with 10s or average counts,
# which would violate the known constraints. We're also ensuring the estimated
# number of deaths doesn't exceed 9, which respects the censoring in the original data.

# Calculate the death rate for each county using only the non-zero death counts
death_rates = (
    merged_df[merged_df["Total_Deaths"] > 0]
    .groupby("County_Code")
    .apply(lambda x: x["Total_Deaths"].sum() / x["Total_Pop"].sum())
    .reset_index(name="Death_Rate")
)

# Merge the death rates back into the main DataFrame
merged_df = pd.merge(merged_df, death_rates, on="County_Code", how="left")

# Estimate the number of deaths for rows with zero deaths
merged_df["Estimated_Deaths"] = np.where(
    merged_df["Total_Deaths"] == 0,
    merged_df["Total_Pop"] * merged_df["Death_Rate"],
    merged_df["Total_Deaths"],
)

# Here, we make sure that the estimated deaths do not exceed the censoring threshold
merged_df.loc[merged_df["Estimated_Deaths"] < 10, "Estimated_Deaths"] = np.minimum(
    merged_df.loc[merged_df["Estimated_Deaths"] < 10, "Estimated_Deaths"], 9
)

# Normalize the estimated deaths by population to get the rate per capita
merged_df["Overdoses_Per_Capita"] = (
    merged_df["Estimated_Deaths"] / merged_df["Total_Pop"]
)
# Cast Estimated_Deaths to int
merged_df["Estimated_Deaths"] = merged_df["Estimated_Deaths"].astype(int)

merged_df.head()


# Subset for County_Code Overdoses_Per_Capita and Year
merged_df = merged_df[
    ["County_Code", "Estimated_Deaths", "Overdoses_Per_Capita", "Year"]
]
merged_df.to_csv(save_file_path + "final_v1.csv", index=False)


