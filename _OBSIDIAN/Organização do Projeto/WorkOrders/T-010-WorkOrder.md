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
  - `log_event(event_type, source_id, details, actor=None)`
  - `query_audit_log(filters)`
  - `get_audit_stats()`
- `tests/test_audit_log.py` (tests unitários com stubs)
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
# Rodar testes
pytest -q tests/test_audit_log.py
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
- [x] tests/test_audit_log.py (3 testes, pass)
- [x] commands.log (pytest)
- [x] tests.log (saídas de testes)
- [x] notes.md (decisões + tempo)

---

## 9. Quality Gate

- [x] Tests (pytest) ✅
- [x] Lint (black, flake8, isort) ✅

---

## 10. Próximo passo

T-011: Bot - URL frontier

---

**Criado por:** ORQ
**Data:** 20260130 23:58 UTC

---
