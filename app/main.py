import profiles as pf
import json
import time

def cs():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
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
        time.sleep(1)
        main()

def user_id():
    id = input("Digite um user ID: ")
    # check if user_id already exists
    with open("data/student_profiles.json", "r") as f:
        profiles = json.load(f)
    if id in profiles.keys():
        print(profiles.keys())
        print("User ID já existe. Tente novamente.")
        time.sleep(1)
        cs()
        return user_id()
    return id

def password():
    senha = input("Digite sua senha: ")
    repetir_senha = input("Repita sua senha: ")
    if senha != repetir_senha:
        print("As senhas não coincidem. Tente novamente.")
        time.sleep(1)
        cs()
        password()
        return
    return senha

def user_data():
    name = input("Digite seu nome: ")
    idade = input("Digite sua idade: ")
    nivel_conhecimento = input("Digite seu nível de conhecimento (iniciante/intermediario/avancado): ")
    estilo_aprendizagem = input("Digite seu estilo de aprendizagem (visual/auditivo/leitura-escrita/cinestesico): ")
    
    # formatar nivel de conhecimento, estilo de aprendizagem

    return {
        "name": name,
        "idade": idade,
        "nivel de conhecimento": nivel_conhecimento,
        "estilo de aprendizagem": estilo_aprendizagem
    }

def register_menu():
    cs()
    print("Registro de usuário")
    id = user_id()
    senha = password()

    profile_data = user_data()
    profile_data["senha"] = str(senha)
    
    # transforma em json
    


    try:        
        pf.register_user_profile(id, profile_data)
        print("Registro bem-sucedido!")
    except ValueError as e:
        print(str(e))
        time.sleep(1)
        register_menu()

def tentar_senha(user_id, profile):
    senha = input("Digite sua senha: ")
    # hash da senha
    senha_hashed = pf.hash_password(senha)
    if profile is None:
        print("Perfil não encontrado.")
        return False
    if profile["senha"] == senha_hashed:
        return True
    else:
        print("Senha incorreta. Tente novamente.")
        time.sleep(1)
        
        return tentar_senha(user_id, profile)

def login_menu():
    cs()
    # entra com o user_id, pega o perfil do usuário, e depois mostra as opções de geração de conteúdo
    user_id = input("Digite seu user ID: ")
    profile = pf.get_user_profile(user_id)
    if tentar_senha(user_id, profile):
        print("Login bem-sucedido!")
        time.sleep(1)
        cs()
        content_generation_menu(user_id)
    
    

def content_generation_menu(user_id):
    print("Menu de geração de conteúdo")
    print("1. Gerar explicação")
    print("2. Gerar exemplos")
    print("3. Gerar perguntas de reflexão")
    print("4. Gerar resumo visual")
    print("5. Sair")

def main():
    ## Menu
    cs()
    main_menu()


    # fazer login:


    
    
    


if __name__ == "__main__":
    main()
