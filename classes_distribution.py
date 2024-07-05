import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

n_rows = 18
df = pd.read_excel(
    f'./transformed_data/modified_rank_prior_{n_rows}.xlsx')
personality_labels = ['Extraversion',	'Agreeableness',
                      'Conscientiousness',	'Neuroticism',	'Openness to Experiences']
# strong and weak classes calculation
strong_threshold = []
weak_threshold = []

for idx, (col_name, col_values) in enumerate(df.iloc[:, 4:9].to_dict('list').items()):
    strong_threshold.append(df[col_name].mean() + 0.5 * df[col_name].std())
    weak_threshold.append(df[col_name].mean() - 0.5 * df[col_name].std())

print(strong_threshold, weak_threshold)

personalities = {}
for idx, (col_name, col_values) in enumerate(df.iloc[:, 4:9].to_dict('list').items()):
    personalities[f"High {col_name}"] = df[df[col_name]
                                           >= strong_threshold[idx]]
    personalities[f"Low {col_name}"] = df[df[col_name] <= weak_threshold[idx]]

personalities = dict(sorted(personalities.items()))

# plot distribution


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])


D = {k: len(v) for k, v in personalities.items()}

x = list(D.keys())
y = list(D.values())

fig, ax = plt.subplots()
width = 0.75  # the width of the bars
ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color="blue")
ax.set_yticks(ind)
ax.set_yticklabels(x, minor=False)
for i, v in enumerate(y):
    ax.text(v + 0.5, i - 0.25, str(v), color='green', fontweight='bold')
plt.title('number of responses to the question according to personalities')
plt.xlabel('number of responses to the question')
plt.ylabel('personalities')

plt.tight_layout()

plt.savefig("./figures/personalities_distribution.png")
plt.close()
