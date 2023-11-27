"""This file was originally used to merge the opioid data with the population data. We decided in stride not to 
normalize opioid shipments by population since it resulted in plots which were difficult to interpret. This script now just
aggregates the opioid shipments by state and year and saves the result to a parquet file."""
import dask.dataframe as dd

wp_data = dd.read_parquet("..\\20_intermediate_files\\wp_avg_trimmed.parquet")


population_data = dd.read_csv("..\\20_intermediate_files\\population.csv")


# melt the population data so that there is an observation for each county-year
pop_melt = population_data.melt(
    id_vars=[
        "BUYER_COUNTY",
        "STUSAB",
        "STATE",
        "COUNTY",
        "STNAME",
        "CTYNAME",
        "_merge",
        "County Code",
    ],
    var_name="Year",
    value_name="Population",
)


# rename Year to TRANSACTION_YEAR in pop_melt
pop_melt = pop_melt.rename(columns={"Year": "TRANSACTION_DATE"})
# Rename STUSAB to BUYER_STATE
pop_melt = pop_melt.rename(columns={"STUSAB": "BUYER_STATE"})


# convert TRANSACTION_DATE to int32 in pop_melt
pop_melt["TRANSACTION_DATE"] = pop_melt["TRANSACTION_DATE"].astype("int32")


# merge pop_melt and wp_data on BUYER_COUNTY, BUYER_STATE, and TRANSACTION_YEAR keeping population data and CALC_BASE_WT_GM
wp_data_merged = wp_data.merge(
    pop_melt, on=["BUYER_COUNTY", "BUYER_STATE", "TRANSACTION_DATE"], how="outer"
).compute()


# drop STATE, COUNTY, STNAME, CTYNAME, _merge, and County Code
wp_data_merged = wp_data_merged.drop(
    columns=["STATE", "COUNTY", "STNAME", "CTYNAME", "_merge", "County Code"]
)


# Compute the gross opioids shipped in each state for each year
state_gross = (
    wp_data.groupby(["BUYER_STATE", "TRANSACTION_DATE"])["CALC_BASE_WT_IN_GM"]
    .sum()
    .reset_index()
)


# convert state_gross to pandas dataframe
state_gross = state_gross.compute()


# write state_gross to a parquet file called state_gross_opioid.parquet
state_gross.to_parquet("..\\20_intermediate_files\\state_gross_opioid.parquet")
