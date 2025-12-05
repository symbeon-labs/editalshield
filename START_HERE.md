# 🎯 AGORA: Seus Próximos Passos
### Sprint 1 Started! 🚀

---

## ✅ O QUE JÁ ESTÁ PRONTO

Você já tem:
- ✅ Branch `sprint-1-production-ready` criada
- ✅ GitHub Actions configurado (CI/CD)
- ✅ Dockerfile production-ready
- ✅ Docker Compose com PostgreSQL + Dashboard
- ✅ `.env.example` (template de configuração)
- ✅ **Checklist completo:** `docs/SPRINT_1_CHECKLIST.md`

---

## 🏃 PASSO 1: Instalar Ferramentas (5 min)

Abra um terminal novo e rode:

```bash
cd c:\Users\João\Desktop\PROJETOS\00_ECOSYSTEM_COMERCIAL\EDITALSHIELD

# Ativar venv
venv\Scripts\activate

# Instalar ferramentas de testes
pip install pytest pytest-cov black flake8 mypy pre-commit
```

---

## 🧪 PASSO 2: Rodar Testes e Ver Coverage (10 min)

```bash
# Rodar todos os testes
pytest tests/ -v

# Rodar com coverage
pytest --cov=src/editalshield --cov-report=html

# Abrir relatório no browser
start htmlcov\index.html
```

**O que você vai ver:**
- Coverage atual (~60%)
- Arquivos que precisam de mais testes (vermelho/amarelo)
- Linhas não cobertas

---

## 📝 PASSO 3: Expandir Testes (60-90 min)

Baseado no relatório de coverage, adicione testes:

### 1. Expandir `test_memorial_protector.py`

Adicione no final do arquivo:

```python
def test_pattern_weights():
    """Test that Pattern Weights work correctly"""
    protector = MemorialProtector()
    
    # Text with critical IP (algorithm)
    text_high = "O BehaviorAnalyzer V2 é nosso algoritmo proprietário"
    analysis_high = protector.analyze_paragraph(text_high, 0)
    
    # Text with common term
    text_low = "O pipeline de dados processa informações"
    analysis_low = protector.analyze_paragraph(text_low, 0)
    
    # High weight pattern should have higher risk
    assert analysis_high.risk_score > analysis_low.risk_score


def test_protection_levels():
    """Test LOW, MEDIUM, HIGH protection levels"""
    protector = MemorialProtector()
    text = "O algoritmo tem learning_rate=0.01"
    
    # LOW: Remove apenas valores
    protected_low, _ = protector.generate_protected_memorial(text, protection_level="LOW")
    assert "learning_rate" in protected_low  # Contexto mantido
    assert "0.01" not in protected_low  # Valor removido
    
    # MEDIUM: Placeholder genérico
    protected_med, _ = protector.generate_protected_memorial(text, protection_level="MEDIUM")
    assert "[PARÂMETROS OTIMIZADOS]" in protected_med or "[ALGORITMO" in protected_med
    
    # HIGH: Redação agressiva
    protected_high, _ = protector.generate_protected_memorial(text, protection_level="HIGH")
    assert "[REMOVIDO" in protected_high or len(protected_high) < len(text)
```

Salve e rode: `pytest tests/test_core.py::test_pattern_weights -v`

---

### 2. Criar `test_juridical_agent.py`

Crie novo arquivo `tests/test_juridical_agent.py`:

```python
import pytest
from editalshield.modules import JuridicalAgent, MemorialProtector


def test_juridical_agent_low_risk():
    """Test legal opinion for low-risk memorial"""
    agent = JuridicalAgent()
    
    # Simulate low-risk analysis
    mock_analysis = {
        'overall_risk_score': 20,
        'sensitive_patterns': []
    }
    
    opinion = agent.analyze_legal_risk(mock_analysis)
    
    assert opinion.risk_level == "LOW"
    assert "aprovação" in opinion.recommendation.lower() or "seguro" in opinion.recommendation.lower()
    assert len(opinion.citations) == 0  # No violations


def test_juridical_agent_high_risk():
    """Test legal opinion for high-risk memorial"""
    agent = JuridicalAgent()
    
    # Simulate high-risk analysis
    mock_analysis = {
        'overall_risk_score': 85,
        'sensitive_patterns': ['BehaviorAnalyzer V2', 'learning_rate=0.01']
    }
    
    opinion = agent.analyze_legal_risk(mock_analysis)
    
    assert opinion.risk_level in ["HIGH", "MODERATE"]
    assert len(opinion.citations) > 0  # Has legal citations
    assert any("LPI" in c.law or "9.279" in c.law for c in opinion.citations)
```

Rode: `pytest tests/test_juridical_agent.py -v`

---

## 🎨 PASSO 4: Formatar Código (5 min)

```bash
# Formatar automaticamente
black src/ tests/

# Verificar linting
flake8 src/ tests/ --max-line-length=100

# Type checking (vai ter alguns warnings, ok)
mypy src/ --ignore-missing-imports
```

---

## 🐳 PASSO 5: Testar Docker (15 min)

```bash
# Copiar .env
copy .env.example .env

# Editar .env (opcional, mas recomendado)
# Mudar DB_PASSWORD para algo seguro

# Build containers
docker-compose build

# Subir apenas o banco de dados
docker-compose up -d db

# Esperar 10s e verificar
docker-compose ps

# Ver logs
docker-compose logs db

# Se funcionou, subir tudo
docker-compose up
```

**Acessar:**
- Dashboard: http://localhost:8501
- pgAdmin: http://localhost:5050

Pressione `Ctrl+C` para parar.

---

## 📊 PASSO 6: Acompanhar Progresso

Abra `docs/SPRINT_1_CHECKLIST.md` e vá marcando tasks:

```markdown
- [x] Expandir test_memorial_protector.py ✅
- [x] Criar test_juridical_agent.py ✅
- [x] Rodar black ✅
...
```

---

## 🎯 META DA SEMANA 1

Até o final da **Semana 1** (próximos 7 dias):

- [ ] Coverage de testes: 70%+ (atual: ~60%)
- [ ] CI/CD rodando no GitHub (push para ver)
- [ ] Docker funcionando localmente
- [ ] Documentação básica criada

---

## 💡 DICA PRO

Trabalhe em **blocos focados de 90 minutos**:

**Bloco 1 (Hoje):**
- Instalar ferramentas ✅
- Rodar testes e ver coverage ✅
- Expandir 2-3 testes

**Bloco 2 (Amanhã):**
- Criar test_juridical_agent.py
- Criar test_knowledge_connectors.py
- Rodar black + flake8

**Bloco 3:**
- Testar Docker
- Criar documentação USER_GUIDE.md

**Bloco 4:**
- Polish README
- Adicionar badges
- Push para GitHub (ativar CI/CD)

---

## 🆘 PRECISA DE AJUDA?

**Se travar em alguma task:**
1. Veja exemplos em `tests/test_core.py` existentes
2. Use ChatGPT: "Como testar X em pytest?"
3. Consulte docs: https://docs.pytest.org

**Prioridade:**
Testes > Docker > Docs > Polish

---

## 🚀 READY TO GO!

Comece com:

```bash
# 1. Instalar
pip install pytest pytest-cov black

# 2. Rodar
pytest --cov=src/editalshield --cov-report=html

# 3. Ver
start htmlcov\index.html

# 4. Expandir testes baseado no que está vermelho
```

**Boa sorte!** 💪

---

**Criado:** 2025-12-05  
**Sprint:** 1-2 (Production-Ready Core)  
**Deadline:** 2 semanas
