import sqlite3
from senha import Senha

class Database:
    def __init__(self, db_name='senhas.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS senhas (
                                id INTEGER PRIMARY KEY,
                                servico TEXT NOT NULL,
                                email TEXT NOT NULL,
                                senha TEXT NOT NULL
                              )''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_senha(self, servico, email, senha):
        senha_criptografada = senha.criptografar_senha(senha)
        self.cursor.execute('INSERT INTO senhas (servico, email, senha) VALUES (?, ?, ?)', (servico, email, senha_criptografada))
        self.conn.commit()

    def fetch_all_senhas(self):
        self.cursor.execute('SELECT * FROM senhas')
        return self.cursor.fetchall()

    def fetch_senha_by_id(self, senha_id):
        self.cursor.execute('SELECT * FROM senhas WHERE id = ?', (senha_id,))
        return self.cursor.fetchone()

    def delete_senha(self, senha_id):
        self.cursor.execute('DELETE FROM senhas WHERE id = ?', (senha_id,))
        self.conn.commit()

    def update_senha(self, senha_id, servico, email, senha):
        senha_criptografada = Senha.criptografar_senha(senha)
        self.cursor.execute('UPDATE senhas SET servico=?, email=?, senha=? WHERE id=?', (servico, email, senha_criptografada, senha_id))
        self.conn.commit()

    def descriptografar_senha(self, senha_id):
        senha_criptografada = self.fetch_senha_by_id(senha_id)[3]  # índice 3 é a coluna da senha criptografada
        return Senha.descriptografar_senha(senha_criptografada)


