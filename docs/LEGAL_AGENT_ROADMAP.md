# 🧠 Roadmap: Juridical & Innovation Agent Upgrade

## 🎯 Objetivo
Transformar o `JuridicalAgent` de um validador passivo para um **Consultor de Inovação Proativo**.
Ele não deve apenas dizer "isso viola o Art. 12", mas sim: "Se você ajustar X para Y, isso se torna patenteável como Modelo de Utilidade".

---

## 📚 Base de Conhecimento (Knowledge Base)

Precisamos alimentar o agente com os seguintes contextos (em `docs/legal_references/`):

### 1. Lei da Propriedade Industrial (LPI 9.279/96)
- **Foco:** Artigos 10 (não invenção), 12 (novidade), 13 (atividade inventiva), 15 (aplicação industrial), 18 (não patenteável).
- **Ação:** Criar `LPI_HIGHLIGHTS.md`.

### 2. Manual de Patentes do INPI (Diretrizes)
- **Foco:** Como o INPI avalia "atividade inventiva" em software (Computer Implemented Inventions).
- **Ação:** Criar `INPI_SOFTWARE_GUIDELINES.md`.

### 3. TRL (Technology Readiness Levels) - NASA/ABNT
- **Foco:** Classificar o estágio de maturidade da tecnologia descrita.
- **Ação:** Criar `TRL_SCALE.md`.

---

## 🤖 Novas Capabilities (Habilidades)

### 1. `suggest_innovation_pivot`
- **Input:** Descrição da tecnologia (recusada ou fraca).
- **Lógica:** Analisar "Delta de Inovação".
- **Output:** Sugestão de alteração técnica para aumentar o "Inventive Step".
  - *Ex:* "Sua descrição foca em regra de negócio (não patenteável). Se focar no algoritmo de ofuscação de dados utilizado, torna-se patenteável."

### 2. `assess_patentability_score`
- **Métricas:**
  - **Novidade (0-10):** Quão único é?
  - **Atividade Inventiva (0-10):** É óbvio para um técnico no assunto?
  - **Aplicação Industrial (0-10):** É replicável?
  - **Suficiência Descritiva (0-10):** Está bem explicado?

### 3. `generate_claim_draft` (Rascunho de Reivindicação)
- **Ação:** Gerar um rascunho da "Reivindicação Independent 1" focado na parte técnica.

---

## 🛠️ Plano de Implementação

1.  **Ingestão:** Criar os arquivos Markdown na pasta `docs/legal_references`.
2.  **Indexing:** Criar um script simples para carregar esses MDs como contexto para o LLM.
3.  **Prompt Engineering:** Atualizar o System Prompt do Agente para agir como "Examinador Sênior do INPI".
4.  **Tools:** Implementar as funções no `JuridicalAgent`.

---

## 🔗 Integração com MCP
Essas novas habilidades serão expostas via MCP como:
- `consult_lpi`
- `evaluate_innovation`
