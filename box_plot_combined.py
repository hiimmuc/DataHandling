import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

import plotly.graph_objects as go
from docx.shared import Inches
from docx.enum.section import WD_ORIENT
from docx import Document
import os
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


map_big5_sents = pd.read_csv(
    './data/sentences.csv')
map_big5_sents = map_big5_sents.to_dict('list')
map_big5_sents = dict((vi.lower(), k)
                      for k, v in map_big5_sents.items() for vi in v)
map_big5_sents['Nonverbal communications (e.g. Head nod, gestures, eye contact)'.lower(
)] = 'NonVerbal'
map_big5_sents['showing hand gestures and eye contact on the display screen'.lower()
               ] = 'Silent'

# map_big5_sents['-'] = '-'
key_order = ['Agreeableness', 'Conscientiousness',
             'Openness to Experiences',	'Extraversion',	'Neuroticism', 'NonVerbal', 'Silent']
ques_ans_map = {}
for idx, (k, v) in enumerate(map_big5_sents.items()):
    ques_ans_map.setdefault(idx % 3, set()).add(k)

ques_ans_map[0].add(
    'Nonverbal communications (e.g. Head nod, gestures, eye contact)'.lower())
ques_ans_map[1].add(
    'Nonverbal communications (e.g. Head nod, gestures, eye contact)'.lower())
ques_ans_map[2].add(
    'Nonverbal communications (e.g. Head nod, gestures, eye contact)'.lower())
ques_ans_map[0].add(
    'showing hand gestures and eye contact on the display screen'.lower())
ques_ans_map[1].add(
    'showing hand gestures and eye contact on the display screen'.lower())
ques_ans_map[2].add(
    'showing hand gestures and eye contact on the display screen'.lower())


def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)


n_rows = 18
df = pd.read_excel(
    f'./transformed_data/modified_sent_prior_{n_rows}_avg.xlsx')

strong_threshold = []
weak_threshold = []

for idx, (col_name, col_values) in enumerate(df.iloc[:, 4:9].to_dict('list').items()):
    # print(col_name)
    strong_threshold.append(df[col_name].mean() + 0.5 * df[col_name].std())
    weak_threshold.append(df[col_name].mean() - 0.5 * df[col_name].std())
    pass

# print(strong_threshold, weak_threshold)

personalities = {'Vietnamese': {'High': {}, 'Low': {}},
                 'Japanese': {'High': {}, 'Low': {}}}
df_vn = df[df['What is your nationality?']
           == 'Vietnamese']
df_jp = df[df['What is your nationality?']
           == 'Japanese']

for idx, (col_name, col_values) in enumerate(df.iloc[:, 4:9].to_dict('list').items()):

    personalities['Vietnamese']['High'][col_name] = df_vn[df_vn[col_name]
                                                          >= strong_threshold[idx]]
    personalities['Vietnamese']['Low'][col_name] = df_vn[df_vn[col_name]
                                                         <= weak_threshold[idx]]
    personalities['Japanese']['High'][col_name] = df_jp[df_jp[col_name]
                                                        >= strong_threshold[idx]]
    personalities['Japanese']['Low'][col_name] = df_jp[df_jp[col_name]
                                                       <= weak_threshold[idx]]

personalities = dict(sorted(personalities.items()))
personality_labels = ['Extraversion', 'Agreeableness', 'Conscientiousness',
                      'Neuroticism', 'Openness to Experiences']

# print(personalities)

# Settings
x = 6  # Want figures to be A6
plt.rc('figure', figsize=[46.82 * .5**(.5 * x), 33.11 * .5**(.5 * x)])
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Define which colours you want to use
colors = ['blue', 'red', 'lightblue', 'pink']
# Define the groups
groups = ['High score of Vietnamese',
          'Low score of Vietnamese',
          'High score of Japanese',
          'Low score of Japanese']

datasets = [personalities[nationality][level]
            for nationality in personalities.keys() for level in ['High', 'Low']]

y_min = 0
y_max = 6
y_range = 6

# # Create the plot
ax = plt.axes()
# Set x-positions for boxes
x_pos_range = np.arange(len(datasets)) / (len(datasets) - 1)
x_pos = (x_pos_range * 0.5) + 0.75
# print("", len(x_pos_range))
# # Plot
for i in range(2):  # case 0, 1
    for personality in personality_labels:  # personality 5
        for idx, df in enumerate(datasets):  # 4 each label in col
            start_index = 9 + i * 6
            df_qa = df[personality].iloc[:, start_index: start_index + 6]
            case_num, _ = list(df_qa.columns)[0].split(' with ')

            # Case_0 with Agreeableness
            myKeys = list([x.split(' with ')[-1] for x in df_qa.keys()])
            myKeys.sort()

            sorted_dict = {' with '.join([case_num, personality]): df_qa[' with '.join(
                [case_num, personality])] for personality in myKeys}

            data = [col_list/3 for col_name, col_list in sorted_dict.items()]

            labels = [col_name for col_name, col_list in sorted_dict.items()]
            # print(labels, '\n', data)

            positions = [x_pos[idx] + j * 1 for j in range(len(key_order) - 1)]
            print(np.array(data).T, labels)

            bp = ax.boxplot(
                np.array(data).T,
                sym='', whis=[0, 100], widths=0.6 / len(datasets),
                labels=labels, patch_artist=True,
                positions=positions
            )

        # Fill the boxes with colours (requires patch_artist=True)
        k = i % len(colors)
        for box in bp['boxes']:
            box.set(facecolor=colors[k])

        # Make the median lines more visible
        plt.setp(bp['medians'], color='black')

        # Get the samples' medians
        medians = [bp['medians'][j].get_ydata()[0]
                   for j in range(len(key_order) - 1)]
        medians = [str(round(s, 2)) for s in medians]
        # Increase the height of the plot by 5% to fit the labels
        ax.set_ylim([y_min - 0.1 * y_range, y_max + 0.05 * y_range])
        # Set the y-positions for the labels
        y_pos = y_min - 0.075 * y_range

        for tick, label in zip(range(len(key_order) - 1), ax.get_xticklabels()):
            k = tick % 2
            ax.text(
                positions[tick], y_pos, r'$\tilde{x} =' +
                fr' {medians[tick]}$m',
                horizontalalignment='center', size='small'
            )

        # Axis details
        details = ax.set(
            title=f'How likely {personality} participant like each sentence list',
            ylabel='Average Score'
        )
        ax.tick_params(axis='x', bottom=False)
        xticks = ax.set_xticks(np.arange(len(list(df_qa))) + 1)
        xticks = ax.set_xticks(
            np.arange(len(list(df_qa)) + 1) + 0.5, minor=True)
        xlim = ax.set_xlim([0.5, len(list(df_qa)) + 0.5])
        # Legend
        legend_elements = []
        for i in range(len(datasets)):
            j = i % len(groups)
            k = i % len(colors)
            legend_elements.append(
                Patch(facecolor=colors[k], label=groups[j]))
        ax.legend(handles=legend_elements, fontsize=8)

        # plt.show()
        plt.tight_layout()
        # plt.grid(True)
        # plt.show()
        os.makedirs('./figures/survey_box_images_avg/', exist_ok=True)
        plt.savefig(
            f'./figures/survey_box_images_avg/{case_num}-{personality}.png', bbox_inches='tight')
        plt.close()
