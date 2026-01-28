# Script para verificar e corrigir estrutura
Write-Host "🔍 Verificando estrutura do TrackFlix..." -ForegroundColor Cyan

# Verificar pasta app
if (-not (Test-Path "app")) {
    Write-Host "❌ Pasta 'app' não encontrada!" -ForegroundColor Red
    exit
}

# Verificar arquivos obrigatórios
 = @(
    "app\__init__.py",
    "app\main.py",
    "app\models\__init__.py",
    "app\models\media.py",
    "app\database\__init__.py", 
    "app\database\db.py",
    "app\services\__init__.py",
    "app\services\media_service.py",
    "app\ui\__init__.py",
    "app\ui\cli.py",
    "run.py"
)

Write-Host "
📁 Verificando arquivos..." -ForegroundColor Yellow
foreach ( in ) {
    if (Test-Path ) {
        Write-Host "✅ " -ForegroundColor Green
    } else {
        Write-Host "❌  - NÃO ENCONTRADO" -ForegroundColor Red
        
        # Criar diretório se não existir
         = Split-Path  -Parent
        if (-not (Test-Path )) {
            New-Item -ItemType Directory -Path  -Force | Out-Null
            Write-Host "   📁 Criado diretório: " -ForegroundColor Yellow
        }
        
        # Criar arquivo vazio
        "" | Out-File -FilePath  -Encoding UTF8
        Write-Host "   📄 Criado arquivo vazio" -ForegroundColor Yellow
    }
}

# Testar Python
Write-Host "
🐍 Testando Python..." -ForegroundColor Cyan
try {
    python -c "print('✅ Python funciona!'); import sqlite3; print('✅ SQLite funciona!')"
} catch {
    Write-Host "❌ Python não está funcionando corretamente" -ForegroundColor Red
}

Write-Host "
🎉 Verificação completa!" -ForegroundColor Green
Write-Host "Execute: python run.py" -ForegroundColor Yellow
