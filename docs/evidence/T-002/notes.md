# T-002 Evidence Pack — Notes

## Resumo Executivo

**Data:** 2026-01-30
**Tarefa:** T-002 — Python bootstrap + venv + pre-commit
**Status:** ✅ CONCLUÍDA (com adaptações para Python 3.14)

---

## O que foi feito

### 1. Ambiente Virtual Python

- ✅ Venv já existente: `.venv/` (path curto para evitar DUV-003)
- ✅ Python 3.14.2 configurado
- ✅ 66 packages instalados (core MVP)

### 2. Correções de Compatibilidade Python 3.14

Foram necessárias atualizações no `requirements.txt` para compatibilidade:

| Package           | Original | Atualizado | Razão                                                            |
| ----------------- | -------- | ---------- | ---------------------------------------------------------------- |
| scikit-learn      | 1.3.2    | >=1.4.0    | Incompatível com Python 3.14 (Cython errors)                     |
| datasketch        | 1.0.8    | >=1.5.0    | Versão não encontrada                                            |
| lxml              | 4.9.3    | >=4.9.0    | Conflito de dependências                                         |
| pydantic          | 2.5.0    | >=2.10.0   | Requer compilação Rust (pydantic-core 2.14.1); >=2.10 tem wheels |
| pydantic-settings | 2.1.0    | >=2.7.0    | Compatibilidade com pydantic 2.10+                               |
| psycopg[binary]   | 3.1.18   | >=3.2.10   | Incompatível com Python 3.14                                     |

**Decisão:** Usar versões flexíveis (`>=`) para permitir resolução automática de dependências.

### 3. Correção bootstrap.ps1

- Mudança: `venv` → `.venv` (linha 33, 38, 122)
- Garantir consistência com path curto (resolução DUV-003)

### 4. Pre-commit Hooks

- ✅ Configurado: `.git/hooks/pre-commit`
- Hooks ativos (conforme `.pre-commit-config.yaml`):
  - black (formatter)
  - flake8 (linter)
  - mypy (type checker)

### 5. Arquivo .env

- ✅ Criado a partir de `.env.example`
- Configuração manual pendente (DATABASE_URL, REDIS_URL, etc.)

---

## Quality Gate

### Lint/Typecheck

- ⚠️ **Não executado ainda** (src/ vazio)
- Comando esperado: `black src/ && flake8 src/ && mypy src/`

### Testes

- ⚠️ **Não executado ainda** (tests/ vazio)
- Comando esperado: `pytest tests/`

---

## Packages Instalados (MVP - 66 total)

**Core:**

- python-dotenv 1.2.1
- pydantic 2.12.5, pydantic-settings 2.12.0
- fastapi 0.128.0, uvicorn 0.40.0, httpx 0.28.1

**Database:**

- sqlalchemy 2.0.46, alembic 1.18.3
- psycopg 3.3.2, psycopg-binary 3.3.2
- pgvector 0.4.2

**Queue:**

- redis 7.1.0, rq 2.6.1

**Dev/Test:**

- pytest 9.0.2
- black 26.1.0, flake8 7.3.0, mypy 1.19.1
- pre-commit 4.5.1

**Outros:** numpy 2.4.1, etc. (ver `get_python_environment_details`)

---

## Packages NÃO instalados (bloqueados temporariamente)

**Parsing/Extraction:**

- ❌ sentence-transformers, torch (depende de heavy deps, instalar T-037+)
- ❌ trafilatura, beautifulsoup4, lxml (instalar T-021+)
- ❌ python-docx, pypdf (instalar T-021+)

**PII/Privacy:**

- ❌ presidio-analyzer, presidio-anonymizer (instalar T-032+)

**Dedup/Quality:**

- ❌ datasketch, ftfy, regex (instalar T-027+)

**Logging/Monitoring:**

- ❌ structlog, python-json-logger (instalar T-020+)

**Docs:**

- ❌ markdown, mkdocs (instalar T-final)

**Razão:** Instalar apenas quando necessário (conforme roadmap); evita problemas de dependências complexas.

---

## Pendências / Próximos Passos

1. **T-003:** Configurar CI/CD com GitHub Actions
2. **T-004:** ✅ JÁ CONCLUÍDO (allowlist + sources.yaml)
3. **T-005:** Postgres schema v0 (metadata + pgvector)
4. **Manual:** Editar `.env` com configurações locais (DB, Redis, etc.)

---

## DUVs Identificadas (nenhuma crítica)

- **DUV-004:** pymupdf bloqueado (requer VS2019 build tools). Decisão: usar pypdf como alternativa.
- Nenhuma DUV crítica bloqueante.

---

## Como validar

### Ativação venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Versão Python:

```powershell
python --version
# Esperado: Python 3.14.2
```

### List packages:

```powershell
pip list
# Esperado: 66+ packages (conforme get_python_environment_details)
```

### Pre-commit check:

```powershell
pre-commit run --all-files
# Esperado: [INFO] Stashing unstaged files...
#          [INFO] Restored unstaged files...
# (ou avisos se houver código para lint)
```

### Arquivo .env existe:

```powershell
Test-Path .env
# Esperado: True
```

---

**Evidência completa:** `/docs/evidence/T-002/`
