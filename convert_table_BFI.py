import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

org_table = pd.read_excel(
    r'./data/dataBFI.xlsx')

tipi_list = ['Extroverted, enthusiastic.',
             'Critical, quarrelsome.',
             'Dependable, self-disciplined.',
             'Anxious, easily upset.',
             'Open to new experiences, complex.',
             'Reserved, quiet.',
             'Sympathetic, warm.',
             'Disorganized, careless.',
             'Calm, emotionally stable.',
             'Conventional, uncreative.',]

version = 'new'
n_rows = len(org_table.index)

org_table = org_table.replace('Disagree strongly', 1)
org_table = org_table.replace('Disagree a little', 2)
org_table = org_table.replace('Neither agree nor disagree', 3)
org_table = org_table.replace('Agree a little', 4)
org_table = org_table.replace('Agree strongly', 5)
# org_table = org_table.replace(np.nan, '-')
org_table.fillna('-')

modified_table = org_table[['ID', 'What is your nationality?',
                            'What is your age?', 'What best describes your gender?']]

# calculate scores for personalities and save to modified -11 -> -2 (-12 + sent num)
for i in range(5):
    start_idx = 34 + 10 * i
    modified_table[f'Extraversion of scene {i+1}'] = (
        org_table.iloc[:, start_idx + 6]) + (6 - (org_table.iloc[:, start_idx + 1]))
    modified_table[f'Agreeableness of scene {i+1}'] = (
        6 - (org_table.iloc[:, start_idx + 7])) + (org_table.iloc[:, start_idx + 2])
    modified_table[f'Conscientiousness of scene {i+1}'] = (
        org_table.iloc[:, start_idx + 8]) + (6 - (org_table.iloc[:, start_idx + 3]))
    modified_table[f'Neuroticism of scene {i+1}'] = (
        org_table.iloc[:, start_idx + 9]) + (6 - (org_table.iloc[:, start_idx + 4]))
    modified_table[f'Openness to Experiences of scene {i+1}'] = (
        org_table.iloc[:, start_idx + 10]) + (6 - (org_table.iloc[:, start_idx + 5]))

modified_table.to_excel(
    f'./transformed_data/modified_BFI_{n_rows}.xlsx', index=False)
