import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

from database.stockdb import add_stock_transaction, get_all_products  # Funções que você precisa definir

class NewTransactionScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Frame de campos
        fields_frame = ttk.Frame(self)
        fields_frame.columnconfigure(0, weight=20)
        fields_frame.columnconfigure(1, weight=80)
        fields_frame.pack(fill='both', expand=True, pady=5)

        # Produto
        ttk.Label(fields_frame, text='Produto:', anchor='e').grid(row=0, column=0, sticky='nsew')
        self.product_options = [f"{prod[1]} - {prod[0]}" for prod in get_all_products()]
        self.combo_product = ttk.Combobox(fields_frame, values=self.product_options, width=65)
        self.combo_product.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        # Tipo de Movimento
        ttk.Label(fields_frame, text='Tipo de Movimento:', anchor='e').grid(row=1, column=0, sticky='nsew')
        self.movement_type = tk.StringVar(value="Entrada")
        ttk.Radiobutton(fields_frame, text='Entrada', variable=self.movement_type, value="entrada").grid(row=1, column=1, sticky='w')
        ttk.Radiobutton(fields_frame, text='Saída', variable=self.movement_type, value="saída").grid(row=1, column=1, padx=80, sticky='w')

        # Quantidade
        ttk.Label(fields_frame, text='Quantidade:', anchor='e').grid(row=2, column=0, sticky='nsew')
        self.quantity_entry = ttk.Entry(fields_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        # Botões de Ações
        actions_frame = ttk.Frame(self)
        actions_frame.columnconfigure(0, weight=90)
        actions_frame.columnconfigure(1, weight=5)
        actions_frame.columnconfigure(2, weight=5)
        actions_frame.pack(fill='both', expand=True, pady=5, padx=5)

        # Botão Salvar
        ttk.Button(actions_frame, text='Salvar', command=self.handle_save).grid(row=0, column=0, sticky='nsew')

    def handle_save(self):
        # Obter dados dos campos
        produto_selecionado = self.combo_product.get().split(' - ')[0]
        tipo_movimento = self.movement_type.get()
        quantidade = self.quantity_entry.get()

        if not produto_selecionado or not quantidade:
            mb.showwarning("Aviso", "Todos os campos devem estar preenchidos.")
            return

        try:
            quantidade = float(quantidade)
            if tipo_movimento == "Saída":
                quantidade *= -1  # Se for saída, transformar quantidade em valor negativo

            # Realizar movimento no banco de dados
            message = add_stock_transaction(produto_id=produto_selecionado, quantidade=quantidade)
            mb.showinfo("Sucesso!", message)
            self.clear_fields()
        except ValueError:
            mb.showerror("Erro", "Quantidade inválida. Informe um número.")
        except Exception as e:
            mb.showerror("Erro", str(e))

    def clear_fields(self):
        # Limpar campos após o salvamento
        self.combo_product.set("")
        self.movement_type.set("Entrada")
        self.quantity_entry.delete(0, 'end')
