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
def inserir_empresa(nome, cnpj, email, telefone):
    conn = sqlite3.connect('empresa_turismo.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO empresa (nome, cnpj, email, telefone) VALUES (?, ?, ?, ?)',
                       (nome, cnpj, email, telefone))
        conn.commit()
        print(f'Empresa "{nome}" cadastrada com sucesso!')
    except sqlite3.IntegrityError:
        print(f'Erro: CNPJ "{cnpj}" já cadastrado.')
    conn.close()


# Função para alterar dados da empresa
def alterar_empresa(id_empresa, nome, cnpj, email, telefone):
    conn = sqlite3.connect('empresa_turismo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE empresa SET nome = ?, cnpj = ?, email = ?, telefone = ? WHERE id = ?',
                   (nome, cnpj, email, telefone, id_empresa))
    conn.commit()
    if cursor.rowcount > 0:
        print(f'Empresa de ID {id_empresa} alterada com sucesso!')
    else:
        print(f'Empresa com ID {id_empresa} não encontrada.')
    conn.close()


# Função para excluir uma empresa
def excluir_empresa(id_empresa):
    conn = sqlite3.connect('empresa_turismo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM empresa WHERE id = ?', (id_empresa,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f'Empresa de ID {id_empresa} excluída com sucesso!')
    else:
        print(f'Empresa com ID {id_empresa} não encontrada.')
    conn.close()


# Função para listar todas as empresas
def listar_empresas():
    conn = sqlite3.connect('empresa_turismo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM empresa')
    empresas = cursor.fetchall()
    conn.close()
    if empresas:
        for empresa in empresas:
            print(
                f'ID: {empresa[0]} | Nome: {empresa[1]} | CNPJ: {empresa[2]} | E-mail: {empresa[3]} | Telefone: {empresa[4]}')
    else:
        print('Nenhuma empresa cadastrada.')


# Exemplo de uso
if __name__ == '__main__':
    criar_tabela()

    while True:
        print("\n1. Inserir nova empresa")
        print("2. Alterar dados da empresa")
        print("3. Excluir empresa")
        print("4. Listar todas as empresas")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome da empresa: ")
            cnpj = input("CNPJ: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")
            inserir_empresa(nome, cnpj, email, telefone)

        elif opcao == '2':
            id_empresa = input("ID da empresa a ser alterada: ")
            nome = input("Novo nome da empresa: ")
            cnpj = input("Novo CNPJ: ")
            email = input("Novo e-mail: ")
            telefone = input("Novo telefone: ")
            alterar_empresa(id_empresa, nome, cnpj, email, telefone)

        elif opcao == '3':
            id_empresa = input("ID da empresa a ser excluída: ")
            excluir_empresa(id_empresa)

        elif opcao == '4':
            listar_empresas()

        elif opcao == '5':
            break

        else:
            print("Opção inválida, tente novamente.")
