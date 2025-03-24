import sqlite3, os

db_path = os.path.join('temp', 'estoque.db')

# Conexão com o banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criação da tabela de produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    diameter TEXT NOT NULL,
    length REAL,
    description TEXT,
    unity TEXT NOT NULL,
    aplication TEXT NOT NULL,
    weight REA,
    ni TEXT
)
""")

# Criação da tabela de movimentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    quantidade INTEGER NOT NULL,
    data_movimento TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
""")

conn.commit()


# Função para adicionar um novo produto
def add_new_product(code="", category="", diameter="", length=0, description="", unity="", aplication="", weight=0, ni=""):
    cursor.execute("""
                    INSERT INTO produtos (code, category, diameter, length, description, unity, aplication, weight, ni)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (code, category, diameter, length, description, unity, aplication, weight, ni))
    conn.commit()
    return f"Produto '{description}' adicionado com sucesso."

# Função para registrar um movimento de entrada ou saída
def add_stock_transaction(produto_id, quantidade):
    
    cursor.execute("INSERT INTO movimentos (produto_id, quantidade) VALUES (?, ?)",
                   (produto_id, quantidade))
    conn.commit()
    print(f"Movimento de {'saída' if quantidade < 0 else 'entrada' } de {quantidade} unidades registrado para o produto ID {produto_id}.")

def get_all_products():
    return []

# Função para calcular o saldo atual de cada produto
def calcular_saldo():
    cursor.execute("""
    SELECT p.id, p.nome, p.descricao, COALESCE(SUM(m.quantidade), 0) AS saldo
    FROM produtos p
    LEFT JOIN movimentos m ON p.id = m.produto_id
    GROUP BY p.id
    """)
    saldo = cursor.fetchall()
    for produto in saldo:
        print(f"ID: {produto[0]}, Nome: {produto[1]}, Saldo: {produto[3]}")
    return saldo
