import pandas as pd
import numpy as np

pd.set_option("mode.copy_on_write", True)

# Specify the file paths
file_path_pop = (
    r"Group Work\opioid-2023-pds-final-f4\20_intermediate_files\population.csv"
)
file_path_vs = (
    r"Group Work\opioid-2023-pds-final-f4\20_intermediate_files\vs_dataset.csv"
)
save_file_path = "Group Work/opioid-2023-pds-final-f4/20_intermediate_files/"

report_file_path = "Group Work/opioid-2023-pds-final-f4/30_reports/"

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

merged_df.head()

# Set the policy change year for each state
policy_change_year_fl = 2010
policy_change_year_tx = 2007
policy_change_year_wa = 2012

# Set subset groups for each treated state
state_prefixes_fl = ["FL", "CA-", "NC-", "MO-"]
state_prefixes_tx = ["TX", "CA-", "NC-", "MO-"]
state_prefixes_wa = ["WA", "CA-", "CO-", "GA-", "AZ-", "NE-"]

# Subset the data for each state
subset_fl = merged_df[merged_df["County_Code"].str.startswith(tuple(state_prefixes_fl))]
subset_tx = merged_df[merged_df["County_Code"].str.startswith(tuple(state_prefixes_tx))]
subset_wa = merged_df[merged_df["County_Code"].str.startswith(tuple(state_prefixes_wa))]
subset_fl.head()


# Function to create time_relative variable based on the policy change year
def add_time_relative(subset_df, policy_year):
    subset_df = subset_df.copy()  # Make a copy to avoid SettingWithCopyWarning
    subset_df["Time_Relative"] = subset_df["Year"] - policy_year
    return subset_df


# Apply the function to each subset
subset_fl = add_time_relative(subset_fl, policy_change_year_fl)
subset_tx = add_time_relative(subset_tx, policy_change_year_tx)
subset_wa = add_time_relative(subset_wa, policy_change_year_wa)
subset_fl.head()

# Create dictionaries for treated and control counties
treated_control_fl = {"FL-": ["CA-", "NC-", "MO-"]}
treated_control_tx = {"TX-": ["CA-", "NC-", "MO-"]}
treated_control_wa = {"WA-": ["CA-", "CO-", "GA-", "AZ-", "NE-"]}


# Function to create treated_control variable based on created dictionary
def add_treated_control(subset_df, treated_control_dict):
    # Copy the DataFrame to avoid SettingWithCopyWarning
    subset_df = subset_df.copy()

    # Initialize the column with zeros
    subset_df["Treated_Control"] = 0

    # Assign treatment to treated counties
    for treated_prefix in treated_control_dict.keys():
        subset_df.loc[
            subset_df["County_Code"].str.startswith(treated_prefix), "Treated_Control"
        ] = "True"

    # Assign control to control counties
    for control_prefixes in treated_control_dict.values():
        for control_prefix in control_prefixes:
            subset_df.loc[
                subset_df["County_Code"].str.startswith(control_prefix),
                "Treated_Control",
            ] = "False"

    return subset_df


# Apply the function to each subset
subset_fl = add_treated_control(subset_fl, treated_control_fl)
subset_tx = add_treated_control(subset_tx, treated_control_tx)
subset_wa = add_treated_control(subset_wa, treated_control_wa)


# Subset for Florida
pre_post_fl = subset_fl[subset_fl["County_Code"].str.startswith("FL-")]

# Create a DataFrame with the sum of overdoses per time
sum_overdoses_per_time_fl = (
    pre_post_fl.groupby("Time_Relative")["Overdoses_Per_Capita"].sum().reset_index()
)

# Subset for Texas
pre_post_tx = subset_tx[subset_tx["County_Code"].str.startswith("TX-")]
# Create a DataFrame with the sum of overdoses per time
sum_overdoses_per_time_tx = (
    pre_post_tx.groupby("Time_Relative")["Overdoses_Per_Capita"].sum().reset_index()
)

# Subset for Washington
pre_post_wa = subset_wa[subset_wa["County_Code"].str.startswith("WA-")]
# Create a DataFrame with the sum of overdoses per time
sum_overdoses_per_time_wa = (
    pre_post_wa.groupby("Time_Relative")["Overdoses_Per_Capita"].sum().reset_index()
)
# Create a dictionary with the states as keys and (DataFrames,policy change year) as values
pre_post_dict = {
    "Florida": (sum_overdoses_per_time_fl, policy_change_year_fl),
    "Texas": (sum_overdoses_per_time_tx, policy_change_year_tx),
    "Washington": (sum_overdoses_per_time_wa, policy_change_year_wa),
}

# import necessary libraries for plotting
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# Create a loop to plot each state's pre-post policy change
for state, (sum_overdoses_per_time, policy_change_year) in pre_post_dict.items():
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=sum_overdoses_per_time,
        x="Time_Relative",
        y="Overdoses_Per_Capita",
        marker="o",
    )
    plt.axvline(
        x=0, color="red", linestyle="--", label=f"Policy Change - {policy_change_year}"
    )
    plt.title(f"Pre-Post Policy Intervention Analysis - {state}")
    plt.xlabel("Years Relative to Policy Change")
    plt.ylabel("Overdoses Per Capita")

    plt.legend()
    # save the the plot
    plt.savefig(report_file_path + f"pre_post_{state}.png")
    plt.show()

# Create a dic of dataframes for each treated_control dataframe
did_list = {
    "Florida": (subset_fl, policy_change_year_fl),
    "Texas": (subset_tx, policy_change_year_tx),
    "Washington": (subset_wa, policy_change_year_wa),
}

# Create a loop to plot each DiD plot
for state, (subset, policy_change_year) in did_list.items():
    # DiD Plot for for all tha datasets
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=subset,
        x="Time_Relative",
        y="Overdoses_Per_Capita",
        hue="Treated_Control",
        style="Treated_Control",
        markers=True,
    )
    plt.axvline(
        x=0, color="red", linestyle="--", label=f"Policy Change - {policy_change_year}"
    )
    plt.title(f"Difference-in-Differences Analysis of Overdoses Per Capita - {state}")
    plt.xlabel("Years Relative to Policy Change")
    plt.ylabel("Overdoses Per Capita")
    plt.legend(title="Counties in states with policy change", loc="upper left")
    plt.tight_layout()

    # save the the plot
    plt.savefig(report_file_path + f"did_{state}.png")
    plt.show()
