from decouple import config
from user import UserManager
from menu import display_menu

def main():
    db_config = {
        'dbname': config('DB_NAME'),
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'port': config('DB_PORT')
    }

    user_manager = UserManager(db_config)

    print("=== Bem-vindo ao Sistema Acadêmico ===")
    
    while True:
        print("\n1. Cadastrar Usuário")
        print("2. Login")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            user_manager.register_user()
        elif choice == '2':
            user, user_type = user_manager.login()
            if user:
                display_menu(user_manager, user, user_type)
            else:
                print("Login falhou. Tente novamente.")
        elif choice == '3':
            print("Saindo do sistema.")
            user_manager.close_connection()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
