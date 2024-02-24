import datetime

from pdf_generator import generate_pdf
from handler_data import get_data

materials = get_data('D3-2900-04-T-1001')

data = {
        'company': 'Montisol',
        'request_number': '0088',
        'date': datetime.datetime.today().strftime("%d/%m/%Y"),
        'expediton_date:' ''
        'local': 'Canteiro MONTISOL',
        'destiny':'FABRICAÇÃO ÁREA 97A',
        'materials': materials,
        # ... other template data
    }

generate_pdf(data)