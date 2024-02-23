import pandas as pd

from utils import round_to_nearest_multiple_of_6

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