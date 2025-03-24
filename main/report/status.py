import pandas as pd

import os, datetime

import utils

from utils.config import Settings

settings = Settings()

def build_report_status_material_por_sistema(project='CALDEIRAS'):

    
    df = pd.read_excel(os.path.join(utils.get_temp_folder(project=project), 'data.xlsx'), sheet_name='NECESSIDADES')


    df = df[df['Categoria'] != 'Suportes']

    grouped = df.groupby(['Sistema', 'Categoria', 'Cód', 'Descrição', 'Diâmetro']).agg({
        'Qtd. Desenho': 'sum',
        'Qtd. Solicitada RMM': 'sum',
        'Qtd. Retirada': 'sum'
    })

    grouped.columns = ['Projeto', 'Solicitada', 'Retirada']

    project_contract = utils.get_project_contract(project=project)

    date = datetime.datetime.today().strftime("%d-%m-%Y_%Hhrs%Mmin%Sseg")

    filepath = os.path.join(settings.get_report_path(), f'{project_contract}_status_material_por_sistema_{date}.csv')

    grouped.to_csv(filepath, sep=';', encoding='utf-8')

    return filepath