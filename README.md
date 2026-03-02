# V-Lab

Este repositório contém o backend e a interface web para o desafio técnico de IA e engenharia de prompt.

## Estrutura relevante

- `app/` – código python responsável por perfis, prompt engine, cache, etc.
- `front/` – aplicação Flask simples (login/registro/tópico) destinada a ser implantada no Vercel ou outro provedor.

## Como rodar localmente

1. crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. copie `.env.example` para `.env` e ajuste suas chaves

3. inicie o servidor frontal:

```bash
cd front
python server.py
```

4. abra o navegador em `http://localhost:5000` para registrar, fazer login e testar a interface.

## Deploy no Vercel

O arquivo `vercel.json` já aponta para `front/server.py` e utiliza o runtime `@vercel/python`.
Basta conectar este repositório ao Vercel, definir as variáveis de ambiente (`OPENAI_API_KEY`,
`FLASK_SECRET_KEY`) e a aplicação estará disponível.

## Observações

- A interface é propositalmente simples; foco na estrutura funcional.
- O formulário de dashboard aceita um tópico e tenta invocar o motor de prompt para
  gerar resultados, gravando um histórico em `data/`.

