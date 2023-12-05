import pandas as pd
import json

def get_AOI_hits(data: pd.DataFrame) -> dict:
    """Returns a dictionary containing AOIs and timestamps of their samples.
    """
    AOIs = [col for col in data.columns if "AOI" in col]
    AOI_hits = {AOI: {'timestamps': [], 'hits': 0} for AOI in AOIs}

    # Iterate over rows and columns. If a cell contains 1, append the timestamp to the list of the corresponding AOI.
    for row in data.iterrows():
        for AOI in AOIs:
            for col in data.columns:
                if (col == AOI) and (row[1][col] == 1):
                    AOI_hits[AOI]['timestamps'].append(row[1]['Recording timestamp'])
    
    # add number of hits to the dictionary
    for AOI in AOI_hits.keys():
        AOI_hits[AOI]['hits'] = len(AOI_hits[AOI]['timestamps'])
    
    return AOI_hits

# data = pd.read_csv('trim.tsv', sep='\t', header=0)
# print(data.head())
# AOI_hits = get_AOI_hits(data)
# json.dump(AOI_hits, open('AOI_hits.json', 'w'))

def get_gaze_by_stimulus(data: pd.DataFrame) -> dict:
    """Returns a list of dictionarys containing gaze coordinates for each stimulus.
    """
    gaze_by_stimulus = []
    stimuli = data['StimulusName'].unique()
    