import pingouin as pg
import pandas as pd

n_rows = 18
df = pd.read_excel(
    f'./transformed_data/modified_rank_prior_{n_rows}.xlsx')
# df.head()
personality_labels = ['Extraversion',	'Agreeableness',
                      'Conscientiousness',	'Neuroticism',	'Openness to Experiences']
column = 'What best describes your gender?'
pairwise_df = {}
for personality in personality_labels:
    pw_test = pg.pairwise_tests(
        data=df, dv=personality, between=column, padjust='bonf').round(3)
    groupby_df = df.groupby(column)[personality].agg(
        ['mean', 'std', 'count']).round(3)
    pairwise_df.setdefault('Female mean', []).append(
        groupby_df['mean'].iloc[0])
    pairwise_df.setdefault('Female std', []).append(groupby_df['std'].iloc[0])
    pairwise_df.setdefault('Male mean', []).append(groupby_df['mean'].iloc[1])
    pairwise_df.setdefault('Male std', []).append(groupby_df['std'].iloc[1])
    pairwise_df.setdefault('T-value', []).append(pw_test['T'].values.item())
    pairwise_df.setdefault('DoF', []).append(pw_test['dof'].values.item())
    pairwise_df.setdefault(
        'p-value', []).append(pw_test['p-unc'].values.item())
    pairwise_df.setdefault('BF-10', []).append(pw_test['BF10'].values.item())
    pairwise_df.setdefault('hedges’ g', []).append(
        pw_test['hedges'].values.item())

# pd.DataFrame.from_dict(pairwise_df)
pd.DataFrame.from_dict(pairwise_df).to_excel(
    './plot_document/pairwise_genders.xlsx', index=False)
