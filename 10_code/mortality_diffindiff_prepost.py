import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv("..\\20_intermediate_files\\final_v1.csv")

# Set subset groups for each treated state
state_prefixes_fl = ["FL", "CA-", "NC-", "MO-"]
state_prefixes_tx = ["TX", "CA-", "NC-", "MO-"]
state_prefixes_wa = ["WA", "CA-", "CO-", "GA-", "AZ-", "NE-"]

# Subset the data for each state
subset_fl = data[data["County_Code"].str.startswith(tuple(state_prefixes_fl))]
subset_tx = data[data["County_Code"].str.startswith(tuple(state_prefixes_tx))]
subset_wa = data[data["County_Code"].str.startswith(tuple(state_prefixes_wa))]
print(subset_fl.head())


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("..\\20_intermediate_files\\final_v1.csv")

def DiffinDiff(treatment_state, control_list, start_year, end_year, policy_year, data):
    treatment_data = data[
        (data["County_Code"].str.startswith(treatment_state))
        & (data["Year"] > start_year)
        & (data["Year"] < end_year)
    ]
    treatment_pre = treatment_data[data["Year"] < policy_year]
    treatment_post = treatment_data[data["Year"] >= policy_year]

    control_data = data[
        (data["County_Code"].str.startswith(tuple(control_list)))
        & (data["Year"] > start_year)
        & (data["Year"] < end_year)
    ]
    control_pre = control_data[data["Year"] < policy_year]
    control_post = control_data[data["Year"] >= policy_year]

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot control states
    sns.regplot(
        x="Year",
        y="Overdoses_Per_Capita",
        data=control_pre,
        ax=ax,
        scatter=False,
        color="orange",
    )
    sns.regplot(
        x="Year",
        y="Overdoses_Per_Capita",
        data=control_post,
        ax=ax,
        scatter=False,
        color="orange",
        label="Control States",
    )

    # Plot treatment state
    sns.regplot(
        x="Year",
        y="Overdoses_Per_Capita",
        data=treatment_pre,
        ax=ax,
        scatter=False,
        color="blue",
    )
    sns.regplot(
        x="Year",
        y="Overdoses_Per_Capita",
        data=treatment_post,
        ax=ax,
        scatter=False,
        color="blue",
        label="Treatment State",
    )

    # Add policy year vertical line
    ax.axvline(x=policy_year, color="r", linestyle="--")

    # Set plot labels and legend
    plt.title(f"Overdoses in {treatment_state} vs. {', '.join(control_list)}")
    plt.xlabel("Year")
    plt.ylabel("Overdoses Per Capita")
    plt.legend()

    # Save and show the plot
    plt.savefig(f"..\\30_results\\{treatment_state}_mortality_DiD.png")
    plt.show()

# Function calls
DiffinDiff("FL", ["CA", "NC", "MO"], 2003, 2014, 2010, data)
DiffinDiff("WA", ["CA", "CO", "GA", "AZ", "NE"], 2008, 2016, 2012, data)
DiffinDiff("TX", ["AZ", "SC"], 2008, 2016, 2012, data)


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("..\\20_intermediate_files\\final_v1.csv")

def PrePostAnalysis(state, policy_year, data):
    state_data = data[
        (data["County_Code"].str.startswith(state))
        & (data["Year"] >= policy_year - 5)  # 5 years before policy
        & (data["Year"] <= policy_year + 5)  # 5 years after policy
    ]

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot pre-policy years
    sns.regplot(
        x="Year",
        y="Overdoses_Per_Capita",
        data=state_data[state_data["Year"] < policy_year],
        ax=ax,
        scatter=False,
        color="blue",
        label="Pre-Policy",
    )

    # Plot post-policy years
    sns.regplot(
        x="Year",
        y="Overdoses_Per_Capita",
        data=state_data[state_data["Year"] >= policy_year],
        ax=ax,
        scatter=False,
        color="orange",
        label="Post-Policy",
    )
    ax.axvline(x=policy_year, color="r", linestyle="--")
    # Set plot labels and legend
    plt.title(f"Overdoses in {state} - 5 Years Before and After Policy")
    plt.xlabel("Year")
    plt.ylabel("Overdoses Per Capita")
    plt.legend()

    # Save and show the plot
    plt.savefig(f"..\\30_results\\{state}_mortality_pre_post.png")
    plt.show()

# Function calls for pre-post analysis
PrePostAnalysis("WA", 2012, data)
PrePostAnalysis("TX", 2007, data)
PrePostAnalysis("FL", 2010, data)