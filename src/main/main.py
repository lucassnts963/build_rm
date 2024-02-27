import datetime, subprocess, os

from handler_data import generate_json
from pdf_generator import generate_pdf_with_node

import PySimpleGUI as sg

data = {
    'company': 'Montisol',
    'request_number': '0088',
    'date': datetime.datetime.today().strftime("%d-%m-%Y"),
    'expedition_date': ' ',
    'local': 'Canteiro MONTISOL',
    'destiny':'FABRICAÇÃO ÁREA 97A',
    'materials': [],
    'draw_number': 'D3-2900-14-T-1010',
    'tag': '5384',
    'aplication': ' '
}

def save(draw, aplication, destiny):
    data['aplication'] = aplication
    data['draw_number'] = draw
    data['destiny'] = destiny
    generate_json(os.path.join(os.getcwd(), 'temp'), draw_number=draw)
    generate_pdf_with_node(data)

aplication_default = 'MATERIAL DE APLICAÇÃO: ÁREA 14 - GERAÇÃO DE VAPOR E AR COMPRIMIDO - POLIMENTO'
local = 'Canteiro MONTISOL'
destiny = 'FABRICAÇÃO ÁREA 97A'

layout = [
    [sg.Text('Informe o desenho')], 
    [sg.Input(key='draw')],
    [sg.Text('Immersed Electrode Boiler Project')],
    [sg.Input(key='local', default_text=local)],
    [sg.Text('Nº AREA DE TRABALHO')],
    [sg.Input(key='destiny', default_text=destiny)],
    [sg.Text('Infome a aplicação do desenho')], 
    [sg.Input(key='aplication', default_text=aplication_default)],
    [sg.Button("Gerar"), sg.Button("Cancelar")],
]

window = sg.Window(title='Requisição', layout=layout, margins=(100, 100))

while True:
    event, values = window.read()

    if event == 'Cancelar' or event == sg.WIN_CLOSED:
        break
    if event == 'Gerar':
        save(values['draw'], values['aplication'], values['destiny'])

window.close()

