# 📝 Checklist de Migração - EditalShield → Symbeon Labs

## ✅ Passo 1: Transferir no GitHub (MANUAL)
- [ ] Acessar: https://github.com/SH1W4/editalshield/settings
- [ ] Ir em "Danger Zone" → "Transfer ownership"
- [ ] Transferir para: `symbeon-labs`
- [ ] Confirmar nome: `editalshield`
- [ ] Aguardar confirmação por email

---

## ✅ Passo 2: Atualizar Remote Local

Executar o script:
```powershell
.\migrate-to-symbeon.ps1
```

Ou manualmente:
```bash
git remote set-url origin https://github.com/symbeon-labs/editalshield.git
git fetch origin
git status
```

---

## ✅ Passo 3: Atualizar Documentação

Arquivos que precisam ser atualizados:

### README.md
- [ ] Badges (GitHub Actions, etc)
- [ ] Link do repositório
- [ ] Clone command

### SESSION.md
- [ ] Link do repositório (linha 23)
- [ ] Atualizar de `SH1W4/editalshield` para `symbeon-labs/editalshield`

### STRATEGY.md
- [ ] Links de referência ao GitHub
- [ ] URLs de exemplo

### SYSTEM_CONTEXT.md
- [ ] Link do repositório
- [ ] Seção "Support & Resources"

### mcp.json
- [ ] Campo `repository` (se existir)

### pyproject.toml
- [ ] Campo `repository` em `[project.urls]`

---

## ✅ Passo 4: Commit e Push

```bash
git add .
git commit -m "chore: migrate to symbeon-labs organization

Updated all references from SH1W4/editalshield to symbeon-labs/editalshield:
- README.md badges and links
- SESSION.md repository reference
- STRATEGY.md URLs
- SYSTEM_CONTEXT.md support links
- pyproject.toml repository URL

Organization: https://github.com/symbeon-labs"

git push origin main
```

---

## ✅ Passo 5: Verificação Final

- [ ] Acessar: https://github.com/symbeon-labs/editalshield
- [ ] Verificar que GitHub Actions está funcionando
- [ ] Verificar que README está renderizando corretamente
- [ ] Verificar redirect de https://github.com/SH1W4/editalshield

---

## 🎯 Benefícios da Migração

✅ **Profissionalismo** - Organização empresarial  
✅ **Branding** - Symbeon Labs consistente  
✅ **Credibilidade** - Melhor para B2G/B2B  
✅ **Escalabilidade** - Preparado para crescimento  
✅ **Investimento** - Melhor para due diligence  

---

**Status:** 🟡 Aguardando transferência no GitHub  
**Próximo:** Executar `migrate-to-symbeon.ps1` após confirmação
