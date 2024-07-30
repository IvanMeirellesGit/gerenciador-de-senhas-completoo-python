import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database
from senha import Senha

class App:
    def __init__(self, root):
        self.db = Database()  # Inicializa o banco de dados
        self.root = root
        self.root.title("Gerenciador de Senhas")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Gerenciador de Senhas", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.generate_button = tk.Button(self.root, text="Gerar Senha", command=self.generate_password)
        self.generate_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Guardar Senha", command=self.save_password)
        self.save_button.pack(pady=5)

        self.show_button = tk.Button(self.root, text="Exibir Senhas", command=self.show_passwords)
        self.show_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Sair", command=self.root.quit)
        self.exit_button.pack(pady=5)

    def generate_password(self):
        tamanho = simpledialog.askinteger("Tamanho da Senha", "Digite o tamanho da senha:")
        if tamanho:
            senha = Senha.gerar_senha(tamanho)
            messagebox.showinfo("Senha Gerada", f"Senha: {senha}")

    def save_password(self):
        self.save_window = tk.Toplevel(self.root)
        self.save_window.title("Guardar Senha")

        self.option_label = tk.Label(self.save_window, text="Escolha uma opção:")
        self.option_label.pack(pady=5)

        self.auto_button = tk.Button(self.save_window, text="Gerar e Guardar Automaticamente", command=self.auto_save)
        self.auto_button.pack(pady=5)

        self.manual_button = tk.Button(self.save_window, text="Inserir Manualmente", command=self.manual_save)
        self.manual_button.pack(pady=5)

    def auto_save(self):
        self.save_window.destroy()

        servico = simpledialog.askstring("Serviço", "Digite o serviço:")
        email = simpledialog.askstring("Email", "Digite o email:")
        tamanho = simpledialog.askinteger("Tamanho da Senha", "Digite o tamanho da senha:")
        if servico and email and tamanho:
            senha = Senha.gerar_senha(tamanho)
            self.db.insert_senha(servico, email, senha)
            messagebox.showinfo("Sucesso", "Senha salva com sucesso!")

    def manual_save(self):
        self.save_window.destroy()

        servico = simpledialog.askstring("Serviço", "Digite o serviço:")
        email = simpledialog.askstring("Email", "Digite o email:")
        senha = simpledialog.askstring("Senha", "Digite a senha:")
        if servico and email and senha:
            self.db.insert_senha(servico, email, senha)
            messagebox.showinfo("Sucesso", "Senha salva com sucesso!")

    def show_passwords(self):
        senhas = self.db.fetch_all_senhas()
        if not senhas:
            messagebox.showinfo("Senhas", "Nenhuma senha encontrada.")
        else:
            self.show_window = tk.Toplevel(self.root)
            self.show_window.title("Senhas Armazenadas")

            self.senhas_label = tk.Label(self.show_window, text="Senhas Armazenadas", font=("Helvetica", 14))
            self.senhas_label.pack(pady=10)

            self.senhas_listbox = tk.Listbox(self.show_window, width=80, height=10)
            self.senhas_listbox.pack(padx=10, pady=5)

            for senha in senhas:
                self.senhas_listbox.insert(tk.END, f"ID: {senha[0]} - Serviço: {senha[1]} - Email: {senha[2]}")

            self.view_button = tk.Button(self.show_window, text="Ver Senha", command=self.view_password)
            self.view_button.pack(pady=5)

            self.edit_button = tk.Button(self.show_window, text="Editar Senha", command=self.edit_password)
            self.edit_button.pack(pady=5)

            self.delete_button = tk.Button(self.show_window, text="Deletar Senha", command=self.delete_password)
            self.delete_button.pack(pady=5)

    def view_password(self):
        selected_index = self.senhas_listbox.curselection()
        if selected_index:
            senha_id = int(self.senhas_listbox.get(selected_index).split()[1])
            senha_criptografada = self.db.descriptografar_senha(senha_id)
            messagebox.showinfo("Senha Descriptografada", f"Senha: {senha_criptografada}")

    def edit_password(self):
        selected_index = self.senhas_listbox.curselection()
        if selected_index:
            senha_id = int(self.senhas_listbox.get(selected_index).split()[1])
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Editar Senha")

            self.edit_label = tk.Label(self.edit_window, text="Editar Senha", font=("Helvetica", 14))
            self.edit_label.pack(pady=10)

            self.servico_label = tk.Label(self.edit_window, text="Serviço:")
            self.servico_label.pack(pady=5)
            self.servico_entry = tk.Entry(self.edit_window)
            self.servico_entry.pack(pady=5)

            self.email_label = tk.Label(self.edit_window, text="Email:")
            self.email_label.pack(pady=5)
            self.email_entry = tk.Entry(self.edit_window)
            self.email_entry.pack(pady=5)

            self.senha_label = tk.Label(self.edit_window, text="Senha:")
            self.senha_label.pack(pady=5)
            self.senha_entry = tk.Entry(self.edit_window, show="*")
            self.senha_entry.pack(pady=5)

            self.load_password_data(senha_id)

            self.save_button = tk.Button(self.edit_window, text="Salvar", command=lambda: self.save_edited_password(senha_id))
            self.save_button.pack(pady=5)

    def load_password_data(self, senha_id):
        senha_data = self.db.fetch_senha_by_id(senha_id)
        if senha_data:
            self.servico_entry.insert(0, senha_data[1])
            self.email_entry.insert(0, senha_data[2])
            # A senha criptografada não deve ser carregada aqui
            # self.senha_entry.insert(0, senha_data[3])

    def save_edited_password(self, senha_id):
        servico = self.servico_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if servico and email and senha:
            self.db.update_senha(senha_id, servico, email, senha)
            messagebox.showinfo("Sucesso", "Senha editada com sucesso!")
            self.edit_window.destroy()
            self.show_passwords()

    def view_plain_password(self):
        selected_index = self.senhas_listbox.curselection()
        if selected_index:
            senha_id = int(self.senhas_listbox.get(selected_index).split()[1])
            senha_criptografada = self.db.fetch_senha_by_id(senha_id)[3]
            senha_descriptografada = Senha.descriptografar_senha(senha_criptografada)
            messagebox.showinfo("Senha Descriptografada", f"Senha Descriptografada: {senha_descriptografada}")
    def delete_password(self):
        selected_index = self.senhas_listbox.curselection()
        if selected_index:
            senha_id = int(self.senhas_listbox.get(selected_index).split()[1])
            self.db.delete_senha(senha_id)
            messagebox.showinfo("Sucesso", "Senha deletada com sucesso!")
            self.show_passwords()

    def __del__(self):
        self.db.close()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()