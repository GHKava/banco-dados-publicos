# WorkOrder T-009 — Bot: robots checker

**ID:** T-009
**Data criação:** 20260131
**Persona:** DE + SEC
**Roadmap link:** [[Roadmap detalhado do Projeto#T-009]]

---

## 1. Objetivo

Implementar bot para verificar robots.txt por URL/fonte, retornando status **allowed/disallowed/unknown** com justificativa e crawl-delay quando disponível.

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-008 (policy gate) completo
- [x] Arquivos-alvo definidos
- [x] Critérios de aceite documentados
- [x] Riscos identificados
- [x] Persona designada

---

## 3. Entradas

- `src/bots/policy_gate.py` (contexto de compliance)
- `configs/sources.yaml` (URLs de referência)
- RFC/robots.txt spec (conhecimento padrão)

---

## 4. Saídas (Artefatos esperados)

- `src/bots/robots_checker.py` (nova implementação)
- `tests/test_robots_checker.py` (testes unitários)
- `docs/evidence/T-009/`:
  - `commands.log`
  - `tests.log`
  - `files_changed.json`
  - `notes.md`

---

## 5. Comandos previstos

```bash
pytest -q tests/test_robots_checker.py
```

---

## 6. Riscos

| Risco                         | Severidade | Mitigação                                   |
| ----------------------------- | ---------- | ------------------------------------------- |
| robots.txt inválido (HTML)    | Média      | Reportar status unknown                     |
| Bloqueio indevido por falhas  | Alta       | Não inferir bloqueio quando fetch falhar    |
| Divergência de user-agent     | Média      | Parametrizar user-agent no checker          |

---

## 7. Evidência mínima necessária

- [x] commands.log (comandos executados)
- [x] tests.log (pytest)
- [x] files_changed.json (arquivos criados/alterados)
- [x] notes.md (resumo + decisões)

---

## 8. Quality Gate aplicável

- [x] Tests (pytest)
- [x] Lint (black/isort) — se necessário

---

## 9. Próximo passo (tarefa dependente)

T-010: Audit logging

---

**Criado por:** ORQ
**Data:** 20260131
