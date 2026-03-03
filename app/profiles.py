

import hashlib
import json
import os
from config import DATA_DIR

PROFILES_FILE = os.path.join(DATA_DIR, 'student_profiles.json')


def get_user_profile(user_id):

    with open(PROFILES_FILE, "r") as f:
        profiles = json.load(f)

    return profiles.get(user_id, None)

def format_data(name, senha, idade, nivel_conhecimento, estilo_aprendizado):

    profile_data = {
        "name": name,
        "idade": idade,
        "nivel de conhecimento": nivel_conhecimento,
        "estilo de aprendizagem": estilo_aprendizado,
        "senha": senha
    }

    with open(PROFILES_FILE, "w") as f:
        json.dump({name: profile_data}, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user_profile(user_id, profile_data):

    # check if student_profiles.json exists, if not create it
    try:
        with open(PROFILES_FILE, "r") as f:
            profiles = json.load(f)
    except FileNotFoundError:
        profiles = {}

    if user_id in profiles:
        raise ValueError("User ID already exists")

    profile_data["senha"] = hash_password(profile_data["senha"])
    profiles[user_id] = profile_data

    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

def delete_user_profile(user_id):

    with open(PROFILES_FILE, "r") as f:
        profiles = json.load(f)

    if user_id in profiles:
        del profiles[user_id]

    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)


"""
Formato do student_profiles.json

{
    "user_id_1": {
        "name": "John Doe",
        "idade": 25,
        "nivel de conhecimento": "intermediário",
        "estilo de aprendizagem": "visual",
        "senha": "hashed_password"}
}
b. Incluir: nome, idade, nível de conhecimento (iniciante/intermediário/avançado), estilo de
aprendizado (visual/auditivo/leitura-escrita/cinestésico)


"""


if __name__ == "__main__":
    # Exemplo de uso
    user_id = "user123"
    profile_data = {
        "name": "John Doe",
        "idade": 25,
        "nivel de conhecimento": "intermediário",
        "estilo de aprendizagem": "visual",
        "senha": "hashed_password"
    }

    register_user_profile(user_id, profile_data)
    print(get_user_profile(user_id))
    #delete_user_profile(user_id)