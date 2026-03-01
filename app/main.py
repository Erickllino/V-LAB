import profiles as pf


def register_menu():
    pass

def login_menu():
    # entra com o user_id, pega o perfil do usuário, e depois mostra as opções de geração de conteúdo
    user_id = input("Digite seu user ID: ")
    profile = pf.get_profile(user_id)
    if profile is None:
        print("Perfil não encontrado.")
        return
    print(f"Perfil do usuário: {profile}")
    print("1. Gerar explicação")
    print("2. Gerar exemplos")
    print("3. Gerar perguntas de reflexão")
    print("4. Gerar resumo visual")
    print("5. Sair")



def main():
    ## Menu
    print("Bem-vindo ao V-Lab!")
    print("1. Registrar")
    print("2. Login")
    print("3. Sair")

    a = input("Escolha uma opção: ")
    if a == "1":
        register_menu()
    elif a == "2":
        login_menu()
    elif a == "3":
        print("Até mais!")
        exit()
    else:
        print("Opção inválida. Tente novamente.")
        main()
    # fazer login:
    print("1. Gerar explicação")
    print("2. Gerar exemplos")
    print("3. Gerar perguntas de reflexão")
    print("4. Gerar resumo visual")
    print("5. Sair")

    
    
    


if __name__ == "__main__":
    main()
