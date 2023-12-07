import os, pandas as pd

def get_gaze_by_stimulus(data: pd.DataFrame) -> None:
    """Saves data frames containing gaze coordinates for each stimulus as pickled files.
    """

    stimuli = ["Speedmaster (1)", "Rolex_bearbeitet", "00_Zenit", "Zeppelin"]

    for participant in data['Participant name'].unique():
        print('Participant: ', participant)
        data_participant = data[data['Participant name'] == participant].copy()
        for event in stimuli:
            start_index = data_participant[(data_participant['Event value'] == event) &
                                           (data_participant['Event'] == 'ImageStimulusStart')]
            end_index = data_participant[(data_participant['Event value'] == event) &
                                         (data_participant['Event'] == 'ImageStimulusEnd')]

            gaze = data_participant[start_index.index[0]:end_index.index[0]].copy()
            gaze = gaze.dropna(subset=['Gaze point X', 'Gaze point Y'])

            # Create the stimuli directory if it doesn't exist
            if not os.path.exists('stimuli'):
                os.makedirs('stimuli')

            # Save the DataFrame as a pickled file
            gaze.to_pickle(f'stimuli/{participant}_{event}.pkl')

        data = data[data['Participant name'] != participant]
        data = data.reset_index(drop=True)

data = pd.read_csv('raw_data_trimmed.tsv', sep='\t', header=0)
get_gaze_by_stimulus(data)