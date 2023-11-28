import dask.dataframe as dd

# Path to the TSV file
# TSV file is ~100gb so this is a local path that will not work remotely.
# Had to download the entire dataset since parsing from zip was not working
tsv_path = "D:\\MIDS\Practical Data Science\\PDS_Data\\arcos_all_washpost.tsv"

# Specify the data types of the problematic columns
# This is a recommended fix for an error I was recieving, these columns are not being used
dtypes = {"NDC_NO": "object", "REPORTER_ADDL_CO_INFO": "object"}

# Read the TSV file in chunks
ddf = dd.read_csv(
    tsv_path, sep="\t", blocksize="500MB", dtype=dtypes
)  # adjust blocksize as needed

# Select the desired columns
ddf_subset = ddf[
    ["BUYER_STATE", "BUYER_COUNTY", "CALC_BASE_WT_IN_GM", "TRANSACTION_DATE"]
]

# Write the subset to a Parquet file
ddf_subset.to_parquet("..\\20_intermediate_files\\wp_trimmed.parquet")
