import pandas as pd
import numpy as np

import os, json, datetime

from utils import round_to_nearest_multiple_of_6, get_request_number, get_temp_folder

# Corrigindo warning fillna
pd.set_option('future.no_silent_downcasting', True)

temp = get_temp_folder()

columns = [
        'code', 
        'description', 
        'category', 
        'unit', 
        'dn', 
        'item', 
        'application', 
        'draw_number', 
        'page', 
        'tag', 
        'tie_in', 
        'systems', 
        'quantity_required', 
        'quantity_requested', 
        'quantity_taken', 
        'quantity_send_to_field', 
        'quantity_stock', 
        'quantity_used', 
        'quantity_redirected', 
        'tag_destiny_redirect', 
        'left', 
        'status', 
        'n_rm', 
        'request_date', 
        'taken_date', 
        'applicant', 
        'receiver', 
        'observation'
    ]

status_substitution = {
    'RECEBIDO': 'recebido',
    'SOBRA': 'recebido',
    'RECEBIDO PARCIAL': 'recebido-parcial',
    'PENDENTE': 'pendente',
    'CANTEIRO MONTISOL': 'canteiro',
    'RETIRAR ALMOXARIFADO': 'almoxarifado',
    'FABRICAÇÃO EXTERNA NF': 'fabricacao-externa',
    'NÃO TEM NO ALMOXARIFADO': 'nao-tem-almoxarifado',
    'SEM SOLICITAÇÃO': 'almoxarifado',
    'NF': 'fabricacao-externa'
}

def round_decimal(number):
    return round(number, 3)

def get_data(draw_number = 'D3-2900-04-T-1001'):

    df = pd.read_excel('data.xlsx', sheet_name='NECESSIDADES')

    df.columns = columns

    df = df[(df['category'] != 'Suportes') & (df['draw_number'] == draw_number)]

    df = df.copy().groupby(['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn']).sum(['quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']).reset_index()
    
    df = df[['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn', 'quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']]

    df['quantity_requested'] = df['quantity_required'].apply(round_to_nearest_multiple_of_6)
    materials = df.to_dict('records')

    return materials

def generate_json(path = temp, draw_number = '', local = '', destiny = '', aplication = '', number = (get_request_number() + 1), revision = 0, date = '', username = 'FLÁVIO RODRIGUES', contract = 'CT 4600011605 CALDEIRAS'):
    filename = 'data.json'
    datapath = os.path.join(temp, 'data.xlsx')
    path = os.path.join(os.getcwd(), temp, filename)

    df = pd.read_excel(datapath, sheet_name='NECESSIDADES')

    df.columns = columns

    df = df[(df['category'] != 'Suportes') & (df['draw_number'] == draw_number.strip())]
    df.fillna(0, inplace=True)

    df = df.copy().groupby(['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn', 'unit', 'status']).agg({
        'quantity_required': 'sum', 
        'quantity_requested': 'sum', 
        'quantity_taken': 'sum', 
        'quantity_redirected': 'sum'
    }).reset_index()

    df = df[['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn', 'unit', 'status', 'quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']]

    df['status'] = df['status'].replace(status_substitution)

    df['quantity_requested'] = df['quantity_required'].apply(round_to_nearest_multiple_of_6)
    df['quantity_required'] = df['quantity_required'].apply(round_decimal)

    materials = df.to_dict('records')

    data = {
        'rm': number,
        'materials': materials
    }

    if df.size > 0:
        tag = df.iloc[0]['tag']

        
        if revision != 0:
            data['rm'] = f'{data['rm']}-REVISÃO-{revision}'


        data['tag'] = tag
        data['expedition'] = ' '
        data['draw'] = draw_number
        data['local'] = local
        data['destiny'] = destiny
        data['aplication'] = aplication
        data['date'] = date,
        data['company'] = 'MONTISOL'
        data['username'] = username
        data['contract'] = contract


    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

    return path, data['rm'].strip()

def get_draws():
    df = pd.read_excel(os.path.join(temp, 'data.xlsx'), sheet_name='NECESSIDADES')

    df.columns = columns

    df = df[['draw_number', 'tag']]

    df['draw_tag'] = df['draw_number'].map(str) + ' (' + df['tag'].map(str) + ')'

    df.drop_duplicates(subset=['draw_tag'], inplace=True)
    
    return dict(zip(df['draw_tag'], df['draw_number']))

def get_project(draw):
    datapath = os.path.join(temp, 'projetos.xlsx')

    columns = [
        'tag',
        'tiein',
        'local',
        'system',
        'rev',
        'draw',
        'map',
        'status',
        'contract',
        'sender_field',
        'material_save',
        'description',
        'aplication',
        'obs'
    ]

    df = pd.read_excel(datapath, sheet_name='DESENHOS')

    df.columns = columns

    df = df[df['draw'] == str(draw)]

    if len(df) > 0:
        return df.iloc[0].to_dict()
    else:
        return None
    