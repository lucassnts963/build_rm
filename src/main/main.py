import datetime, subprocess, os

from handler_data import generate_json
from pdf_generator import generate_pdf_with_node

# materials = get_data('D3-2900-04-T-1001')

data = {
    'company': 'Montisol',
    'request_number': '0088',
    'date': datetime.datetime.today().strftime("%d-%m-%Y"),
    'expedition_date': ' ',
    'local': 'Canteiro MONTISOL',
    'destiny':'FABRICAÇÃO ÁREA 97A',
    'materials': [],
    'draw_number': 'D3-2900-14-T-1010',
    'tag': '5384'
}

data_path = generate_json(os.path.join(os.getcwd(), 'temp'))
generate_pdf_with_node(data)