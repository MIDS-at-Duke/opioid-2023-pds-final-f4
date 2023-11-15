import vd_lib as vd
import pandas as pd
import numpy as np

# Load data
datasets = vd.read_data()

# datasets[0].head()

for i in range(len(datasets)):
    datasets[i]["Cause_of_Death"] = datasets[i]["Drug/Alcohol Induced Cause"].apply(
        vd.categorize_causes
    )

# datasets[0][
#     ["Drug/Alcohol Induced Cause", "Cause_of_Death"]
# ]  # Show the original and new categorized columns for comparison


# Extract the state prefix, strip the comma and space, and concatenate with 'County Code'
for i in range(len(datasets)):
    datasets[i]["County_Code"] = (
        datasets[i]["County"].str.extract(r", (\w\w)")[0]
        + "-"
        + datasets[i]["County Code"].astype(str)
    )
    # Strip off the comma and state prefix from the 'County' column
    datasets[i]["County"] = datasets[i]["County"].str.replace(r", \w\w", "", regex=True)

    # cast Year to int
    datasets[i]["Year"] = datasets[i]["Year"].astype(int)


# datasets[0].head(5)

# Let’s drop the columns we don’t need to make them easier to work with.
for i in range(len(datasets)):
    datasets[i] = datasets[i].drop(
        [
            "Notes",
            "County Code",
            "Drug/Alcohol Induced Cause Code",
            "Year Code",
            "Drug/Alcohol Induced Cause",
        ],
        axis=1,
    )
# datasets[0].head(5)

# Let's Subset for only Drug overdose deaths
# And drop Alaska - AK in the process
for i in range(len(datasets)):
    datasets[i] = datasets[i][datasets[i]["Cause_of_Death"].str.contains("Overdose")]

    datasets[i] = datasets[i][~datasets[i]["County_Code"].str.startswith("AK-")]

# datasets[0].head(5)

# Now we can drop the 'Cause_of_Death' column since it's no longer needed
for i in range(len(datasets)):
    datasets[i] = datasets[i].drop(["Cause_of_Death"], axis=1)

# datasets[2].head(5)

# Concatenate all DataFrames
merged_df = pd.concat(datasets)

# Pivot table to sum deaths by year, with years as columns.
cleaned_vs_dataset = pd.pivot_table(
    merged_df,
    values="Deaths",
    index=["County", "County_Code"],
    columns="Year",
    aggfunc="sum",
    fill_value=0,  # Fill missing values with 0 for now
)  # We will deal with missing values later

cleaned_vs_dataset.reset_index()
# Save the cleaned dataset to a csv file
cleaned_vs_dataset.to_csv("../20_intermediate_files/vs_dataset.csv")
