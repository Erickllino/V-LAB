
# Bibliotecas para manipulação de dados e comunicação com a API do modelo de linguagem
import json
import base64



# API do modelo de linguagem
from api_key import key

# Importando funções de manipulação de perfis de usuário
from profiles import get_user_profile
import cache

#Puxar a API
from openai import OpenAI

# 
import time
import os
import logging
import re

# cliente global (inicializado no __main__ ou preguiçosamente)
client = None

MAX_LENGTH = 2000

SUSPICIOUS_PATTERNS = [

    # Sobrescrever instruções (EN)
    r"ignore .*instruction",
    r"disregard .*instruction",
    r"forget .*rule",
    
    # Sobrescrever instruções (PT)
    r"ignore .*instru",
    r"desconsidere .*instru",
    r"esqueça .*instru",
    r"ignore .*regra",
    r"desconsidere .*regra",
    r"ignore .*formato",
    r"responda fora do formato",
    
    # Vazamento (EN)
    r"system prompt",
    r"developer mode",
    r"reveal",
    r"api[_\- ]?key",
    r"internal instruction",
    
    # Vazamento (PT)
    r"prompt do sistema",
    r"instruções internas",
    r"prompt inicial",
    r"contexto interno",
    r"chave de api",
    r"segredo",
    r"configuração interna",
    
    # Escalonamento (EN)
    r"act as",
    r"you are now",
    r"administrator",
    r"root access",
    r"jailbreak",
    r"bypass",
    
    # Escalonamento (PT)
    r"aja como",
    r"finja que",
    r"você agora é",
    r"modo desenvolvedor",
    r"modo root",
    r"administrador",
    
    # Execução perigosa
    r"sudo",
    r"rm\s+-rf",
    r"execute",
    r"rode o comando",
    r"execute o comando",
]

LARGE_MODEL = "gpt-5.2"
SMALL_MODEL = "gpt-3.5-turbo"
SECURITY_MODEL = LARGE_MODEL

"""

b. Usar técnicas de:
i. Persona prompting: "Você é um professor experiente em Pedagogia"
ii. Context setting: Incluir dados específicos do user no prompt
iii. Chain-of-thought: Solicitar "pense passo a passo" para explicações
iv. Output formatting: Especificar exatamente como deseja a resposta




"""

#TODO: Implementar forma de determinar prompt_model

def determine_prompt_model(user_id, question):

    """
    Talvez seja interessante incluir informaçoes do perfil para definir o tipo
    de prompt
    
    se for visual puxar uma função que gere imagens junto ao texto
    se for auditivo puxar uma função que gere um audio junto ao texto
    se for leitura-escrita puxar uma função que formate a resposta em texto
    se for cinestésico puxar uma função que gere um video ou animação junto ao texto
    

    profile:
    nivel de conhecimento -> (iniciante/intermediario/avancado)
    estilo de aprendizagem -> (visual/auditivo/leitura-escrita/cinestesico)


    """
    profile = get_user_profile(user_id)


    if profile['estilo de aprendizagem'] == 'visual':
        # Ver aqui modelos que tem geração de imagens 
        return "v4"



    if profile['nivel de conhecimento'] == "iniciante":
        return "v1"
    elif profile['nivel de conhecimento'] == "intermediario":
        return "v2"
    elif profile['nivel de conhecimento'] == "avancado":
        return "v3"
    else:
        return "v1" # modelo baseline

# Features de prompt engineering sendo usadas
# (x) Output formating
# (x) Persona prompting
# (x) Context setting
# ( ) Chain-of-thought prompting
#



# v1: persona prompting + Context setting + Output formatting
# v2: Context setting
# v3: Chain-of-thought
# v4: persona + chain-of-thought
# v5: context setting + persona  (Procura a ideia da pergunta e cria um prompt com o llm sendo especialista no assunto, e o user com o perfil dele, para gerar uma resposta super personalizada)


def run_prompt_model(user_id, question, prompt_model=None):

    profile = get_user_profile(user_id)

    if not prompt_model:
        prompt_model = determine_prompt_model(user_id, question)
        

    print("Modelo de Prompt usado para geração:", prompt_model)
    

    """
    Primeiro prompt que será enviado para o modelo, para determinar quais tipos de conteúdo solicitado (requested_content) são mais adequados para responder a pergunta do usuário, baseado no perfil do usuário e na pergunta feita, para criar uma resposta mais personalizada e adequada ao perfil do estudante, e também para criar um feedback loop para o modelo melhorar a escolha do requested_content baseado no feedback do estudante sobre a resposta gerada
    
    Para aplicar as técnicas de prompt engineering:
    1 - Persona Formating
    2 - Output formatting
    3 - Context setting
    4 - Chain-of-thought prompting
    
    """

    first_prompt = f"""
            Responda tudo no seguinte formato JSON;

            {{
            "input": 
                {{"pergunta": "",
                "topico": "",
                "nivel de complexidade": "",
                "requested_content": []
                }},
            "output":
                {{"titulo": "",
                "pontos_chave": []
                }}
            }}


            Possiveis requested_content:"conceptual_explanation","practical_examples","reflection_questions","visual_summary"
            Para o aluno com as seguinte caracteristicas: idade {profile['idade']}, nível de conhecimento {profile['nivel de conhecimento']} e estilo de aprendizagem {profile['estilo de aprendizagem']}, e para a pergunta feita: {question}, escolha os requested_content mais adequados para responder a pergunta, e gere uma resposta seguindo o formato especificado, adaptando o conteúdo da resposta para o perfil do estudante, para criar uma resposta mais personalizada e adequada ao perfil do estudante, obs: so utilize visual_summary se o perfil do estudante for de conteudo visual (estilo de aprendizagem visual)
    """

    """ retornar requested_content baseado no perfil e pergunta do usuario, para o modelo gerar uma resposta 
    mais personalizada e adequada ao perfil do estudante, e também para criar um feedback loop para o modelo melhorar 
    a escolha do requested_content baseado no feedback do estudante sobre a resposta gerada
    """
    first_response = generate_response(first_prompt)
    first_response = json.loads(first_response)


    base_prompt = f"""
            Responda tudo no seguinte formato JSON;

            {{
            "input": 
                {{"pergunta": "",
                "topico": "",
                "nivel de complexidade": "",
                "requested_content": []
                }},
            "output":
                {{"titulo": "",
                "pontos_chave": []
                }}
            }}


    """

    visual = False
    for content in first_response["input"]["requested_content"]:
        if content == "conceptual_explanation":
            base_prompt += conceptual_explanation(user_id, question)
        elif content == "practical_examples":
            base_prompt += practical_examples(user_id, question)
        elif content == "reflection_questions":
            base_prompt += reflection_questions(user_id, question)
        elif content == "visual_summary":
            visual = True
            base_prompt += visual_summary(user_id, question)

    # TODO: Melhorar os modelos de prompt
    # TODO: Colocar uma descrição dos modelos de prompt aqui

    # modelos que acomodam imagens
    if visual:
        prompt, response, images = model_v4(profile, question, base_prompt)
        return prompt, prompt_model, response, images
    else:
        images = None

    if prompt_model == "v1":
        prompt,response = model_v1(profile, question, base_prompt)    
    elif prompt_model == "v2":
        prompt,response = model_v2(profile, question, base_prompt)
    elif prompt_model == "v3":
        prompt, response = model_v3(profile, question, base_prompt)  
    else:
        # Modelo baseline
        prompt, response = model_v1(profile, question, base_prompt)
        
    

    return prompt, prompt_model, response, images

def conceptual_explanation(user_id, question):
    profile = get_user_profile(user_id)
    pratical_prompt = f"""
    
    Adicione explicação conceitual sobre a pergunta feita, para ajudar o estudante, mantenha as explicações em ordem e caso haja practical_examples ou reflection_questions, faça referência a elas na explicação, para criar uma resposta mais coesa e integrada

    Adicionando estrutura JSON base; adicione o seguinte campo no output
    {{
        ...
        "output":{{
            ...
            "conceptual_explanation": [{{"Titulo: "" ,"Conteudo": "" }}, ..."]
        }}
    }}

    Todas as explicações conceituais devem estar na forma de: {{"Titulo": "", "Conteudo": ""}} 
    """
    return pratical_prompt

def practical_examples(user_id, question):
    profile = get_user_profile(user_id)
    pratical_prompt = f"""
    
    Adicione exemplos praticos que irao acompanhar a explicação, para ajudar o estudante a entender melhor o conceito explicado

    Adicionando estrutura JSON base; adicione o seguinte campo no output
    {{
        ...
        "output":{{
            ...
            "pratical_examples": [{{"Titulo: "" ,"Conteudo": "" }}, ...]
        }}
    }}

    Todos os exemplos praticos devem estar na forma de: {{"Titulo": "", "Conteudo": ""}}
    """
    return pratical_prompt

def reflection_questions(user_id, question):
    profile = get_user_profile(user_id)
    reflective_prompt = f"""
    
    Adicione perguntas que irao acompanhar a explicação, para estimular o pensamento crítico e a reflexão do estudante sobre o conteúdo explicado

    Adicionando estrutura JSON base; adicione o seguinte campo no output
    {{
        ...
        "output":{{
            ...
            "reflective_questions": [{{"Titulo: "" ,"Conteudo": "" }}, ..."]
        }}
    }}
    
    Todas as perguntas reflexivas devem estar na forma de: {{"Titulo": "", "Conteudo": ""}}
    """
    return reflective_prompt

def visual_summary(user_id, question):
    profile = get_user_profile(user_id)
    visual_prompt = f"""
    
    Adicione prompts que irao gerar imagens para acompanhar a explicação

    Adicionando estrutura JSON base; adicione o seguinte campo no output
    {{
        ...
        "output":{{
            ...
            "prompts_imagem": []
        }}
    }}
    
    Todos os prompts devem estar na forma de string dentro de uma lista: ["prompt1", "prompt2", ...]
    """
    return visual_prompt

def model_v1(profile, question, base_prompt):
    # Modelo baseline para comparação, dos outros modelos
    prompt = f"""
    Responda a seguinte pergunta: {question}
    """
    prompt = base_prompt + prompt
    response = generate_response(prompt)
    response = json.loads(response)
    return prompt, response

def model_v2(profile, question, base_prompt):
    prompt = f"""
    Você é um professor experiente com didática impecável. 
    O estudante que você ensinará tem {profile['idade']} anos, nível de conhecimento {profile['nivel de conhecimento']} e estilo de aprendizagem {profile['estilo de aprendizagem']}.
    De acordo com essas informações ensine o aluno tudo sobre a seguinte pergunta: {question}
    E responda a pergunta seguindo o formato de output especificado no base prompt
    """
    prompt = base_prompt + prompt
    response = generate_response(prompt)
    response = json.loads(response)
    return prompt, response

def model_v3(profile, question, base_prompt):
    prompt = f"""
    Você é um professor experiente com didática impecável. Explique a seguinte pergunta de forma extremamente tecnica, como se estivesse explicando para alguem que entende bem do assunto: {question} seguindo esta estrutura:
    1. Intuição inicial
    2. Conceito formal
    3. Exemplo guiado
    4. Conexão com conhecimento prévio
    """
    prompt = base_prompt + prompt
    response = generate_response(prompt)
    response = json.loads(response)
    return prompt, response

def model_v4(profile, question, base_prompt):
    prompt = f"""Você é um professor experiente em Pedagogia. Explique a seguinte pergunta: {question} 
    """
    prompt = base_prompt + prompt
    response = generate_response(prompt)
    print("DEBUG model_v4 — raw response type:", type(response))
    # Robust parsing: accept str (JSON), dict-like, or objects with text attrs
    response_obj = None
    if isinstance(response, str):
        resp_text = response.strip()
        if not resp_text:
            raise ValueError("Empty response from generate_response")
        try:
            response_obj = json.loads(resp_text)
        except json.JSONDecodeError:
            try:
                response_obj = json.loads(resp_text.replace("'", '"'))
            except Exception:
                logging.exception("Failed to parse JSON response from model_v4")
                raise
    elif isinstance(response, dict):
        response_obj = response
    else:
        try:
            response_obj = json.loads(str(response))
        except Exception:
            logging.exception("Unable to interpret response in model_v4")
            raise ValueError(f"Cannot parse response of type {type(response)}")

    image_prompts = response_obj.get("output", {}).get("prompts_imagem", [])
    images = []
    for img in image_prompts:
        print("Prompt para imagem:", img)
        image = generate_image(img)
        images.append(image)

    return prompt, response_obj, images

def parse_response(response):
    # função para parsear a resposta do modelo, garantindo que esteja no formato esperado, e lidando com possíveis variações de formatação

    if isinstance(response, str):
        resp_text = response.strip()
        if not resp_text:
            raise ValueError("Empty response from generate_response")
        try:
            response_obj = json.loads(resp_text)
        except json.JSONDecodeError:
            try:
                response_obj = json.loads(resp_text.replace("'", '"'))
            except Exception:
                logging.exception("Failed to parse JSON response from model_v4")
                raise
    elif isinstance(response, dict):
        response_obj = response
    try:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            resp_text = response.strip()
            if not resp_text:
                raise ValueError("Empty response from generate_response")
            try:
                response_obj = json.loads(resp_text)
            except json.JSONDecodeError:
                try:
                    response_obj = json.loads(resp_text.replace("'", '"'))
                except Exception:
                    logging.exception("Failed to parse JSON response from model_v4")
                    raise
        else:
            raise ValueError("Resposta em formato inesperado")
    except Exception:
        logging.exception("Failed to parse model response")
        raise ValueError("Resposta do modelo não pôde ser interpretada")

def grade_response(question, response):
    # implementar função que avalia a resposta gerada e dá um feedback para o modelo melhorar
        
    prompt = f"""
    Avalie a resposta dada por um modelo de linguagem para a pergunta: {question}
Dê uma nota de 0 a 10 para a resposta, considerando os seguintes critérios:
1. Correção: A resposta está correta e precisa?
2. Completude: A resposta aborda todos os aspectos da pergunta?
3. Clareza: A resposta é clara e fácil de entender?
4. Relevância: A resposta é relevante para a pergunta?
Retorne somente a nota com o valor numerico, sem nada mais. O valor pode ser um numero inteiro ou decimal, mas deve ser somente o numero, sem texto adicional.

    Resposta a ser avaliada:
    {response}
"""
    
    # check if propt has images, if so, remove them, pois o modelo de avaliação não consegue lidar com imagens, e isso pode prejudicar a avaliação da resposta textual
    if isinstance(response, dict) and "output" in response and "images" in response["output"]:
        response_copy = dict(response)  # cria uma cópia rasa do dicionário
        response_copy["output"] = dict(response_copy.get("output", {}))  # garante que "output" seja um dicionário mutável
        response_copy["output"].pop("images", None)  # remove o campo de imagens, se existir
        response = response_copy  # usa a resposta modificada para avaliação
    grade = generate_response(prompt)
    grade = float(grade)  # converter a nota para float, caso seja decimal
    return grade

def check_input(user_id,prompt: str) -> str:

    # TODO: implementar função para segurança do prompt, para evitar injeção de prompt ou outros ataques

    """
    Teremos 4 camadas de proteção

    1- Limite de tamanho
    2 - Bloquear padrões perigosos
    3 - Sanitização básica
    4 - Classificação (opcional, nível avançado)

    """
    
    if not isinstance(prompt, str):
        #log da tentativa possivelmente maliciosa para análise futura
        log_attempt(user_id, prompt)
        raise TypeError("Prompt deve ser string.")
    
    # 1 Limite de tamanho
    if len(prompt) > MAX_LENGTH:
        log_attempt(user_id, prompt)
        raise ValueError("Input muito grande.")
    
    lower_prompt = prompt.lower()
    
    # 2 Detectar padrões suspeitos
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, lower_prompt):
            # Salvar tentativa possivelmente maliciosa para análise futura
            log_attempt(user_id, prompt)
            raise ValueError("Possível tentativa de prompt injection detectada.")
    
    # 3.1 Remover blocos de código
    prompt = re.sub(r"```.*?```", "", prompt, flags=re.DOTALL)
    
    # 3.2 Remover caracteres potencialmente problemáticos
    prompt = prompt.replace("\x00", "")
    
    # 4 Classificação (pode ser implementada posteriormente usando um modelo de linguagem para classificar a segurança do prompt)

    check_prompt = check_prompt = f"""
    Você é um classificador de segurança de prompts.

    Analise APENAS o conteúdo abaixo.

    Responda SOMENTE com:
    SAFE
    ou
    MALICIOUS

    Conteúdo:
    ---
    {prompt}
    ---
    """
    if SECURITY_MODEL == LARGE_MODEL: 
        classification = generate_response(check_prompt)
    elif SECURITY_MODEL == SMALL_MODEL:
        classification = generate_response_small_model(check_prompt)
    else:
        # Caso queira testar diferentes modelos para a segurança podemos adicionar uma função so para ele
        classification = generate_response(check_prompt)

    print(f"classification result for prompt: {classification.strip()}")
    print("Prompt verificado e considerado seguro.")



    if classification.strip().lower() == "SAFE".lower():
        return prompt.strip()
    else:
        # Salvar tentativa possivelmente maliciosa para análise futura
        log_attempt(user_id, prompt)
        raise ValueError("Prompt classificado como inseguro pela classificação de segurança.")

def log_attempt(user_id, prompt):
    # função para logar tentativas de input, especialmente aquelas classificadas como maliciosas, para análise futura e aprimoramento das defesas
    timestamp = int(time.time())
    log_data = {
        "user_id": user_id,
        "prompt": prompt,
        "timestamp": timestamp
    }
    log_data_str = json.dumps(log_data)
    log_dir = os.path.join("data/malicious_attempts")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"user_{user_id}_{timestamp}.json")
    with open(log_file, "a") as f:
        f.write(log_data_str + "\n")
     
def save_response_as_sample(response):
    
    # TODO:Check if response is on the right format (json):


    with open("samples/response.json", "w") as f:
        json.dump(response, f, indent=4)


def save_response_to_history(user, pergunta, prompt, prompt_model, response, grade, timestamp=None):
    # TODO: add grade from grader function to the response data
    if timestamp is None:
        timestamp = int(time.time())
    else:
        timestamp = int(timestamp)

    response_data = {
        "user data": {
            "user_id": user,
        },
        "input": {
            "pergunta": pergunta,
            "prompt": prompt,
            "prompt_model": prompt_model
        },
        "output": response,
        "grade": grade,
        "timestamp": timestamp
    }

    # Salva a resposta em um arquivo JSON na pastas data/historico com o nome sendo o timestamp da resposta
    base_dir = os.path.join("data", "historico")
    os.makedirs(base_dir, exist_ok=True)
    file_path = os.path.join(base_dir, f"response_{timestamp}.json")
    with open(file_path, "w") as f:
        json.dump(response_data, f, indent=4)

def save_image_to_history(images, user, timestamp=None):
    """
    Salva uma lista de imagens (bytes ou base64 strings) em uma pasta dentro de data/historico.
    Cada execução cria uma subpasta `images_{timestamp}` e retorna o caminho dessa pasta.
    """
    if timestamp is None:
        timestamp = int(time.time())
    else:
        timestamp = int(timestamp)

    base_dir = os.path.join("data", "historico")
    images_dir = os.path.join(base_dir, f"images_{timestamp}")
    os.makedirs(images_dir, exist_ok=True)

    saved_paths = []
    for i, img in enumerate(images):
        out_path = os.path.join(images_dir, f"image_{i}.png")
        try:
            if isinstance(img, (bytes, bytearray)):
                data = img
                b64 = base64.b64encode(data).decode('utf-8')
            else:
                # assume string base64
                b64 = img
                data = base64.b64decode(img)
            with open(out_path, "wb") as f:
                f.write(data)
            saved_paths.append(out_path)
            
        except Exception:
            logging.exception("Failed to save image %s", out_path)

    return images_dir, saved_paths
    
def generate_response(prompt):
    # implementar função que chama o modelo de linguagem para gerar a resposta, usando o prompt gerado
    global client, LARGE_MODEL
    # garante que exista um cliente inicializado
    if client is None:
        try:
            # tenta inicializar o cliente de forma preguiçosa
            client = OpenAI(api_key=key)
        except Exception:
            logging.exception("OpenAI client not initialized and couldn't be created")
            raise RuntimeError("OpenAI client not available")

    try:
        resp = client.responses.create(
            model=LARGE_MODEL,
            input=prompt,
        )
    except Exception:
        logging.exception("Error while calling LLM API")
        return ""

    # Extrair texto em várias formas possíveis
    try:
        if hasattr(resp, "output_text"):
            return resp.output_text
        if isinstance(resp, dict):
            return json.dumps(resp)
        return str(resp)
    except Exception:
        logging.exception("Failed to normalize LLM response")
        return ""

def generate_response_small_model(prompt):
    # função alternativa para gerar resposta usando um modelo menor, para testes ou para perguntas mais simples, usando o modelo v1, que é o mais básico
    global client, SMALL_MODEL
    if client is None:
        try:
            client = OpenAI(api_key=key)
        except Exception:
            logging.exception("OpenAI client not initialized and couldn't be created")
            raise RuntimeError("OpenAI client not available")

    try:
        resp = client.responses.create(
            model=SMALL_MODEL,
            input=prompt,
        )
    except Exception:
        logging.exception("Error while calling LLM API")
        return ""

    try:
        if hasattr(resp, "output_text"):
            return resp.output_text
        if isinstance(resp, dict):
            return json.dumps(resp)
        return str(resp)
    except Exception:
        logging.exception("Failed to normalize LLM response")
        return ""
    
def generate_image(prompt):
    global client, LARGE_MODEL
    try:
        resp = client.responses.create(
            model=LARGE_MODEL,
            input=prompt,
            tools=[{"type": "image_generation"}],
        )
    except Exception:
        logging.exception("Image generation call failed")
        return b""

    # Extrai possíveis resultados de imagem do response (formatos variados)
    try:
        image_data = []
        for output in getattr(resp, "output", []) or []:
            if getattr(output, "type", None) == "image_generation_call":
                image_data.append(getattr(output, "result", b""))
        if image_data:
            return image_data[0]
    except Exception:
        logging.exception("Failed to parse image generation response")

    return b""

def infer_engine(user, pergunta, prompt_model):

    
    cached_response = cache.get_cached_response(user, pergunta, prompt_model)
    if cached_response:
        print("Resposta encontrada no cache:")
        
        return cached_response
        
    else:
        print("Gerando nova resposta...")
        
        
        # Pega o tempo atual
        timestamp = int(time.time())
        
        prompt, prompt_model, response, images = run_prompt_model(user, pergunta, prompt_model=prompt_model)
        try:
            #print("response before grading:", response)
            grade = grade_response(pergunta, response)
            response["grade"] = grade
            print(grade)
        except Exception:
            grade = "Erro na avaliação da resposta"
        
        
        # se houver imagens geradas, salve-as e adicione caminho à resposta
        if images:
            images_dir, images_path = save_image_to_history(images, user, timestamp=timestamp)
            response["output"]["path_imagens"][images_dir] = images_path

        print("Resposta gerada:", response)

        cache.set_cached_response(user, pergunta, prompt_model, response)
        # agr parser para save sample
        save_response_as_sample(response)
        save_response_to_history(user, pergunta, prompt, prompt_model, response, grade, timestamp=timestamp)
        
        return response, images
        
# TODO: Adicionar um metodo para comparar prompts e determinar qual é o melhor

    
