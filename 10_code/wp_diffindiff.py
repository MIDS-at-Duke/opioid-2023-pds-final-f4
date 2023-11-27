import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_parquet("..\\20_intermediate_files\\wp_avg_trimmed.parquet")


data.head()


def DiffinDiff(treatment_state, control_list, start_year, end_year, policy_year, data):
    """Based on dataframe with column headers BUYER_STATE, BUYER_COUNTY, TRANSACTION_DATE, and CALC_BASE_WT_IN_GM"""
    treatment_data = data[
        (data["BUYER_STATE"] == treatment_state)
        & (data["TRANSACTION_DATE"] > start_year)
        & (data["TRANSACTION_DATE"] < end_year)
    ]
    treatment_pre = treatment_data[treatment_data["TRANSACTION_DATE"] < policy_year]
    treatment_post = treatment_data[treatment_data["TRANSACTION_DATE"] >= policy_year]
    control_data = data[
        (data["BUYER_STATE"].isin(control_list))
        & (data["TRANSACTION_DATE"] > start_year)
        & (data["TRANSACTION_DATE"] < end_year)
    ]
    control_pre = control_data[control_data["TRANSACTION_DATE"] < policy_year]
    control_post = control_data[control_data["TRANSACTION_DATE"] >= policy_year]

    # plot lmplots of fl_pre_2010 and fl_post_2010 on the same plot with x= TRANSACTION_DATE and y = CALC_BASE_WT_IN_GM
    # Create a figure and axes
    fig, ax = plt.subplots()

    sns.regplot(
        x="TRANSACTION_DATE",
        y="CALC_BASE_WT_IN_GM",
        data=control_pre,
        ax=ax,
        scatter=False,
        color="orange",
    )
    sns.regplot(
        x="TRANSACTION_DATE",
        y="CALC_BASE_WT_IN_GM",
        data=control_post,
        ax=ax,
        scatter=False,
        color="orange",
        label="Control States",
    )

    # Plot the first regplot on the axes
    sns.regplot(
        x="TRANSACTION_DATE",
        y="CALC_BASE_WT_IN_GM",
        data=treatment_pre,
        ax=ax,
        scatter=False,
        color="blue",
    )

    # Plot the second regplot on the same axes
    sns.regplot(
        x="TRANSACTION_DATE",
        y="CALC_BASE_WT_IN_GM",
        data=treatment_post,
        ax=ax,
        scatter=False,
        color="blue",
        label="Treatment State",
    )
    ax.axvline(x=policy_year, color="r", linestyle="--")
    # Show the plot

    plt.title(f"Opioid Shipments in {treatment_state} vs. {', '.join(control_list)}")
    plt.xlabel("Year")
    plt.ylabel("Opioid Shipments (in grams)")
    plt.legend()
    plt.savefig(f"..\\30_results\\{treatment_state}_vs_{control_list}_pre_post.png")
    plt.show()


DiffinDiff("FL", ["TN", "NC", "IN", "TX", "CA"], 2006, 2014, 2010, data)


DiffinDiff("WA", ["AZ", "CA", "ID", "IA", "NE", "OR"], 2008, 2016, 2012, data)
