# Exemplos - EditalShield

Esta pasta contém exemplos **fictícios** de uso do EditalShield.

## ⚠️ IMPORTANTE

**Todos os dados nesta pasta são FICTÍCIOS e criados apenas para demonstração.**

- Nomes de projetos são inventados
- CPFs e CNPJs são fake
- Dados financeiros são ilustrativos
- Nenhum projeto real é mencionado

---

## 📁 Exemplos Disponíveis

### 1. RetailTech X (Varejo)
**Pasta**: `example_varejo_tech/`  
**Setor**: Varejo  
**Problema**: Sistema de análise comportamental em checkout  
**Edital**: Centelha BA 2025

**Arquivos**:
- `projeto_config.json` - Configuração do projeto
- `memorial_raw.md` - Memorial técnico original (com exposição de PI)
- `memorial_protected.md` - Memorial protegido pelo EditalShield
- `nda_generated.pdf` - NDA customizado gerado
- `README.md` - Documentação do exemplo

### 2. HealthTech Y (Saúde)
**Pasta**: `example_healthtech/`  
**Setor**: Saúde  
**Problema**: Plataforma de telemedicina com IA  
**Edital**: PIPE FAPESP Fase 1

**Arquivos**:
- `projeto_config.json`
- `memorial_raw.md`
- `memorial_protected.md`
- `gap_analysis.json`
- `README.md`

### 3. FinTech Z (Finanças)
**Pasta**: `example_fintech/`  
**Setor**: Fintech  
**Problema**: Sistema de análise de crédito alternativo  
**Edital**: Finep Inovacred

**Arquivos**:
- `projeto_config.json`
- `memorial_raw.md`
- `memorial_protected.md`
- `cost_scenarios.json`
- `README.md`

---

## 🚀 Como Usar os Exemplos

### Exemplo 1: Proteger Memorial
```bash
cd examples/example_varejo_tech/

# Proteja o memorial
editalshield protect-memorial \
  --input memorial_raw.md \
  --sensitivity high \
  --output memorial_protected.md \
  --report analysis_report.md
```

### Exemplo 2: Gerar NDA
```bash
cd examples/example_healthtech/

# Gere NDA customizado
editalshield generate-nda \
  --project-config projeto_config.json \
  --consultant "Consultoria ABC" \
  --success-fee 20 \
  --teto 15000 \
  --output nda_healthtech.pdf
```

### Exemplo 3: Calcular Custos
```bash
cd examples/example_fintech/

# Calcule cenários de custo
editalshield calculate-fee \
  --valor-aprovado 200000 \
  --success-fee 15 \
  --teto 30000 \
  --parcelas 4
```

---

## 📝 Estrutura de Cada Exemplo

Cada pasta de exemplo contém:

```
example_X/
├── README.md                  # Documentação do exemplo
├── projeto_config.json        # Configuração do projeto (fictício)
├── memorial_raw.md            # Memorial original
├── memorial_protected.md      # Memorial protegido (output)
├── nda_generated.pdf          # NDA gerado (output)
└── [outros outputs]           # Análises, relatórios, etc.
```

---

## 🤝 Contribuindo

Quer adicionar um novo exemplo? 

1. Crie uma nova pasta `example_SETOR/`
2. Use dados **100% fictícios**
3. Inclua `README.md` explicando o caso
4. Adicione arquivos de configuração e outputs
5. Abra um Pull Request

Veja [CONTRIBUTING.md](../CONTRIBUTING.md) para mais detalhes.

---

## 🔐 Privacidade

**Nenhum dado real deve ser adicionado a esta pasta.**

Se você quer testar com seu projeto real:
1. Crie uma pasta local fora do repositório
2. Use EditalShield normalmente
3. **Nunca** commite dados reais para o GitHub
