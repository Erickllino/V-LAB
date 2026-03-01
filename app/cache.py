import json
import os
import hashlib

CACHE_FILE = "data/cache.json"

def hash_content(content):
    return hashlib.sha256(content.encode()).hexdigest()


def _generate_key(student_id, content, prompt_version):
    raw_string = f"{student_id}_{content}_{prompt_version}"
    # Função para de hash caso queira trocar o formato de hashing no futuro sem precisar mudar a lógica de geração de chave
    hash_string = hash_content(raw_string)
    return hash_string


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(cache_data):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=4)


def check_content_in_cache(student_id, content, prompt_version):
    # usa um modelo pequeno para checar se a resposta já existe no cache antes de chamar o modelo grande
    response = get_cached_response(student_id, content, prompt_version)
    # infere 
    return response is not None

def get_cached_response(student_id, content, prompt_version):
    cache = load_cache()
    #TODO: implementar a função de checagem de cache usando o modelo pequeno para gerar uma chave de hash e comparar com as chaves do cache, para evitar chamadas desnecessárias ao modelo grande
    #check_content_in_cache(student_id, content, prompt_version)
    key = _generate_key(student_id, content, prompt_version)
    return cache.get(key)


def set_cached_response(student_id, content, prompt_version, response):
    cache = load_cache()
    key = _generate_key(student_id, content, prompt_version)
    cache[key] = response
    save_cache(cache)


