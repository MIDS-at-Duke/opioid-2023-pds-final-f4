import pandas as pd

state_gross = pd.read_parquet("..\\20_intermediate_files\\state_gross_opioid.parquet")

# create a new column called policy_state which is a 1 if BUYER_STATE is FL or WA otherwise 0
state_gross["policy_state"] = state_gross["BUYER_STATE"].apply(
    lambda x: 1 if x in ["FL", "WA"] else 0
)
