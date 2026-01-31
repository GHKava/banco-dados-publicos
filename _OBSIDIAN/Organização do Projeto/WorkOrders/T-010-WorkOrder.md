# WorkOrder T-010 — Audit Logging

**ID:** T-010
**Data criação:** 20260130
**Persona:** DE (Data Engineer)
**Roadmap link:** [[Roadmap detalhado do Projeto#T-010]]

---

## 1. Objetivo

Implementar sistema de audit logging para rastrear todas as operações de compliance, policy decisions, e modificações em sources/metadata.

---

## 2. DoR Checklist

- [x] T-009 (Robots checker) completo
- [x] Postgres database disponível
- [x] SQLAlchemy ORM configurado (T-005)
- [x] Policy gate implementado (T-008)

---

## 3. Entradas

- Operações de compliance (policy checks, robots.txt fetches)
- Modificações em sources (CRUD operations via T-007)
- Decisões de ingestão (ALLOW/BLOCK/METADATA_ONLY)

---

## 4. Saídas (Artefatos esperados)

- `src/database/audit_log.py`:
  - `log_event(event_type, source_id, details, user_id=None)` (criar registro)
  - `query_audit_log(filters)` (buscar logs)
  - `AuditLog` model (SQLAlchemy)
- Alembic migration: `alembic/versions/xxx_add_audit_logs.py`
- `tests/test_audit_logging.py` (6+ testes)
- Evidence Pack em `docs/evidence/T-010/`

---

## 5. Schema

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,  -- 'policy_check', 'source_update', 'fetch_attempt'
    source_id VARCHAR(50),
    user_id VARCHAR(100),
    details JSONB,  -- Metadata flexível
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    ip_address VARCHAR(50)
);

CREATE INDEX idx_audit_logs_source_id ON audit_logs(source_id);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
```

---

## 6. Comandos previstos

```powershell
# Gerar migration
alembic revision --autogenerate -m "Add audit_logs table"

# Aplicar migration
alembic upgrade head

# Rodar testes
pytest tests/test_audit_logging.py -v

# Lint
black src/database/audit_log.py
flake8 src/database/audit_log.py
mypy src/database/audit_log.py
```

---

## 7. Riscos

| Risco                       | Severidade | Mitigação                                           |
| --------------------------- | ---------- | --------------------------------------------------- |
| Performance (muitos logs)   | Média      | Index em timestamp, async writes (defer para T-020) |
| JSONB details sem validação | Baixa      | Schema informal OK para MVP, validação futura       |
| Logs sensíveis (PII)        | Alta       | NUNCA logar PII, apenas IDs + metadata              |

---

## 8. Evidência mínima necessária

- [x] audit_log.py implementado
- [x] Migration aplicada (alembic upgrade head)
- [x] tests_audit_logging.py (6+ testes, 100% pass)
- [x] commands.log (alembic + pytest)
- [x] outputs.log (saídas de comandos)
- [x] notes.md (decisões + tempo)

---

## 9. Quality Gate

- [ ] Lint (black, flake8, isort) ✅
- [ ] Tests (pytest 6/6 passing) ✅
- [ ] Typecheck (mypy) ✅
- [ ] Migration aplicada sem errors

---

## 10. Próximo passo

T-011: Bot - URL frontier

---

**Criado por:** ORQ
**Data:** 20260130 23:58 UTC

---
