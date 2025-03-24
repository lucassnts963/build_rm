import tkinter as tk
import tkinter.ttk as ttk

import os

from screens.new_rm_screen import NewRMScreen
from screens.edit_rm_screen import EditRMScreen
from screens.settings_screen import SettingScreen
from screens.new_product_screen import NewProductScreen
from screens.new_transaction_screen import NewTransactionScreen

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


        # Frames for screen

        self.new_product_screen = NewProductScreen(self)

        self.setting_screen = SettingScreen(self)

        self.new_transaction_screen = NewTransactionScreen(self)

        self.pack(fill='both', expand=True)

    def create_menu(self, master):
        menubar = tk.Menu(self)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Novo Produto', command=self.show_new_product_screen)
        filemenu.add_command(label='Nova Movimentação', command=self.show_new_transaction_screen)
        
        editmenu = tk.Menu(menubar, tearoff=0)

        reportmenu = tk.Menu(menubar, tearoff=0)
        reportmenu.add_command(label='01 - Relatório saldo de estoque', command=self.handle_report_by_systems)

        menubar.add_cascade(label='Arquivo', menu=filemenu)
        menubar.add_cascade(label='Editar', menu=editmenu)
        menubar.add_cascade(label='Relatórios', menu=reportmenu)
        menubar.add_command(label='Configurações', command=self.show_setting_screen)
        master.config(menu=menubar)

    def show_new_product_screen(self):
        self.new_product_screen.grid(row=0, column=0, sticky='nsew')
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.new_transaction_screen.grid_forget()
    
    def show_new_transaction_screen(self):
        self.new_transaction_screen.grid(row=0, column=0, sticky='nsew')
        self.main_screen.grid_forget()
        self.setting_screen.grid_forget()
        self.new_product_screen.grid_forget()

    def show_setting_screen(self):
        self.setting_screen.grid(row=0, column=0, sticky='nsew')
        self.main_screen.grid_forget()
        self.new_product_screen.grid_forget()
        self.new_transaction_screen.grid_forget()
    
    def handle_report_by_systems(self):
        filepath = build_report_status_material_por_sistema()
        open_file(filepath)
    