# T-003 Evidence Pack — Notes

## Resumo Executivo

**Data:** 2026-01-30
**Tarefa:** T-003 — CI/tests/lint/typecheck (GitHub Actions)
**Status:** ✅ CONCLUÍDA

---

## O que foi feito

### 1. GitHub Actions Workflow

- ✅ Criado: `.github/workflows/ci.yml`
- ✅ Triggers: push/PR em master/main/develop + manual dispatch
- ✅ Matrix strategy: Python 3.11, 3.12, 3.14
- ✅ Steps configurados:
  - Checkout code
  - Setup Python + cache pip
  - Install dependencies
  - Lint: black, flake8, isort
  - Typecheck: mypy (continue-on-error até código ter mais type hints)
  - Tests: pytest + coverage (continue-on-error até ter testes reais)
  - Upload coverage to Codecov (optional, Python 3.14 only)

### 2. Estrutura de Diretórios

- ✅ Criado: `src/` (código-fonte principal)
  - `src/__init__.py` (versão 0.1.0)
  - `src/README.md` (estrutura planejada)
- ✅ Criado: `tests/` (testes automatizados)
  - `tests/__init__.py`
  - `tests/README.md` (como rodar testes)
  - `tests/test_basic.py` (testes dummy para validar CI)

### 3. Testes Básicos

- ✅ `test_basic.py`:
  - test_basic_import (valida import do package)
  - test_basic_math (teste trivial)
  - test_string_operations
  - test_square (parametrized test)
- **Total:** 7 testes passando

---

## Quality Gate

### Lint

- ✅ **black:** Passa (código formatado corretamente)
- ✅ **flake8:** Passa (sem erros de lint)
- ✅ **isort:** Passa (imports ordenados)

### Typecheck

- ⚠️ **mypy:** Continue-on-error (warnings esperados até código ter mais type hints)

### Tests

- ✅ **pytest:** 7/7 testes passando

---

## Como validar localmente

### Ativar venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Lint (black):

```powershell
black --check --line-length=120 src/ tests/
```

### Lint (flake8):

```powershell
flake8 src/ tests/ --max-line-length=120 --ignore=E203,W503
```

### Check imports (isort):

```powershell
isort --check-only --profile=black --line-length=120 src/ tests/
```

### Typecheck (mypy):

```powershell
mypy src/ --ignore-missing-imports --no-implicit-optional
```

### Run tests:

```powershell
pytest tests/ -v
```

### Run tests with coverage:

```powershell
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## GitHub Actions

**Workflow:** `.github/workflows/ci.yml`
**Status:** ✅ Configurado (será ativado no próximo push)
**URL:** https://github.com/GHKava/banco-dados-publicos/actions

### Primeira execução esperada:

- Trigger: Push do commit T-003
- Matrix: 3 jobs (Python 3.11, 3.12, 3.14)
- Duração estimada: ~3-5 min por job
- Resultado esperado: ✅ PASS (lint + tests passam)

---

## Decisões

**DEC-011:** Continue-on-error para mypy e pytest inicialmente (até código ter mais type hints e testes reais). Lint (black/flake8/isort) é blocking.

**DEC-012:** Matrix strategy com 3 versões Python (3.11, 3.12, 3.14) para garantir compatibilidade ampla.

---

## Próximos Passos

1. **T-005:** Postgres schema v0 (criar models SQLAlchemy)
2. **T-007+:** Criar bots individuais (source_registry, policy_gate, etc.)
3. **T-061+:** Adicionar testes reais (unit/integration/e2e)
4. **T-final:** Remover continue-on-error de mypy/pytest quando código estiver maduro

---

**Evidência completa:** `/docs/evidence/T-003/`
