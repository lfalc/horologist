import matplotlib.pyplot as plt
import json


############################################## Plotten der Diagramme mit Absolut Wert ##########################################################
def plot_AOI_hits(AOI_hits, filename, text_size=12, text_x=1, text_y=1):
    """Plots AOI hits.
    """
    fig = plt.figure(figsize=(30, 15))  # Increase the size of the figure
    ax = fig.add_subplot(111)
    labels = []
    low_values = []
    for i, (key, value) in enumerate(AOI_hits.items()):
        if value['hits'] >= 100:  # Only plot bars for values >= 100
            ax.bar(i, value['hits'], label=key)
            ax.text(i, value['hits'], key, ha='center', va='bottom', fontsize="20")  # Add the bar name
            labels.append(key)  # Use the original key as the label
        else:
            low_values.append(key)
    ax.set_xticks(range(len(labels)))
    # ax.set_xticklabels(labels, rotation=45, fontsize=12, ha='right')  # Set horizontal alignment to 'right'
    ax.text(text_x, text_y, 'Low values: ' + ', '.join(low_values), transform=ax.transAxes, ha='right', va='top', fontsize=20)  # Add the names of the low values
    total_hits = sum(AOI['hits'] for AOI in AOI_hits.values())
    ax.text(text_x, text_y, 'Total hits: ' + str(total_hits), transform=ax.transAxes, ha='left', va='top', fontsize=text_size)
    plt.tight_layout()  # Adjust the layout to make room for the x-axis labels
    fig.savefig(filename)  # Save the figure
    return fig


hits_arrays = {} # Create a dictionary to store the arrays

def process_and_plot(filename, output_filename, text_size=12, text_x=1, text_y=1):
    with open(filename, 'r') as f:
        AOI_hits = json.load(f)

    # Combine entries 
    combined_hits_3_6_9 = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["3 Uhr Anzeige", "6 Uhr Anzeige", "9 Uhr Anzeige"]))
    combined_hits_start_reset_krone = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Startknopf", "Resetknopf", "Krone"]))
    combined_hits_rechts_links_leer = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Rechts leer", "Links leer"]))
    combined_hits_armband_oben_Armband_unten = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Armband oben", "Armband unten"]))
    combined_hits_marke = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Marke"]))
    combined_hits_zifferblatt = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Zifferblatt"]))
    combined_hits_luenette = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Luenette"]))
    combined_hits_zeiger = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Zeiger"]))
    combined_hits_datum = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Datum"]))
    AOI_hits = {AOI: AOI_hits[AOI] for AOI in AOI_hits.keys() if "Zwischenbild X" not in AOI}
    AOI_hits = {AOI: AOI_hits[AOI] for AOI in AOI_hits.keys() if all(name not in AOI for name in ["3 Uhr Anzeige", "6 Uhr Anzeige", "9 Uhr Anzeige", "Startknopf", "Resetknopf", "Krone", "Rechts leer", "Links leer", "Armband oben", "Armband unten", "Marke", "Zifferblatt", "Luenette", "Zeiger", "Datum"])}

    AOI_hits["Combined Subdials"] = {'hits': combined_hits_3_6_9}
    AOI_hits["Combined Knöpfe"] = {'hits': combined_hits_start_reset_krone}
    AOI_hits["Combined Seiten"] = {'hits': combined_hits_rechts_links_leer}
    AOI_hits["Combined Armband "] = {'hits': combined_hits_rechts_links_leer}
    AOI_hits["Combined Marke"] = {'hits': combined_hits_marke}
    AOI_hits["Combined Zifferblatt"] = {'hits': combined_hits_zifferblatt}
    AOI_hits["Combined Luenette"] = {'hits': combined_hits_luenette}
    AOI_hits["Combined Zeiger"] = {'hits': combined_hits_zeiger}
    AOI_hits["Combined Datum"] = {'hits': combined_hits_datum}



    AOI_hits = dict(sorted(AOI_hits.items(), key=lambda item: item[1]['hits'], reverse=True))

    fig = plot_AOI_hits(AOI_hits, output_filename, text_size, text_x, text_y)
    fig.savefig(output_filename)  # Save the figure
    
    # Write the number of hits and the name to an array
    hits_array = [(AOI, AOI_hits[AOI]['hits']) for AOI in AOI_hits.keys()]

    # Add the combined values to the array
    hits_array.append(("Combined Subdials", combined_hits_3_6_9))
    hits_array.append(("Combined Knöpfe", combined_hits_start_reset_krone))
    hits_array.append(("Combined Seiten", combined_hits_rechts_links_leer))
    hits_array.append(("Combined Armband", combined_hits_armband_oben_Armband_unten))
    hits_array.append(("Combined Marke", combined_hits_marke))
    hits_array.append(("Combined Zifferblatt", combined_hits_zifferblatt))
    hits_array.append(("Combined Luenette", combined_hits_luenette))
    hits_array.append(("Combined Zeiger", combined_hits_zeiger))
    hits_array.append(("Combined Datum", combined_hits_datum))

    # Store the array in the dictionary using the filename as the key
    hits_arrays[filename] = hits_array

    # Print the array
    print(hits_array)
    
     # Return the array along with the figure
     

     
    return fig, hits_array

process_and_plot('first_AOI_hits.json', 'first_AOI_hits_absolut.png', text_size=14)
process_and_plot('AOI_hits.json', 'AOI_hits_absolut.png', text_size=14)
process_and_plot('first_AOI_hits_A.json', 'first_AOI_Hits_A_absolut.png', text_size=14)
process_and_plot('first_AOI_hits_B.json', 'first_AOI_hits_B_absolut.png', text_size=14)
process_and_plot('AOI_hits_A.json', 'AOI_hits_A_absolut.png', text_size=14)
process_and_plot('AOI_hits_B.json', 'AOI_hits_B_absolut.png', text_size=14)
############################################## END ##########################################################




############################################## Plotten der Diagramme mit Relativ Wert ##########################################################
import matplotlib.pyplot as plt
import json


def plot_AOI_hits(AOI_hits, filename, text_size=12, text_x=1, text_y=1):
    """Plots AOI hits.
    """
    fig = plt.figure(figsize=(30, 15))  # Increase the size of the figure
    ax = fig.add_subplot(111)
    labels = []
    low_values = []
    total_hits = sum(AOI['hits'] for AOI in AOI_hits.values())
    for i, (key, value) in enumerate(AOI_hits.items()):
        percentage = (value['hits'] / total_hits) * 100  # Calculate the percentage of total hits
        if value['hits'] >= 100:  # Only plot bars for values >= 100
            ax.bar(i, value['hits'], label=key)
            ax.text(i, value['hits'], f"{key} ({percentage:.2f}%)", ha='center', va='bottom', fontsize="20", rotation=10)  # Add the bar name and the percentage
            labels.append(key)  # Use the original key as the label
        else:
            low_values.append(key)
    ax.set_xticks(range(len(labels)))
    #ax.set_xticklabels(labels, rotation=45, fontsize=12, ha='right')  
    ax.text(text_x, text_y, 'Low values: ' + ', '.join(low_values), transform=ax.transAxes, ha='right', va='top', fontsize=20)  # Add the names of the low values
    ax.text(text_x, text_y, 'Total hits: ' + str(total_hits), transform=ax.transAxes, ha='left', va='top', fontsize=text_size)
    plt.tight_layout()  # Adjust the layout to make room for the x-axis labels
    fig.savefig(filename)  # Save the figure
    return fig


hits_arrays = {} # Create a dictionary to store the arrays

def process_and_plot(filename, output_filename, text_size=12, text_x=1, text_y=1):
    with open(filename, 'r') as f:
        AOI_hits = json.load(f)

    # Combine entries 
    combined_hits_3_6_9 = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["3 Uhr Anzeige", "6 Uhr Anzeige", "9 Uhr Anzeige"]))
    combined_hits_start_reset_krone = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Startknopf", "Resetknopf", "Krone"]))
    combined_hits_rechts_links_leer = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Rechts leer", "Links leer"]))
    combined_hits_armband_oben_Armband_unten = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Armband oben", "Armband unten"]))
    combined_hits_marke = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Marke"]))
    combined_hits_zifferblatt = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Zifferblatt"]))
    combined_hits_luenette = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Luenette"]))
    combined_hits_zeiger = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Zeiger"]))
    combined_hits_datum = sum(AOI_hits[AOI]['hits'] for AOI in AOI_hits.keys() if any(name in AOI for name in ["Datum"]))
    AOI_hits = {AOI: AOI_hits[AOI] for AOI in AOI_hits.keys() if "Zwischenbild X" not in AOI}
    AOI_hits = {AOI: AOI_hits[AOI] for AOI in AOI_hits.keys() if all(name not in AOI for name in ["3 Uhr Anzeige", "6 Uhr Anzeige", "9 Uhr Anzeige", "Startknopf", "Resetknopf", "Krone", "Rechts leer", "Links leer", "Armband oben", "Armband unten", "Marke", "Zifferblatt", "Luenette", "Zeiger", "Datum"])}

    AOI_hits["Combined Subdials"] = {'hits': combined_hits_3_6_9}
    AOI_hits["Combined Knöpfe"] = {'hits': combined_hits_start_reset_krone}
    AOI_hits["Combined Seiten"] = {'hits': combined_hits_rechts_links_leer}
    AOI_hits["Combined Armband "] = {'hits': combined_hits_rechts_links_leer}
    AOI_hits["Combined Marke"] = {'hits': combined_hits_marke}
    AOI_hits["Combined Zifferblatt"] = {'hits': combined_hits_zifferblatt}
    AOI_hits["Combined Luenette"] = {'hits': combined_hits_luenette}
    AOI_hits["Combined Zeiger"] = {'hits': combined_hits_zeiger}
    AOI_hits["Combined Datum"] = {'hits': combined_hits_datum}



    AOI_hits = dict(sorted(AOI_hits.items(), key=lambda item: item[1]['hits'], reverse=True))

    fig = plot_AOI_hits(AOI_hits, output_filename, text_size, text_x, text_y)
    fig.savefig(output_filename)  # Save the figure
    
    # Write the number of hits and the name to an array
    hits_array = [(AOI, AOI_hits[AOI]['hits']) for AOI in AOI_hits.keys()]

    # Add the combined values to the array
    hits_array.append(("Combined Subdials", combined_hits_3_6_9))
    hits_array.append(("Combined Knöpfe", combined_hits_start_reset_krone))
    hits_array.append(("Combined Seiten", combined_hits_rechts_links_leer))
    hits_array.append(("Combined Armband", combined_hits_armband_oben_Armband_unten))
    hits_array.append(("Combined Marke", combined_hits_marke))
    hits_array.append(("Combined Zifferblatt", combined_hits_zifferblatt))
    hits_array.append(("Combined Luenette", combined_hits_luenette))
    hits_array.append(("Combined Zeiger", combined_hits_zeiger))
    hits_array.append(("Combined Datum", combined_hits_datum))

    # Store the array in the dictionary using the filename as the key
    hits_arrays[filename] = hits_array

    # Print the array
    print(hits_array)
    
     # Return the array along with the figure
     

     
    return fig, hits_array

process_and_plot('first_AOI_hits.json', 'first_AOI_hits_relativ.png', text_size=14)
process_and_plot('AOI_hits.json', 'AOI_hits_relativ.png', text_size=14)
process_and_plot('first_AOI_hits_A.json', 'first_AOI_Hits_A_relativ.png', text_size=14)
process_and_plot('first_AOI_hits_B.json', 'first_AOI_hits_B_relativ.png', text_size=14)
process_and_plot('AOI_hits_A.json', 'AOI_hits_A_relativ.png', text_size=14)
process_and_plot('AOI_hits_B.json', 'AOI_hits_B_relativ.png', text_size=14)
############################################## END ##########################################################
