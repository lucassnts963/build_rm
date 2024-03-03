import pandas as pd

import os

import utils

def build_report_status_material_por_sistema():

    
    df = pd.read_excel(os.path.join(utils.get_temp_folder(), 'data.xlsx'), sheet_name='NECESSIDADES')


    df = df[df['Categoria'] != 'Suportes']

    grouped = df.groupby(['Sistema', 'Categoria', 'Cód', 'Descrição', 'Diâmetro']).agg({
        'Qtd. Desenho': 'sum',
        'Qtd. Solicitada RMM': 'sum',
        'Qtd. Retirada': 'sum'
    })

    grouped.columns = ['Projeto', 'Solicitada', 'Retirada']

    filepath = os.path.join(utils.get_temp_folder(), 'status_material_por_sistema.csv')

    grouped.to_csv(filepath, sep=';', encoding='utf-8')

    return filepath