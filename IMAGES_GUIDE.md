# 🎨 Guia de Imagens do EditalShield

## 📸 Imagens Geradas

Foram criadas 5 imagens profissionais para o projeto EditalShield:

### 1. **Logo Principal** (`editalshield_logo.png`)
- **Uso**: README, documentação, apresentações
- **Descrição**: Logo moderno com escudo e documento integrados
- **Cores**: Azul profundo, verde vibrante, acentos dourados
- **Localização sugerida**: `docs/images/logo.png`

### 2. **Diagrama de Arquitetura** (`architecture_diagram.png`)
- **Uso**: Documentação técnica, apresentações
- **Descrição**: Diagrama hexagonal mostrando os 6 módulos
- **Localização sugerida**: `docs/images/architecture.png`

### 3. **Ilustração de Workflow** (`workflow_illustration.png`)
- **Uso**: README, pitch deck, apresentações
- **Descrição**: Fluxo do processo EditalShield (4 etapas)
- **Localização sugerida**: `docs/images/workflow.png`

### 4. **Banner Hero** (`hero_banner.png`)
- **Uso**: Topo do README, GitHub social preview
- **Descrição**: Banner abstrato com tema de proteção e inovação
- **Localização sugerida**: `docs/images/banner.png`

### 5. **Memorial Protector** (`module_memorial_protector.png`)
- **Uso**: Documentação do módulo 4, exemplos
- **Descrição**: Ilustração do módulo de proteção de memoriais
- **Localização sugerida**: `docs/images/memorial_protector.png`

## 📁 Estrutura de Diretórios Recomendada

```
EDITALSHIELD/
├── docs/
│   ├── images/
│   │   ├── logo.png
│   │   ├── architecture.png
│   │   ├── workflow.png
│   │   ├── banner.png
│   │   └── memorial_protector.png
│   └── ...
└── ...
```

## 🔧 Como Adicionar as Imagens ao Projeto

### Passo 1: Criar Diretório
```bash
mkdir -p docs/images
```

### Passo 2: Copiar Imagens
As imagens foram salvas em:
```
C:/Users/João/.gemini/antigravity/brain/13e4c364-fef6-4ba7-bd52-d63c7b22246b/
```

Copie-as para o projeto:
```bash
# Você pode copiar manualmente ou usar comandos
cp ~/.gemini/antigravity/brain/*/editalshield_logo_*.png docs/images/logo.png
cp ~/.gemini/antigravity/brain/*/architecture_diagram_*.png docs/images/architecture.png
cp ~/.gemini/antigravity/brain/*/workflow_illustration_*.png docs/images/workflow.png
cp ~/.gemini/antigravity/brain/*/hero_banner_*.png docs/images/banner.png
cp ~/.gemini/antigravity/brain/*/module_memorial_protector_*.png docs/images/memorial_protector.png
```

### Passo 3: Atualizar README.md

Adicione o banner no topo do README:
```markdown
![EditalShield Banner](docs/images/banner.png)

<p align="center">
  <img src="docs/images/logo.png" alt="EditalShield Logo" width="200"/>
</p>

# EditalShield

Framework open-source para proteção de PI em editais de inovação brasileiros.

## 🏗️ Arquitetura

![Arquitetura EditalShield](docs/images/architecture.png)

## 🔄 Como Funciona

![Workflow EditalShield](docs/images/workflow.png)

## 🛡️ Módulo Memorial Protector

![Memorial Protector](docs/images/memorial_protector.png)
```

## 🎯 Uso das Imagens

### Logo
- **README principal**: Cabeçalho centralizado
- **Documentação**: Rodapé ou cabeçalho
- **Apresentações**: Slide de título
- **Social media**: Posts sobre o projeto

### Diagrama de Arquitetura
- **Documentação técnica**: Seção de arquitetura
- **Apresentações**: Explicação dos módulos
- **Issues do GitHub**: Contexto para desenvolvimento

### Workflow
- **README**: Seção "Como Funciona"
- **Pitch deck**: Proposta de valor
- **Tutoriais**: Introdução ao framework

### Banner Hero
- **README**: Topo da página
- **GitHub Social Preview**: Configurar em Settings
- **Website**: Header principal

### Memorial Protector
- **Documentação do módulo**: Explicação visual
- **Exemplos**: Demonstração de uso
- **Tutoriais**: Guia passo a passo

## 🔄 Atualizar no GitHub

Após adicionar as imagens:

```bash
# Adicionar ao Git
git add docs/images/

# Commit
git commit -m "docs: add professional images and diagrams

- Add EditalShield logo
- Add architecture diagram
- Add workflow illustration
- Add hero banner
- Add Memorial Protector module illustration"

# Push
git push origin main
```

## 🎨 Configurar GitHub Social Preview

1. Acesse: https://github.com/SH1W4/editalshield/settings
2. Vá em "Social preview"
3. Upload `docs/images/banner.png`
4. Salve as alterações

## 📊 Otimização de Imagens (Opcional)

Para reduzir o tamanho dos arquivos:

```bash
# Instalar imagemagick ou usar ferramentas online
# TinyPNG: https://tinypng.com/
# Squoosh: https://squoosh.app/

# Ou via CLI (se tiver imagemagick)
mogrify -resize 1200x -quality 85 docs/images/*.png
```

## ✨ Próximos Passos

1. ✅ Copiar imagens para `docs/images/`
2. ✅ Atualizar README.md com as imagens
3. ✅ Fazer commit e push
4. ✅ Configurar GitHub Social Preview
5. ⬜ Criar mais imagens conforme necessário:
   - Screenshots da CLI
   - Diagramas de fluxo detalhados
   - Exemplos de uso visual
   - Comparações antes/depois

## 🎨 Paleta de Cores do Projeto

Para manter consistência visual:

```
Azul Profundo: #1e3a8a
Verde Vibrante: #10b981
Dourado: #fbbf24
Azul Claro: #3b82f6
Verde Escuro: #059669
```

---

**As imagens estão prontas para uso!** 🎉

Elas darão um visual profissional ao EditalShield e ajudarão a comunicar melhor a proposta de valor do projeto.
