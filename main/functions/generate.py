import os

from database.handler_data import generate_json
from pdf_generator import generate_pdf_with_node
from database.rmdb import RMDB
from utils import get_request_number, increment_request_number

def generate(draw, aplication, destiny, local, number = (get_request_number() + 1), revision = 0):
    _, rm = generate_json(os.path.join(os.getcwd(), 'temp'), draw_number=draw, aplication=aplication, destiny=destiny, local=local, number=number, revision=revision)
    generate_pdf_with_node()
    return rm

def save(draw, aplication, destiny, local, to_revision = False):

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

