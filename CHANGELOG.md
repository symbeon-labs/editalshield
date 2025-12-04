# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.1.0] - 2025-12-04

### 🎉 Lançamento Inicial

#### Adicionado
- Estrutura completa do projeto EditalShield
- Configuração do projeto Python (`pyproject.toml`, `requirements.txt`)
- Sistema de módulos base:
  - `src/editalshield/` com estrutura modular
  - `src/editalshield/config.py` para configurações globais
  - Estrutura para 6 módulos principais
- Interface CLI base em `cli/`
- Estrutura de testes em `tests/`
- Diretórios para notebooks tutoriais
- Diretórios para exemplos fictícios
- Documentação completa:
  - `README.md` principal
  - `CONTRIBUTING.md` com diretrizes de contribuição
  - `LICENSE` (MIT)
  - `docs/architecture.md` com arquitetura detalhada
  - READMEs em subdiretórios
- `.gitignore` configurado para Python
- Documentos de especificação movidos para `docs/`:
  - `EditalShield_Complete_Spec.md`
  - `EditalShield_Agent_Instructions.md`
  - `EditalShield_Gap_Analysis_v1.md`
  - `EditalShield_Whitepaper_Executivo.md`
  - `EditalShield_Whitepaper_Tech.tex`
  - `editalshield_gap_coverage_analysis.json`

#### Estrutura de Diretórios
```
editalshield/
├── src/editalshield/
│   ├── modules/
│   ├── templates/
│   │   └── scenario_playbooks/
│   ├── data/
│   └── utils/
├── cli/
├── notebooks/
├── tests/
├── examples/
│   ├── example_varejo_tech/
│   ├── example_healthtech/
│   └── example_fintech/
└── docs/
```

### 📋 Próximos Passos

#### Em Desenvolvimento
- [ ] Implementação do Módulo 1 (Edital Selector)
- [ ] Implementação do Módulo 2 (Gap Analyzer)
- [ ] Implementação do Módulo 3 (NDA Generator)
- [ ] Implementação do Módulo 4 (Memorial Protector)
- [ ] Implementação do Módulo 5 (Cost Calculator)
- [ ] Implementação do Módulo 6 (Scenario Planner)
- [ ] CLI completa com 6 comandos
- [ ] Base de dados de editais brasileiros
- [ ] Templates parametrizados
- [ ] Testes unitários (cobertura >= 95%)
- [ ] Notebooks tutoriais
- [ ] Exemplos fictícios completos

---

## [Unreleased]

### Planejado para v0.2
- ML para classificação automática de sensibilidade
- API REST
- Dashboard web
- Integração com sistemas externos

### Planejado para v0.3
- Expansão para editais internacionais (NSF, Horizon Europe)
- Automação de scraping de editais
- Monitoramento pós-aprovação

---

## Tipos de Mudanças

- **Adicionado** para novas funcionalidades
- **Modificado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para vulnerabilidades corrigidas
