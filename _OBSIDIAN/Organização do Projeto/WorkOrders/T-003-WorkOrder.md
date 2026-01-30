# WorkOrder T-003 — CI/tests/lint/typecheck

**ID:** T-003
**Data criação:** 20260130
**Persona:** TL (Tech Lead)
**Roadmap link:** [[Roadmap detalhado do Projeto#T-003]]

---

## 1. Objetivo

Configurar GitHub Actions CI pipeline com lint (black, isort, flake8), testes (pytest), typecheck (mypy), e security scan (bandit).

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-002 completa (Python bootstrap + venv + dependencies)
- [x] .venv criado com pytest, black, mypy, flake8, isort, bandit instalados
- [x] tests/ folder criado com test_basic.py
- [x] Critérios de aceite documentados
- [x] Persona designada (TL)

---

## 3. Entradas

- `.venv/` com packages: pytest, black, mypy, flake8, isort, bandit
- `tests/test_basic.py` existente
- `src/` com código Python
- `pyproject.toml` para configuração de tools

---

## 4. Saídas (Artefatos esperados)

- `.github/workflows/ci.yml` — GitHub Actions workflow
- `pyproject.toml` atualizado com configurações de lint/test/typecheck
- `tests/` com testes passando
- Evidence pack em `docs/evidence/T-003/`

---

## 5. Comandos previstos

```powershell
# Ativar ambiente
.venv\Scripts\Activate.ps1

# Rodar lint
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/

# Rodar typecheck
mypy src/

# Rodar testes
pytest tests/ -v

# Rodar security scan
bandit -r src/ -ll
```

---

## 6. Riscos

| Risco                              | Severidade | Mitigação                                  |
| ---------------------------------- | ---------- | ------------------------------------------ |
| Testes falhando                    | Média      | Corrigir código ou marcar skip temporário  |
| Lint/format conflitos              | Baixa      | Configurar pyproject.toml adequadamente    |
| GitHub Actions não configurado     | Baixa      | Usar template oficial de Python            |
| Mypy type errors em código inicial | Média      | Adicionar type hints ou configurar lenient |

---

## 7. Evidência mínima necessária

- [x] commands.log (comandos executados)
- [x] outputs.log (outputs dos comandos)
- [x] tests.log (pytest output)
- [x] files_changed.json (arquivos criados/alterados)
- [x] notes.md (resumo + decisões)

---

## 8. Quality Gate aplicável

- [x] Lint (black, isort, flake8) — OBRIGATÓRIO
- [x] Tests (pytest) — OBRIGATÓRIO
- [x] Typecheck (mypy) — OBRIGATÓRIO
- [x] Security (bandit) — OBRIGATÓRIO
- [x] GitHub Actions CI passando

---

## 9. Próximo passo (tarefa dependente)

- T-ONB-SRC-001 a T-ONB-SRC-005: Onboarding de fontes (READY)
- T-005: Postgres schema v0 (READY)

---

**Criado por:** ORQ
**Data:** 20260130

---
