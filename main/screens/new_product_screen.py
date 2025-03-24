import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

from utils.config import Settings

from database.stockdb import add_new_product

class NewProductScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.settings = Settings()

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Additional Fields Section
        fields_frame = ttk.Frame(self)
        fields_frame.columnconfigure(0, weight=20)
        fields_frame.columnconfigure(1, weight=80)
        fields_frame.pack(fill='both', expand=True, pady=5)

        ttk.Label(fields_frame, text='Descrição:', anchor='e').grid(row=0, column=0, sticky='nsew')
        self.description_entry = ttk.Entry(fields_frame)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        ttk.Label(fields_frame, text='Código [Commodity]:', anchor='e').grid(row=1, column=0, sticky='nsew')
        self.code_entry = ttk.Entry(fields_frame)
        self.code_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        ttk.Label(fields_frame, text='NI [Código Hydro]:', anchor='e').grid(row=2, column=0, sticky='nsew')
        self.ni_entry = ttk.Entry(fields_frame)
        self.ni_entry.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        ttk.Label(fields_frame, text='Diâmetro:', anchor='e').grid(row=3, column=0, sticky='nsew')
        self.diameter_entry = ttk.Entry(fields_frame)
        self.diameter_entry.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')

        self.category_options = ["Tubos", "Flanges", "Figuras", "Conexões", "Juntas", "Válvulas", "Suportes", "Parafusos", "Instrumentos"]

        ttk.Label(fields_frame, text='Categoria:').grid(row=4, column=0)
        self.combo_category = ttk.Combobox(fields_frame, values=self.category_options, width=65)
        self.combo_category.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')

        self.unity_options = ["un", "m"]

        ttk.Label(fields_frame, text='Unidade:').grid(row=5, column=0)
        self.combo_unity = ttk.Combobox(fields_frame, values=self.unity_options, width=65)
        self.combo_unity.grid(row=5, column=1, padx=5, pady=5, sticky='nsew')

        self.combo_unity.set(self.unity_options[0])

        self.aplication_options = ["Montagem", "Fabricação"]

        ttk.Label(fields_frame, text='Aplicação:').grid(row=6, column=0)
        self.combo_aplication = ttk.Combobox(fields_frame, values=self.unity_options, width=65)
        self.combo_aplication.grid(row=6, column=1, padx=5, pady=5, sticky='nsew')


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
        ttk.Button(actions_frame, text='Salvar', command=self.handle_save).grid(row=0, column=0, sticky='nsew')

    #  Placeholders for your action functions
    def handle_search(self):
        search_term = self.description_entry.get()

        if len(search_term) > 0:
            new_data = [item for item in self.options if search_term in item.lower()]

            self.combo_draw['values'] = new_data
            if len(new_data) > 0:
                self.combo_draw.set(new_data[0])
            
    
    def handle_clear(self):
        self.description_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.code_entry.delete(0, 'end')
        self.ni_entry.delete(0, 'end')
        self.combo_category['values'] = self.category_options
        self.combo_category.set(self.category_options[0])
        self.combo_unity['values'] = self.unity_options
        self.combo_unity.set(self.unity_options[0])
    
    def handle_load(self):
        pass

    def handle_save(self):
        description = self.description_entry.get()
        code = self.code_entry.get()
        ni = self.ni_entry.get()
        diameter = self.diameter_entry.get()
        aplication = self.combo_aplication.get()
        category = self.combo_category.get()
        unity = self.combo_unity.get()
        

        if category == '' or description == '' or code == '' or unity == '' or diameter == '' or aplication == '':
            mb.showwarning('Aviso!', 'Todos os campos devem esta preenchidos clique em "Carregar" e preencha os campos com os valores padrão!')
            return
        

        try:
          message = add_new_product(code=code,category=category, aplication=aplication, description=description, diameter=diameter, ni=ni, unity=unity)
          mb.showinfo('Sucesso!', message)
        except Exception as e:
            mb.showerror('Error!', e)

        
