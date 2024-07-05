import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

org_table = pd.read_excel(
    r'.\data\Survey.xlsx')

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

if version == "old":
    org_table = org_table.replace('Disagree strongly', 1)
    org_table = org_table.replace('Disagree moderately', 2)
    org_table = org_table.replace('Disagree a little', 3)
    org_table = org_table.replace('Neither agree nor disagree', 4)
    org_table = org_table.replace('Agree a little', 5)
    org_table = org_table.replace('Agree moderately', 6)
    org_table = org_table.replace('Agree strongly', 7)
    org_table = org_table.replace(np.nan, '-')
    org_table.fillna('-')
    start_idx = -11

    modified_table = org_table[['ID', 'What is your nationality?',
                                'Age', 'Gender']]
else:
    org_table = org_table.replace(np.nan, '-')
    org_table.fillna('-')
    start_idx = -11

    modified_table = org_table[['Id', 'What is your nationality?',
                                'What is your age?', 'What best describes your gender?']]
# calculate scores for personalities and save to modified -11 -> -2 (-12 + sent num)

modified_table['Extraversion'] = (
    org_table.iloc[:, start_idx + 1]) + (8 - (org_table.iloc[:, start_idx + 6]))
modified_table['Agreeableness'] = (
    8 - (org_table.iloc[:, start_idx + 2])) + (org_table.iloc[:, start_idx + 7])
modified_table['Conscientiousness'] = (
    org_table.iloc[:, start_idx + 3]) + (8 - (org_table.iloc[:, start_idx + 8]))
modified_table['Neuroticism'] = (
    org_table.iloc[:, start_idx + 4]) + (8 - (org_table.iloc[:, start_idx + 9]))
modified_table['Openness to Experiences'] = (
    org_table.iloc[:, start_idx + 5]) + (8 - (org_table.iloc[:, start_idx + 10]))


# Case<#>-Question<#>-Rank<#>
addition_columns = {}

# 12 questions
for i, (question, answers) in enumerate(org_table.iloc[:, 1: 1 + (3 * 2) * 2].to_dict('List').items()):
    # print(question, len(answers))
    for j, answer in enumerate(answers):  # n responses
        # print(answer)
        try:
            if ';' in answer:
                sentences = answer[:-1].split(';')
            else:
                sentences = answer.split(';')

            if len(sentences) < 6:
                sentences.extend(['-'] * (6-len(sentences)))

            if i % 2 == 0:
                for k, sentence in enumerate(sentences):  # 6 ranked answers
                    addition_columns.setdefault(
                        f'Case_{i//6}-Question_{((i//2) % 6) % 3}-Answer_{k % 6}', []).append(sentence)
                    pass
            else:
                addition_columns.setdefault(
                    f'Case_{i//6}-Question_{((i//2) % 6) % 3}-Answer_prefered', []).append(sentences[0])
        except:
            print(answer)
addition_columns = dict(sorted(addition_columns.items()))

for k, v in addition_columns.items():
    modified_table[k] = v

modified_table.to_excel(
    f'./transformed_data/modified_rank_prior_{n_rows}.xlsx', index=False)


# calculate scores for personalities and save to modified -11 -> -2 (-12 + sent num)
# Case<#>-Question<#>-Sentence<#>
if version == "old":
    org_table = org_table.replace('Disagree strongly', 1)
    org_table = org_table.replace('Disagree moderately', 2)
    org_table = org_table.replace('Disagree a little', 3)
    org_table = org_table.replace('Neither agree nor disagree', 4)
    org_table = org_table.replace('Agree a little', 5)
    org_table = org_table.replace('Agree moderately', 6)
    org_table = org_table.replace('Agree strongly', 7)
    org_table = org_table.replace(np.nan, '-')
    org_table.fillna('-')
    start_idx = -11

    modified_table = org_table[['ID', 'What is your nationality?',
                                'Age', 'Gender']]
else:
    org_table = org_table.replace(np.nan, '-')
    org_table.fillna('-')
    start_idx = -11

    modified_table = org_table[['Id', 'What is your nationality?',
                                'What is your age?', 'What best describes your gender?']]
# calculate scores for personalities and save to modified -11 -> -2 (-12 + sent num)

modified_table['Extraversion'] = (
    org_table.iloc[:, start_idx + 1]) + (8 - (org_table.iloc[:, start_idx + 6]))
modified_table['Agreeableness'] = (
    8 - (org_table.iloc[:, start_idx + 2])) + (org_table.iloc[:, start_idx + 7])
modified_table['Conscientiousness'] = (
    org_table.iloc[:, start_idx + 3]) + (8 - (org_table.iloc[:, start_idx + 8]))
modified_table['Neuroticism'] = (
    org_table.iloc[:, start_idx + 4]) + (8 - (org_table.iloc[:, start_idx + 9]))
modified_table['Openness to Experiences'] = (
    org_table.iloc[:, start_idx + 5]) + (8 - (org_table.iloc[:, start_idx + 10]))


addition_columns_2 = {}
# 12 questions
for i, (question, answers) in enumerate(org_table.iloc[:, 1: 1 + (3 * 2) * 2].to_dict('List').items()):
    # print(question, len(answers))
    for j, answer in enumerate(answers):  # n responses
        # print(answer)
        try:
            if ';' in answer:
                sentences = answer[:-1].split(';')
            else:
                sentences = answer.split(';')

            if len(sentences) < 6:
                sentences.extend(['-'] * (6-len(sentences)))

            if i % 2 == 0:
                for k, sentence in enumerate(sentences):  # 6 ranked answers
                    addition_columns_2.setdefault(
                        f'Case_{i//6}-Question_{((i//2) % 6) % 3}-Sent[{sentence}]', []).append(6 - k % 6)
                    pass
            else:
                pass
        except:
            print(answer)
addition_columns_2 = dict(sorted(addition_columns_2.items()))

for k, v in addition_columns_2.items():
    modified_table[k] = v


modified_table.to_excel(
    f'./transformed_data/modified_sent_prior_{n_rows}.xlsx', index=False)


# //
map_big5_sents = pd.read_csv(
    './data/sentences.csv')
map_big5_sents = map_big5_sents.to_dict('list')
map_big5_sents = dict((vi.lower(), k)
                      for k, v in map_big5_sents.items() for vi in v)
map_big5_sents['Nonverbal communications (e.g. Head nod, gestures, eye contact)'.lower(
)] = 'Voiceless'
map_big5_sents['showing hand gestures and eye contact on the display screen'.lower()
               ] = 'Silent'

modified_combined_table = modified_table.iloc[:, 0:9]

if len(modified_table.columns) > 10:
    addition_columns_3 = {}
    # 12 questions
    for i, (col_name, list_rank) in enumerate(modified_table.iloc[:, 9:].to_dict('List').items()):
        case, question, sent = col_name.split("-")
        personality = map_big5_sents[sent.replace(
            '[', '').replace("]", "").replace("Sent", "").lower()]
        key = f"{case} with {personality}"
        if key not in addition_columns_3:
            addition_columns_3[key] = list_rank
        else:
            new_col = [x + y for x,
                       y in zip(list_rank, addition_columns_3[key])]
            addition_columns_3[key] = new_col

    addition_columns_3 = dict(sorted(addition_columns_3.items()))

    for k, v in addition_columns_3.items():
        modified_combined_table[k] = v

    modified_combined_table.to_excel(
        f'./transformed_data/modified_sent_prior_{n_rows}_avg.xlsx', index=False)
