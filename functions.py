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
                    AOI_hits[AOI]['timestamps'].append(
                        row[1]['Recording timestamp'])

    # add number of hits to the dictionary
    for AOI in AOI_hits.keys():
        AOI_hits[AOI]['hits'] = len(AOI_hits[AOI]['timestamps'])

    return AOI_hits

# data = pd.read_csv('trim.tsv', sep='\t', header=0)
# print(data.head())
# AOI_hits = get_AOI_hits(data)
# json.dump(AOI_hits, open('AOI_hits.json', 'w'))


def get_gaze_by_stimulus(data: pd.DataFrame) -> list:
    """Returns a list of data frames containing gaze coordinates for each stimulus.
    """

    data = data[data['Event'] != 'MouseEvent']
    stimuli = ["Speedmaster (1)", "Rolex_bearbeitet", "00_Zenit", "Zeppelin"]

    gaze_by_stimulus = []

    for participant in data['Participant name'].unique():
        print('Participant: ', participant)
        data_participant = data[data['Participant name'] == participant].copy()
        print(data_participant.head())
        for event in stimuli:
            start_index = data_participant[(data_participant['Event value'] == event) &
                                           (data_participant['Event'] == 'ImageStimulusStart')].copy()
            end_index = data_participant[(data_participant['Event value'] == event) &
                                         (data_participant['Event'] == 'ImageStimulusEnd')].copy()
            
            gaze = data_participant[start_index.index[0]:end_index.index[0]+1].copy()
            print(gaze.isna().sum())
            gaze = gaze[['Gaze point X', 'Gaze point Y']].copy().dropna()

            
            # print(f"Gaze size: {gaze.shape[0]}")  # Print the size of the gaze DataFrame
            # print(gaze.head())

            gaze_by_stimulus.append({'participant': str(participant),
                                     'event': str(event),
                                     'gaze_X': gaze['Gaze point X'].astype(int).tolist(),
                                     'gaze_Y': gaze['Gaze point Y'].astype(int).tolist()
                                     })

    return gaze_by_stimulus


data = pd.read_csv('raw_data_trimmed.tsv', sep='\t', header=0)
gaze_by_stimulus = get_gaze_by_stimulus(data)
json.dump(gaze_by_stimulus, open('gaze_by_stimulus.json', 'w'))
