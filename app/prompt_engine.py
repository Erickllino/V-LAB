
import json

from api_key import key
from profiles import get_user_profile

from openai import OpenAI
client = OpenAI()



"""

b. Usar técnicas de:
i. Persona prompting: "Você é um professor experiente em Pedagogia"
ii. Context setting: Incluir dados específicos do aluno no prompt
iii. Chain-of-thought: Solicitar "pense passo a passo" para explicações
iv. Output formatting: Especificar exatamente como deseja a resposta




"""



def save_response_as_json(response):
    response_data = {
        "titulo": response.get("titulo", ""),
        "explicacao": response.get("explicacao", ""),
        "pontos_chave": response.get("pontos_chave", []),
        "nivel_complexidade": response.get("nivel_complexidade", "")
    }

    with open("response.json", "w") as f:
        json.dump(response_data, f, indent=4)


def determine_prompt_version(user_id, question):

    """
    Talvez seja interessante incluir informaçoes do perfil para definir o tipo
    de prompt
    
    se for visual puxar uma função que gere imagens junto ao texto
    se for auditivo puxar uma função que gere um audio junto ao texto
    se for leitura-escrita puxar uma função que formate a resposta em texto
    se for cinestésico puxar uma função que gere um video ou animação junto ao texto
    
    """
    profile = get_user_profile(user_id)
    if profile['nivel de conhecimento'] == "iniciante":
        return "v1"
    elif profile['nivel de conhecimento'] == "intermediario":
        return "v2"
    elif profile['nivel de conhecimento'] == "avancado":
        return "v3"
    else:
        return "v0"



def generate_explanation(user_id, question):
    profile = get_user_profile(user_id)
    return f"Explicação detalhada para o aluno {profile['name']} sobre a pergunta: {question}"

def generate_examples(user_id, question):
    profile = get_user_profile(user_id)
    return f"Exemplos para o aluno {profile['name']} sobre a pergunta: {question}"

def generate_reflection_questions(user_id, question):
    profile = get_user_profile(user_id)
    return f"Perguntas de reflexão para o aluno {profile['name']} sobre a pergunta: {question}"

def generate_visual_summary(user_id, question):
    profile = get_user_profile(user_id)
    return f"Resumo visual para o aluno {profile['name']} sobre a pergunta: {question}"

def generate_prompt(user_id, question):

    profile = get_user_profile(user_id)

    prompt_version = determine_prompt_version(user_id, question)


    base_prompt = """
            Responda tudo no seguinte formato JSON;

            {
            "titulo": "",
            "explicacao": "",
            "pontos_chave": [],
            "nivel_complexidade": ""
            }
    """




    if prompt_version == "v1":
        prompt = f"""
    Você é um professor experiente em Pedagogia. 
    O aluno tem {profile['idade']} anos, nível de conhecimento {profile['nivel de conhecimento']} e estilo de aprendizagem {profile['estilo de aprendizagem']}.
    Responda a seguinte pergunta: {question}
    """
    #elif prompt_version == "v2":
    

    return base_prompt + prompt














if __name__ == "__main__":

    aluno = "user123"
    pergunta = "Explique o que é a Teoria da Aprendizagem de Piaget."



    prompt = generate_prompt(aluno, pergunta)


    response = client.responses.create(
        model="gpt-5.2",
        input=prompt,
        #api_key=key
    )

    print(response.output_text)