# 🎯 Sprint 1-2 Checklist: Production-Ready Core
### Semanas 1-2 | EditalShield v1.0.0

**Branch:** `sprint-1-production-ready`  
**Responsável:** João (Symbeon Labs)  
**Deadline:** 2 semanas a partir de hoje

---

## ✅ Status Geral

- **Total Tasks:** 20
- **Completed:** 5 (25%)
- **In Progress:** 0
- **Blocked:** 0

---

## 📋 TAREFAS

### 🧪 1. Testes & Qualidade (6 tasks)

#### 1.1 Aumentar Cobertura de Testes
- [x] Criar `.github/workflows/tests.yml`
- [ ] Expandir `test_memorial_protector.py`
  - [ ] Testar Pattern Weights
  - [ ] Testar Protection Levels
  - [ ] Testar edge cases
- [ ] Criar `test_juridical_agent.py`
  - [ ] Test all risk levels
  - [ ] Test legal citations
- [ ] Criar `test_knowledge_connectors.py`
  - [ ] Mock USPTO API
  - [ ] Mock ArXiv API
  - [ ] Test novelty checker
- [ ] Criar `test_edital_matcher.py`
  - [ ] Test TF-IDF
  - [ ] Test sector filtering
- [ ] Rodar: `pytest --cov=src/editalshield --cov-report=html`
- [ ] **Meta:** Atingir 80%+ coverage

#### 1.2 Linting & Formatting
- [x] Criar `.github/workflows/lint.yml`
- [ ] Instalar ferramentas: `pip install black flake8 mypy`
- [ ] Rodar `black src/ tests/` (formatar código)
- [ ] Configurar `.flake8` (criar arquivo config)
- [ ] Rodar `flake8 src/ tests/`
- [ ] Rodar `mypy src/` (fix type errors)

#### 1.3 Pre-commit Hooks
- [ ] Instalar: `pip install pre-commit`
- [ ] Criar `.pre-commit-config.yaml`
- [ ] Rodar: `pre-commit install`
- [ ] Testar: fazer commit pequeno

**Comando rápido:**
```bash
pytest --cov=src/editalshield --cov-report=html
open htmlcov/index.html  # Ver relatório
```

---

### 📚 2. Documentação (5 tasks)

#### 2.1 Technical Docs
- [ ] Criar `docs/ARCHITECTURE.md`
  - [ ] Diagrama de componentes
  - [ ] Fluxo de dados
  - [ ] Design decisions
- [ ] Criar `docs/API_REFERENCE.md`
  - [ ] Todas classes e funções
  - [ ] Exemplos de uso
- [ ] Atualizar `docs/MCP_INTEGRATION.md`
  - [ ] Adicionar exemplos práticos
  - [ ] Screenshots (opcional)

#### 2.2 User Docs
- [ ] Criar `docs/USER_GUIDE.md`
  - [ ] Tutorial passo-a-passo
  - [ ] Screenshots do Dashboard
- [ ] Criar `docs/CLI_GUIDE.md`
  - [ ] Todos os comandos
  - [ ] Flags e opções
  - [ ] Exemplos reais

#### 2.3 Academic Paper
- [ ] Revisar `ARTICLE_DRAFT.md`
- [ ] Converter para LaTeX (Overleaf)
- [ ] Submit arXiv: https://arxiv.org/submit

**Dica:** Use ChatGPT para converter MD → LaTeX

---

### 🐳 3. Deployment (4 tasks)

#### 3.1 Docker
- [x] Criar `Dockerfile`
- [x] Criar `docker-compose.yml`
- [x] Criar `.dockerignore`
- [ ] Testar build: `docker-compose build`
- [ ] Testar run: `docker-compose up`
- [ ] Acessar http://localhost:8501 (dashboard)
- [ ] Acessar http://localhost:5050 (pgAdmin)

#### 3.2 Environment
- [x] Criar `.env.example`
- [ ] Copiar: `cp .env.example .env`
- [ ] Editar `.env` com valores reais
- [ ] Adicionar `.env` ao `.gitignore` ✅

**Comando teste Docker:**
```bash
docker-compose up -d db
docker-compose ps  # Verificar status
docker-compose logs db  # Ver logs
```

---

### 🎨 4. Repository (5 tasks)

#### 4.1 README Polish
- [ ] Adicionar badges:
  - [ ] ![Tests](https://github.com/.../workflows/tests/badge.svg)
  - [ ] ![Coverage](https://codecov.io/gh/.../badge.svg)
  - [ ] ![License](https://img.shields.io/badge/license-MIT-blue.svg)
  - [ ] ![Python](https://img.shields.io/badge/python-3.10+-green.svg)
- [ ] Seção "Installation" detalhada
- [ ] Seção "Quick Start" com GIFs
- [ ] Seção "Used By" (após lançamento)

#### 4.2 GitHub Settings
- [ ] **Topics:** python, legal-tech, ip-protection, brazil, grants, ai
- [ ] **About:** "AI-powered IP protection for Brazilian innovation grants"
- [ ] **Website:** https://streamlit-app-url (após deploy)
- [ ] **Issues:** Enable issues
- [ ] **Discussions:** Enable (opcional)

#### 4.3 Templates
- [ ] Criar `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] Criar `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Criar `CONTRIBUTING.md`
- [ ] Criar `CODE_OF_CONDUCT.md`

**Exemplo badge:**
```markdown
[![Tests](https://github.com/symbeon-labs/editalshield/workflows/Tests/badge.svg)](...)
```

---

### ⚖️ 5. License & Legal (2 tasks)

#### 5.1 Open-Source License
- [ ] Confirmar MIT License no `LICENSE` file
- [ ] Adicionar header a todos `.py`:
  ```python
  # Copyright © 2025 Symbeon Labs
  # Licensed under the MIT License
  ```
- [ ] Script para adicionar headers automaticamente

#### 5.2 Contributor Docs
- [ ] Criar `CONTRIBUTING.md`
  - [ ] Como rodar testes
  - [ ] Como fazer PR
  - [ ] Code style guide
- [ ] Criar `CODE_OF_CONDUCT.md` (use template GitHub)

---

## 🎯 DELIVERABLE FINAL

Ao completar este checklist, você terá:

✅ **EditalShield Core v1.0.0**
- 80%+ test coverage
- CI/CD funcionando
- Docker production-ready
- Documentação completa
- Pronto para abrir ao público

---

## 📊 COMO ACOMPANHAR

### Diariamente
```bash
# Ver tasks pendentes
cat docs/SPRINT_1_CHECKLIST.md | grep "\[ \]"

# Rodar testes
pytest --cov

# Verificar linting
black --check src/ && flake8 src/
```

### Semanalmente
- [ ] Review: quantas tasks completadas?
- [ ] Bloqueios identificados?
- [ ] Ajustar timeline se necessário

---

## 🚀 PRÓXIMO PASSO

**AGORA MESMO (próximos 30 min):**

1. Instalar ferramentas:
   ```bash
   pip install pytest pytest-cov black flake8 mypy pre-commit
   ```

2. Rodar testes:
   ```bash
   pytest tests/ -v --cov=src/editalshield
   ```

3. Ver coverage atual:
   ```bash
   pytest --cov=src/editalshield --cov-report=html
   # Abrir htmlcov/index.html no browser
   ```

4. Expandir testes conforme o relatório de coverage

---

**Update este checklist:**
Marque [x] quando completar cada task!

**Última atualização:** 2025-12-05  
**Status:** 🟡 In Progress
