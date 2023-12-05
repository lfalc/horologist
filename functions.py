import pandas as pd

def get_AIO_hits(data: pd.DataFrame,) -> dict:
    """Returns a dictionary containing AOIs and timestamps of their samples.
    """
    # Get the AOIs from column names. Get columns which contain "AOI" in their names.
    AOIs = [col for col in data.columns if "AOI" in col]
    # Get AOI indices from column names.
    

    # Create a dictionary with AOIs as keys and empty lists as values.
    AOI_hits = {AOI: [] for AOI in AOIs}

    # Iterate over rows and columns. If a cell contains 1, append the timestamp to the list of the corresponding AOI.
    for row in data.iterrows():
        for AOI in AOIs:
            for col in data.columns:
                if (col == AOI) and (row.ix[col] == 1):
                    AOI_hits[AOI].append(data['Recording timestamp]'])
        return AOI_hits

data = pd.read_csv('trim.tsv', sep='\t', header=0, index_col=0)
AOI_hits = get_AIO_hits(data)
print(AOI_hits)
