import psycopg2
import bcrypt
from decouple import config

class UserManager:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password, hashed_password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError:
            print("O hash armazenado não é válido.")
            return False

    def register_user(self):
        username = input("Digite o nome de usuário: ")
        self.cursor.execute("SELECT username FROM ps.users WHERE username = %s", (username,))
        if self.cursor.fetchone():
            print("Usuário já existe.")
            return

        password = input("Digite a senha: ")
        hashed_password = self.hash_password(password)

        user_type = selecionar_usertype()
        if user_type not in ['administrador', 'professor', 'aluno']:
            print("Tipo de usuário inválido.")
            return

        query = "INSERT INTO ps.users (username, password, user_type) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, hashed_password, user_type))
        self.connection.commit()
        print(f"Usuário {user_type} cadastrado com sucesso.")

    def login(self):
        username = input("Digite seu nome de usuário: ")
        password = input("Digite sua senha: ")

        query = "SELECT password, user_type FROM ps.users WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()

        if result:
            hashed_password, user_type = result
            if self.check_password(password, hashed_password):
                print(f"Login realizado com sucesso como {user_type}.")
                return username, user_type
            else:
                print("Senha incorreta.")
                return None, None
        else:
            print("Usuário não encontrado.")
            return None, None

    def delete_user(self):
        username = input("Digite o nome de usuário que deseja excluir: ")
        self.cursor.execute("DELETE FROM ps.users WHERE username = %s", (username,))
        self.connection.commit()
        print("Usuário excluído com sucesso.")

    def display_users(self):
        self.cursor.execute("SELECT username, user_type FROM ps.users")
        users = self.cursor.fetchall()

        if not users:
            print("Nenhum usuário cadastrado.")
            return

        print("=== Usuários Cadastrados ===")
        for username, user_type in users:
            print(f"Usuário: {username} - Tipo: {user_type}")

def selecionar_usertype():
    print("Selecione o tipo de usuário:")
    print("1 - Administrador")
    print("2 - Professor")
    print("3 - Aluno")

    while True:
        opcao = input("Digite o número correspondente ao tipo de usuário: ")
        if opcao == '1':
            return 'administrador'
        elif opcao == '2':
            return 'professor'
        elif opcao == '3':
            return 'aluno'
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
