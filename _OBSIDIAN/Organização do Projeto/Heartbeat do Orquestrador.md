# Heartbeat do Orquestrador — Banco de Dados Interrelacional

**Última atualização:** 2026-01-30 19:40 UTC
**Rodada:** #3 (T-003 CI/TESTS/LINT)
**Status:** 🔄 T-003 IN_PROGRESS

---

## Rodada #2 — T-002: Python bootstrap + venv + pre-commit (2026-01-30)

### Tarefas executadas nesta rodada

- **T-002:** Python bootstrap + venv + pre-commit
  - Status: ✅ DONE
  - Tempo: ~60 min
  - Persona: TL (Tech Lead)
  - Ações:
    - Ambiente virtual criado: `.venv/` (Python 3.14.2)
    - 66 packages core instalados (fastapi, sqlalchemy, pytest, black, mypy, etc.)
    - Correções de compatibilidade Python 3.14:
      - scikit-learn, datasketch, lxml, pydantic, pydantic-settings, psycopg
    - Bootstrap.ps1 corrigido: venv → .venv
    - Pre-commit hooks configurados (.pre-commit-config.yaml criado)
    - Arquivo .env criado a partir de .env.example
    - Commit d0c256b + push para origin/master
  - WorkOrder: [T-002-WorkOrder.md](WorkOrders/T-002-WorkOrder.md)
  - Evidence: [T-002 Evidence Pack](../../docs/evidence/T-002/)
  - Handoff: [T-002-Handoff.md](Handoffs/T-002-Handoff.md)

### Tarefas do próximo ciclo (READY)

1. **T-003:** CI/tests/lint/typecheck (DESBLOQUEADA - T-002 DONE)
2. **T-ONB-SRC-001 a T-ONB-SRC-005:** Onboarding compliance de 5 fontes (READY)
3. **T-005:** Postgres schema v0 (READY - pode executar após T-002)

### Métricas da rodada

| Métrica                    | Valor                                                    |
| -------------------------- | -------------------------------------------------------- |
| Tarefas completadas        | 1 (T-002)                                                |
| Tempo total                | ~60 min                                                  |
| Bloqueadores resolvidos    | 0                                                        |
| Dependências desbloqueadas | 1 (T-003)                                                |
| Packages instalados        | 66 (core MVP)                                            |
| Files changed              | 8 (requirements, bootstrap, .pre-commit, .env, evidence) |
| Commits                    | 1 (d0c256b)                                              |

### STOP.md status

✅ **Não existe** → Loop continua (próxima rodada autorizada)

---

## Rodada #1 — T-001: Git setup + GitHub remote (2026-01-30)

### Tarefas executadas nesta rodada

- **T-001:** Git setup + GitHub remote
  - Status: ✅ DONE
  - Tempo: ~10 min
  - Persona: TL (Tech Lead)
  - Ações:
    - Repositório GitHub criado: https://github.com/GHKava/banco-dados-publicos
    - Remote `origin` configurado e testado
    - Branch `master` com tracking para `origin/master`
    - Push inicial completo (3 commits: 53a2fe6, d411ce9, defa893)
    - 47+ arquivos sincronizados
  - WorkOrder: [T-001-WorkOrder.md](WorkOrders/T-001-WorkOrder.md)
  - Evidence: [T-001-notes.md](../../docs/evidence/T-001-notes.md)
  - Handoff: [T-001-Handoff.md](Handoffs/T-001-Handoff.md)

### Tarefas do próximo ciclo (READY)

1. **T-002:** Python bootstrap + venv + pre-commit (READY - T-001 DONE)
2. **T-003:** CI/tests/lint/typecheck (BLOCKED - aguarda T-002)
3. **T-ONB-SRC-001 a T-ONB-SRC-005:** Onboarding compliance de 5 fontes (READY)
4. **T-005:** Postgres schema v0 (READY - pode executar após T-002)

### Métricas da rodada

| Métrica                    | Valor                            |
| -------------------------- | -------------------------------- |
| Tarefas completadas        | 1 (T-001)                        |
| Tempo total                | ~10 min                          |
| Bloqueadores resolvidos    | 0                                |
| Dependências desbloqueadas | 1 (T-002)                        |
| Files changed              | 3 (WorkOrder, Evidence, Handoff) |
| Repos criados              | 1 (GitHub)                       |

### STOP.md status

✅ **Não existe** → Loop continua (próxima rodada autorizada)

---

## Rodada #0.1 — RESOLUÇÃO DUV-001/DUV-002 (2026-01-30)

### Tarefas executadas nesta rodada

- **T-DUV-001-002:** Resolução de DUV-001 e DUV-002 + criação de allowlist completa
  - Status: ✅ DONE
  - Tempo: ~30 min
  - Ações:
    - DUV-001 RESOLVIDA: GitHub pessoal FREE (DEC-007)
    - DUV-002 RESOLVIDA: Allowlist com 5 fontes gov (DEC-008)
    - Criados: configs/sources.yaml, Fontes_Licencas.md
    - Criado: Template - Source Onboarding Checklist.md
    - Criados: 5 onboarding notes (SRC-001 a SRC-005)
    - Atualizados: Backlog.md, Dúvidas & Decisões.md
    - Atualizado: Escopo.md (nova seção Allowlist e Onboarding)
    - Git init + commit inicial realizado
  - Evidence: Commit 53a2fe6 (47 files changed, 7086+ insertions)

### Tarefas do próximo ciclo (READY)

1. **T-001:** Git setup + GitHub remote (DESBLOQUEADA ✅)
2. **T-002:** Python bootstrap + venv + pre-commit
3. **T-003:** CI/tests/lint/typecheck
4. **T-004:** Define allowlist + sources.yaml (✅ DONE)
5. **T-ONB-SRC-001 a T-ONB-SRC-005:** Onboarding compliance de 5 fontes (READY)
6. **T-005:** Postgres schema v0

### Dúvidas abertas (SLA 24h)

| ID      | Descrição                     | SLA      | Status       | Resolução                     |
| ------- | ----------------------------- | -------- | ------------ | ----------------------------- |
| DUV-001 | GitHub org: pessoal ou nova?  | 20260131 | ✅ RESOLVIDA | GitHub pessoal FREE (DEC-007) |
| DUV-002 | Primeiras 5 fontes allowlist? | 20260131 | ✅ RESOLVIDA | 5 fontes gov (DEC-008)        |

### Métricas da rodada

| Métrica                    | Valor                                                           |
| -------------------------- | --------------------------------------------------------------- |
| Tarefas completadas        | 1 (T-DUV-001-002)                                               |
| Tempo total                | ~30 min                                                         |
| Dúvidas resolvidas         | 2 (DUV-001, DUV-002)                                            |
| Dependências desbloqueadas | 2 (T-001, T-004)                                                |
| Files changed              | 47 (sources.yaml, onboarding notes, templates, Escopo.md, etc.) |
| Commits                    | 1 (53a2fe6)                                                     |

### STOP.md status

✅ **Não existe** → Loop continua (próxima rodada autorizada)

---

## Rodada #0 — INICIAÇÃO (2026-01-30)

### Tarefas executadas nesta rodada

- **T-000:** Preflight + scaffold inicial
  - Status: ✅ DONE
  - Tempo: ~15 min
  - WorkOrder: [T-000.md](WorkOrders/T-000.md)
  - Evidence: [docs/evidence/T-000/](../../docs/evidence/T-000/)
  - Handoff: [T-000.md](Handoffs/T-000.md)

---

## Histórico de rodadas anteriores

(Nenhuma anterior à #0)

---

## Observações operacionais

1. ✅ Estrutura Obsidian criada completamente
2. ✅ Documentos mandatórios inicializados
3. ✅ Personas templates prontos
4. ✅ WorkOrders/Handoffs/CRs pastas criadas
5. ✅ DUV-001 e DUV-002 RESOLVIDAS
6. ✅ Allowlist com 5 fontes governamentais criada (policy fail-closed)
7. ✅ Git inicializado + commit inicial (53a2fe6)
8. ✅ T-001 e T-004 DESBLOQUEADAS
9. ⏳ Próxima: T-001 (Git setup + remote GitHub)

---

## SLA Tracker (geral)

| Tipo         | Total | Aberto | Vencido | Resolvido | Próx. revisão |
| ------------ | ----- | ------ | ------- | --------- | ------------- |
| Dúvidas      | 2     | 0      | 0       | 2         | —             |
| Impedimentos | 0     | 0      | 0       | 0         | —             |

---

## Proximas ações imediatas

- [ ] Iniciar T-001 (Git setup + configurar remote GitHub)
- [ ] Criar WorkOrder T-001
- [ ] Assumir persona TL para T-001
- [ ] Push inicial para GitHub
- [ ] Opcional: Iniciar T-ONB-SRC-001 (onboarding compliance DOU)

---

**Próxima atualização:** Ao final de T-001 ou quando orçamento de rodada atingir 90 min.

---
