# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.2.0] - 2025-11-28

### Added
- 🤖 **AI Integration**: Real LLM support with multiple providers
  - OpenAI (GPT-4o-mini, GPT-4o)
  - Anthropic Claude (3.5 Haiku, 3.5 Sonnet)
  - Google Gemini (2.0 Flash)
- 🔌 **MCP Server**: Model Context Protocol integration
  - `list_docs`: List all markdown files
  - `read_doc`: Read document content
  - `improve_doc`: AI-powered documentation improvements
  - `get_stats`: Project statistics
- 🎨 **CLI Enhancements**:
  - `docsync improve` command with provider selection (`--provider` flag)
  - `docsync serve` command to start MCP server
- 🏗️ **Architecture**:
  - `LLMProvider` interface for extensible AI support
  - Modular provider system for easy extension

### Changed
- 📦 Updated dependencies: `openai`, `anthropic`, `google-generativeai`, `mcp`

### Technical Features
- Full support for external agents (Claude Desktop, IDEs) via MCP
- Provider-agnostic AI interface
- Async MCP server with stdio transport

## [Unreleased]

### Planned
- [ ] Suporte para GitLab/GitHub integrations
- [ ] Plugin system para extensões customizadas
- [ ] Web interface para gerenciamento
- [ ] Docker containerization
- [ ] CI/CD pipeline automation

## [0.1.0] - 2025-01-07

### Added
- 🎉 **Lançamento inicial do DocSync**
- 📝 Sistema de sincronização bidirecional entre arquivos locais e Notion
- 🔄 Engine de sincronização em tempo real com watchdog
- 🎨 Sistema de templates flexível com Jinja2
- 🧪 Suporte para processamento AI-enhanced de documentos
- 📊 Análise de qualidade automática de documentação
- 🔍 Validação metacognitiva de conteúdo
- 🛡️ Sistema de backup automatizado
- 📈 Monitoramento de métricas em tempo real
- 🔧 CLI intuitiva com Rich interface
- ⚙️ Configuração flexível via YAML
- 🧩 Arquitetura modular e extensível

### Technical Features
- **Core**: Sistema base de sincronização
- **Notion Integration**: Cliente completo para API do Notion
- **Templates**: Engine de renderização para relatórios ESG
- **AI Processor**: Processamento inteligente de documentos
- **Utils**: Filtros customizados e utilitários
- **CLI**: Interface de linha de comando rica

### Documentation
- 📖 README abrangente com guias de uso
- 🤝 Guia completo de contribuição
- 💼 Análise detalhada de mercado ($45B TAM)
- 🎯 Templates de negócio para análises competitivas
- 🔧 Documentação técnica completa
- 📋 Exemplos práticos de integração

### Quality Assurance
- ✅ 100% conformidade com PEP 8
- 🧪 Suporte completo para testes unitários e de integração
- 🔍 Type hints em todo o código
- 📊 Configuração para análise de cobertura
- 🎨 Formatação automática com Black
- 📤 Organização de imports com isort
- 🔧 Linting com flake8 e mypy

### Infrastructure
- 📦 Configuração completa de packaging (pyproject.toml)
- 🔄 Setup para CI/CD com GitHub Actions
- 🏗️ Estrutura modular e escalável
- 🛡️ Licença MIT para máxima flexibilidade
- 📋 Pre-commit hooks configurados

## [Future Releases]

### v0.2.0 - Planned Q1 2025
- GitLab/GitHub integrations
- Enhanced AI processing capabilities
- Plugin architecture

### v0.3.0 - Planned Q2 2025
- Web dashboard
- Advanced analytics
- Multi-tenant support

### v1.0.0 - Planned Q3 2025
- Production-ready release
- Enterprise features
- Professional support

---

**Links:**
- [Unreleased]: https://github.com/SH1W4/docsync/compare/v0.2.0...HEAD
- [0.2.0]: https://github.com/SH1W4/docsync/releases/tag/v0.2.0
- [0.1.0]: https://github.com/SH1W4/docsync/releases/tag/v0.1.0

