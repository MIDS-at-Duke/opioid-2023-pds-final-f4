import pandas as pd
import zipfile
import os

# Define the path to our zip file and the extraction directory
zip_file_path = "../00_source_data/US_VitalStatistics.zip"
extraction_directory = "../00_source_data/us_vital_stats/"


# File extraction function
def extract_files(zip_file_path, extraction_directory):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extraction_directory)
    return None


# Function to count the number of rows before the footer
def count_data_rows(file_path):
    with open(file_path, "r") as file:
        for i, line in enumerate(file):
            if line.startswith('"---"'):
                return i
    return -1  # In case the footer is not found


# Function to get all the file paths
def get_file_paths(directory):
    file_paths = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Only get the text files
            file_paths.append(os.path.join(directory, filename))

    return file_paths


# Function to read the data
def read_data():
    # Set the path and files to read
    file_paths = get_file_paths(extraction_directory)
    data = []

    for i in range(len(file_paths)):
        # Get the number of rows to read
        nrows = count_data_rows(file_paths[i])
        # Read the data
        data.append(
            pd.read_csv(
                file_paths[i], delimiter="\t", skipinitialspace=True, nrows=nrows - 1
            )
        )  # Skip the footer
        assert (
            len(data[i]) == nrows - 1
        ), f"The number of rows read for {data[i]} is not correct"
    # Check that the number of files read is correct
    assert len(data) == len(file_paths), "The number of files read is not correct"
    return data


# We will define a function that categorizes cause based on our interest in drug overdose
def categorize_causes(cause):
    if "Drug poisonings (overdose)" in cause:
        return "Drug Overdose"
    else:
        return "Other"


# Test functions here
if __name__ == "__main__":
    data = read_data()
    print(len(data))
    print(data[0].head())
