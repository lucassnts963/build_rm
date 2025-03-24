import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk

from screens.main_screen_2 import MainApplication

def start():

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
