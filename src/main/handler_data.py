import pandas as pd

import os, json

from utils import round_to_nearest_multiple_of_6

status_substitution = {
    'RECEBIDO': 'recebido',
    'SOBRA': 'recebido',
    'RECEBIDO PARCIAL': 'recebido-parcial',
    'PENDENTE': 'pendente',
    'CANTEIRO MONTISOL': 'canteiro',
    'RETIRAR ALMOXARIFADO': 'almoxarifado',
    'FABRICAÇÃO EXTERNA NF': 'fabricacao-externa',
    'NÃO TEM NO ALMOXARIFADO': 'nao-tem-almoxarifado',
}

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

def generate_json(path_origin, path_destiny = 'temp', draw_number = 'D3-2900-04-T-1001'):
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

    df = df[(df['category'] != 'Suportes') & (df['draw_number'] == draw_number)]

    df = df.copy().groupby(['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn', 'unit', 'status']).sum(['quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']).reset_index()
    
    df = df[['draw_number', 'tag', 'n_rm', 'code', 'description', 'dn', 'unit', 'status', 'quantity_required', 'quantity_requested', 'quantity_taken', 'quantity_redirected']]

    df['status'] = df['status'].replace(status_substitution)

    df['quantity_requested'] = df['quantity_required'].apply(round_to_nearest_multiple_of_6)

    materials = df.to_dict('records')

    # json.dumps(materials)

    with open(path, 'w') as file:
        json.dump(materials, file, indent=4)

    return path