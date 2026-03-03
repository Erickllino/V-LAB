# Prompt Engineering Notes

## Visão geral da abordagem

O projeto usa um pipeline de multiplos passos antes de chamar o modelo principal. No primeiro passo, analisamos o prompt de entrada para checar sehá possibilidade do prompt ser malicioso, passamos a entrada por uma sanitização ee depois por multiplos testes para checar se há um problema, e então finalmente, se não falhar nenhum teste, enviamos o prompt para um modelo menor dando instruções para determinar se o prompt é malicioso.   

Então, no proximo passo, um prompt de roteamento analisa o perfil do aluno e a pergunta para decidir quais tipos de conteúdo são relevantes (`conceptual_explanation`, `pratical_examples`, `reflection_questions`, `visual_summary`) isso abre a possibilidade de adicionar mais tipos de conteudo (Audio, vídeo etc). 

Depois, passamos por  fragmentos de prompt correspondentes aos tipos escolhidos são concatenados e entregues ao modelo de geração junto com a instrução do modelo de versão selecionado (v1–v4).

Isso separa a decisão de *o que gerar* da decisão de *como gerar*, tornando cada parte mais fácil de ajustar independentemente.

---

## Técnicas de Prompt-Engineering

### 1. Output Formatting

Usado em todos os modelos! O prompt especifica explicitamente o formato JSON da saída que é esperado esperado. Isso reduz a variabilidade do output e permite parsing direto com `json.loads`.

Exemplo de instrução no prompt:
```
Responda tudo no seguinte formato JSON:
{
  "input": {"pergunta": "", "topico": "", "nivel de complexidade": "", "requested_content": []},
  "output": {"titulo": "", "pontos_chave": []}
}
```

Cada função de "geração" conteúdo (`conceptual_explanation`, `pratical_examples`, etc) adiciona seu próprio campo ao prompt final, instruindo o modelo a adicionar ao JSON base em vez de substituí-lo.

---

### 2. Persona Prompting

Usado nos modelos v2, v3 e v4. Atribuir um papel ao modelo muda o tom, a profundidade e o vocabulário da resposta. Em v2 a persona é genérica ("professor experiente com didática impecável"), enquanto em v3 ela é mais direcionada ao nível do aluno ("explique de forma extremamente técnica, como se estivesse explicando para alguém que entende bem do assunto").

A ausência de persona prompting no modelo v1 serve como baseline para testar o quanto essa tecnica melhorou ou piorou o resultado. Não coloco o persona para que o modelo responda de forma direta sem nenhuma "voz" atribuída.

---

### 3. Context Setting

Usado no modelo v2. Os dados do perfil do aluno (idade, nível de conhecimento, estilo de aprendizagem) são injetados diretamente no prompt para que o modelo adapte vocabulário, complexidade e exemplos. Sem essa instrução, o modelo vai usar um nível de abstração genérico que pode não servir ao perfil específico.

```
O estudante que você ensinará tem {idade} anos,
nível de conhecimento {nivel} e estilo de aprendizagem {estilo}.
```

---

### 4. Chain-of-Thought

Usado nos modelos v3 e v4. Em vez de pedir uma resposta direta, o prompt instrui o modelo a seguir uma estrutura de raciocínio com 4 etapas explícitas:

1. **Intuição inicial** — conectar o conceito a algo familiar antes de formalizar
2. **Conceito formal** — definição estruturada
3. **Exemplo guiado** — aplicação pratica passo a passo
4. **Conexão com conhecimento prévio** — ancoragem no que o aluno já deve saber

Isso força o modelo a construir o output de forma progressiva em vez de despejar informação.

---

## Comparação entre versões

| Modelo | Técnicas Utilizadas                                                 | Aluno         | Diferencial                                                  |
| ------ | ------------------------------------------------------------------- | ------------- | ------------------------------------------------------------ |
| **v1** | Output formatting                                                   | Qualquer      | Baseline. Sem interferência com resposta direta ao tópico    |
| **v2** | Persona + Context setting + Output formatting                       | Intermediário | Adapta vocabulário e profundidade ao perfil do aluno         |
| **v3** | Persona + Chain-of-thought + Output formatting                      | Avançado      | Estrutura o raciocínio em 4 etapas progressivas              |
| **v4** | Persona + Chain-of-thought + Output formatting + Geração de imagens | Visual        | Igual ao v3, mas gera prompts de imagem e os executa via API |

### Por que v1 existe se é o "pior"?

O v1 serve como referência para comparação. Sem um baseline, é impossível medir o ganho real das técnicas aplicadas nas outras versões. O sistema salva a versão usada no histórico justamente para permitir essa comparação posterior.

---

## Seleção automática de modelo

A função `determine_prompt_model` ve o perfil para indicar versão mais adequada:

```
estilo visual          - v4  (geração de imagens )
nível iniciante        - v1  (resposta direta e acessível)
nível intermediário    - v2  (adaptação ao perfil melhora a experiência)
nível avançado         - v3  (chain-of-thought aproveita a capacidade analítica do aluno)
```

O usuário também pode escolher não utilizar a seleção automática pelo seletor no dashboard, o que é útil para comparar versões com o mesmo tópico e perfil.

---

## Segurança de input

O sistema aplica três camadas de proteção antes de qualquer chamada à API do modelo principal:

1. **Limite de tamanho** — inputs acima de 2000 caracteres são rejeitados
2. **Regex de padrões suspeitos** — lista de expressões que cobrem tentativas de override de instruções, vazamento de sistema e escalonamento de privilégios em PT e EN
3. **Classificação por LLM** — um modelo de menor custo analisa o input e retorna `SAFE` ou `MALICIOUS`; tentativas detectadas são logadas em `data/malicious_attempts/`

Tentativas bloqueadas são salvas com timestamp e user ID para análise posterior.

---

## Avaliação automática de respostas

Após cada geração de output, a função `grade_response` envia a resposta que foi gerada para o usuario, para um modelo de LLM com instruçoes para avaliar a resposta  em 4 critérios (correção, completude, clareza, relevância) e retorna *somente* uma nota de 0 a 10. Essa nota é exibida no dashboard e salva no histórico, permitindo comparar objetivamente respostas geradas por versões diferentes do prompt para o mesmo tópico.
