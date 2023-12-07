import pandas as pd
import os


def aggregate_AOIs(directory: str) -> pd.DataFrame:
    """
    Aggregates AOI (Area of Interest) hits from all pickled files in a directory into a single DataFrame.

    This function iterates over all .pkl files in the specified directory, loading each one into a DataFrame.
    It then identifies all columns in the DataFrame that contain AOI data, and aggregates this data across all DataFrames.
    The aggregated data is returned as a new DataFrame, where each column corresponds to an AOI and each row corresponds to a data record.

    Parameters:
    directory (str): The path to the directory containing the .pkl files.

    Returns:
    pd.DataFrame: A DataFrame containing the aggregated AOI data.
    """

    # List all .pkl files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.pkl')]

    # Load each DataFrame and store them in a list
    dataframes = [pd.read_pickle(os.path.join(directory, f)) for f in files]

    max_rows = max(len(df) for df in dataframes)
    AOIs = [col for col in dataframes[0].columns if "AOI" in col]
    AOIs_by_index = {AOI: [0] * max_rows for AOI in AOIs}

    for AOI in AOIs:
        print('Processing: ', AOI, '...')
        for df in dataframes:
            for i in range(len(df)):
                if df[AOI].iloc[i] == 1:
                    AOIs_by_index[AOI][i] += 1
    return AOIs_by_index


combined_hits = aggregate_AOIs('stimuli')
df = pd.DataFrame(combined_hits)
df.to_csv('AOI_hits.csv', index=False)
