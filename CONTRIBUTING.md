# Contribuindo para EditalShield

Obrigado por considerar contribuir para o EditalShield! 🎉

Este documento fornece diretrizes para contribuir com o projeto.

---

## 🎯 Princípios Fundamentais

Antes de contribuir, entenda os princípios do EditalShield:

### 1. **Genérico = Reutilizável**
- ❌ Nada hardcoded (nomes, CPFs, projetos específicos)
- ✅ Tudo parametrizado (inputs do usuário)
- ✅ Templates com placeholders (`{{NOME}}`, `{{VALOR}}`)

### 2. **Modular = Independente**
- Cada módulo funciona standalone
- Podem ser usados separadamente ou em conjunto
- Sem dependências entre módulos (baixo acoplamento)

### 3. **Validado = Credível**
- Cada módulo testado com dados fictícios
- Nunca dados reais no código (apenas em exemplos/documentação)
- 95%+ test coverage

### 4. **Documentado = Claro**
- Código autodocumentado (docstrings)
- Type hints em todas as funções
- Exemplos de uso em docstrings

---

## 🚫 RESTRIÇÕES ABSOLUTAS

### ❌ PROIBIDO:

1. **Hardcode de dados pessoais**
   - CPF, email, nome, telefone no código
   - Dados de projetos reais em `src/`

2. **Dados específicos em código**
   - Valores hardcoded (use parâmetros)
   - Nomes de editais específicos hardcoded
   - Nomes de projetos reais

3. **Templates não-genéricos**
   - Template NDA com nomes reais preenchidos
   - Exemplo de memorial que é verdadeiro

### ✅ OBRIGATÓRIO:

1. **Parametrização 100%**
   - Funções aceitam parâmetros
   - Templates com placeholders
   - Tudo via CLI/input do usuário

2. **Dados em `data/` = públicos**
   - Editais públicos (FAPESB, FINEP, etc.)
   - Critérios genéricos
   - Keywords universais

3. **Exemplos em `examples/` = fictícios**
   - Projetos inventados
   - CPF/CNPJ fake
   - Dados não reais

---

## 🔧 Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/editalshield.git
cd editalshield

# Adicione o repositório original como upstream
git remote add upstream https://github.com/symbeon/editalshield.git
```

### 2. Crie um Branch

```bash
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
```

### 3. Configure o Ambiente

```bash
# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências de desenvolvimento
pip install -r requirements.txt
```

### 4. Faça suas Alterações

- Siga o estilo de código (Black, PEP 8)
- Adicione testes para novas funcionalidades
- Atualize documentação se necessário
- Use type hints
- Escreva docstrings completas

### 5. Execute Testes

```bash
# Execute todos os testes
pytest tests/ --cov

# Verifique cobertura (deve ser >= 95%)
pytest tests/ --cov --cov-report=html

# Formate código
black src/ tests/ cli/

# Verifique tipos
mypy src/

# Verifique linting
flake8 src/ tests/ cli/
```

### 6. Commit e Push

```bash
# Commit com mensagem descritiva
git add .
git commit -m "feat: adiciona funcionalidade X"

# Push para seu fork
git push origin feature/nome-da-feature
```

### 7. Abra Pull Request

- Vá para o repositório original no GitHub
- Clique em "New Pull Request"
- Descreva suas alterações claramente
- Referencie issues relacionadas

---

## 📝 Padrões de Código

### Estilo de Código

```python
# Use Black para formatação
# Linha máxima: 100 caracteres

def funcao_exemplo(parametro: str, valor: int = 10) -> Dict[str, Any]:
    """Descrição breve da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        parametro: Descrição do parâmetro
        valor: Descrição do valor (default: 10)
        
    Returns:
        Dicionário com resultados
        
    Raises:
        ValueError: Se parâmetro for inválido
        
    Example:
        >>> resultado = funcao_exemplo("teste", 20)
        >>> print(resultado)
        {'status': 'ok'}
    """
    if not parametro:
        raise ValueError("Parâmetro não pode ser vazio")
    
    return {"status": "ok", "valor": valor}
```

### Estrutura de Testes

```python
import pytest
from editalshield.modules import ModuloX


class TestModuloX:
    """Testes para ModuloX."""
    
    def setup_method(self):
        """Setup antes de cada teste."""
        self.modulo = ModuloX()
    
    def test_input_validation(self):
        """Testa validação de input."""
        with pytest.raises(ValueError):
            self.modulo.processar(None)
    
    def test_output_structure(self):
        """Testa estrutura de output."""
        resultado = self.modulo.processar({"param": "valor"})
        assert "resultado" in resultado
        assert isinstance(resultado["resultado"], list)
```

---

## 🎯 Tipos de Contribuição

### 🐛 Reportar Bugs

Abra uma issue com:
- Descrição clara do bug
- Passos para reproduzir
- Comportamento esperado vs. atual
- Ambiente (OS, Python version, etc.)

### ✨ Sugerir Features

Abra uma issue com:
- Descrição da feature
- Caso de uso
- Benefícios esperados
- Possível implementação

### 📝 Melhorar Documentação

- Corrigir erros de digitação
- Adicionar exemplos
- Melhorar clareza
- Traduzir documentação

### 💻 Implementar Features

- Escolha uma issue marcada como "good first issue"
- Comente na issue que está trabalhando nela
- Siga os padrões de código
- Adicione testes

---

## 📋 Checklist Antes de Submeter PR

- [ ] Código segue padrões (Black, PEP 8)
- [ ] Todos os testes passam (`pytest tests/`)
- [ ] Cobertura >= 95% (`pytest --cov`)
- [ ] Type hints adicionados
- [ ] Docstrings completas
- [ ] Documentação atualizada
- [ ] Nenhum dado pessoal no código
- [ ] Exemplos são fictícios
- [ ] Templates usam placeholders

---

## 🏗️ Estrutura do Projeto

```
editalshield/
├── src/editalshield/          # Código fonte
│   ├── modules/               # 6 módulos principais
│   ├── templates/             # Templates parametrizados
│   ├── data/                  # Dados públicos
│   └── utils/                 # Utilitários
├── cli/                       # Interface CLI
├── tests/                     # Testes unitários
├── notebooks/                 # Tutoriais
├── examples/                  # Exemplos fictícios
└── docs/                      # Documentação
```

---

## 💬 Comunicação

- **Issues**: Para bugs e features
- **Discussions**: Para perguntas e discussões
- **Email**: contato@symbeon.lab (para questões privadas)

---

## 📜 Código de Conduta

- Seja respeitoso e inclusivo
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros

---

## 🙏 Agradecimentos

Toda contribuição é valiosa, seja código, documentação, testes ou feedback!

Obrigado por ajudar a democratizar o acesso a ferramentas de inovação no Brasil! 🇧🇷
