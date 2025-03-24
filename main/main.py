import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk

import utils

from screens.main_screen import MainApplication

def start():

    try:
        utils.copy_files()
    except Exception as e:
        mb.showerror('Error', f'Error ao carregar o arquivos de dados [{e}]')
        return

    root = tk.Tk()

    style = ttk.Style(root)
    style.configure("TMenu", background='lightgray') 

    root.tk.call('source',  'main\\azure\\azure.tcl')
    root.tk.call('set_theme',  'dark')

    root.title('Requisição')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.geometry('800x600')

    app = MainApplication(root)
    root.mainloop()

start()
