# V-Lab — Plataforma de Conteúdo Educativo com IA

Plataforma que gera conteúdo educativo personalizado a partir de um tópico e do perfil do aluno, utilizando técnicas avançadas de engenharia de prompt com a API da OpenAI.

Desenvolvido como desafio técnico para o processo seletivo de estágio em IA e Engenharia de Prompt no V-Lab.

---

## Funcionalidades

- **Geração de 4 tipos de conteúdo** a partir de um único tópico:
  - Explicação conceitual
  - Exemplos práticos
  - Perguntas de reflexão
  - Resumo visual com imagens geradas por IA (para perfis visuais)
- **4 versões de prompt** com técnicas distintas, selecionáveis pelo usuário ou automaticamente pelo perfil
- **Avaliação automática** de qualidade da resposta (nota 0–10)
- **Cache** para evitar chamadas desnecessárias à API
- **Proteção contra prompt injection** com múltiplas camadas de segurança
- **Histórico** de todas as gerações com timestamp
- **Interface web** com Flask
- **Testes automatizados** de construção de prompt

---

## Setup

**Pré-requisitos:** Conda instalado, chave de API da OpenAI.

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd V-Lab

# 2. Crie e ative o ambiente conda
conda create -n V-Lab python=3.11
conda activate V-Lab

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e adicione sua OPENAI_API_KEY e FLASK_SECRET_KEY
```

---

## Como rodar

```bash
# A partir da raiz do projeto
conda activate V-Lab
cd front
python server.py
```

Acesse `http://localhost:5000` no navegador.

---

## Como usar

1. **Registre uma conta** em `/register` — informe nome, idade, nível de conhecimento e estilo de aprendizagem
2. **Faça login** com seu user ID e senha
3. No **dashboard**, digite um tópico ou pergunta
4. Escolha a versão do prompt (ou deixe em *Automático* para seleção pelo perfil)
5. Clique em **Gerar conteúdo**

O sistema gera automaticamente os tipos de conteúdo mais adequados ao perfil, exibe a resposta formatada e salva o histórico em `data/historico/`.

---

## Estrutura do projeto

```
V-Lab/
├── app/
│   ├── prompt_engine.py   # Motor de engenharia de prompt (núcleo do sistema)
│   ├── profiles.py        # Gerenciamento de perfis de alunos
│   ├── cache.py           # Sistema de cache com hash
│   ├── api_key.py         # Carregamento seguro da chave de API
│   └── main.py            # CLI (Não mais utilizado)
├── front/
│   ├── server.py          # Servidor escrito em Flask
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       └── register.html
├── data/
│   ├── student_profiles.json      # Perfis dos alunos salvo
│   ├── cache.json                 # Cache de respostas
│   ├── historico/                 # Histórico de tudo que foi gerado (JSON + imagens)
│   └── malicious_attempts/        # Log de tentativas de prompt injection
├── tests/
│   └── test_prompts.py    # Testes de construção de prompt
├── samples/
│   └── response.json      # Exemplo de output gerado
├── .env.example
├── requirements.txt
└── PROMPT_ENGINEERING_NOTES.md
```

---

## Perfis de aluno

Cada perfil contém necessariamente:

| Campo                    | Valores possíveis                                      |
| ------------------------ | ------------------------------------------------------ |
| `nome do aluno`          | String com o nome                                      |
| `idade`                  | número inteiro                                         |
| `nivel de conhecimento`  | `iniciante`, `intermediario`, `avancado`               |
| `estilo de aprendizagem` | `visual`, `auditivo`, `leitura-escrita`, `cinestesico` |



---

## Exemplo de output

Veja `samples/response.json` para um exemplo completo.

exemplo:

```json
{
  "input": {
    "pergunta": "Como funciona a fotossíntese?",
    "topico": "Biologia — Processos metabólicos",
    "nivel de complexidade": "Básico a intermediário",
    "requested_content": ["conceptual_explanation", "pratical_examples", "reflective_questions"]
  },
  "output": {
    "titulo": "Fotossíntese: como as plantas transformam luz em alimento",
    "pontos_chave": ["..."],
    "conceptual_explanation": [{"Titulo": "...", "Conteudo": "..."}],
    "pratical_examples": [{"Titulo": "...", "Conteudo": "..."}],
    "reflective_questions": [{"Titulo": "...", "Conteudo": "..."}]
  },
  "grade": 9.6
}
```

---

## Testes

```bash
conda activate V-Lab
python -m unittest tests/test_prompts.py -v
```

7 testes verificam que cada versão de prompt contém as técnicas esperadas e que versões distintas geram prompts estruturalmente diferentes — sem nenhuma chamada real à API.

---

## Deploy

O arquivo `vercel.json` está configurado para deploy no Vercel apontando para `front/server.py`. Basta conectar o repositório ao Vercel e definir as variáveis `OPENAI_API_KEY` e `FLASK_SECRET_KEY` nas configurações do projeto.
