import pandas as pd

df = pd.read_csv('dataset.csv')
df.loc[df['SIMILARITY'] == 2, 'SIMILARITY'] = 1
print(len(df))
df.to_csv('dataset.csv')

