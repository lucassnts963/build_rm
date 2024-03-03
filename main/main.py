import tkinter as tk
import tkinter.messagebox as mg

import utils

from screens.main_screen import MainApplication

def initialize():
    utils.copy_and_rename_file(utils.get_data_path(), utils.get_temp_folder(), 'data.xlsx')
    utils.copy_and_rename_file(utils.get_project_path(), utils.get_temp_folder(), 'projetos.xlsx')


def start():
    width = 700
    height = 400

    try:
        initialize()
    except Exception as e:
        mg.showerror('Error', f'Error ao carregar o arquivos de dados {e}')
        return

    root = tk.Tk()
    root.title('Requisição')
    root.geometry(f'{width}x{height}')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = MainApplication(root)
    root.mainloop()

start()
