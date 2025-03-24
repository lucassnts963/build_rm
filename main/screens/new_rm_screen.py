import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

import datetime

from database.handler_data import get_draws, get_project, generate_json
from database.rmdb import RMDB
from functions.pdf_generator import generate_pdf_with_node
from utils import get_request_number, put_zero_in_front, increment_request_number
from utils.config import Settings

class NewRMScreen(tk.Frame):
    def __init__(self, master, db: RMDB, project = 'CALDEIRAS', contract='CT 4600011605 CALDEIRAS'):
        super().__init__(master)
        self.db = db

        self.project = project
        self.contract = contract

        self.settings = Settings()

        self.data_path = self.settings.get_materials_data_path(project=self.project)
        self.projects_path = self.settings.get_projects_data_path(project=self.project)

        self.rms = db.list()

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Search Section
        search_frame = tk.Frame(self)
        search_frame.columnconfigure(0, weight=5)
        search_frame.columnconfigure(1, weight=75)
        search_frame.columnconfigure(2, weight=10)
        search_frame.columnconfigure(3, weight=10)
        search_frame.pack(fill='both', expand=True, pady=5, padx=5)

        ttk.Label(search_frame, text='Pesquise:', anchor='e').grid(row=0, column=0)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, sticky='nsew')
        ttk.Button(search_frame, text='Pesquisar', command=self.handle_search).grid(row=0, column=2, padx=2, sticky='nsew')
        ttk.Button(search_frame, text='Limpar', command=self.handle_clear).grid(row=0, column=3, padx=2, sticky='nsew')
        

        # Design Section
        design_frame = ttk.Frame(self)
        design_frame.columnconfigure(0, weight=10)
        design_frame.columnconfigure(1, weight=70)
        design_frame.columnconfigure(2, weight=20)
        design_frame.pack(fill='both', expand=True, pady=5, padx=5) 


        self.data = get_draws(project=self.project)
        self.options = list(self.data.keys())

        ttk.Label(design_frame, text='Informe o desenho:').grid(row=0, column=0)
        self.combo_draw = ttk.Combobox(design_frame, values=self.options, width=65)
        self.combo_draw.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.combo_draw.set(self.options[0])

        ttk.Button(design_frame, text='Carregar', command=self.handle_load).grid(row=0, column=2, sticky='ew')

        # Additional Fields Section
        fields_frame = ttk.Frame(self)
        fields_frame.columnconfigure(0, weight=25)
        fields_frame.columnconfigure(1, weight=75)
        fields_frame.pack(fill='both', expand=True, pady=5)

        ttk.Label(fields_frame, text='Imm. Elect. Boiler Project:', anchor='e').grid(row=0, column=0, sticky='nsew')
        self.local_entry = ttk.Entry(fields_frame)
        self.local_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        ttk.Label(fields_frame, text='Nº AREA DE TRABALHO:', anchor='e').grid(row=1, column=0, sticky='nsew')
        self.destiny_entry = ttk.Entry(fields_frame)
        self.destiny_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        ttk.Label(fields_frame, text='Solicitado por:', anchor='e').grid(row=2, column=0, sticky='nsew')
        self.username_entry = ttk.Entry(fields_frame)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        ttk.Label(fields_frame, text='Aplicação do desenho:', anchor='e').grid(row=3, column=0, sticky='nsew')
        self.aplication_text = tk.Text(fields_frame, height=10)
        self.aplication_text.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')


        actions_frame = ttk.Frame(self)
        actions_frame.columnconfigure(0, weight=90)
        actions_frame.columnconfigure(1, weight=5)
        actions_frame.columnconfigure(2, weight=5)
        actions_frame.pack(fill='both', expand=True, pady=5, padx=5)

        self.to_review = tk.BooleanVar()
        self.to_review.set(False)

        self.isutility = tk.BooleanVar()
        self.isutility.set(False)

        # Button
        ttk.Button(actions_frame, text='Gerar', command=self.handle_generate).grid(row=0, column=0, sticky='nsew')
        self.btn_revision = ttk.Checkbutton(actions_frame, text='REVISÃO', variable=self.to_review, onvalue=True, offvalue=False)
        self.btn_revision.grid(row=0, column=1, sticky='nsew', padx=5)

        self.btn_utility = ttk.Checkbutton(actions_frame, text='UTILIDADES',variable=self.isutility, onvalue=True, offvalue=False)
        self.btn_utility.grid(row=0, column=2, sticky='nsew')

    #  Placeholders for your action functions
    def handle_search(self):
        search_term = self.search_entry.get()

        if len(search_term) > 0:
            new_data = [item for item in self.options if search_term in item.lower()]

            self.combo_draw['values'] = new_data
            if len(new_data) > 0:
                self.combo_draw.set(new_data[0])
            
    
    def handle_clear(self):
        self.search_entry.delete(0, 'end')
        self.local_entry.delete(0, 'end')
        self.destiny_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.aplication_text.delete('1.0', tk.END)
        self.combo_draw['values'] = self.options
        self.combo_draw.set(self.options[0])
    
    def handle_load(self):
        if not self.combo_draw.get():
            return
        
        project = get_project(draw=self.data[self.combo_draw.get()], project=self.project)

        if project:
            self.username_entry.insert(0, 'FLÁVIO RODRIGUES')
            self.local_entry.insert(0, 'Canteiro MONTISOL')
            self.destiny_entry.insert(0, 'FABRICA\u00c7\u00c3O \u00c1REA 97A')
            self.aplication_text.insert('end', project['aplication'])

    def handle_generate(self):
        draw = self.data[self.combo_draw.get()]
        local =  self.local_entry.get()
        destiny = self.destiny_entry.get()
        aplication = self.aplication_text.get('1.0', tk.END)
        date = datetime.datetime.today().strftime("%d-%m-%Y")
        username = self.username_entry.get()

        if draw == '' or local == '' or destiny == '' or aplication == '' or username == '':
            mb.showwarning('Aviso!', 'Todos os campos devem esta preenchidos clique em "Carregar" e preencha os campos com os valores padrão!')
            return

        number = f'MTS-RMM-{put_zero_in_front(get_request_number(project=self.project) + 1)}'
        
        rm = self.db.get_by_draw(draw)

        if self.to_review.get() and rm != None:
            try:
                generate_json(
                    draw_number=draw, 
                    local=local, 
                    destiny=destiny, 
                    aplication=aplication, 
                    number=rm['number'],
                    revision=rm['revision'] + 1,
                    date=date,
                    username=rm['username'], 
                    project=self.project,
                    contract=self.contract),
                generate_pdf_with_node(project=self.project)
                self.db.create(number=rm['number'], draw=rm['draw'], local=rm['local'], destiny=rm['destiny'], revision=rm['revision'] + 1, date=rm['date'], username=rm['username'])
                return
            except Exception as e:
               mb.showerror('Erro ao gerar PDF', f'{e}')

        if rm != None:
            try:
                generate_json(
                    draw_number=draw, 
                    local=local, 
                    destiny=destiny, 
                    aplication=aplication, 
                    number=rm['number'],
                    revision=rm['revision'], 
                    date=rm['date'],
                    username=rm['username'],
                    project=self.project,
                    contract=self.contract)
                generate_pdf_with_node(project=self.project)
            except Exception as e:
               mb.showerror('Erro ao gerar PDF', f'{e}')
        else:
            try:
                generate_json(
                    draw_number=draw, 
                    local=local, 
                    destiny=destiny, 
                    aplication=aplication, 
                    number=number, 
                    revision=0, 
                    date=date,
                    username=username,
                    project=self.project,
                    contract=self.contract)
                self.db.create(number=number, draw=draw, local=local, destiny=destiny, revision=0, date=date, username=username)
                generate_pdf_with_node(self.project)
                increment_request_number()
                self.handle_clear()
            except Exception as e:
               mb.showerror('Erro ao gerar PDF', f'{e}')
