import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

n_rows = 20
# df = pd.read_excel(
# f'./transformed_data/modified_rank_prior_{n_rows}.xlsx')
df = pd.read_excel(
    f'./transformed_data/onvehicleexp.xlsx')
# df = df[df['ID'].isin([17, 6, 13, 16, 5, 11, 23, 7, 30, 33, 25, 35])]

personality_labels = ['Extraversion',	'Agreeableness',
                      'Conscientiousness',	'Neuroticism',	'Openness to Experiences']

per_start_idx = 6
personalities_corr = df.iloc[:,
                             per_start_idx:per_start_idx+5].corr(method='pearson')
print(personalities_corr)

g = sns.heatmap(personalities_corr,
                vmax=1,
                vmin=-1,
                cmap='RdBu',
                annot=True,
                annot_kws={'size': 8})
# fig = plt.figure(figsize=(10, 10))
plt.title(f"On-Vehicle Experiment")
plt.setp(g.get_xticklabels(), rotation=70)
plt.setp(g.get_yticklabels(), rotation=0)
plt.savefig("./figures/personalities_correlation_exp.png")
plt.close()
