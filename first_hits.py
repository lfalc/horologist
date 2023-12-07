import pandas as pd
import json
############################################## FIRST HIT AOI GROUP A & B ##########################################################
def get_first_AOI_hits_A_B(data: pd.DataFrame, participants: list) -> dict:
    """Returns a dictionary containing AOIs and timestamps of their samples."""
    AOIs = [col for col in data.columns if "AOI" in col]
    AOI_hits = {AOI: {'timestamps': [], 'hits': 0, 'Participant Name': None} for AOI in AOIs}

    stimuli = ["Speedmaster (1)", "Rolex_bearbeitet", "00_Zenit", "Zeppelin"]
    current_stimulus = None
    row_counter = 0

    # Iterate over rows and columns. If a cell contains 1, append the timestamp to the list of the corresponding AOI.
    for i, (index, row) in enumerate(data.iterrows()):
        if row['Presented Stimulus name'] in stimuli and row['Participant name'] in participants:
            if row['Presented Stimulus name'] != current_stimulus:
                current_stimulus = row['Presented Stimulus name']
                row_counter = 0
            if row_counter < 450:
                for AOI in AOIs:
                    if row[AOI] == 1:
                        AOI_hits[AOI]['timestamps'].append(row['Recording timestamp'])
                        AOI_hits[AOI]['Participant name'] = row['Participant name']  # Add participant name
                row_counter += 1

    # add number of hits to the dictionary
    for AOI in AOI_hits.keys():
        AOI_hits[AOI]['hits'] = len(AOI_hits[AOI]['timestamps'])
    
    return AOI_hits



with open('Fragen Eyetracking Ranking.json', 'r') as f:
    data = json.load(f)

# Extract the participant numbers
participant_numbers = [item['Teilnehmer Nummer'] for item in data]

# Split the participant numbers into two halves
mid = len(participant_numbers) // 2
participants1 = participant_numbers[:mid]
participants2 = participant_numbers[mid:]

print(participants1)
print(participants2)


data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
AOI_hits1 = get_first_AOI_hits_A_B(data, participants1)
json.dump(AOI_hits1, open('first_AOI_hits_B.json', 'w'))


data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
AOI_hits2 = get_first_AOI_hits_A_B(data, participants2)
json.dump(AOI_hits2, open('first_AOI_hits_A.json', 'w'))

############################################## END ##########################################################







############################################## ALL HITS AOI GROUP A & B ##########################################################

import pandas as pd
import json

def get_AOI_hits_A_B(data: pd.DataFrame, participants: list) -> dict:
    """Returns a dictionary containing AOIs and timestamps of their samples."""
    AOIs = [col for col in data.columns if "AOI" in col]
    AOI_hits = {AOI: {'timestamps': [], 'hits': 0, 'Participant Name': None} for AOI in AOIs}

    stimuli = ["Speedmaster (1)", "Rolex_bearbeitet", "00_Zenit", "Zeppelin"]
    current_stimulus = None
    row_counter = 0

    # Iterate over rows and columns. If a cell contains 1, append the timestamp to the list of the corresponding AOI.
    for i, (index, row) in enumerate(data.iterrows()):
        if row['Presented Stimulus name'] in stimuli and row['Participant name'] in participants:
            if row['Presented Stimulus name'] != current_stimulus:
                current_stimulus = row['Presented Stimulus name']
            for AOI in AOIs:
                if row[AOI] == 1:
                    AOI_hits[AOI]['timestamps'].append(row['Recording timestamp'])
                    AOI_hits[AOI]['Participant name'] = row['Participant name']  # Add participant name
               

    # add number of hits to the dictionary
    for AOI in AOI_hits.keys():
        AOI_hits[AOI]['hits'] = len(AOI_hits[AOI]['timestamps'])
    
    return AOI_hits


with open('Fragen Eyetracking Ranking.json', 'r') as f:
    data = json.load(f)

# Extract the participant numbers
participant_numbers = [item['Teilnehmer Nummer'] for item in data]

# Split the participant numbers into two halves
mid = len(participant_numbers) // 2
participants1 = participant_numbers[:mid]
participants2 = participant_numbers[mid:]

print(participants1)
print(participants2)


data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
AOI_hits3 = get_AOI_hits_A_B(data, participants1)
json.dump(AOI_hits3, open('AOI_hits_B.json', 'w'))


data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
AOI_hits4 = get_AOI_hits_A_B(data, participants2)
json.dump(AOI_hits4, open('AOI_hits_A.json', 'w'))

############################################## END ##########################################################





############################################## HIT AOI ALL ##########################################################
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

data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
print(data.head())
AOI_hits = get_AOI_hits(data)
json.dump(AOI_hits, open('AOI_hits.json', 'w'))
############################################## END ##########################################################






############################################## FIRST HIT AOI ALL ##########################################################
import pandas as pd
import json

def get_first_AOI_hits(data: pd.DataFrame) -> dict:
    """Returns a dictionary containing AOIs and timestamps of their samples.
    """
    AOIs = [col for col in data.columns if "AOI" in col]
    AOI_hits = {AOI: {'timestamps': [], 'hits': 0} for AOI in AOIs}

    stimuli = ["Speedmaster (1)", "Rolex_bearbeitet", "00_Zenit", "Zeppelin"]
    current_stimulus = None
    row_counter = 0

    # Iterate over rows and columns. If a cell contains 1, append the timestamp to the list of the corresponding AOI.
    for i, (index, row) in enumerate(data.iterrows()):
        if row['Presented Stimulus name'] in stimuli:
            if row['Presented Stimulus name'] != current_stimulus:
                current_stimulus = row['Presented Stimulus name']
                row_counter = 0
            if row_counter < 450:
                for AOI in AOIs:
                    if row[AOI] == 1:
                        AOI_hits[AOI]['timestamps'].append(row['Recording timestamp'])
                row_counter += 1

    # add number of hits to the dictionary
    for AOI in AOI_hits.keys():
        AOI_hits[AOI]['hits'] = len(AOI_hits[AOI]['timestamps'])
    
    return AOI_hits

data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
AOI_hits = get_first_AOI_hits(data)
json.dump(AOI_hits, open('first_AOI_hits.json', 'w'))

############################################## END ##########################################################








############################################## Create Small File ##########################################################

# import pandas as pd
# import json

# def get_AOI_hits(data: pd.DataFrame) -> dict:
#     """Returns a dictionary containing AOIs and timestamps of their samples.
#     """
#     AOIs = [col for col in data.columns if "AOI" in col]
#     AOI_hits = {AOI: {'timestamps': [], 'hits': 0} for AOI in AOIs}

# # Iterate over rows and columns. If a cell contains 1, append the timestamp to the list of the corresponding AOI.
#     for i, (index, row) in enumerate(data.iterrows()):
#         if i % 20 == 0:  # Add this condition to use only every 20th element
#             for AOI in AOIs:
#                 for col in data.columns:
#                     if (col == AOI) and (row[col] == 1):
#                         AOI_hits[AOI]['timestamps'].append(row['Recording timestamp'])
    
#     # add number of hits to the dictionary
#     for AOI in AOI_hits.keys():
#         AOI_hits[AOI]['hits'] = len(AOI_hits[AOI]['timestamps'])
    
#     return AOI_hits

# data = pd.read_csv('Uhren Data Export no useless AOI.tsv', sep='\t', header=0)
# print(data.head())
# AOI_hits = get_AOI_hits(data)
# json.dump(AOI_hits, open('first_AOI_hits.json', 'w'))

############################################## END ##########################################################

