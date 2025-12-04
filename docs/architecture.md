# Arquitetura do EditalShield

## 🏗️ Visão Geral

EditalShield é um framework modular composto por 6 módulos independentes que podem ser usados isoladamente ou em conjunto.

```
┌─────────────────────────────────────────────────────────────┐
│                      EditalShield CLI                        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Módulo 1   │      │   Módulo 2   │      │   Módulo 3   │
│    Edital    │      │     Gap      │      │     NDA      │
│   Selector   │      │   Analyzer   │      │  Generator   │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Módulo 4   │      │   Módulo 5   │      │   Módulo 6   │
│   Memorial   │      │     Cost     │      │   Scenario   │
│  Protector   │      │  Calculator  │      │   Planner    │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Data & Templates │
                    │   - editais.json  │
                    │   - criterios.json│
                    │   - keywords.json │
                    │   - templates/    │
                    └──────────────────┘
```

---

## 📦 Módulos

### 1️⃣ Edital Selector
**Responsabilidade**: Comparar editais e recomendar o melhor fit

**Input**:
- Perfil do projeto (setor, estágio, valor, prazo)

**Output**:
- Ranking de editais por fit score
- ROI estimado
- Recomendações

**Dependências**:
- `data/editais_brasil.json`

---

### 2️⃣ Gap Analyzer
**Responsabilidade**: Identificar gaps de elegibilidade

**Input**:
- Perfil do projeto
- Edital escolhido

**Output**:
- Lista de gaps críticos
- Plano de ação
- Nota projetada

**Dependências**:
- `data/criterios_padrao.json`
- `data/editais_brasil.json`

---

### 3️⃣ NDA Generator
**Responsabilidade**: Gerar contratos customizados

**Input**:
- Dados do projeto
- Dados do consultor
- Termos (success fee, teto, etc.)

**Output**:
- NDA customizado (PDF)
- Guia de negociação
- Fairness score

**Dependências**:
- `templates/nda_*.md`
- `utils/pdf_generator.py`

---

### 4️⃣ Memorial Protector ⭐
**Responsabilidade**: Proteger PI em memoriais técnicos

**Input**:
- Memorial técnico (texto)
- Nível de sensibilidade

**Output**:
- Risk score
- Lista de exposições
- Memorial protegido
- Relatório de análise

**Dependências**:
- `data/trade_secrets_keywords.json`
- `utils/text_analyzer.py`

---

### 5️⃣ Cost Calculator
**Responsabilidade**: Calcular custos e simular cenários

**Input**:
- Valor aprovado
- Success fee %
- Teto máximo
- Parcelas

**Output**:
- Cálculo detalhado
- 4 cenários (aprovado integral/parcial, glosado, negado)
- Termo de liquidação

**Dependências**:
- `data/formulas.json`
- `utils/pdf_generator.py`

---

### 6️⃣ Scenario Planner
**Responsabilidade**: Planejar cenários e contingências

**Input**:
- Edital
- Valor aprovado
- Dados do NDA

**Output**:
- Matriz de cenários
- Playbooks de resposta
- Planos de contingência

**Dependências**:
- `templates/scenario_playbooks/`
- Módulo 5 (Cost Calculator)

---

## 🗂️ Estrutura de Diretórios

```
editalshield/
│
├── src/editalshield/              # Código fonte
│   ├── __init__.py
│   ├── config.py                  # Configurações globais
│   │
│   ├── modules/                   # 6 módulos principais
│   │   ├── __init__.py
│   │   ├── edital_selector.py     # Módulo 1
│   │   ├── gap_analyzer.py        # Módulo 2
│   │   ├── nda_generator.py       # Módulo 3
│   │   ├── memorial_protector.py  # Módulo 4
│   │   ├── cost_calculator.py     # Módulo 5
│   │   └── scenario_planner.py    # Módulo 6
│   │
│   ├── templates/                 # Templates parametrizados
│   │   ├── nda_centelha.md
│   │   ├── nda_pipe.md
│   │   ├── nda_finep.md
│   │   ├── nda_generic.md
│   │   ├── memorial_structure.md
│   │   ├── termo_liquidacao.md
│   │   └── scenario_playbooks/
│   │       ├── glosa_response.md
│   │       ├── contingency_plan.md
│   │       └── rejection_response.md
│   │
│   ├── data/                      # Base de dados genérica
│   │   ├── editais_brasil.json
│   │   ├── criterios_padrao.json
│   │   ├── trade_secrets_keywords.json
│   │   └── formulas.json
│   │
│   └── utils/                     # Utilitários
│       ├── __init__.py
│       ├── text_analyzer.py       # NLP genérico
│       ├── pdf_generator.py       # Gerar PDFs
│       ├── validators.py          # Validações
│       └── formatters.py          # Formatação
│
├── cli/                           # Interface CLI
│   ├── __init__.py
│   └── editalshield_cli.py        # 6 comandos
│
├── notebooks/                     # Tutoriais
│   ├── 00_quickstart.ipynb
│   ├── 01_edital_selector_tutorial.ipynb
│   ├── 02_gap_analyzer_tutorial.ipynb
│   ├── 03_nda_generator_tutorial.ipynb
│   ├── 04_memorial_protector_tutorial.ipynb
│   ├── 05_cost_calculator_tutorial.ipynb
│   └── 06_scenario_planner_tutorial.ipynb
│
├── tests/                         # Testes unitários
│   ├── __init__.py
│   ├── test_edital_selector.py
│   ├── test_gap_analyzer.py
│   ├── test_nda_generator.py
│   ├── test_memorial_protector.py
│   ├── test_cost_calculator.py
│   └── test_scenario_planner.py
│
├── examples/                      # Exemplos fictícios
│   ├── example_varejo_tech/
│   ├── example_healthtech/
│   └── example_fintech/
│
├── docs/                          # Documentação
│   ├── architecture.md            # Este arquivo
│   ├── api_reference.md
│   ├── cli_usage.md
│   ├── whitepaper_tecnico.pdf
│   └── whitepaper_executivo.pdf
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── pyproject.toml
├── requirements.txt
└── .gitignore
```

---

## 🔄 Fluxo de Dados

### Fluxo Típico de Uso

```
1. Usuário define perfil do projeto
        ↓
2. Módulo 1 (Edital Selector) recomenda editais
        ↓
3. Módulo 2 (Gap Analyzer) identifica gaps
        ↓
4. Usuário corrige gaps e prepara documentação
        ↓
5. Módulo 3 (NDA Generator) cria contrato
        ↓
6. Módulo 4 (Memorial Protector) protege PI
        ↓
7. Usuário submete ao edital
        ↓
8. [SE APROVADO] Módulo 5 (Cost Calculator) calcula fees
        ↓
9. Módulo 6 (Scenario Planner) prepara contingências
```

---

## 🎯 Princípios de Design

### 1. Modularidade
- Cada módulo é independente
- Podem ser usados separadamente
- Baixo acoplamento

### 2. Parametrização
- Nenhum dado hardcoded
- Tudo via inputs do usuário
- Templates com placeholders

### 3. Extensibilidade
- Fácil adicionar novos módulos
- Fácil adicionar novos editais
- Fácil adicionar novos templates

### 4. Testabilidade
- Cada módulo testado isoladamente
- Cobertura >= 95%
- Dados fictícios em testes

---

## 🔧 Tecnologias

- **Python 3.9+**: Linguagem principal
- **Click**: Interface CLI
- **Jinja2**: Templates
- **Pydantic**: Validação de dados
- **ReportLab**: Geração de PDFs
- **NumPy**: Cálculos numéricos
- **Pytest**: Testes unitários

---

## 📈 Roadmap Técnico

### v0.1 (Atual)
- ✅ Estrutura base
- 🔄 Implementação dos 6 módulos
- 🔄 CLI completa
- 🔄 Documentação

### v0.2 (Futuro)
- ML para classificação automática de sensibilidade
- API REST
- Dashboard web

### v0.3 (Futuro)
- Expansão para editais internacionais
- Integração com sistemas externos
- Automação de scraping de editais

---

## 🤝 Contribuindo

Veja [../CONTRIBUTING.md](../CONTRIBUTING.md) para diretrizes de contribuição.
