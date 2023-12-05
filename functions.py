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


def get_gaze_by_stimulus(data: pd.DataFrame) -> dict:
    """Returns a list of dictionarys containing gaze coordinates for each stimulus.
    """
    # drop rows with Event "MouseEvent"
    data = data[data['Event'] != 'MouseEvent']

    gaze_by_stimulus = []

    for participant in data['Participant name'].unique():
        data_participant = data[data['Participant name'] == participant]
        for event in data_participant['Event value'].unique():
            start_index = data_participant[(data_participant['Event value'] == event) &
                                           (data_participant['Event'] == 'ImageStimulusStart')]
            end_index = data_participant[(data_participant['Event value'] == event) &
                                         (data_participant['Event'] == 'ImageStimulusEnd')]
            print(f"Participant: {participant}, Event: {event}")
            gaze = data_participant[(data_participant['Recording timestamp'] >= start_index['Recording timestamp'].values[0]) &
                                    (data_participant['Recording timestamp'] <= end_index['Recording timestamp'].values[0])]
            gaze_by_stimulus.append({'participant': participant,
                                     'event': event,
                                     'gaze': gaze})


data = pd.read_csv('trim.tsv', sep='\t', header=0)
gaze_by_stimulus = get_gaze_by_stimulus(data)
print(gaze_by_stimulus[0]['gaze'].head())
