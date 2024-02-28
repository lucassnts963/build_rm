import pandas as pd
import numpy as np

import os, json, datetime

from utils import round_to_nearest_multiple_of_6, get_request_number

# Corrigindo warning fillna
pd.set_option('future.no_silent_downcasting', True)

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

    df.columns = [
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

    df = df[(df['category'] != 'Suportes') & (df['draw_number'] == draw_number)]

    df = df.copy().groupby(['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn']).sum(['quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']).reset_index()
    
    df = df[['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn', 'quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']]

    df['quantity_requested'] = df['quantity_required'].apply(round_to_nearest_multiple_of_6)
    materials = df.to_dict('records')

    return materials

def generate_json(path_origin, path_destiny = 'temp', draw_number = 'D3-2900-04-T-1001', local = '', destiny = '', aplication = '', number = (get_request_number() + 1), revision = 0):
    filename = 'data.json'
    path = os.path.join(os.getcwd(), path_destiny, filename)

    df = pd.read_excel(os.path.join(path_origin, 'data.xlsx'), sheet_name='NECESSIDADES')

    df.columns = [
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
        'materials': materials
    }

    if df.size > 0:
        rms = df['n_rm'].unique().astype(str)
        tag = df.iloc[0]['tag']
        draw = df.iloc[0]['draw_number']

        if rms.size >= 1:
            data['rm'] = rms[0]

        if rms.size > 1:
            if '0' in rms:
                rms = rms[~np.char.equal(rms, "0")]
                data['rm'] = '|'.join(str(e) for e in rms)
            else:
                data['rm'] = '|'.join(str(e) for e in rms)
        
        if revision != 0:
            data['rm'] = f'{data['rm']}-REVISÃO-{revision}'


        data['tag'] = tag
        data['expedition'] = ' '
        data['draw'] = draw
        data['local'] = local
        data['destiny'] = destiny
        data['aplication'] = aplication
        data['date'] = datetime.datetime.today().strftime("%d-%m-%Y"),
        data['company'] = 'MONTISOL'


    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

    return path, data['rm'].strip()