# V-Lab

Desafio técnico para o processo seletivo de estágio em IA e Engenharia de Prompt no V-Lab.

Demo: https://v-lab-chi.vercel.app/

---

O sistema recebe um tópico e o perfil do aluno (idade, nível, estilo de aprendizagem) e gera conteúdo educativo personalizado via OpenAI. Dependendo do perfil, o conteúdo pode incluir explicação conceitual, exemplos práticos, perguntas de reflexão e imagens geradas por IA.

Tem 4 versões de prompt com técnicas diferentes (baseline, persona + contexto, chain-of-thought, visual com imagens) — o modelo é escolhido automaticamente pelo perfil ou manualmente pelo usuário no dashboard. Cada resposta recebe uma nota de 0 a 10 gerada pelo próprio modelo.

---

## Setup

Precisa de Conda e uma chave da OpenAI.

```bash
git clone <url-do-repositorio>
cd V-Lab

conda create -n V-Lab python=3.11
conda activate V-Lab
pip install -r requirements.txt

cp .env.example .env
# adicione OPENAI_API_KEY e FLASK_SECRET_KEY no .env
```

Para rodar:

```bash
conda activate V-Lab
cd front
python server.py
```

Abre em `http://localhost:5000`.

---

## Como usar

1. Crie uma conta em `/register` com nome, idade, nível de conhecimento e estilo de aprendizagem
2. Faça login
3. No dashboard, escreva um tópico, escolha a versão do prompt (ou deixe no automático) e clique em gerar

O histórico de cada geração fica em `data/historico/`.

---

## Estrutura

```
V-Lab/
├── app/
│   ├── prompt_engine.py   # núcleo — monta prompts, chama a API, avalia respostas
│   ├── profiles.py        # leitura e escrita de perfis de alunos
│   ├── cache.py           # cache por hash para evitar chamadas repetidas
│   ├── config.py          # paths (adapta para /tmp/ no Vercel)
│   └── api_key.py         # carrega a chave do .env
├── front/
│   ├── server.py          # Flask
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       └── register.html
├── data/
│   ├── student_profiles.json
│   ├── cache.json
│   ├── historico/
│   └── malicious_attempts/
├── tests/
│   └── test_prompts.py
├── samples/
│   └── response.json
├── .env.example
├── requirements.txt
└── PROMPT_ENGINEERING_NOTES.md
```

---

## Perfis de aluno

| Campo | Valores |
|---|---|
| `nivel de conhecimento` | `iniciante`, `intermediario`, `avancado` |
| `estilo de aprendizagem` | `visual`, `auditivo`, `leitura-escrita`, `cinestesico` |

---

## Exemplo de output

Output completo em `samples/response.json`. Estrutura básica:

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

6 testes de construção de prompt, sem chamadas reais à API.

---

## Deploy

Está no Vercel em https://v-lab-chi.vercel.app/

Para subir uma instância própria: conecte o repositório ao Vercel e defina `OPENAI_API_KEY` e `FLASK_SECRET_KEY` nas variáveis de ambiente do projeto.
