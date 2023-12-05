import matplotlib.pyplot as plt
import functions as f

def plot_AOI_hits(AOI_hits):
    """Plots AOI hits.
    """
    fig = plt.figure(figsize=(30, 15))  # Increase the size of the figure
    ax = fig.add_subplot(111)
    labels = []
    for i, (key, value) in enumerate(AOI_hits.items()):
        ax.bar(i, value['hits'], label=key)
        label = key.split('AOI hit ')[1]  # Split the key at 'AOI hit ' and keep only the second part
        label = label.replace('[', '').replace(']', '')  # Remove square brackets
        labels.append(label)
    ax.set_xticks(range(len(AOI_hits)))
    ax.set_xticklabels(labels, rotation=45, fontsize=12, ha='right')  # Set horizontal alignment to 'right'
    plt.tight_layout()  # Adjust the layout to make room for the x-axis labels
    return fig

import json
with open('AOI_hits.json', 'r') as f:
    AOI_hits = json.load(f)

AOI_hits = {AOI: AOI_hits[AOI] for AOI in AOI_hits.keys() if AOI_hits[AOI]['hits'] > 100}
AOI_hits = {AOI: AOI_hits[AOI] for AOI in AOI_hits.keys() if "Zwischenbild" not in AOI}
AOI_hits = dict(sorted(AOI_hits.items(), key=lambda item: item[1]['hits'], reverse=True))


fig = plot_AOI_hits(AOI_hits)
# Save the figure.	
fig.savefig('AOI_hits.png')

