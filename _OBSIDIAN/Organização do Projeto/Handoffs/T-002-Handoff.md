# Handoff — T-002: Python bootstrap + venv + pre-commit

**ID:** T-002  
**Data:** 2026-01-30  
**Persona:** TL (Tech Lead)  
**Status:** ✅ DONE  
**Commit:** d0c256b

---

## O que mudou

### 1. Ambiente Python
- ✅ Virtual environment: `.venv/` (Python 3.14.2)
- ✅ 66 packages core instalados:
  - Web: fastapi 0.128.0, uvicorn 0.40.0, httpx 0.28.1
  - Database: sqlalchemy 2.0.46, alembic 1.18.3, psycopg 3.3.2, pgvector 0.4.2
  - Queue: redis 7.1.0, rq 2.6.1
  - Dev/Test: pytest 9.0.2, black 26.1.0, flake8 7.3.0, mypy 1.19.1
  - Tools: pre-commit 4.5.1
  - Data: numpy 2.4.1

### 2. Configuração Pre-commit
- ✅ Arquivo: `.pre-commit-config.yaml` (criado)
- ✅ Hooks configurados:
  - trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files
  - black (formatter)
  - flake8 (linter)
  - isort (import sorting)
  - mypy (type checker)

### 3. Correções de Compatibilidade Python 3.14
- ✅ `requirements.txt` atualizado com versões compatíveis:

| Package | Original | Atualizado | Razão |
|---------|----------|------------|-------|
| scikit-learn | 1.3.2 | >=1.4.0 | Incompatibilidade Python 3.14 (Cython errors) |
| datasketch | 1.0.8 | >=1.5.0 | Versão não encontrada |
| lxml | 4.9.3 | >=4.9.0 | Conflito de dependências |
| pydantic | 2.5.0 | >=2.10.0 | Requer compilação Rust; >=2.10 tem wheels pré-compiladas |
| pydantic-settings | 2.1.0 | >=2.7.0 | Compatibilidade com pydantic 2.10+ |
| psycopg[binary] | 3.1.18 | >=3.2.10 | Incompatibilidade Python 3.14 |

### 4. Correção bootstrap.ps1
- ✅ Mudança: `venv` → `.venv` (linhas 33, 38, 122)
- ✅ Consistência com resolução DUV-003 (path curto)

### 5. Arquivo .env
- ✅ Criado a partir de `.env.example`
- ⚠️ Configuração manual pendente (DATABASE_URL, REDIS_URL, etc.)

---

## Decisões tomadas

**DEC-009:** Usar versões flexíveis (`>=`) no requirements.txt para Python 3.14+ (ao invés de pinned versions), permitindo resolução automática de dependências.

**DEC-010:** Instalar apenas pacotes core MVP na T-002. Pacotes heavyweights (torch, sentence-transformers, presidio, etc.) serão instalados sob demanda nas tarefas correspondentes (T-021+, T-032+, T-037+).

---

## Como validar

### Ativar venv:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Verificar Python:
```powershell
python --version
# Esperado: Python 3.14.2
```

### Listar packages:
```powershell
pip list | Select-String -Pattern "(fastapi|sqlalchemy|pytest|black|mypy)"
# Esperado: fastapi 0.128.0, sqlalchemy 2.0.46, pytest 9.0.2, black 26.1.0, mypy 1.19.1
```

### Testar pre-commit:
```powershell
pre-commit run --all-files
# Esperado: All hooks pass (ou warnings triviais)
```

### Arquivo .env existe:
```powershell
Test-Path .env
# Esperado: True
```

---

## Próximos passos

1. **T-003:** CI/tests/lint/typecheck (GitHub Actions)
2. **T-004:** ✅ JÁ CONCLUÍDO (allowlist + sources.yaml)
3. **T-005:** Postgres schema v0 (metadata + pgvector)
4. **Manual:** Editar `.env` com configurações locais

---

## Packages pendentes (instalar sob demanda)

**Parsing/Extraction (T-021+):**
- trafilatura, beautifulsoup4, lxml
- python-docx, pypdf

**Embeddings (T-037+):**
- sentence-transformers, torch

**PII/Privacy (T-032+):**
- presidio-analyzer, presidio-anonymizer

**Dedup/Quality (T-027+):**
- datasketch, ftfy, regex, unidecode, langdetect

**Logging/Monitoring (T-020+):**
- structlog, python-json-logger

**Docs (Final):**
- markdown, mkdocs

---

## Evidência

- **Evidence Pack:** `docs/evidence/T-002/`
  - commands.log
  - notes.md
  - files_changed.json

- **Commit:** d0c256b (master)
- **Push:** ✅ origin/master atualizado

---

**Handoff criado por:** AGENTE ORQUESTRADOR (Persona: TL)  
**Data:** 2026-01-30 19:30 UTC
