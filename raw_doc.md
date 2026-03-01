Desafio Técnico – Estágio em IA e Engenharia de Prompt
Descrição Geral do Desafio
Você deverá desenvolver uma plataforma educativa precisa gerar conteúdo personalizado para alunos de diferentes
níveis. O desafio é criar um sistema que receba tópicos e características de alunos (idade, nível de conhecimento, estilo
de aprendizado) e gere materiais educativos otimizados usando técnicas avançadas de engenharia de prompt.
Este desafio focará principalmente em sua capacidade de estruturar prompts efetivos, técnicas como "chain-of-
thought", "persona prompting" e otimização de instruções para melhorar a qualidade do conteúdo gerado.
Objetivo
Desenvolver uma aplicação que:
• Receba parâmetros sobre o aluno (idade, nível, estilo de aprendizado) Receba um tópico a ser ensinado
• Gere 4 tipos diferentes de conteúdo usando prompts otimizados:
o Explicação conceitual (usando técnica de chain-of-thought)
o Exemplos práticos (contextualizados para a idade/nível)
o Perguntas de reflexão (que estimulem pensamento crítico)
o Resumo em formato visual (sugestão de diagrama/mapa mental em ASCII ou descrição)
• Salve os resultados em arquivo JSON estruturado
• Permita comparação de qualidade entre diferentes versões de prompts
Requisitos Técnicos
1. Linguagem: Python ou JavaScript
2. API: OpenAI (GPT-4o ou GPT-4o mini), Google Gemini ou Anthropic Claude (use versão gratuita/free tier)
3. Bibliotecas recomendadas:
a. Python: requests, python-dotenv, json
b. JavaScript: axios, dotenv, fs
4. Infraestrutura:
a. Aplicação CLI ou simples interface web (opcional, mas pontos extras)
b. Arquivo .env para configuração de chaves de API
c. Sistema de cache para evitar chamadas desnecessárias à API
Requisitos Funcionais
1. Sistema de Perfil de Aluno
a. Armazenar 3-5 perfis de alunos diferentes em JSON
b. Incluir: nome, idade, nível de conhecimento (iniciante/intermediário/avançado), estilo de
aprendizado (visual/auditivo/leitura-escrita/cinestésico)
2. Motor de Engenharia de Prompt
a. Implementar função que monta prompts dinâmicos baseado no perfil do aluno
b. Usar técnicas de:
i. Persona prompting: "Você é um professor experiente em Pedagogia"
ii. Context setting: Incluir dados específicos do aluno no prompt
iii. Chain-of-thought: Solicitar "pense passo a passo" para explicações
iv. Output formatting: Especificar exatamente como deseja a resposta
3. Geração de Conteúdo Diverso
a. Implementar 4 funções separadas, cada uma gerando um tipo diferente de conteúdo
b. Cada função deve usar um prompt distinto e otimizado
4. Persistência e Comparação
a. Salvar conteúdo gerado em arquivo JSON com timestamp
b. Permitir gerar mesmo conteúdo com diferentes versões de prompts
c. Armazenar histórico para análise posterior
5. Interface de Uso
a. CLI com menu de opções OU
b. Pequena interface web com Flask/Express (básica, sem necessidade de ser bonita)
c. Permitir selecionar aluno, tópico, tipo de conteúdo
6. Critério de Pontuação Extra
a. Código instalado e funcional em algum ambiente de nuvem (Vercel, Heroku ou afins)
Critérios de Avaliação
1. Qualidade da Engenharia de Prompt (40%)
a. Prompts são específicos e bem estruturados
b. Usa técnicas avançadas efetivamente
c. Diferenças entre prompts geram diferenças significativas de qualidade
d. Documentação explica as escolhas de engenharia de prompt
2. Implementação Técnica (30%)
a. Código bem organizado e fácil de manter
b. Tratamento robusto de erros e edge cases
c. Boas práticas de segurança (chaves não expostas)
d. Implementação eficiente (cache, reutilização)
3. Documentação (20%)
a. README claro e completo
b. Exemplos de uso e outputs
c. Explicação das técnicas de prompt utilizadas
d. Instruções de setup fáceis de seguir
4. Criatividade e Extras (10%)
a. Implementação de features além do requisito mínimo
b. Testes automatizados
c. Análise comparativa de resultados de prompts diferentes
d. Interface polida ou funcionalidades inovadoras
Entrega
• Repositório Git com histórico de commits
• Código-fonte bem organizado
• README conforme template
• Arquivo requirements.txt (Python) ou package.json (JavaScript)
• Arquivo .env.example mostrando variáveis necessárias
• Diretório /samples com exemplos de output JSON
• Arquivo /PROMPT_ENGINEERING_NOTES.md explicando estratégias de prompts utilizadas
Observação 1: Para este desafio, está autorizado o uso de Agentes/Prompts de auxílio à programação, como GitHub
Copilot e afins. Sendo que o projeto passará por verificação para uso de IA em excesso. Este é um critério eliminatório.
Fique atento(a)!!!
Observação 2: Este desafio avalia tanto competências técnicas quanto capacidade de aprendizado, organização e
documentação. Foque na qualidade do código e na experiência do usuário, mesmo que isso signifique implementar
menos funcionalidades.