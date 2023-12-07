import pandas as pd, json


def combine_aois(AOIs: pd.DataFrame) -> pd.DataFrame:
    """Combine AOI hits from all pickled files in a directory into a single DataFrame."""

    stimuli = ["Speedmaster", "Rolex_bearbeitet", "Zenit", "Zeppelin"]

    # Define AOI groups in a dictionary
    aoi_mapping = {
        "subdials": ["3 Uhr Anzeige", "6 Uhr Anzeige", "9 Uhr Anzeige"],
        "buttons": ["Startknopf", "Resetknopf", "Krone"],
        "background": ["Rechts leer", "Links leer"],
        "bracelet": ["Armband oben", "Armband unten"],
        "brand": ["Marke"],
        "dial": ["Zifferblatt"],
        "bezel": ["Luenette"],
        "hands": ["Zeiger"],
        "date": ["Datum"]
    }

    column_mapping = {
        "subdials": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["subdials"]],
        "buttons": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["buttons"]],
        "background": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["background"]],
        "bracelet": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["bracelet"]],
        "brand": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["brand"]],
        "dial": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["dial"]],
        "bezel": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["bezel"]],
        "hands": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["hands"]],
        "date": ["AOI hit [{stimulus} - {aoi}]".format(stimulus=stimulus, aoi=aoi) for stimulus in stimuli for aoi in aoi_mapping["date"]]
    }



    # Initialize a new DataFrame to hold the combined AOIs
    AOI_combined = pd.DataFrame(columns=column_mapping.keys())
    with open('column_mapping.json', 'w') as f:
        json.dump(column_mapping, f)

    # Iterate over the AOI groups
    for group, columns in column_mapping.items():
        # Initialize a new column in the DataFrame
        print(columns)
        AOI_combined[group] = AOIs[columns].sum(axis=1)
    return AOI_combined


with open('AOI_hits.csv', 'r') as f:
    AOI_hits = pd.read_csv(f, sep=',', header=0)
    with open('AOI_hits.json', 'w') as g:
        json.dump(AOI_hits.columns.values.tolist(), g)    

AOI_combined = combine_aois(AOI_hits)
