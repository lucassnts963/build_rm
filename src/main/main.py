import datetime, subprocess, os

from handler_data import generate_json
from pdf_generator import generate_pdf_with_node
from database import RMDB
from utils import get_request_number, increment_request_number

import PySimpleGUI as sg

to_revision = False

def generate(draw, aplication, destiny, local, number = (get_request_number() + 1), revision = 0):
    _, rm = generate_json(os.path.join(os.getcwd(), 'temp'), draw_number=draw, aplication=aplication, destiny=destiny, local=local, number=number, revision=revision)
    generate_pdf_with_node()
    return rm

def save(draw, aplication, destiny, local):

    db = RMDB()

    row = db.get_by_draw(draw)

    if (row == None):
        number = get_request_number() + 1
        rm = generate(draw, aplication, destiny, local, number)
        if rm != '0':
            db.create(rm, draw, aplication, local, destiny, revision=0)
        else:
            db.create(f'MTS-RMM-{number}', draw, aplication, local, destiny, revision=0)
            increment_request_number()
    else:
        id = row[0]
        number = row[1]
        draw = row[2]
        aplication = row[3]
        local = row[4]
        destiny = row[5]
        revision = row[6]
        

        if to_revision:
            db.update(id, number=number, draw=draw, aplication=aplication, destiny=destiny, local=local, revision=revision+1)
            generate(draw, aplication, destiny, local, revision=revision + 1)
            return
        
        generate(draw, aplication, destiny, local)

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
    [sg.Button("Gerar"), sg.Button("Cancelar"), sg.Checkbox('Revisão', default=False, key='revision')],
]

window = sg.Window(title='Requisição', layout=layout, margins=(100, 100))

while True:
    event, values = window.read()

    if event == 'Cancelar' or event == sg.WIN_CLOSED:
        break
    if event == 'Gerar':
        to_revision = values['revision']
        save(values['draw'], values['aplication'], values['destiny'], values['local'])

window.close()

