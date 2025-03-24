import tkinter as tk
import tkinter.ttk as ttk

import os

from screens.new_rm_screen import NewRMScreen
from screens.edit_rm_screen import EditRMScreen
from screens.settings_screen import SettingScreen
from screens.new_product_screen import NewProductScreen

from database.rmdb import RMDB

from report.status import build_report_status_material_por_sistema
from utils import open_file, get_temp_folder
from utils.config import Settings

settings = Settings()

class MainApplication(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_menu(master)

        # Create a placeholder for the main screen
        self.main_screen = ttk.Frame(self) 
        self.main_screen.grid(row=0, column=0, sticky='nsew')

        image_path = os.path.join(os.getcwd(), 'main', 'images', 'logo.png')

        self.image = tk.PhotoImage(file=image_path)
        label = ttk.Label(self.main_screen, image=self.image, text='Bem vindo')
        label.place(relx=0.5, rely=0.5, anchor="center")

        db_caldeiras = RMDB(db_name=os.path.join(get_temp_folder(), settings.get_database_path()))
        db_utility = RMDB(db_name=os.path.join(get_temp_folder(project='UTILIDADES'), settings.get_database_path()))

        # Frames for screens
        self.edit_rm_screen = EditRMScreen(self, db=db_caldeiras)
        self.edit_rm_screen_utility = EditRMScreen(self, db=db_utility)

        self.new_rm_screen = NewRMScreen(self, db=db_caldeiras)
        self.new_rm_screen_utility = NewRMScreen(self, db=db_utility, project='UTILIDADES', contract='CT 4600011662 UTILIDADES')

        self.new_product_screen = NewProductScreen(self, db=db_utility)

        self.setting_screen = SettingScreen(self)

        self.pack(fill='both', expand=True)

    def create_menu(self, master):
        menubar = tk.Menu(self)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Nova requisição Caldeiras', command=self.show_new_rm_screen)
        filemenu.add_command(label='Nova requisição Utilidades', command=self.show_new_rm_utility_screen)
        filemenu.add_command(label='Novo Produto', command=self.show_new_rm_utility_screen)
        
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label='Editar requisição Caldeiras', command=self.show_edit_rm_screen)
        editmenu.add_command(label='Editar requisição Utilidades', command=self.show_edit_rm_screen_utility)

        reportmenu = tk.Menu(menubar, tearoff=0)
        reportmenu.add_command(label='01 - Relatório materiais por sistema', command=self.handle_report_by_systems)
        
        reportmenu_utility = tk.Menu(menubar, tearoff=0)
        reportmenu_utility.add_command(label='01 - Relatório materiais por sistema', command=self.handle_report_by_systems_utility)

        menubar.add_cascade(label='Arquivo', menu=filemenu)
        menubar.add_cascade(label='Editar', menu=editmenu)
        menubar.add_cascade(label='Relatórios Caldeiras', menu=reportmenu)
        menubar.add_cascade(label='Relatórios Utilidades', menu=reportmenu_utility)
        menubar.add_command(label='Configurações', command=self.show_setting_screen)
        master.config(menu=menubar)

    def show_new_rm_utility_screen(self):
        self.new_rm_screen_utility.grid(row=0, column=0, sticky='nsew')
        self.new_rm_screen.grid_forget()
        self.edit_rm_screen.grid_forget()
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.edit_rm_screen_utility.grid_forget()
        self.new_product_screen.grid_forget()

    def show_new_product_screen(self):
        self.new_product_screen.grid(row=0, column=0, sticky='nsew')
        self.edit_rm_screen.grid_forget()
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.edit_rm_screen_utility.grid_forget()
        self.new_rm_screen_utility.grid_forget()
        self.new_rm_screen.grid_forget()

    def show_new_rm_screen(self):
        self.new_rm_screen.grid(row=0, column=0, sticky='nsew')
        self.edit_rm_screen.grid_forget()
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.new_rm_screen_utility.grid_forget()
        self.edit_rm_screen_utility.grid_forget()
        self.new_product_screen.grid_forget()

    def show_edit_rm_screen(self):
        self.edit_rm_screen.grid(row=0, column=0, sticky='nsew')
        self.new_rm_screen.grid_forget()
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.new_rm_screen_utility.grid_forget()
        self.edit_rm_screen_utility.grid_forget()
        self.new_product_screen.grid_forget()

    def show_edit_rm_screen_utility(self):
        self.edit_rm_screen_utility.grid(row=0, column=0, sticky='nsew')
        self.new_rm_screen.grid_forget()
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.new_rm_screen_utility.grid_forget()
        self.edit_rm_screen.grid_forget()
        self.new_product_screen.grid_forget()

    def show_setting_screen(self):
        self.setting_screen.grid(row=0, column=0, sticky='nsew')
        self.new_rm_screen.grid_forget()
        self.edit_rm_screen.grid_forget()
        self.main_screen.grid_forget()
        self.new_rm_screen_utility.grid_forget()
        self.new_product_screen.grid_forget()
    
    def handle_report_by_systems(self):
        filepath = build_report_status_material_por_sistema()
        open_file(filepath)
    
    def handle_report_by_systems_utility(self):
        filepath = build_report_status_material_por_sistema(project='UTILIDADES')
        open_file(filepath)
    