# 🔄 Script de Migração para Symbeon Labs
# Execute este script APÓS transferir o repositório no GitHub

Write-Host "🚀 Migrando EditalShield para Symbeon Labs..." -ForegroundColor Cyan

# 1. Atualizar remote para nova organização
Write-Host "`n📡 Atualizando remote..." -ForegroundColor Yellow
git remote set-url origin https://github.com/symbeon-labs/editalshield.git

# 2. Verificar remote atualizado
Write-Host "`n✅ Verificando remote..." -ForegroundColor Yellow
git remote -v

# 3. Fetch para sincronizar
Write-Host "`n🔄 Sincronizando com novo remote..." -ForegroundColor Yellow
git fetch origin

# 4. Verificar status
Write-Host "`n📊 Status atual..." -ForegroundColor Yellow
git status

Write-Host "`n✅ Remote atualizado com sucesso!" -ForegroundColor Green
Write-Host "Novo repositório: https://github.com/symbeon-labs/editalshield" -ForegroundColor Cyan
