# DocSync - Session Guide

## 🎯 Quick Start Session

Este guia fornece um fluxo completo de uso do DocSync.

---

## 📦 Setup Inicial

```bash
# Clone e instale
git clone https://github.com/SH1W4/docsync.git
cd docsync
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

**Variáveis de Ambiente (.env):**
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
```

---

## 🚀 Comandos Principais

### Melhorar Documentação com IA
```bash
docsync improve README.md                                    # OpenAI (padrão)
docsync improve README.md --provider claude                  # Claude
docsync improve README.md --provider gemini                  # Gemini
docsync improve README.md --provider claude --model claude-3-5-sonnet-20241022
```

### Servidor MCP
```bash
docsync serve  # Inicia servidor para agentes externos
```

**Claude Desktop Config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "docsync": {
      "command": "docsync",
      "args": ["serve"],
      "cwd": "/caminho/para/projeto"
    }
  }
}
```

---

## 🔧 Ferramentas MCP

- `list_docs`: Lista arquivos markdown
- `read_doc(path)`: Lê documento
- `improve_doc(path, provider, model)`: Analisa com IA
- `get_stats`: Estatísticas do projeto

---

## 🧪 Desenvolvimento

```bash
pytest tests/ -v                    # Testes
pytest --cov=docsync               # Com cobertura
black src/ tests/ && isort src/    # Formatação
flake8 src/ && mypy src/           # Linting
```

---

## 🐛 Troubleshooting

**API key not found:** Configure `export OPENAI_API_KEY="..."`  
**MCP não conecta:** Verifique path em `claude_desktop_config.json`  
**Testes falham:** `pip install -e ".[dev]"` e `pytest --cache-clear`

---

## 💡 Dicas

```bash
# Aliases úteis
alias dsi="docsync improve"
alias dss="docsync serve"

# Processar múltiplos arquivos
for file in docs/*.md; do docsync improve "$file" --provider claude; done
```
