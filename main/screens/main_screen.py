import tkinter as tk

from screens.new_rm_screen import NewRMScreen
from screens.edit_rm_screen import EditRMScreen

from database.rmdb import RMDB

from report.status import build_report_status_material_por_sistema
from utils import get_temp_folder, open_file

db = RMDB()

class MainApplication(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_menu(master)

        # Create a placeholder for the main screen
        self.main_screen = tk.Frame(self) 
        self.main_screen.grid(row=0, column=0, sticky='nsew')

        # Frames for screens
        self.edit_rm_screen = EditRMScreen(self, db=db)

        self.new_rm_screen = NewRMScreen(self, db=db)

        self.pack(fill='both', expand=True)

    def create_menu(self, master):
        menubar = tk.Menu(master)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Nova requisição', command=self.show_new_rm_screen)
        
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label='Editar requisição', command=self.show_edit_rm_screen)

        reportmenu = tk.Menu(menubar, tearoff=0)
        reportmenu.add_command(label='01 - Relatório materiais por sistema', command=self.handle_report_by_systems)

        menubar.add_cascade(label='Arquivo', menu=filemenu)
        menubar.add_cascade(label='Editar', menu=editmenu)
        menubar.add_cascade(label='Relatórios', menu=reportmenu)
        master.config(menu=menubar)

    def show_new_rm_screen(self):
        self.new_rm_screen.grid(row=0, column=0, sticky='nsew')
        self.edit_rm_screen.grid_forget()

    def show_edit_rm_screen(self):
        self.edit_rm_screen.grid(row=0, column=0, sticky='nsew')
        self.new_rm_screen.grid_forget()
    
    def handle_report_by_systems(self):
        filepath = build_report_status_material_por_sistema()
        open_file(filepath)
    