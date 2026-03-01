# Desafio Técnico – Estágio em IA e Engenharia de Prompt

## 📌 Visão Geral

Este projeto consiste no desenvolvimento de uma plataforma educativa capaz de gerar conteúdo personalizado para alunos com diferentes perfis.

O sistema deve receber:
- Tópico a ser ensinado
- Perfil do aluno (idade, nível de conhecimento, estilo de aprendizado)

E gerar automaticamente **4 tipos distintos de conteúdo educacional**, utilizando técnicas avançadas de engenharia de prompt.

O foco principal do desafio é demonstrar domínio em:
- Estruturação de prompts
- Técnicas de engenharia de prompt
- Organização técnica
- Documentação clara
- Boas práticas de desenvolvimento

---

# 🎯 Objetivo do Sistema

Desenvolver uma aplicação que:

1. Receba parâmetros do aluno:
   - Nome
   - Idade
   - Nível de conhecimento (iniciante / intermediário / avançado)
   - Estilo de aprendizado (visual / auditivo / leitura-escrita / cinestésico)

2. Receba um tópico a ser ensinado

3. Gere automaticamente os seguintes 4 tipos de conteúdo:

   ### 1️⃣ Explicação Conceitual
   - Utilizar técnica de *chain-of-thought*
   - Explicação estruturada passo a passo

   ### 2️⃣ Exemplos Práticos
   - Contextualizados para idade e nível
   - Adequados ao estilo de aprendizado

   ### 3️⃣ Perguntas de Reflexão
   - Estimulem pensamento crítico
   - Adaptadas ao perfil do aluno

   ### 4️⃣ Resumo Visual
   - Diagrama em ASCII OU
   - Descrição estruturada de mapa mental

4. Salvar todos os resultados em arquivo JSON estruturado

5. Permitir comparação entre diferentes versões de prompts

---

# 🧠 Técnicas Obrigatórias de Engenharia de Prompt

O sistema deve implementar:

## 1. Persona Prompting
Exemplo:
> "Você é um professor experiente em pedagogia cognitiva..."

---

## 2. Context Setting
Incluir no prompt:
- Idade
- Nível
- Estilo de aprendizado
- Informações específicas do aluno

---

## 3. Chain-of-Thought
Solicitar raciocínio estruturado passo a passo para explicações.

---

## 4. Output Formatting
Especificar claramente o formato de saída esperado (preferencialmente JSON estruturado).

---

# 🛠️ Requisitos Técnicos

## Linguagem
- Python OU JavaScript

## API
- OpenAI (GPT-4o ou GPT-4o mini)
- OU Google Gemini
- OU Anthropic Claude
- Pode usar versão gratuita

## Bibliotecas Recomendadas

### Python
- requests
- python-dotenv
- json

### JavaScript
- axios
- dotenv
- fs

---

# 🏗️ Infraestrutura

- CLI (menu de opções) OU
- Interface web simples (Flask ou Express)
- Arquivo `.env` para variáveis sensíveis
- Sistema de cache para evitar chamadas desnecessárias à API

---

# 📂 Requisitos Funcionais

## 1️⃣ Sistema de Perfil de Aluno

- Armazenar 3 a 5 perfis em JSON
- Cada perfil deve conter:
  - Nome
  - Idade
  - Nível de conhecimento
  - Estilo de aprendizado

---

## 2️⃣ Motor de Engenharia de Prompt

Implementar função responsável por:

- Construir prompts dinamicamente
- Adaptar prompt com base no perfil do aluno
- Usar:
  - Persona prompting
  - Context setting
  - Chain-of-thought
  - Output formatting

---

## 3️⃣ Geração de Conteúdo

Implementar 4 funções separadas:

- generate_explanation()
- generate_examples()
- generate_reflection_questions()
- generate_visual_summary()

Cada função deve:
- Utilizar prompt distinto e otimizado
- Demonstrar diferenças claras entre versões de prompt

---

## 4️⃣ Persistência e Comparação

- Salvar conteúdo gerado em JSON
- Incluir timestamp
- Permitir gerar conteúdo com diferentes versões de prompt
- Armazenar histórico de execuções
- Permitir análise comparativa posterior

---

## 5️⃣ Interface de Uso

Permitir:

- Selecionar aluno
- Inserir tópico
- Escolher tipo de conteúdo
- Escolher versão do prompt

Pode ser:
- CLI estruturado
OU
- Interface web simples

---

# 🌟 Critério de Pontuação Extra

- Deploy em ambiente de nuvem (Vercel, Heroku, etc.)
- Implementação de testes automatizados
- Interface mais polida
- Sistema de avaliação comparativa de prompts
- Funcionalidades inovadoras além do mínimo exigido

---

# 📊 Critérios de Avaliação

## 1️⃣ Engenharia de Prompt (40%)

- Prompts específicos e bem estruturados
- Uso efetivo de técnicas avançadas
- Diferença clara entre versões de prompt
- Documentação explicando decisões

---

## 2️⃣ Implementação Técnica (30%)

- Código organizado e modular
- Tratamento de erros
- Segurança (chaves protegidas)
- Cache funcional
- Eficiência e reutilização

---

## 3️⃣ Documentação (20%)

- README claro
- Exemplos de uso
- Exemplos de output
- Explicação das estratégias de prompt
- Instruções de setup

---

## 4️⃣ Criatividade e Extras (10%)

- Features adicionais
- Testes automatizados
- Comparação inteligente de resultados
- Interface bem estruturada

---

# 📦 Entregáveis Obrigatórios

O repositório final deve conter:

- Código-fonte organizado
- Histórico de commits
- README.md
- requirements.txt (ou package.json)
- .env.example
- Diretório /samples com exemplos de outputs
- Arquivo PROMPT_ENGINEERING_NOTES.md explicando:
  - Estratégias utilizadas
  - Justificativas
  - Comparação entre versões de prompt

---

# ⚠️ Observações Importantes

- É permitido usar ferramentas como Copilot
- O projeto passará por verificação de uso excessivo de IA
- Código deve demonstrar entendimento real
- Documentação é extremamente importante
- Qualidade > Quantidade

---

# 🎯 Objetivo Final

Demonstrar:

- Maturidade em engenharia de prompt
- Organização de software
- Pensamento crítico
- Capacidade de comparação e análise
- Clareza na comunicação técnica