import dask.dataframe as dd

# This script leverages Dask to parse the wp data into specific columns and
# write those columns to a parquet file.

# Path to the directory of Parquet files
parquet_dir = "..\\20_intermediate_files\\wp_trimmed.parquet"

# Read the Parquet files as a single Dask DataFrame
ddf = dd.read_parquet(parquet_dir)

# Now you can perform operations on the DataFrame
print(ddf.head())

# Convert the TRANSACTION_DATE column to datetime
ddf["TRANSACTION_DATE"] = dd.to_datetime(ddf["TRANSACTION_DATE"])

# Extract the year and assign it back to the TRANSACTION_DATE column
ddf["TRANSACTION_DATE"] = ddf["TRANSACTION_DATE"].dt.year

print(ddf.head())

# Group by the specified columns and compute the average of CALC_BASE_WT_IN_GM
ddf_grouped = ddf.groupby(["BUYER_STATE", "BUYER_COUNTY", "TRANSACTION_DATE"])[
    "CALC_BASE_WT_IN_GM"
].sum()

# Reset the index to make the result a DataFrame
ddf_grouped = ddf_grouped.reset_index()

# Compute the result
result_df = ddf_grouped.compute()

# Print the result
print(result_df.head())


result_df.to_parquet("..\\20_intermediate_files\\wp_avg_trimmed.parquet")
