from decouple import config
import psycopg2
from hashlib import sha256

class UserManager:
    def __init__(self, db_config):
        try:
            self.connection = psycopg2.connect(**db_config)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def hash_password(password):
        return sha256(password.encode()).hexdigest()

    def register_user(self, username, password, user_type):
        try:
            hashed_password = self.hash_password(password)
            query = """INSERT INTO ps.users (username, password, user_type) 
                        VALUES (%s, %s, %s)"""
            self.cursor.execute(query, (username, hashed_password, user_type))
            self.connection.commit()
            print(f"Usuário {user_type} cadastrado com sucesso.")
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar usuário: {e}")

    def login(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            query = """SELECT user_type FROM ps.users 
                        WHERE username = %s AND password = %s"""
            self.cursor.execute(query, (username, hashed_password))
            result = self.cursor.fetchone()
            if result:
                print(f"Login realizado com sucesso como {result[0]}.")
                return username, result[0]
            else:
                print("Nome de usuário ou senha incorretos.")
                return None, None
        except psycopg2.Error as e:
            print(f"Erro ao realizar login: {e}")
            return None, None

    def delete_user(self, username):
        try:
            query = "DELETE FROM ps.users WHERE username = %s"
            self.cursor.execute(query, (username,))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("Usuário excluído com sucesso.")
            else:
                print("Usuário não encontrado.")
        except psycopg2.Error as e:
            print(f"Erro ao excluir usuário: {e}")

    def display_users(self):
        try:
            self.cursor.execute("SELECT username, user_type FROM ps.users")
            users = self.cursor.fetchall()
            if not users:
                print("Nenhum usuário cadastrado.")
            else:
                print("=== Usuários Cadastrados ===")
                for username, user_type in users:
                    print(f"Usuário: {username} - Tipo: {user_type}")
        except psycopg2.Error as e:
            print(f"Erro ao exibir usuários: {e}")

    def insert_nota(self, user_id, curso_id, nota):
        try:
            query = """INSERT INTO ps.notas (id_user, id_cursos, nota) 
                        VALUES (%s, %s, %s)"""
            self.cursor.execute(query, (user_id, curso_id, nota))
            self.connection.commit()
            print("Nota inserida com sucesso.")
        except psycopg2.Error as e:
            print(f"Erro ao inserir nota: {e}")

    def insert_falta(self, user_id, curso_id, date):
        try:
            query = """INSERT INTO ps.faltas (id_user, id_cursos, date) 
                        VALUES (%s, %s, %s)"""
            self.cursor.execute(query, (user_id, curso_id, date))
            self.connection.commit()
            print("Falta inserida com sucesso.")
        except psycopg2.Error as e:
            print(f"Erro ao inserir falta: {e}")

    def display_notas(self, user_id):
        try:
            query = """SELECT c.name, n.nota FROM ps.notas n
                        JOIN ps.cursos c ON n.id_cursos = c.id_cursos 
                        WHERE n.id_user = %s"""
            self.cursor.execute(query, (user_id,))
            notas = self.cursor.fetchall()
            if not notas:
                print("Nenhuma nota encontrada para este aluno.")
            else:
                print("\nNotas do aluno:")
                for curso, nota in notas:
                    print(f"Curso: {curso}, Nota: {nota}")
        except psycopg2.Error as e:
            print(f"Erro ao exibir notas: {e}")

    def display_faltas(self, user_id):
        try:
            query = """SELECT c.name, f.date FROM ps.faltas f
                        JOIN ps.cursos c ON f.id_cursos = c.id_cursos 
                        WHERE f.id_user = %s"""
            self.cursor.execute(query, (user_id,))
            faltas = self.cursor.fetchall()
            if not faltas:
                print("Nenhuma falta encontrada para este aluno.")
            else:
                print("\nFaltas do aluno:")
                for curso, date in faltas:
                    print(f"Curso: {curso}, Data: {date}")
        except psycopg2.Error as e:
            print(f"Erro ao exibir faltas: {e}")

    def cadastrar_curso(self, curso_name):
        try:
            query = "INSERT INTO ps.cursos (name) VALUES (%s)"
            self.cursor.execute(query, (curso_name,))
            self.connection.commit()
            print("Curso cadastrado com sucesso.")
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar curso: {e}")

    def exibir_cursos(self):
        try:
            self.cursor.execute("SELECT id_cursos, name FROM ps.cursos")
            cursos = self.cursor.fetchall()
            print("\nCursos disponíveis:")
            if not cursos:
                print("Nenhum curso encontrado.")
            else:
                for curso_id, curso_name in cursos:
                    print(f"ID: {curso_id}, Nome: {curso_name}")
        except psycopg2.Error as e:
            print(f"Erro ao exibir cursos: {e}")

if __name__ == "__main__":
    db_config = {
        'dbname': config('DB_NAME'),
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'port': config('DB_PORT')
    }

    try:
        user_manager = UserManager(db_config)

        # Exemplo: Registrar um usuário
        user_manager.register_user("admin", "senha123", "administrador")

        # Exemplo: Exibir usuários cadastrados
        user_manager.display_users()

        # Exemplo: Fechar conexão
        user_manager.close_connection()

    except Exception as e:
        print(f"Erro no sistema: {e}")

def selecionar_usertype():
    print("Selecione o tipo de usuário:")
    print("1 - Admin")
    print("2 - Prof")
    print("3 - aluno")

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

def display_menu(user_manager, user, user_type):
    if user_type == 'administrador':
        admin_menu(user_manager)
    elif user_type == 'professor':
        professor_menu(user_manager)
    elif user_type == 'aluno':
        student_menu(user_manager)
    else:
        print("Tipo de usuário inválido.")

def admin_menu(user_manager):
    while True:
        print("\n=== Menu do Administrador ===")
        print("1. Adicionar Usuário")
        print("2. Excluir Usuário")
        print("3. Exibir Usuários")
        print("4. Cadastrar Curso")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            username = input("Digite o nome de usuário: ")
            password = input("Digite a senha: ")
            user_type = input("Digite o tipo de usuário (administrador/professor/aluno): ")
            user_manager.register_user(username, password, user_type)
        elif opcao == '2':
            username = input("Digite o nome de usuário a ser excluído: ")
            user_manager.delete_user(username)
        elif opcao == '3':
            user_manager.display_users()
        elif opcao == '4':
            curso_name = input("Digite o nome do curso: ")
            user_manager.cadastrar_curso(curso_name)
        elif opcao == '5':
            print("Saindo do menu do administrador.")
            break
        else:
            print("Opção inválida. Tente novamente.")


def professor_menu(user_manager):
    while True:
        print("\n=== Menu do Professor ===")
        print("1. Inserir Nota")
        print("2. Inserir Falta")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            user_id = input("Digite o ID do aluno: ")
            curso_id = input("Digite o ID do curso: ")
            nota = input("Digite a nota: ")
            user_manager.insert_nota(user_id, curso_id, nota)
        elif opcao == '2':
            user_id = input("Digite o ID do aluno: ")
            curso_id = input("Digite o ID do curso: ")
            falta = input("Digite a falta")
            user_manager.insert_faltas(user_id, curso_id, falta)
        elif opcao == '3':
            print("Saindo do menu.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def student_menu(user_manager):
    while True:
        print("\n=== Menu do Aluno ===")
        print("1. Exibir Notas")
        print("2. Exibir Carga Horária")
        print("3. Exibir Faltas")
        print("4. Sair do Menu")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            user_id = input("Informe seu ID: ")
            user_manager.display_notas(user_id)
        elif choice == '2':
            print("Exibição de carga horária ainda não implementada.")
        elif choice == '3':
            user_id = input("Informe seu ID: ")
            user_manager.display_faltas(user_id)
        elif choice == '4':
            print("Saindo do menu.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def exibir_cursos(user_manager):
    user_manager.cursos.execute("SELECT * FROM courses")
    cursos = user_manager.cursos.fetchall()
    print("\nCursos disponíveis:")
    if not cursos:
        print("Nenhum curso encontrado.")
    else:
        for i, curso in enumerate(cursos, 1):
            print(f"{i}. {curso[1]}")

if __name__ == "__main__":
    user_manager = UserManager()
    admin_menu(user_manager)
    user_manager.close()