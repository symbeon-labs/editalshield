# DocSync

<div align="center">

![DocSync Logo](./assets/logo.png)

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-v0.2.0-blue.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

**AI-Powered Documentation Agent & Sync Tool**

*Bidirectional synchronization, multi-LLM support, and Model Context Protocol (MCP) server.*

[🇧🇷 Português](./docs/pt-br/README.md) | 🇺🇸 English

</div>

---

## 📋 Overview

DocSync is a developer-first tool designed to manage, synchronize, and improve technical documentation. It goes beyond simple file syncing by integrating **Large Language Models (LLMs)** directly into your workflow.

![DocSync CLI Preview](./assets/cli_preview.png)

With **v0.2.0**, DocSync introduces an **MCP Server**, allowing external agents (like Claude Desktop or IDEs) to use DocSync as a specialized tool.

> 🏗️ **See the [Architecture Diagram](./ARCHITECTURE.md) for technical details.**

## ✨ Key Features

- **🤖 AI Multi-Provider**: Built-in support for OpenAI, Anthropic (Claude), and Google (Gemini).
- **🔌 MCP Server**: Exposes project documentation as tools (`read_doc`, `improve_doc`) via Model Context Protocol.
- **🔄 Bidirectional Sync**: Keep local Markdown files in sync with Notion (Beta).
- **🛠️ Developer CLI**: Rich command-line interface for all operations.
- **📊 Quality Analysis**: Automated checks for documentation structure and quality.
- **🏗️ Extensible Architecture**: Plugin-ready design for new providers and integrations.

## 🚀 Installation

```bash
# Install via pip
pip install docsync

# Or for local development
git clone https://github.com/SH1W4/docsync.git
cd docsync
pip install -e ".[dev]"
```

## 💡 Usage

### 1. AI Documentation Improvement

Analyze and improve your docs using your preferred LLM provider.

```bash
# Default (OpenAI)
docsync improve README.md

# Use Claude (Anthropic)
docsync improve docs/api.md --provider claude --model claude-3-5-sonnet-20241022

# Use Gemini (Google)
docsync improve CONTRIBUTING.md --provider gemini
```

**Configuration**: Set the corresponding environment variable for your provider:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`

### 2. MCP Server (Agent Integration)

Start the MCP server to allow external agents to interface with your documentation.

```bash
docsync serve
```

**Claude Desktop Configuration**:
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "docsync": {
      "command": "docsync",
      "args": ["serve"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### 3. Synchronization (Beta)

```bash
# Sync local docs directory
docsync sync ./docs --config config.yaml
```

## 🏗️ Architecture

DocSync follows a clean, layered architecture:

- **Presentation**: CLI (Click/Rich)
- **Application**: MCP Server, Sync Engine
- **Domain**: LLM Providers (Abstracted), Document Models
- **Infrastructure**: File System, API Clients

See [ARCHITECTURE.json](./ARCHITECTURE.json) for a detailed breakdown.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to set up your development environment and submit PRs.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🏠 Homepage](https://github.com/SH1W4/docsync) • [🐛 Issues](https://github.com/SH1W4/docsync/issues) • [💬 Discussions](https://github.com/SH1W4/docsync/discussions)**

</div>
