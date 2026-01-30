# Bootstrap script for Windows (PowerShell)
# Usage: .\scripts\setup\bootstrap.ps1

param(
    [switch]$NoVenv,
    [switch]$NoDocker,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Colors for output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Blue = "Cyan"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$Timestamp] [$Level] $Message"
}

Write-Log "🚀 Iniciando bootstrap do projeto..." $Blue

# Step 1: Check Python
Write-Log "Step 1: Verificando Python 3.11+" $Blue
$PythonVersion = & python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ Python não encontrado ou não está no PATH" $Red
    exit 1
}
Write-Log "✅ Python encontrado: $PythonVersion" $Green

# Step 2: Create venv (unless --NoVenv)
if (-not $NoVenv) {
    Write-Log "Step 2: Criando virtual environment..." $Blue
    if (Test-Path "venv") {
        Write-Log "⚠️  venv já existe, pulando criação" $Yellow
    } else {
        & python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            Write-Log "❌ Erro ao criar venv" $Red
            exit 1
        }
        Write-Log "✅ venv criado" $Green
    }
    
    # Activate venv
    & ".\venv\Scripts\Activate.ps1"
    Write-Log "✅ venv ativado" $Green
}

# Step 3: Install dependencies
Write-Log "Step 3: Instalando dependências..." $Blue
& pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ Erro ao atualizar pip" $Red
    exit 1
}

& pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ Erro ao instalar dependências" $Red
    exit 1
}
Write-Log "✅ Dependências instaladas" $Green

# Step 4: Setup pre-commit
Write-Log "Step 4: Configurando pre-commit hooks..." $Blue
& pre-commit install
if ($LASTEXITCODE -ne 0) {
    Write-Log "⚠️  Erro ao configurar pre-commit (não bloqueante)" $Yellow
} else {
    Write-Log "✅ Pre-commit hooks configurado" $Green
}

# Step 5: Create .env (if not exists)
Write-Log "Step 5: Configurando arquivo .env..." $Blue
if (Test-Path ".env") {
    Write-Log "⚠️  .env já existe, pulando" $Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Log "✅ .env criado (copiar de .env.example; configurar manualmente)" $Yellow
}

# Step 6: Docker (unless --NoDocker)
if (-not $NoDocker) {
    Write-Log "Step 6: Verificando Docker..." $Blue
    $DockerCheck = & docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✅ Docker encontrado: $DockerCheck" $Green
        Write-Log "Subindo containers Postgres/Redis..." $Blue
        & docker-compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✅ Containers rodando" $Green
            Start-Sleep -Seconds 5
            Write-Log "Instalando extensão pgvector..." $Blue
            & docker-compose run --rm postgres-init
            Write-Log "✅ pgvector instalado" $Green
        } else {
            Write-Log "⚠️  Erro ao subir containers Docker (não bloqueante)" $Yellow
        }
    } else {
        Write-Log "⚠️  Docker não encontrado (não bloqueante; configure Postgres/Redis manualmente)" $Yellow
    }
}

# Step 7: Run basic checks
Write-Log "Step 7: Rodando checks básicos..." $Blue

Write-Log "  - Lint (flake8)..." $Blue
& flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
Write-Log "  ✅ Lint OK" $Green

Write-Log "  - Typecheck (mypy)..." $Blue
& mypy src --ignore-missing-imports --no-implicit-optional --warn-unused-ignores
Write-Log "  ✅ Typecheck OK (ou avisos esperados)" $Green

# Final message
Write-Log "✨ Bootstrap concluído com sucesso!" $Green
Write-Log ""
Write-Log "Próximos passos:" $Blue
Write-Log "  1. Editar .env com suas configurações (banco de dados, etc.)"
Write-Log "  2. Ler README.md para mais instruções"
Write-Log "  3. Ler _OBSIDIAN/Organização do Projeto/Contexto Global de Agentes.md"
Write-Log "  4. Iniciar T-001: Git setup + GitHub remote"
Write-Log ""
Write-Log "Para ativar venv novamente: .\venv\Scripts\Activate.ps1" $Yellow
