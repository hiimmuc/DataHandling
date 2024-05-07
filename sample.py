import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Results of the long jump finals at four olympic games
athens = pd.DataFrame({
    'Men': [8.59, 8.47, 8.32, 8.31, 8.25, 8.24, 8.23, 8.21],
    'Women': [7.07, 7.05, 7.05, 6.96, 6.85, 6.83, 6.80, 6.73]
})
beijing = pd.DataFrame({
    'Men': [8.34, 8.24, 8.20, 8.19, 8.19, 8.16, 8.07, 8.00],
    'Women': [7.04, 7.03, 6.91, 6.79, 6.76, 6.70, 6.64, 6.58]
})
london = pd.DataFrame({
    'Men': [8.31, 8.16, 8.12, 8.11, 8.10, 8.07, 8.01, 7.93],
    'Women': [7.12, 7.07, 6.89, 6.88, 6.77, 6.76, 6.72, 6.67]
})
rio = pd.DataFrame({
    'Men': [8.38, 8.37, 8.29, 8.25, 8.17, 8.10, 8.06, 8.05],
    'Women': [7.17, 7.15, 7.08, 6.95, 6.81, 6.79, 6.74, 6.69]
})
datasets = [athens, beijing, london, rio]

# Create the plot
ax = plt.axes()
# Set x-positions for boxes
x_pos_range = np.arange(len(datasets)) / (len(datasets) - 1)
x_pos = (x_pos_range * 0.5) + 0.75
# Plot
for i, data in enumerate(datasets):
    print(np.array(data), list(datasets[0]))
    bp = ax.boxplot(
        np.array(data), sym='', whis=[0, 100], widths=0.6 / len(datasets),
        labels=list(datasets[0]),
        positions=[x_pos[i] + j * 1 for j in range(len(data.T))]
    )
# Titles
ax.set(
    title='Long Jump Finals at the Last Four Olympic Games',
    ylabel='Distance [m]'
)
# Remove the major x-axis tickmarks
ax.tick_params(axis='x', bottom=False)
# Positions of the x-axis labels
xticks = ax.set_xticks(np.arange(len(list(datasets[0]))) + 1)
# Positions of the minor x-axis tickmarks
xticks = ax.set_xticks(np.arange(len(list(datasets[0])) + 1) + 0.5, minor=True)
# Change the limits of the x-axis
xlim = ax.set_xlim([0.5, len(list(datasets[0])) + 0.5])

plt.show()
