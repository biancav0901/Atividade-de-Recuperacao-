import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Função para criar a tabela se ela não existir
def criar_tabela():
    conn = sqlite3.connect('empresa_turismo.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS empresa (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cnpj TEXT NOT NULL UNIQUE,
                        email TEXT,
                        telefone TEXT)''')
    conn.commit()
    conn.close()

# Função para inserir nova empresa
def inserir_empresa():
    nome = entry_nome.get()
    cnpj = entry_cnpj.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    if nome and cnpj:
        conn = sqlite3.connect('empresa_turismo.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO empresa (nome, cnpj, email, telefone) VALUES (?, ?, ?, ?)', (nome, cnpj, email, telefone))
            conn.commit()
            messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")
            limpar_campos()
            listar_empresas()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", f"CNPJ {cnpj} já cadastrado.")
        conn.close()
    else:
        messagebox.showerror("Erro", "Nome e CNPJ são obrigatórios.")

# Função para alterar empresa
def alterar_empresa():
    id_empresa = entry_id.get()
    nome = entry_nome.get()
    cnpj = entry_cnpj.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    if id_empresa:
        conn = sqlite3.connect('empresa_turismo.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE empresa SET nome = ?, cnpj = ?, email = ?, telefone = ? WHERE id = ?', (nome, cnpj, email, telefone, id_empresa))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Empresa alterada com sucesso!")
            limpar_campos()
            listar_empresas()
        else:
            messagebox.showerror("Erro", f"Empresa com ID {id_empresa} não encontrada.")
        conn.close()
    else:
        messagebox.showerror("Erro", "ID da empresa é obrigatório para alteração.")

# Função para excluir empresa
def excluir_empresa():
    id_empresa = entry_id.get()

    if id_empresa:
        conn = sqlite3.connect('empresa_turismo.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM empresa WHERE id = ?', (id_empresa,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Empresa excluída com sucesso!")
            limpar_campos()
            listar_empresas()
        else:
            messagebox.showerror("Erro", f"Empresa com ID {id_empresa} não encontrada.")
        conn.close()
    else:
        messagebox.showerror("Erro", "ID da empresa é obrigatório para exclusão.")

# Função para listar empresas
def listar_empresas():
    conn = sqlite3.connect('empresa_turismo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM empresa')
    empresas = cursor.fetchall()
    conn.close()

    # Limpa a Treeview antes de inserir novos dados
    treeview.delete(*treeview.get_children())

    # Insere os dados no Treeview
    for empresa in empresas:
        treeview.insert('', 'end', values=(empresa[0], empresa[1], empresa[2], empresa[3], empresa[4]))

# Função para limpar os campos
def limpar_campos():
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_cnpj.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

# Criação da interface gráfica
root = tk.Tk()
root.title("Cadastro de Empresa de Turismo")

# Criar os widgets
label_id = tk.Label(root, text="ID:")
label_id.grid(row=0, column=0)

entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=1, column=0)

entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1)

label_cnpj = tk.Label(root, text="CNPJ:")
label_cnpj.grid(row=2, column=0)

entry_cnpj = tk.Entry(root)
entry_cnpj.grid(row=2, column=1)

label_email = tk.Label(root, text="E-mail:")
label_email.grid(row=3, column=0)

entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1)

label_telefone = tk.Label(root, text="Telefone:")
label_telefone.grid(row=4, column=0)

entry_telefone = tk.Entry(root)
entry_telefone.grid(row=4, column=1)

# Botões de ação
btn_inserir = tk.Button(root, text="Inserir", command=inserir_empresa)
btn_inserir.grid(row=5, column=0)

btn_alterar = tk.Button(root, text="Alterar", command=alterar_empresa)
btn_alterar.grid(row=5, column=1)

btn_excluir = tk.Button(root, text="Excluir", command=excluir_empresa)
btn_excluir.grid(row=5, column=2)

btn_limpar = tk.Button(root, text="Limpar Campos", command=limpar_campos)
btn_limpar.grid(row=5, column=3)

# Treeview para exibir as empresas cadastradas
treeview = ttk.Treeview(root, columns=("ID", "Nome", "CNPJ", "E-mail", "Telefone"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Nome", text="Nome")
treeview.heading("CNPJ", text="CNPJ")
treeview.heading("E-mail", text="E-mail")
treeview.heading("Telefone", text="Telefone")
treeview.grid(row=6, column=0, columnspan=4)

# Executar a função para criar a tabela e listar empresas ao iniciar
criar_tabela()
listar_empresas()

root.mainloop()
