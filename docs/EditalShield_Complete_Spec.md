# EditalShield - Especificação Completa de Desenvolvimento

## 🎯 Objetivo Principal

Criar um **framework open-source modular e genérico** para automação de análise, proteção de propriedade intelectual e otimização de submissões a editais de inovação brasileiros (Centelha, PIPE, Finep, CNPq, etc.).

**Escopo**: Framework reutilizável para QUALQUER startup/projeto, sem dados específicos de usuários reais no código base.

---

## 📋 Princípios Fundamentais

### 1. Genérico = Reutilizável
- ❌ Nada hardcoded (nomes, CPFs, projetos específicos)
- ✅ Tudo parametrizado (inputs do usuário)
- ✅ Templates com placeholders (`{{NOME}}`, `{{VALOR}}`)

### 2. Modular = Independente
- Cada módulo funciona standalone
- Podem ser usados separadamente ou em conjunto
- Sem dependências entre módulos (baixo acoplamento)

### 3. Validado = Credível
- Cada módulo testado com dados reais (em whitepapers/docs)
- Nunca dados reais no código (apenas em exemplos/documentação)
- 95%+ test coverage

### 4. Documentado = Claro
- Código autodocumentado (docstrings)
- 6 notebooks de tutorial (um por módulo)
- Whitepaper técnico completo
- README com exemplos reais

---

## 🏗️ Arquitetura: 6 Módulos

### **Módulo 1: Edital Selector** (Pré-Decisão)
**Objetivo**: Comparar editais e recomendar o melhor fit para um projeto

**Problema que resolve**: Startup não sabe qual edital escolher

**Input**:
```json
{
  "setor": "varejo",
  "estagio": "pre-seed",
  "valor_minimo": 50000,
  "valor_maximo": 200000,
  "tempo_disponivel_meses": 6,
  "localizacao": "nacional"
}
```

**Output**:
```json
{
  "ranking": [
    {
      "edital": "Centelha BA III",
      "fit_score": 85,
      "valor_disponivel": 86000,
      "prazo_ciclo_meses": 6,
      "taxa_aprovacao_pct": 40,
      "roi_esperado": 74000,
      "rank": 1
    },
    {
      "edital": "PIPE FAPESP Fase 1",
      "fit_score": 72,
      "valor_disponivel": 300000,
      "prazo_ciclo_meses": 12,
      "taxa_aprovacao_pct": 15,
      "roi_esperado": 245000,
      "rank": 2
    }
  ],
  "recomendacao": "Comece com Centelha BA (fit score 85, timeline curta)"
}
```

**Funcionalidades**:
- [ ] Base de dados com 20+ editais brasileiros (2024-2026)
- [ ] Algoritmo multi-critério de fit score
- [ ] Cálculo de ROI por edital
- [ ] Comparação side-by-side
- [ ] Exports (CSV, JSON, PDF)

**Implementação**:
```python
class EditalSelector:
    def __init__(self, editais_data="data/editais_brasil.json"):
        # Carrega base de editais
        pass
    
    def rank(self, projeto_profile):
        # Retorna ranking ordenado por fit_score
        pass
    
    def compare(self, edital_ids):
        # Compara N editais em tabela
        pass
```

**CLI**:
```bash
editalshield select \
  --sector varejo \
  --stage pre-seed \
  --value-min 50000 \
  --value-max 200000 \
  --time-months 6
```

---

### **Módulo 2: Gap Analyzer** (Pré-Estruturação)
**Objetivo**: Identificar gaps entre projeto atual e critérios do edital

**Problema que resolve**: Startup não sabe o que falta para ser elegível

**Input**:
```json
{
  "projeto": {
    "problema_validado": true,
    "mvp_desenvolvido_pct": 60,
    "equipe_quantidade": 2,
    "patente_status": "provisorio_depositado",
    "traction_usuarios": 10,
    "receita_atual": 0
  },
  "edital": "centelha_ba_2025"
}
```

**Output**:
```json
{
  "nota_projetada": 2.8,
  "nota_minima": 2.0,
  "situacao": "aprovacao_provavel",
  "gaps": [
    {
      "criterio": "Validação de Mercado",
      "status": "gap",
      "peso": 25,
      "acao_recomendada": "Realizar survey com 50+ potenciais clientes",
      "prazo_dias": 14,
      "impacto_nota": 0.5
    },
    {
      "criterio": "Equipe",
      "status": "gap",
      "peso": 25,
      "acao_recomendada": "Recrutar advisor jurídico/comercial",
      "prazo_dias": 21,
      "impacto_nota": 0.3
    }
  ],
  "tempo_total_para_submissao": 21,
  "plan_de_acao": ["survey", "advisor", "refinamento_pitch"]
}
```

**Funcionalidades**:
- [ ] Critérios por edital (data/criterios_por_edital.json)
- [ ] Checklist interativo
- [ ] Cálculo de nota projetada
- [ ] Gerador de plano de ação
- [ ] Estimativa de prazo

**Implementação**:
```python
class GapAnalyzer:
    def __init__(self, edital_id):
        # Carrega critérios do edital
        pass
    
    def analyze(self, projeto_profile):
        # Retorna gaps + plano de ação
        pass
    
    def generate_action_plan(self):
        # Plano sequencial de ações
        pass
```

---

### **Módulo 3: NDA Generator** (Contratação)
**Objetivo**: Gerar NDA customizado e defensivo para contratação de consultoria

**Problema que resolve**: Startup não tem proteção contratual ao compartilhar PI

**Input**:
```json
{
  "projeto": {
    "nome": "Projeto X",
    "setor": "varejo",
    "fundadores": [
      {"nome": "João", "cpf": "***-***", "email": "joão@email.com"},
      {"nome": "Adriano", "cpf": "***-***", "email": "adriano@email.com"}
    ]
  },
  "consultor": {
    "empresa": "RS Advogados Associados S/S",
    "cnpj": "XX.XXX.XXX/0001-XX",
    "representante": "Nome Representante"
  },
  "termos": {
    "success_fee_pct": 20,
    "teto_maximo": 12000,
    "multiplos_editais": true,
    "confidencialidade_anos": 5,
    "trade_secrets_perpettuo": true
  },
  "riscos": ["proprietary_algorithms", "strategic_contacts", "market_strategy"]
}
```

**Output**:
```
Arquivo: nda_projeto_x_customizado.pdf
Seções:
  - Identificação das partes
  - Definições (IC, Propriedade Intelectual)
  - Escopo e finalidade
  - Obrigações de confidencialidade
  - Exceções limitadas
  - Titularidade de PI
  - Success Fee (com teto)
  - Duração e obrigações perpétuas
  - Sanções (multa R$ 250k-500k)
  - Jurisdição (Salvador, mediação prévia)
```

**Funcionalidades**:
- [ ] 5 templates base (Centelha, PIPE, Finep, Genérico, Internacional)
- [ ] Motor de templates (Jinja2)
- [ ] Parametrização de termos
- [ ] Guia de negociação (30 cenários + respostas)
- [ ] Escala de fairness ("é abusivo?" automático)
- [ ] Checklist pré-assinatura
- [ ] Exportar PDF assinável

**Implementação**:
```python
class NDAGenerator:
    def __init__(self, template_type="centelha"):
        # Carrega template base
        pass
    
    def fill_template(self, projeto, consultor, termos):
        # Preenche placeholders
        pass
    
    def validate_fairness(self):
        # Verifica se termos são justos (score 1-10)
        pass
    
    def generate_negotiation_guide(self):
        # Guia de negociação com cenários
        pass
```

**CLI**:
```bash
editalshield nda \
  --project-name "Projeto X" \
  --founders "João,Adriano" \
  --consultant-name "RS Advogados" \
  --success-fee 20 \
  --teto 12000 \
  --template centelha \
  --output nda_projeto_x.pdf
```

---

### **Módulo 4: Memorial Protector** (Preparação - JÁ IMPLEMENTADO)
**Objetivo**: Detectar e proteger trade secrets em memoriais técnicos

**Problema que resolve**: Startup expõe PI desnecessariamente em memoriais

**Input**:
```
Texto bruto do memorial (1000-2000 palavras)
Nível de sensibilidade (low/medium/high)
```

**Output**:
```json
{
  "risk_score": 35,
  "summary": {
    "critical": 2,
    "medium": 5,
    "low": 1
  },
  "findings": [
    {
      "line": 47,
      "text": "Algoritmo XYZ com parâmetros W, V, K...",
      "risk": "critical",
      "reason": "Expõe nome e parâmetros do algoritmo proprietário",
      "suggestion": "Modelo proprietário de análise comportamental..."
    }
  ],
  "recommendation": "Nível de risco MÉDIO: revise 3 seções marcadas",
  "protected_version": "memorial_protegido.md"
}
```

**Funcionalidades**:
- [x] Detector de padrões sensíveis (regex + keywords)
- [x] Score de risco (0-100)
- [x] Gerador de versão protegida
- [x] Relatório em JSON/Markdown/HTML
- [x] Checklist pré-submissão

**Status**: ✅ IMPLEMENTADO (código pronto)

---

### **Módulo 5: Cost Calculator** (Pós-Aprovação)
**Objetivo**: Calcular success fees com precisão e simular cenários financeiros

**Problema que resolve**: Falta de transparência em cálculos de honorários

**Input**:
```json
{
  "valor_aprovado": 86000,
  "success_fee_pct": 20,
  "teto_maximo": 12000,
  "parcelas": 3,
  "glosa_estimada": 0
}
```

**Output**:
```json
{
  "cenarios": {
    "A_aprovado_integral": {
      "probabilidade": 0.40,
      "valor_recurso": 86000,
      "success_fee": 12000,
      "liquido_projeto": 74000,
      "status": "ideal"
    },
    "B_aprovado_parcial": {
      "probabilidade": 0.25,
      "valor_recurso": 60000,
      "success_fee": 12000,
      "liquido_projeto": 48000,
      "status": "sobrevivel"
    },
    "C_glosa_rubrica_juridica": {
      "probabilidade": 0.15,
      "valor_recurso": 86000,
      "success_fee": 0,
      "liquido_projeto": 86000,
      "status": "protegido_nda"
    },
    "D_nao_aprovado": {
      "probabilidade": 0.20,
      "valor_recurso": 0,
      "success_fee": 0,
      "liquido_projeto": 0,
      "status": "sem_risco"
    }
  },
  "propabilidade_positiva": 0.65,
  "fluxo_por_parcela": [
    {"parcela": 1, "recurso": 28667, "fee": 4000, "liquido": 24667},
    {"parcela": 2, "recurso": 28667, "fee": 4000, "liquido": 24667},
    {"parcela": 3, "recurso": 28666, "fee": 4000, "liquido": 24666}
  ],
  "termo_liquidacao": "termo_liquidacao_auto.pdf"
}
```

**Funcionalidades**:
- [ ] Fórmula exata de success fee (com teto)
- [ ] Simulador de 4 cenários (Monte Carlo)
- [ ] Cálculo por parcela
- [ ] Gerador automático de termo de liquidação
- [ ] Impacto de glosas
- [ ] Dashboard financeiro

**Implementação**:
```python
class CostCalculator:
    def __init__(self, valor_aprovado, success_fee_pct, teto):
        pass
    
    def calcular_success_fee(self, parcelas=None, glosa=0):
        # Retorna cálculo por parcela + termo
        pass
    
    def simular_cenarios(self):
        # Retorna 4 cenários com probabilidades
        pass
    
    def gerar_termo_liquidacao(self):
        # PDF assinável com cálculo detalhado
        pass
```

**CLI**:
```bash
editalshield calculate \
  --valor-aprovado 86000 \
  --success-fee 20 \
  --teto 12000 \
  --parcelas 3 \
  --output termo_liquidacao.pdf
```

---

### **Módulo 6: Scenario Planner** (Execução)
**Objetivo**: Planejar cenários pós-aprovação e contingências

**Problema que resolve**: Startup desamparada se edital glosar ou consultor desaparecer

**Input**:
```json
{
  "edital": "centelha_ba_2025",
  "valor_aprovado": 86000,
  "nda_assinado": true,
  "riscos": ["glosa_rubrica_juridica", "consultor_desaparecimento"]
}
```

**Output**:
```json
{
  "cenarios": [
    {
      "nome": "Aprovado Integral + Executado Normal",
      "probabilidade": 0.60,
      "ações": ["Pagar success fee conforme termo", "Prosseguir com projeto"],
      "template": "success_path.md"
    },
    {
      "nome": "Glosa Rubrica Jurídica (não pode pagar advogado)",
      "probabilidade": 0.15,
      "ações": [
        "Ativar Cláusula 6.2 do NDA",
        "Renegociar com consultor (equity vs. cash)",
        "Solicitar extensão de prazo"
      ],
      "template": "glosa_response_playbook.md",
      "contato_urgencia": "email_template_renegociacao.txt"
    },
    {
      "nome": "Contingenciamento (edital libera menos)",
      "probabilidade": 0.15,
      "ações": ["Recalcular success fee com novo valor", "Renegociar com SLA"],
      "template": "contingency_plan.md"
    },
    {
      "nome": "Não Aprovado",
      "probabilidade": 0.10,
      "ações": ["Nenhuma obrigação de payment", "Reutilizar material para próximo edital"],
      "template": "rejection_response.md"
    }
  ],
  "matriz_risco": "scenario_matrix.csv",
  "playbooks": ["templates_de_resposta_gerados"]
}
```

**Funcionalidades**:
- [ ] 4+ cenários pré-mapeados
- [ ] Matriz de risco (probabilidade vs. impacto)
- [ ] Playbooks de resposta (templates)
- [ ] Email templates de renegociação
- [ ] Cronograma de ações por cenário
- [ ] SOS: "O edital glosou, o que faço?" (wizard interativo)

**Implementação**:
```python
class ScenarioPlanner:
    def __init__(self, edital_id, valor_aprovado, nda_data):
        pass
    
    def gerar_cenarios(self):
        # Retorna matriz de cenários
        pass
    
    def playbook(self, cenario_id):
        # Retorna plano de ação específico
        pass
    
    def sos_wizard(self, problema_descrito):
        # Wizard interativo para responder
        pass
```

---

## 📁 Estrutura de Diretórios (Completa)

```
editalshield/
│
├── README.md                          # Genérico, sem dados específicos
├── LICENSE                            # MIT
├── pyproject.toml                     # Setup Python
├── requirements.txt                   # Dependências
├── .gitignore
├── CONTRIBUTING.md                    # Como contribuir
│
├── src/editalshield/
│   ├── __init__.py
│   ├── __version__.py
│   ├── config.py                      # Configurações globais
│   │
│   ├── modules/                       # 6 MÓDULOS
│   │   ├── __init__.py
│   │   ├── edital_selector.py         # Módulo 1
│   │   ├── gap_analyzer.py            # Módulo 2
│   │   ├── nda_generator.py           # Módulo 3
│   │   ├── memorial_protector.py      # Módulo 4 (pronto)
│   │   ├── cost_calculator.py         # Módulo 5
│   │   └── scenario_planner.py        # Módulo 6
│   │
│   ├── templates/                     # Templates parametrizados
│   │   ├── nda_centelha.md            # [PLACEHOLDERS]
│   │   ├── nda_pipe.md
│   │   ├── nda_finep.md
│   │   ├── nda_generic.md
│   │   ├── memorial_structure.md
│   │   ├── termo_liquidacao.md
│   │   └── scenario_playbooks/        # Templates por cenário
│   │       ├── glosa_response.md
│   │       ├── contingency_plan.md
│   │       └── rejection_response.md
│   │
│   ├── data/                          # Base de dados genérica
│   │   ├── editais_brasil.json        # 20+ editais públicos
│   │   ├── criterios_padrao.json      # Critérios genéricos
│   │   ├── trade_secrets_keywords.json # Keywords universais
│   │   └── fórmulas.json              # Fórmulas de cálculo
│   │
│   └── utils/
│       ├── text_analyzer.py           # NLP genérico
│       ├── pdf_generator.py           # Gerar PDFs
│       ├── validators.py              # Validações
│       └── formatters.py              # Formatação de output
│
├── cli/
│   ├── __init__.py
│   └── editalshield_cli.py            # CLI unificada (6 comandos)
│
├── notebooks/                         # Tutoriais com dados fictícios
│   ├── 00_quickstart.ipynb
│   ├── 01_edital_selector_tutorial.ipynb
│   ├── 02_gap_analyzer_tutorial.ipynb
│   ├── 03_nda_generator_tutorial.ipynb
│   ├── 04_memorial_protector_tutorial.ipynb
│   ├── 05_cost_calculator_tutorial.ipynb
│   └── 06_scenario_planner_tutorial.ipynb
│
├── tests/
│   ├── __init__.py
│   ├── test_edital_selector.py        # Mock data
│   ├── test_gap_analyzer.py
│   ├── test_nda_generator.py
│   ├── test_memorial_protector.py     # JÁ PRONTO
│   ├── test_cost_calculator.py
│   └── test_scenario_planner.py
│
├── examples/                          # ÚNICA PASTA COM DADOS FICTÍCIOS
│   ├── example_varejo_tech/
│   │   ├── projeto_config.json        # Projeto fictício
│   │   ├── memorial_raw.md            # Memorial exemplo
│   │   ├── memorial_protected.md      # Output
│   │   └── README.md
│   │
│   ├── example_healthtech/
│   │   └── [estrutura similar]
│   │
│   └── example_fintech/
│       └── [estrutura similar]
│
└── docs/
    ├── whitepaper_tecnico.pdf         # AQUI: dados reais + validação
    ├── whitepaper_executivo.pdf       # AQUI: case GuardDrive anonimizado
    ├── architecture.md                # Diagrama dos 6 módulos
    ├── api_reference.md               # Documentação das classes
    ├── cli_usage.md                   # Exemplos de CLI
    └── contributing.md                # Como contribuir
```

---

## 🔧 Dependências (requirements.txt)

```
click>=8.1          # CLI
jinja2>=3.0         # Templates
pydantic>=2.0       # Validação
reportlab>=4.0      # PDF generation
python-dotenv>=1.0
requests>=2.28      # HTTP calls (web scraper editais)
numpy>=1.24         # Cálculos
```

---

## 🧪 Plano de Testes

### Cobertura: 95%+

**Módulo 1 (Edital Selector)**:
- [ ] Mock 20 editais, testar ranking
- [ ] Testar fit_score para diferentes perfis
- [ ] Testar cálculo de ROI

**Módulo 2 (Gap Analyzer)**:
- [ ] Carregar critérios Centelha, testar análise
- [ ] Validar checklist
- [ ] Testar gerador de plano de ação

**Módulo 3 (NDA Generator)**:
- [ ] Testar preenchimento de template
- [ ] Validar parametrização (placeholders)
- [ ] Testar fairness check
- [ ] Exportar PDF

**Módulo 4 (Memorial Protector)**:
- [x] JÁ PRONTO (95%+ coverage)

**Módulo 5 (Cost Calculator)**:
- [ ] Testar fórmula com teto
- [ ] Simular cenários
- [ ] Testar por parcela
- [ ] Gerar termo

**Módulo 6 (Scenario Planner)**:
- [ ] Testar geração de cenários
- [ ] Validar playbooks
- [ ] Testar wizard interativo

---

## 📊 Dados Públicos Base (data/editais_brasil.json)

```json
{
  "editais": [
    {
      "id": "centelha_ba_2025",
      "nome": "Centelha Bahia III",
      "orgao": "FAPESB/FINEP",
      "ano": 2025,
      "estado": "BA",
      "valor_minimo": 60000,
      "valor_maximo": 100000,
      "contrapartida_pct": 0,
      "prazo_ciclo_dias": 180,
      "taxa_aprovacao_estimada": 0.40,
      "setores": ["tecnologia", "varejo", "saude", "educacao"],
      "url": "https://programacentelha.com.br/ba/",
      "critrios": {
        "problema_mercado": 25,
        "solucao": 25,
        "inovacao": 25,
        "equipe": 25
      },
      "fontes": ["web_oficial", "cnpq_base", "observatorio_sebrae"]
    },
    // ... + 19 editais similares
  ]
}
```

---

## 🎬 CLI Completa (6 Comandos)

```bash
# 1. Selector: Qual edital devo escolher?
editalshield select \
  --sector varejo \
  --stage pre-seed \
  --value-min 50000 \
  --value-max 200000

# 2. Gap Analyzer: O que falta?
editalshield analyze-gaps \
  --project-config projeto.json \
  --edital centelha_ba_2025

# 3. NDA Generator: Contrato defensivo
editalshield generate-nda \
  --project-name "Projeto X" \
  --founders "João,Adriano" \
  --consultant "RS Advogados" \
  --success-fee 20 \
  --teto 12000

# 4. Memorial Protector: Proteja sua PI
editalshield protect-memorial \
  --input memorial.md \
  --sensitivity high \
  --output memorial_safe.md \
  --report analysis_report.md

# 5. Cost Calculator: Quanto vou pagar?
editalshield calculate-fee \
  --valor-aprovado 86000 \
  --success-fee 20 \
  --teto 12000 \
  --parcelas 3

# 6. Scenario Planner: E se der errado?
editalshield plan-scenarios \
  --edital centelha_ba_2025 \
  --valor-aprovado 86000 \
  --nda-file nda_assinado.pdf
```

---

## 📝 Whitepaper Structure

### **Técnico** (8-12 páginas, arXiv)
- Problema em 7 gaps
- Arquitetura dos 6 módulos
- **Validação com dados reais (anonimizados)**:
  - Setor varejo, valor ~R$ 86k, edital Centelha BA
  - Resultados: ↓82% exposição PI, ↓30% custos
- Discussão e trabalhos futuros

### **Executivo** (4-6 páginas, comercial)
- Dor do mercado
- Benefícios EditalShield
- Case (varejo tech, anonimizado)
- Roadmap
- Chamada: "Teste grátis por 14 dias"

---

## ✅ Checklist Final

**Antes de commitar para o GitHub**:

- [ ] Nenhum dado pessoal no código (CPF, email, nome real)
- [ ] Nenhum projeto específico mencionado no código
- [ ] Todos os placeholders em templates ({{NOME}}, {{CPF}}, etc.)
- [ ] Tests passando (95%+ coverage)
- [ ] README.md genérico e claro
- [ ] 6 notebooks funcionando (dados fictícios)
- [ ] Whitepapers prontos (validação com dados anonimizados)
- [ ] CLI testada localmente
- [ ] CONTRIBUTING.md pronto
- [ ] LICENSE (MIT) incluído

---

## 🚀 Cronograma (2 Semanas Intensas)

| Dia | Atividade | Módulos |
|-----|-----------|---------|
| **1-2** | Setup repo + Módulo 1 | Edital Selector |
| **3-4** | Módulo 2 + 5 | Gap Analyzer + Cost Calculator |
| **5-6** | Módulo 3 | NDA Generator |
| **7** | Módulo 6 | Scenario Planner |
| **8-9** | Testes completos | Todos |
| **10-11** | Documentação + Notebooks | Tutoriais |
| **12-14** | Whitepapers + Polish | Publicação pronta |

---

## 📞 Contato para Dúvidas (Dentro do Código)

Cada módulo terá:
- Docstrings completas
- Exemplos de uso em docstring
- Type hints
- Comentários em pontos complexos

Notebooks irão responder:
- "Como usar Módulo X?"
- "Como integrar Módulo X + Y?"
- "Como extender para caso específico?"
