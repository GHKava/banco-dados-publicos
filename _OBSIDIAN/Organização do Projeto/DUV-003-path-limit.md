# DUV-003 — Resolução de Windows Path Limit (260 caracteres)

**ID**: DUV-003  
**Tipo**: BLOCKER TÉCNICO  
**Prioridade**: P0 (CRÍTICO)  
**Data de abertura**: 2026-01-30 18:55  
**Criado por**: Orquestrador (Persona: TL)  
**Estado**: OPEN  

---

## 🔒 Bloqueio

T-002 (Python bootstrap) está **BLOQUEADO** devido ao limite de 260 caracteres de path do Windows.

**Path atual**:
```
C:\Users\Gustavo\My Drive\DriveSyncFiles\1. OBSIDIAN - GUSTAVO - Arquivos Pessoais\02 - PROJECTS\02.03 - PROJETO - SISTEMA - Desenvolvimento de Sistemas\
```

**Comprimento**: 159 caracteres (base)

**Problema**: Ao criar `.venv/`, subpaths dentro do virtual environment ultrapassam 260 caracteres, causando erro:
```
ERROR: [WinError 206] The filename or extension is too long
```

---

## ❓ Pergunta

**Qual solução você prefere para resolver o Windows path limit?**

---

## 🎯 Opções

### Opção A: 🏆 Mover Projeto para Path Curto (RECOMENDADO)

**Ação**:
1. Fechar VS Code
2. Mover pasta inteira para `C:\Dev\banco-dados-publicos\`
3. Reabrir VS Code no novo path
4. Re-executar bootstrap

**Prós**:
- ✅ Solução definitiva
- ✅ Não requer privilégios de administrador
- ✅ Não requer reinicialização do sistema
- ✅ Path final: ~30 caracteres (margem de 230 caracteres para subpaths)
- ✅ Git continua funcionando normalmente
- ✅ Melhor performance (menos overhead de sincronização do Google Drive)

**Contras**:
- ⚠️ Precisa mover arquivos manualmente (ou usar robocopy/xcopy)
- ⚠️ Precisa reconfigurar workspace do VS Code
- ⚠️ Google Drive pode levar tempo para sincronizar novamente

**Path final**: `C:\Dev\banco-dados-publicos\` (30 caracteres)

---

### Opção B: Habilitar LongPathsEnabled (Registry)

**Ação**:
1. Abrir PowerShell como Administrador
2. Executar: `Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1`
3. Reiniciar sistema
4. Re-executar bootstrap

**Prós**:
- ✅ Não precisa mover arquivos
- ✅ Habilita suporte global para paths longos no Windows

**Contras**:
- ❌ Requer privilégios de administrador
- ❌ Requer reinicialização do sistema
- ⚠️ Nem todos os programas respeitam a configuração (Git pode ter problemas)
- ⚠️ Pode causar issues com ferramentas legadas (Node.js antigo, etc.)

**Path final**: Mantém atual (159 caracteres base)

---

### Opção C: Symlink (Workaround Temporário)

**Ação**:
1. Criar symlink: `New-Item -ItemType SymbolicLink -Path "C:\Dev\banco-dados-publicos" -Target "C:\Users\Gustavo\My Drive\..."`
2. Trabalhar em `C:\Dev\banco-dados-publicos\`
3. Re-executar bootstrap

**Prós**:
- ✅ Não requer privilégios de administrador (em teoria, mas pode variar)
- ✅ Não requer reinicialização
- ✅ Mantém arquivos sincronizados com Google Drive

**Contras**:
- ⚠️ Solução temporária
- ❌ Git pode ter problemas com symlinks (commits podem falhar)
- ❌ Alguns programas não seguem symlinks corretamente
- ❌ Pode causar confusão (trabalhar em 2 paths diferentes)

**Path final**: `C:\Dev\banco-dados-publicos\` (via symlink para path longo)

---

## 💡 Recomendação do Agente

**Opção A** (Mover Projeto) é a melhor escolha porque:

1. **Solução definitiva**: Resolve o problema de raiz, sem workarounds
2. **Zero privilégios**: Não precisa de admin nem reboot
3. **Melhor performance**: Trabalhar fora do Google Drive é mais rápido (menos latência de I/O)
4. **Compatibilidade**: Git, Docker, CI/CD funcionam perfeitamente
5. **Futuro-proof**: Evita problemas com outras ferramentas (Node.js, Rust, etc.)

**Trade-off**: Precisa mover arquivos manualmente (~5 min de trabalho) e reconfigurar workspace do VS Code.

---

## 🔄 Impacto no Projeto

**Tasks bloqueadas por DUV-003**:
- ❌ T-002: Python bootstrap (BLOCKED — aguardando resolução)
- ❌ T-003: CI/tests/lint (BLOCKED — depende de T-002)
- ❌ T-005: Postgres schema v0 (BLOCKED — depende de T-002 para Alembic)

**Tasks não afetadas** (podem continuar em paralelo):
- ✅ T-ONB-SRC-001 a T-ONB-SRC-005: Onboarding de fontes (não dependem de Python)

---

## 📋 Passos Após Decisão

### Se escolher Opção A (Mover Projeto):

1. Fechar VS Code
2. Abrir PowerShell/Terminal
3. Executar:
   ```powershell
   # Criar diretório de destino
   New-Item -ItemType Directory -Force -Path "C:\Dev"
   
   # Mover projeto (usar robocopy para preservar metadados)
   robocopy "C:\Users\Gustavo\My Drive\DriveSyncFiles\1. OBSIDIAN - GUSTAVO - Arquivos Pessoais\02 - PROJECTS\02.03 - PROJETO - SISTEMA - Desenvolvimento de Sistemas" "C:\Dev\banco-dados-publicos" /E /MOVE /XD .git .venv node_modules
   
   # Ou usar xcopy:
   # xcopy "C:\Users\Gustavo\My Drive\..." "C:\Dev\banco-dados-publicos" /E /H /I /Y
   ```
4. Abrir VS Code em `C:\Dev\banco-dados-publicos\`
5. Verificar Git: `git status` (deve estar OK)
6. Re-executar bootstrap: `.\scripts\setup\bootstrap.ps1 -NoDocker`
7. Atualizar DUV-003 para RESOLVED
8. Continuar T-002

### Se escolher Opção B (LongPathsEnabled):

1. Fechar VS Code
2. Abrir PowerShell como **Administrador** (Win + X → "PowerShell (Admin)")
3. Executar:
   ```powershell
   Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
   git config --system core.longpaths true
   ```
4. Reiniciar sistema (obrigatório)
5. Abrir VS Code no path atual
6. Re-executar bootstrap: `.\scripts\setup\bootstrap.ps1 -NoDocker`
7. Atualizar DUV-003 para RESOLVED
8. Continuar T-002

### Se escolher Opção C (Symlink):

1. Abrir PowerShell
2. Executar:
   ```powershell
   New-Item -ItemType SymbolicLink -Path "C:\Dev\banco-dados-publicos" -Target "C:\Users\Gustavo\My Drive\DriveSyncFiles\1. OBSIDIAN - GUSTAVO - Arquivos Pessoais\02 - PROJECTS\02.03 - PROJETO - SISTEMA - Desenvolvimento de Sistemas"
   ```
3. Abrir VS Code em `C:\Dev\banco-dados-publicos\`
4. Verificar Git: `git status` (pode ter warnings de symlink)
5. Re-executar bootstrap: `.\scripts\setup\bootstrap.ps1 -NoDocker`
6. Atualizar DUV-003 para RESOLVED (com nota de workaround)
7. Continuar T-002

---

## 🎯 Decisão Aguardada

**Agente está aguardando sua decisão**:

- Digite **"A"** para Opção A (Mover Projeto) ← RECOMENDADO
- Digite **"B"** para Opção B (LongPathsEnabled)
- Digite **"C"** para Opção C (Symlink)

---

**Aberto por**: Orquestrador (Persona: TL)  
**Estado**: OPEN  
**Próxima ação**: Aguardar decisão do usuário
