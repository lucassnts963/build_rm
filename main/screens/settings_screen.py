import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as mb

import configparser

from utils.config import Settings

class SettingScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.settings = Settings()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        top_frame = ttk.Labelframe(main_frame, text='Pasta para salvar relatórios')
        top_frame.columnconfigure(0, weight=2)
        top_frame.columnconfigure(1, weight=78)
        top_frame.columnconfigure(2, weight=20)

        ttk.Label(top_frame, text='Selecione a pasta:').grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.path_report_entry = ttk.Entry(top_frame)
        self.path_report_entry.insert(0, self.settings.get_report_path())
        self.path_report_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        ttk.Button(top_frame, text='Procurar', command=self.handle_get_report_path).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        top_frame.pack(fill='both', expand=True, padx=5, pady=5)

        left_frame = ttk.Labelframe(main_frame, text='CALDEIRAS')
        left_frame.pack(fill='both', expand=True, padx=5, pady=5)
        left_frame.columnconfigure(0, weight=2)
        left_frame.columnconfigure(1, weight=78)
        left_frame.columnconfigure(2, weight=20)

        ttk.Label(left_frame, text='Selecione planilha de materiais:').grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.path_c_entry = ttk.Entry(left_frame)
        self.path_c_entry.insert(0, self.settings.get_materials_data_path())
        self.path_c_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        ttk.Button(left_frame, text='Procurar', command=self.handle_get_material_path_caldeiras).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        ttk.Label(left_frame, text='Selecione planilha de projetos:').grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.path_c_project_entry = ttk.Entry(left_frame)
        self.path_c_project_entry.insert(0,  self.settings.get_projects_data_path())
        self.path_c_project_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        ttk.Button(left_frame, text='Procurar', command=self.handle_get_project_path_caldeiras).grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        right_frame = ttk.Labelframe(main_frame, text='UTILIDADES')
        right_frame.pack(fill='both', expand=True, padx=5, pady=5)
        right_frame.columnconfigure(0, weight=2)
        right_frame.columnconfigure(1, weight=78)
        right_frame.columnconfigure(2, weight=20)

        ttk.Label(right_frame, text='Selecione planilha de materiais:').grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.path_u_entry = ttk.Entry(right_frame)
        self.path_u_entry.insert(0, self.settings.get_materials_data_path('UTILIDADES'))
        self.path_u_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        ttk.Button(right_frame, text='Procurar', command=self.handle_get_material_path_utility).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        ttk.Label(right_frame, text='Selecione planilha de projetos:').grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.path_u_project_entry = ttk.Entry(right_frame)
        self.path_u_project_entry.insert(0, self.settings.get_projects_data_path('UTILIDADES'))
        self.path_u_project_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        ttk.Button(right_frame, text='Procurar', command=self.handle_get_project_path_utility).grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.columnconfigure(0, weight=1)

        ttk.Button(btn_frame, text='Salvar', command=self.handle_save).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        btn_frame.pack(fill='both', expand=True, padx=5, pady=5)

    def handle_save(self):
       material_caldeira = self.path_c_entry.get()
       material_utility = self.path_u_entry.get()
       report_path = self.path_report_entry.get()

       project_caldeira = self.path_c_project_entry.get()
       project_utility = self.path_u_project_entry.get()

       result = mb.askyesno('Alterar pastas', f'Você deseja alterar as pastas padrão para:\n\n MATERIAL CALDEIRA: {material_caldeira}\n\n MATERIAL UTILIDADE: {material_utility}\n\n PROJETOS CALDEIRAS: {project_caldeira}\n\n PROJETOS UTILIDADES: {project_utility}\n\n PASTA RELATÓRIO: {report_path}\n')
       
       if not result:
           return

       self.settings.change_materials_path(material_caldeira)
       self.settings.change_materials_path(material_utility, project='UTILIDADES')
       self.settings.change_project_path(project_caldeira)
       self.settings.change_project_path(project_utility, project='UTILIDADES')
       self.settings.change_report_path(self.path_report_entry.get())

       mb.showinfo('Salvo!', 'As novas configurações foram salva com sucesso!')

    def handle_get_report_path(self):
        if self.path_report_entry.get() != '':
            self.path_report_entry.delete(0, tk.END)
        path = self.get_path()
        self.path_report_entry.insert(0, path.replace('/', '\\'))

    def handle_get_material_path_utility(self):
        if self.path_u_entry.get() != '':
            self.path_u_entry.delete(0, tk.END)
        filepath = self.get_file_path()
        self.path_u_entry.insert(0, filepath.replace('/', '\\'))
    
    def handle_get_material_path_caldeiras(self):
        if self.path_c_entry.get() != '':
            self.path_c_entry.delete(0, tk.END)
        filepath = self.get_file_path()
        self.path_c_entry.insert(0, filepath.replace('/', '\\'))
    
    def handle_get_project_path_utility(self):
        if self.path_u_project_entry.get() != '':
            self.path_u_project_entry.delete(0, tk.END)
        filepath = self.get_file_path()
        self.path_u_project_entry.insert(0, filepath.replace('/', '\\'))
    
    def handle_get_project_path_caldeiras(self):
        if self.path_c_project_entry.get() != '':
            self.path_c_project_entry.delete(0, tk.END)
        filepath = self.get_file_path()
        self.path_c_project_entry.insert(0, filepath.replace('/', '\\'))
    
    def get_path(self):
        folder_path = filedialog.askdirectory(title='Selecione um pasta')
        if folder_path:
            return folder_path

    def get_file_path(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo")
        if file_path:
            return file_path
    def read_config_file(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
        except Exception as e:
            mb.showerror('Error', f'Erro ao tentar carregar arquivos de configuração [{e}]')