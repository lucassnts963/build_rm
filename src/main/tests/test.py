import pandas as pd

import os

df = pd.read_excel(os.path.join(os.getcwd(), 'temp', 'data.xlsx'), sheet_name='NECESSIDADES')
df = df[df['Desenho'] == 'D3-2900-14-T-3079']

print(df)