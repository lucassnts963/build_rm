import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mg

from database.rmdb import RMDB

class EditRMScreen(tk.Frame):
    def __init__(self, master, db: RMDB):
        super().__init__(master)
        self.db = db

        self.create_widgets()
    
    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Design Section
        design_frame = ttk.Frame(self)
        design_frame.pack(fill='both', expand=True, pady=5, padx=5)
        design_frame.columnconfigure(0, weight=5)
        design_frame.columnconfigure(1, weight=80)
        design_frame.columnconfigure(2, weight=5)
        design_frame.columnconfigure(3, weight=5)

        self.rm = None
        self.options = []

        ttk.Label(design_frame, text='Selecione a requisição: ').grid(row=0, column=0, sticky='nsew')
        self.rm_combo = ttk.Combobox(design_frame, values=self.options)
        self.rm_combo.grid(row=0, column=1, sticky='nsew')

        self.load_data()

        if len(self.options) > 0:
            self.rm_combo.set(self.options[0])

        ttk.Button(design_frame, text='Carregar', command=self.handle_load).grid(row=0, column=2, padx=5, sticky='nsew')
        ttk.Button(design_frame, text='Atualizar', command=self.load_data).grid(row=0, column=3, sticky='nsew')

        ttk.Label(design_frame, text='Informe o desenho:').grid(row=1, column=0, sticky='nsew')
        self.draw_entry = ttk.Entry(design_frame)
        self.draw_entry.grid(row=1, column=1, pady=5, sticky='nsew', columnspan=4)

        ttk.Label(design_frame, text='Immersed Electrode Boiler Project:').grid(row=2, column=0, sticky='nsew')
        self.local_entry = ttk.Entry(design_frame)
        self.local_entry.grid(row=2, column=1, pady=5, sticky='nsew', columnspan=3)

        ttk.Label(design_frame, text='Nº AREA DE TRABALHO:').grid(row=3, column=0, sticky='nsew')
        self.destiny_entry = ttk.Entry(design_frame)
        self.destiny_entry.grid(row=3, column=1, pady=5, sticky='nsew', columnspan=3)

        ttk.Label(design_frame, text='Solicitado por:').grid(row=4, column=0, sticky='nsew')
        self.username_entry = ttk.Entry(design_frame)
        self.username_entry.grid(row=4, column=1, pady=5, sticky='nsew', columnspan=3)

        btns_frame = ttk.Frame(design_frame)
        btns_frame.grid(row=5, column=0, columnspan=4, sticky='nsew')
        btns_frame.columnconfigure(0, weight=1)
        btns_frame.columnconfigure(1, weight=1)
        btns_frame.columnconfigure(2, weight=1)

        # Button
        ttk.Button(btns_frame, text='Salvar', command=self.handle_update).grid(row=0, column=0, sticky='nsew')
        ttk.Button(btns_frame, text='Excluir', command=self.handle_delete).grid(row=0, column=1, padx=5, sticky='nsew')
        ttk.Button(btns_frame, text='Limpar', command=self.handle_clear).grid(row=0, column=2, sticky='nsew')
    
    def load_data(self):
        self.options = []
        try:
            self.rms = self.db.list() 
            for rm in self.rms:
                self.options.append(rm['number'])
            self.rm_combo['values'] = self.options
        except Exception as e:
            mg.showerror('Erro', f'Erro ao carregar lista de requisições! {e}')

    def handle_update(self):
        destiny = self.destiny_entry.get()
        local = self.local_entry.get()
        draw = self.draw_entry.get()
        username = self.username_entry.get()
        number = self.rm_combo.get()

        if destiny == '' or local == '' or draw == '' or username == '' or number == '':
            mg.showwarning('Aviso', 'Todos os campos devem está preenchidos!')
            return
        
        result = mg.askokcancel('Atualizar requisição', 'Tem certeza que deseja atualizar as informações?')

        if not result:
            return

        if self.rm != None:
            self.db.update(
                id=self.rm['id'],
                date=self.rm['date'],
                destiny=destiny,
                draw=draw,
                local=local,
                revision=self.rm['revision'],
                username=username,
                number=number,
            )

            mg.showinfo('Atualizado!', 'As informações da requisição foram atualizadas com sucesso!')
    
    def handle_delete(self):
        if self.rm != None:
            result = mg.askokcancel('Excluír', 'Tem certeza que deseja excluir?')

            if not result:
                return
            
            self.db.delete(self.rm['id'])

            mg.showinfo('Excluído', 'A requisição foi excluída com sucesso!')
        else:
            mg.showwarning('Aviso', 'Primeiro carregue as informações da requisição, pressionando o botão "Carregar"')
        
        self.handle_clear()
    
    def handle_clear(self):
        self.draw_entry.delete(0, 'end')
        self.local_entry.delete(0, 'end')
        self.destiny_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.rm_combo['values'] = self.options
        self.rm_combo.set(self.options[0])
        self.rm = None
    
    def handle_load(self):
        if not self.rm_combo.get():
            return

        filtered_data = [item for item in self.rms if item['number'] == self.rm_combo.get()]

        lenght = len(filtered_data)

        if lenght == 1:
            self.rm = filtered_data[0]
            pass
        elif lenght > 1:
            last_revision = max(filtered_data, key=lambda item: item['revision'])
            self.rm = last_revision

        if self.rm:
            self.draw_entry.insert(0, self.rm['draw'])
            self.local_entry.insert(0, self.rm['local'])
            self.destiny_entry.insert(0, self.rm['destiny'])
            self.username_entry.insert(0, self.rm['username'])