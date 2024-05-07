import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

london = pd.DataFrame({
    'Long Jump': [8.31, 8.16, 8.12, 8.11, 8.10, 8.07, 8.01, 7.93],
    'Shot Put': [21.89, 21.86, 21.23, 21.19, 20.93, 20.84, 20.71, 20.69],
    'Discus': [68.27, 68.18, 68.03, 67.38, 67.19, 65.85, 65.56, 64.79],
    'Hammer Throw': [80.59, 79.36, 78.71, 78.25, 77.86, 77.17, 77.10, 76.07],
    'Javelin': [84.58, 84.51, 84.12, 83.34, 82.80, 82.63, 81.91, 81.21]
})
rio = pd.DataFrame({
    'Long Jump': [8.38, 8.37, 8.29, 8.25, 8.17, 8.10, 8.06, 8.05],
    'Shot Put': [22.52, 21.78, 21.36, 21.20, 21.02, 20.72, 20.64, 20.64],
    'Discus': [68.37, 67.55, 67.05, 66.58, 65.10, 64.95, 64.50, 63.72],
    'Hammer Throw': [78.68, 77.79, 77.73, 76.05, 75.97, 75.46, 75.28, 74.61],
    'Javelin': [90.30, 88.24, 85.38, 85.32, 83.95, 83.05, 82.51, 82.42]
})

london2 = pd.DataFrame({
    'Long Jump': [8.31, 8.16, 8.12, 8.11, 8.10, 8.07, 8.01, 7.93],
    'Shot Put': [21.89, 21.86, 21.23, 21.19, 20.93, 20.84, 20.71, 20.69],
    'Discus': [68.27, 68.18, 68.03, 67.38, 67.19, 65.85, 65.56, 64.79],
    'Hammer Throw': [80.59, 79.36, 78.71, 78.25, 77.86, 77.17, 77.10, 76.07],
    'Javelin': [84.58, 84.51, 84.12, 83.34, 82.80, 82.63, 81.91, 81.21]
})

rio2 = pd.DataFrame({
    'Long Jump': [],
    'Shot Put': [],
    'Discus': [],
    'Hammer Throw': [],
    'Javelin': []
})

print(rio2)

datasets = [london, rio, london2, rio2]
# Define which colours you want to use
colors = ['blue', 'red', 'lightblue', 'pink']
# Define the groups
groups = ['Athens 2004', 'Beijing 2008', 'London 2012', 'Rio 2016']

# Get the max of the dataset
y_max = 100
# Get the min of the dataset
y_min = 0
# Calculate the y-axis range
y_range = y_max - y_min

# Create the plot
# plt.axes([left, bottom, width, height])
# Default = [0.125, 0.11, 0.775, 0.77]
ax = plt.axes()
# Set x-positions for boxes
x_pos_range = np.arange(len(datasets)) / (len(datasets) - 1)
x_pos = (x_pos_range * 0.5) + 0.75
# Plot
for i, data in enumerate(datasets):
    positions = [x_pos[i] + j * 1 for j in range(len(data.T))]
    bp = ax.boxplot(
        np.array(data), sym='', whis=[0, 100], widths=0.6 / len(datasets),
        labels=list(datasets[0]), patch_artist=True,
        positions=positions
    )
    # Fill the boxes with colours (requires patch_artist=True)
    k = i % len(colors)
    for box in bp['boxes']:
        box.set(facecolor=colors[k])
    # Make the median lines more visible
    plt.setp(bp['medians'], color='black')

    # Get the samples' medians
    medians = [bp['medians'][j].get_ydata()[0] for j in range(len(data.T))]
    medians = [str(round(s, 1)) for s in medians]
    # Increase the height of the plot by 5% to fit the labels
    ax.set_ylim([y_min - 0.1 * y_range, y_max + 0.05 * y_range])
    # Set the y-positions for the labels
    y_pos = y_min - 0.075 * y_range
    for tick, label in zip(range(len(data.T)), ax.get_xticklabels()):
        k = tick % 2
        ax.text(
            positions[tick], y_pos, r'$\tilde{x}=' + fr'{medians[tick]}$',
            horizontalalignment='center', size='xx-small'
        )
# Axis details
details = ax.set(
    title="Men's Finals at the Last Two Olympic Games",
    ylabel='Distance [m]'
)
ax.set_xlabel('Event')
ax.tick_params(axis='x', bottom=False)
xticks = ax.set_xticks(np.arange(len(list(datasets[0]))) + 1)
xticks = ax.set_xticks(np.arange(len(list(datasets[0])) + 1) + 0.5, minor=True)
xlim = ax.set_xlim([0.5, len(list(datasets[0])) + 0.5])
# for tick in ax.xaxis.get_major_ticks():
#     tick.label.set_fontsize(7)
# Legend
legend_elements = []
for i in range(len(datasets)):
    j = i % len(groups)
    k = i % len(colors)
    legend_elements.append(Patch(facecolor=colors[k], label=groups[j]))
ax.legend(handles=legend_elements, fontsize=8)
# Background
# ax.set_facecolor('0.8')
plt.grid(True, color='black', linestyle='-.', linewidth=0.2)

plt.show()
