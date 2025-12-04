# EditalShield - Instruções para Agente de Desenvolvimento

## 📌 INSTRUÇÕES CRÍTICAS

**Seu objetivo**: Implementar EditalShield **exatamente** conforme especificação.

---

## 🚫 RESTRIÇÕES ABSOLUTAS

### ❌ PROIBIDO:

1. **Hardcode de dados pessoais**
   - ❌ CPF, email, nome, telefone no código
   - ❌ "João", "Adriano", "GuardDrive", "Symbeon"
   - ❌ Dados de projetos reais em `src/`

2. **Dados específicos em código**
   - ❌ `success_fee = 12000` (valor específico)
   - ❌ `edital = "Centelha BA"` (hardcoded)
   - ❌ `projeto_nome = "GuardDrive"` (hardcoded)

3. **Não-genérico em utils/templates**
   - ❌ Template NDA com nomes reais preenchidos
   - ❌ Exemplo de memorial que é verdadeiro

### ✅ OBRIGATÓRIO:

1. **Parametrização 100%**
   - ✅ `def calcular_fee(valor, pct, teto):`
   - ✅ `nda = NDAGenerator(template_type="{{TIPO}}")`
   - ✅ Tudo via CLI/input do usuário

2. **Templates com placeholders**
   - ✅ `Contratante: {{EMPRESA_NOME}}`
   - ✅ `CPF: {{FUNDADOR_CPF}}`
   - ✅ `Valor: R$ {{VALOR_APROVADO}}`

3. **Dados em `data/` = públicos**
   - ✅ `editais_brasil.json` → dados públicos (FAPESB, FINEP, etc.)
   - ✅ `criterios_padrao.json` → critérios genéricos
   - ✅ `trade_secrets_keywords.json` → keywords universais

4. **Exemplos em `examples/` = fictícios**
   - ✅ "RetailTech X" (não GuardDrive)
   - ✅ "HealthTech Y" (não Symbeon)
   - ✅ Dados inventados (CPF fake, emails fake)

---

## 🏗️ ARQUITETURA: Ordem de Implementação

### **FASE 1: Core + Setup (Dias 1-2)**

```bash
# 1. Criar estrutura de diretórios
mkdir -p editalshield/{src/editalshield/{modules,templates,data,utils},cli,notebooks,tests,examples,docs}

# 2. Criar arquivos base
pyproject.toml          # Configuração pip
requirements.txt        # Dependências
src/editalshield/__init__.py
src/editalshield/config.py
cli/editalshield_cli.py
```

**Arquivo**: `src/editalshield/__init__.py`
```python
"""EditalShield - Framework para proteção de PI em editais brasileiros."""
__version__ = "0.1.0"
__author__ = "João M. Oliveira"
__license__ = "MIT"

from editalshield.modules import (
    EditalSelector,
    GapAnalyzer,
    NDAGenerator,
    MemorialProtector,
    CostCalculator,
    ScenarioPlanner,
)

__all__ = [
    "EditalSelector",
    "GapAnalyzer",
    "NDAGenerator",
    "MemorialProtector",
    "CostCalculator",
    "ScenarioPlanner",
]
```

**Arquivo**: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "editalshield"
version = "0.1.0"
description = "Framework sistemático para proteção de PI em editais de inovação brasileiros"
authors = [{name = "João Manoel Oliveira", email = "contato@symbeon.lab"}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = ["click>=8.1", "jinja2>=3.0", "pydantic>=2.0", "reportlab>=4.0"]

[project.scripts]
editalshield = "cli.editalshield_cli:cli"
```

---

### **FASE 2: Base de Dados Genérica (Dias 2-3)**

**Arquivo**: `src/editalshield/data/editais_brasil.json`

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
      "url_oficial": "https://programacentelha.com.br/ba/",
      "criterios": {
        "problema_mercado": 25,
        "solucao": 25,
        "inovacao": 25,
        "equipe": 25
      }
    },
    {
      "id": "pipe_fapesp_2025_fase1",
      "nome": "PIPE FAPESP Fase 1",
      "orgao": "FAPESP",
      "ano": 2025,
      "estado": "SP",
      "valor_minimo": 200000,
      "valor_maximo": 300000,
      "contrapartida_pct": 10,
      "prazo_ciclo_dias": 360,
      "taxa_aprovacao_estimada": 0.15,
      "setores": ["tecnologia", "biotech", "saude"],
      "url_oficial": "https://www.fapesp.br/pipe",
      "criterios": {
        "inovacao": 40,
        "viabilidade": 30,
        "equipe": 30
      }
    }
    // ... + 18 editais similares
  ]
}
```

**Arquivo**: `src/editalshield/data/trade_secrets_keywords.json`
```json
{
  "proprietary_frameworks": [
    "framework proprietário",
    "sistema [A-Za-z]+",
    "engine interno",
    "plataforma customizada"
  ],
  "algorithm_patterns": [
    "algoritmo [A-Za-z0-9_]+",
    "modelo [A-Za-z0-9_]+",
    "função de risco [A-Za-z0-9_]+"
  ],
  "sensitive_metrics": [
    "threshold",
    "parâmetro",
    "coeficiente",
    "peso",
    "limiar"
  ],
  "dangerous_exposures": [
    "arquitetura de dados",
    "pipeline de processamento",
    "fórmula matemática",
    "número de usuários",
    "receita"
  ]
}
```

---

### **FASE 3: Módulo 1 - Edital Selector (Dias 3-4)**

**Arquivo**: `src/editalshield/modules/edital_selector.py`

```python
"""Módulo 1: Edital Selector - Comparar e recomendar editais."""

import json
from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel


class ProjetoProfile(BaseModel):
    """Perfil do projeto para buscar editais adequados."""
    setor: str  # "varejo", "saude", "biotech", etc.
    estagio: str  # "pre-seed", "seed", "series-a"
    valor_minimo: float
    valor_maximo: float
    tempo_disponivel_meses: int
    localizacao: str  # "nacional", "SP", "BA", etc.


class EditalScore(BaseModel):
    """Score de adequação de um edital ao projeto."""
    edital_id: str
    edital_nome: str
    fit_score: int  # 0-100
    valor_disponivel: float
    prazo_meses: int
    taxa_aprovacao: float
    roi_estimado: float
    motivo_score: str


class EditalSelector:
    """Compara editais e recomenda melhor fit."""
    
    def __init__(self, editais_path: str = None):
        """
        Inicializa seletor com base de editais.
        
        Args:
            editais_path: Caminho para editais.json (default: src/editalshield/data/editais_brasil.json)
        """
        if editais_path is None:
            editais_path = Path(__file__).parent.parent / "data" / "editais_brasil.json"
        
        with open(editais_path, "r", encoding="utf-8") as f:
            self.editais_raw = json.load(f)
    
    def rank(self, projeto: ProjetoProfile) -> List[EditalScore]:
        """
        Retorna ranking de editais por fit_score.
        
        Args:
            projeto: Perfil do projeto
        
        Returns:
            Lista de EditalScore ordenada por fit_score (descendente)
        """
        scores = []
        
        for edital in self.editais_raw["editais"]:
            score = self._calcular_fit_score(projeto, edital)
            scores.append(score)
        
        return sorted(scores, key=lambda x: x.fit_score, reverse=True)
    
    def _calcular_fit_score(self, projeto: ProjetoProfile, edital: Dict) -> EditalScore:
        """Calcula fit_score entre projeto e edital."""
        score = 0
        motivos = []
        
        # Critério 1: Valor (40 pontos)
        if edital["valor_minimo"] <= projeto.valor_minimo and projeto.valor_maximo <= edital["valor_maximo"]:
            score += 40
            motivos.append("Valor adequado ao edital")
        else:
            score += max(0, 40 - abs(projeto.valor_minimo - edital["valor_minimo"]) / 10000)
        
        # Critério 2: Setor (30 pontos)
        if projeto.setor in edital["setores"]:
            score += 30
            motivos.append(f"Setor '{projeto.setor}' elegível")
        else:
            motivos.append(f"Setor '{projeto.setor}' não listado (risco)")
        
        # Critério 3: Prazo (20 pontos)
        if edital["prazo_ciclo_dias"] / 30 <= projeto.tempo_disponivel_meses:
            score += 20
            motivos.append("Prazo adequado")
        
        # Critério 4: Taxa de aprovação (10 pontos)
        if edital["taxa_aprovacao_estimada"] >= 0.25:
            score += 10
            motivos.append("Taxa de aprovação aceitável")
        
        roi = edital["valor_maximo"] - (edital["valor_maximo"] * 0.20)  # Menos 20% de success fee
        
        return EditalScore(
            edital_id=edital["id"],
            edital_nome=edital["nome"],
            fit_score=int(min(score, 100)),
            valor_disponivel=edital["valor_maximo"],
            prazo_meses=int(edital["prazo_ciclo_dias"] / 30),
            taxa_aprovacao=edital["taxa_aprovacao_estimada"],
            roi_estimado=roi,
            motivo_score=" | ".join(motivos)
        )
    
    def compare(self, edital_ids: List[str]) -> Dict:
        """Compara N editais em tabela."""
        resultado = {"editais_comparados": [], "recomendacao": ""}
        
        for edital_id in edital_ids:
            edital = next((e for e in self.editais_raw["editais"] if e["id"] == edital_id), None)
            if edital:
                resultado["editais_comparados"].append(edital)
        
        return resultado
```

**CLI para Módulo 1**:
```python
@click.command()
@click.option("--sector", required=True, help="Setor: varejo, saude, biotech, etc.")
@click.option("--stage", required=True, help="Estágio: pre-seed, seed, series-a")
@click.option("--value-min", type=int, required=True, help="Valor mínimo desejado")
@click.option("--value-max", type=int, required=True, help="Valor máximo desejado")
@click.option("--time-months", type=int, required=True, help="Meses disponíveis")
def select(sector, stage, value_min, value_max, time_months):
    """Recomenda melhor edital para seu projeto."""
    projeto = ProjetoProfile(
        setor=sector,
        estagio=stage,
        valor_minimo=value_min,
        valor_maximo=value_max,
        tempo_disponivel_meses=time_months,
        localizacao="nacional"
    )
    
    selector = EditalSelector()
    ranking = selector.rank(projeto)
    
    click.echo("\n📊 RANKING DE EDITAIS RECOMENDADOS\n")
    for i, score in enumerate(ranking[:5], 1):
        click.echo(f"{i}. {score.edital_nome}")
        click.echo(f"   Fit Score: {score.fit_score}/100")
        click.echo(f"   Valor: R$ {score.valor_disponivel:,.0f}")
        click.echo(f"   Prazo: {score.prazo_meses} meses")
        click.echo(f"   Taxa aprovação: {score.taxa_aprovacao*100:.0f}%\n")
```

---

### **FASE 4: Módulos 2, 3, 5, 6 (Dias 5-10)**

Seguir **exatamente** o mesmo padrão do Módulo 1:

1. **Classe principal** com `__init__` genérico
2. **Input/Output como Pydantic models** (type-safe)
3. **Métodos públicos** que aceitam inputs parametrizados
4. **Sem hardcoding** em lugar nenhum
5. **CLI command** correspondente

**Estrutura padrão**:
```python
# src/editalshield/modules/modulo_x.py

from pydantic import BaseModel
from typing import Dict, List

class InputModel(BaseModel):
    """Input para Módulo X."""
    parametro1: str
    parametro2: int
    # ...

class OutputModel(BaseModel):
    """Output do Módulo X."""
    resultado1: str
    resultado2: List[Dict]
    # ...

class ModuloX:
    def __init__(self, config_path=None):
        # Carrega configuração genérica
        pass
    
    def processar(self, input_data: InputModel) -> OutputModel:
        # Lógica principal (100% genérica)
        pass
```

---

### **FASE 5: Módulo 4 - Memorial Protector (Dia 0 ⭐)**

**STATUS**: ✅ JÁ IMPLEMENTADO

Arquivos a usar:
- Código: `src/editalshield/modules/memorial_protector.py` (já pronto)
- Testes: `tests/test_memorial_protector.py` (ja pronto)

**NÃO MODIFICAR** - apenas integrar com CLI.

---

### **FASE 6: Templates Genéricos (Dia 8)**

**Arquivo**: `src/editalshield/templates/nda_centelha.md`

```markdown
# ACORDO DE CONFIDENCIALIDADE E PROTEÇÃO DE PROPRIEDADE INTELECTUAL

**Data**: {{DATA}}

## PARTES

**CONTRATANTE** ("Consultor"):
{{CONSULTOR_EMPRESA}}
CNPJ: {{CONSULTOR_CNPJ}}
Representante: {{CONSULTOR_REPRESENTANTE}}

**CONTRATADA** ("Startup"):
{{STARTUP_NOME}}
CPF/CNPJ: {{STARTUP_CNPJ}}
Fundadores: {{FUNDADORES_NOMES}}

## 1. DEFINIÇÕES

**Informações Confidenciais**: Toda informação técnica, comercial, financeira, 
estratégica compartilhada sobre o projeto {{PROJETO_NOME}}, incluindo:
- Arquitetura técnica
- Parâmetros e algoritmos
- Modelos financeiros
- Contatos estratégicos
- Roadmap e planos futuros

**Propriedade Intelectual ("PI")**: Toda invenção, software, marca, segredo 
comercial, framework, metodologia desenvolvida por {{STARTUP_NOME}}.

## 2. OBRIGAÇÕES DE CONFIDENCIALIDADE

O Consultor obriga-se a:
- Manter sigilo absoluto sobre as Informações Confidenciais
- Não divulgar para terceiros sem consentimento escrito
- Usar exclusivamente para fins de {{EDITAL_NOME}}
- Destruir/retornar documentos ao fim do serviço

## 3. PROPRIEDADE INTELECTUAL

Toda PI desenvolvida anteriormente por {{STARTUP_NOME}} permanece de propriedade 
exclusiva da Startup. Trabalhos desenvolvidos pelo Consultor pertencem à Startup.

## 4. REMUNERAÇÃO

- **Success Fee**: {{SUCCESS_FEE_PCT}}% do valor aprovado
- **Teto máximo**: R$ {{TETO_MAXIMO}}
- **Cálculo**: min(valor_aprovado × {{SUCCESS_FEE_PCT}}%, {{TETO_MAXIMO}})
- **Múltiplos editais**: {{MULTIPLOS_EDITAIS_CLAUSULA}}

## 5. DURAÇÃO

- **Confidencialidade**: {{CONFIDENCIALIDADE_ANOS}} anos a partir da assinatura
- **Proteção perpétua**: Trade secrets são protegidos perpetuamente

## 6. SANÇÕES POR VIOLAÇÃO

Qualquer violação deste NDA implica em:
- Multa de R$ {{MULTA_MIN}} a R$ {{MULTA_MAX}}
- Indenização por danos morais e materiais
- Ação judicial na jurisdição de {{JURISDICAO}}

---

Assinado em {{DATA}} em {{LOCAL}}.

{{CONSULTOR_ASSINATURA}}        {{STARTUP_ASSINATURA_1}}
_________________________        _________________________
{{CONSULTOR_NOME}}              {{FUNDADOR_1_NOME}}

                                {{STARTUP_ASSINATURA_2}}
                                _________________________
                                {{FUNDADOR_2_NOME}}
```

**Arquivo**: `src/editalshield/utils/pdf_generator.py`

```python
"""Gerar PDFs a partir de templates."""

from jinja2 import Template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def render_template(template_md: str, context: Dict) -> str:
    """
    Preenche template markdown com contexto.
    
    Args:
        template_md: Conteúdo do template com {{PLACEHOLDERS}}
        context: Dicionário com valores {PLACEHOLDER: valor}
    
    Returns:
        Markdown preenchido
    """
    template = Template(template_md)
    return template.render(**context)
```

---

### **FASE 7: Exemplos Fictícios (Dias 11-12)**

**Arquivo**: `examples/example_varejo_tech/projeto_config.json`

```json
{
  "projeto_nome": "RetailTech X",
  "setor": "varejo",
  "estagio": "pre-seed",
  "valor_min": 50000,
  "valor_max": 100000,
  "equipe": 2,
  "problema": "Falta sistema de análise comportamental em checkout",
  "solucao": "IA para detecção em tempo real",
  "inovacao": "Algoritmo dual-rail proprietário",
  "traction": {
    "usuarios": 10,
    "receita": 0,
    "mvp_pct": 60
  }
}
```

**Arquivo**: `examples/example_varejo_tech/memorial_raw.md`

```markdown
# MEMORIAL TÉCNICO - RetailTech X

## 1. Problema
O varejo físico carece de ferramentas para análise comportamental de fraude 
em checkout. Estimamos que 3-5% das transações têm risco comportamental.

## 2. Solução Proposta
Desenvolvemos algoritmo BehaviorAnalyzer V2 com parâmetros W=0.7, V=0.3, K=1.5
que processa cada transação em <100ms. Taxa de acurácia: 91%.

## 3. Diferencial Competitivo
Nossa arquitetura usa dual-rail validation em GPU. Modelo foi treinado em 
dataset privado de 2M transações da Loja X com ROI de 240%.

...
```

---

### **FASE 8: Testes Unitários (Dias 12-13)**

Cada módulo:
```python
# tests/test_modulo_x.py

import pytest
from editalshield.modules import ModuloX


class TestModuloX:
    def setup_method(self):
        """Setup antes de cada teste."""
        self.modulo = ModuloX()
    
    def test_input_validation(self):
        """Testa validação de input."""
        with pytest.raises(ValueError):
            self.modulo.processar(InputModel(parametro_invalido=""))
    
    def test_output_structure(self):
        """Testa estrutura de output."""
        resultado = self.modulo.processar(InputModel(parametro1="valor"))
        assert hasattr(resultado, "resultado1")
        assert isinstance(resultado.resultado2, list)
    
    def test_generico_parametrizado(self):
        """Testa que módulo funciona com qualquer input parametrizado."""
        inputs = [
            InputModel(parametro1="input_a", parametro2=100),
            InputModel(parametro1="input_b", parametro2=200),
        ]
        for inp in inputs:
            resultado = self.modulo.processar(inp)
            assert resultado is not None
```

---

### **FASE 9: Documentação + README (Dia 14)**

**Arquivo**: `README.md`

```markdown
# EditalShield

Framework open-source para análise e proteção de propriedade intelectual 
em submissões a editais de inovação brasileiros.

## 🎯 Para Quem?

Startups, desenvolvedores e aceleradoras que querem:
- Comparar múltiplos editais (Centelha, PIPE, Finep)
- Proteger propriedade intelectual em memoriais
- Negociar contratos de consultoria com fairness
- Planejar cenários financeiros

## ⚡ Instalação

```bash
pip install editalshield
```

## 🚀 Uso Rápido

```bash
# 1. Qual edital é melhor para meu projeto?
editalshield select \
  --sector varejo \
  --stage pre-seed \
  --value-min 50000 \
  --value-max 100000 \
  --time-months 6

# 2. Proteja seu memorial técnico
editalshield protect-memorial \
  --input memorial.md \
  --sensitivity high \
  --output memorial_safe.md

# 3. Gere NDA defensivo
editalshield generate-nda \
  --project-name "Seu Projeto" \
  --founders "Nome1,Nome2" \
  --consultant "Consultoria XYZ"
```

## 📦 Módulos

1. **Edital Selector** - Comparar editais
2. **Gap Analyzer** - Identificar gaps
3. **NDA Generator** - Contratos customizados
4. **Memorial Protector** - Proteger PI
5. **Cost Calculator** - Calcular custos
6. **Scenario Planner** - Planejar contingências

## 📚 Documentação

- [Arquitetura](docs/architecture.md)
- [API Reference](docs/api_reference.md)
- [Whitepaper Técnico](docs/whitepaper_tecnico.pdf)

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Licença

MIT License
```

---

## 🎯 CHECKLIST ANTES DE COMMITAR

**Antes de fazer push para GitHub**:

- [ ] **Zero dados pessoais em `src/`**
  - [ ] Nenhum CPF visível
  - [ ] Nenhum email real
  - [ ] Nenhum nome pessoal hardcoded
  - [ ] Nenhum projeto específico (GuardDrive, Symbeon)

- [ ] **100% parametrizado**
  - [ ] Todos os inputs via CLI ou função
  - [ ] Todos os templates com {{PLACEHOLDERS}}
  - [ ] Nenhum valor hardcoded

- [ ] **Dados públicos em `data/`**
  - [ ] Editais (FAPESB, FINEP, FAPESP - públicos)
  - [ ] Critérios genéricos
  - [ ] Keywords universais

- [ ] **Exemplos fictícios em `examples/`**
  - [ ] "RetailTech X" (não GuardDrive)
  - [ ] CPF/CNPJ fake (ex: 123.456.789-00)
  - [ ] Dados inventados (não reais)

- [ ] **Testes passando**
  - [ ] `pytest tests/` → 100% pass
  - [ ] Coverage ≥ 95%: `pytest --cov`

- [ ] **Documentação completa**
  - [ ] README.md pronto
  - [ ] Docstrings em toda função
  - [ ] Type hints em todas as funções
  - [ ] 6 notebooks funcionando

- [ ] **CLI funcionando**
  - [ ] `editalshield --help` mostra 6 comandos
  - [ ] Cada comando testado localmente

- [ ] **Git setup**
  - [ ] `.gitignore` incluído
  - [ ] LICENSE (MIT) presente
  - [ ] CONTRIBUTING.md pronto

---

## 🔍 SANIDADE CHECK FINAL

**Pergunta-se para cada arquivo**:

1. ❓ Tem dado pessoal ou de projeto específico?
   - **SIM**: ❌ Falha
   - **NÃO**: ✅ Pass

2. ❓ Cada módulo funciona independentemente?
   - **Não**: ❌ Falha
   - **Sim**: ✅ Pass

3. ❓ Um usuário novo consegue usar sem ler código?
   - **Não**: ❌ Falha
   - **Sim (via CLI ou notebook)**: ✅ Pass

4. ❓ Alguém consegue usar EditalShield para seu próprio projeto?
   - **Não**: ❌ Falha
   - **Sim**: ✅ Pass

---

## 📞 EM CASO DE DÚVIDA

**Dúvida**: "Posso colocar dados de GuardDrive em X?"
**Resposta**: Não. Sempre pergunte: "Outro dev consegue entender sem conhecer GuardDrive?" Se não, está específico demais.

**Dúvida**: "Preciso fazer Y hardcoded?"
**Resposta**: Não. Tudo deve ser input do usuário (CLI, arquivo JSON, função arg).

**Dúvida**: "Como faço Z de forma genérica?"
**Resposta**: Use templates com {{PLACEHOLDERS}}, inputs parametrizados, ou load de JSON config.

---

## ✅ PRONTO PARA COMEÇAR?

1. ✅ Leu essa especificação completamente?
2. ✅ Entendeu os 6 módulos?
3. ✅ Entendeu a restrição: ZERO dados específicos no código?
4. ✅ Pronto para implementar da forma genérica?

**SIM?** → Comece pelo Módulo 1 (Edital Selector). Fase 1: setup + base de dados.
