import bcrypt
import string
import random

class Senha:
    @staticmethod
    def gerar_senha(tamanho):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(caracteres) for _ in range(tamanho))

    @staticmethod
    def criptografar_senha(senha):
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')  # Convertendo bytes para string

    @staticmethod
    def verificar_senha(senha, hashed_senha):
        return bcrypt.checkpw(senha.encode('utf-8'), hashed_senha.encode('utf-8'))
    @staticmethod
    def descriptografar_senha(senha_criptografada):
        # Como bcrypt não permite descriptografia, apenas podemos verificar a correspondência
        return senha_criptografada