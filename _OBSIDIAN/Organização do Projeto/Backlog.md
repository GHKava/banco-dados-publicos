# Backlog — Banco de Dados Interrelacional

**Data criação:** 2026-01-30  
**Última atualização:** 2026-01-30  
**SLA padrão de dúvidas:** 24h ou próxima rodada

---

## 1. TAREFAS DO BACKLOG

### READY (próximas tarefas a executar)

- **T-001:** Git setup + GitHub remote
  - Descrição: Inicializar repo Git local, configurar .gitignore, conectar remote GitHub.
  - Persona: TL (Tech Lead)
  - DoR: [ ] Nenhuma dependência
  - Dependências: Nenhuma
  - Link WorkOrder: (será criado ao iniciar)

- **T-002:** Python bootstrap + venv + pre-commit
  - Descrição: Criar `scripts/setup/bootstrap.ps1`, venv, instalar deps base, pre-commit hooks.
  - Persona: TL
  - DoR: [ ] T-001 concluído
  - Dependências: T-001
  - Link WorkOrder: (será criado ao iniciar)

- **T-003:** CI/tests/lint/typecheck (GitHub Actions)
  - Descrição: Configurar `.github/workflows/` (lint, pytest, mypy, security scan).
  - Persona: TL
  - DoR: [ ] T-002 concluído
  - Dependências: T-002
  - Link WorkOrder: (será criado ao iniciar)

- **T-004:** Define allowlist + sources.yaml template
  - Descrição: Criar `configs/sources.yaml` com template de fonte permitida, registro de licença, regras robots/ToS.
  - Persona: PM (Product Manager) + LEGAL (se houver)
  - DoR: [ ] Escopo de compliance definido
  - Dependências: Nenhuma (paralela com T-003)
  - Link WorkOrder: (será criado ao iniciar)

- **T-005:** Postgres schema v0 (metadata + pgvector)
  - Descrição: Criar schema Postgres: sources, docs, chunks, embeddings, audit log. Instalar pgvector extension.
  - Persona: DE (Data Engineer)
  - DoR: [ ] T-002 concluído; DB acessível
  - Dependências: T-002
  - Link WorkOrder: (será criado ao iniciar)

### IN_PROGRESS

(Nenhuma no momento)

### BLOCKED

(Nenhuma no momento)

### DONE

(Nenhuma no momento)

---

## 2. DÚVIDAS / IMPEDIMENTOS (SLA 24h)

| ID      | Data     | Tarefa | Descrição                                     | SLA      | Status       | Resolução                                                                                                                              |
| ------- | -------- | ------ | --------------------------------------------- | -------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| DUV-001 | 20260130 | Geral  | GitHub remoto: usar org pessoal ou novo?      | 20260131 | ✅ RESOLVIDA | Decisão: GitHub pessoal FREE. Registrado em DEC-007. (2026-01-30)                                                                      |
| DUV-002 | 20260130 | T-004  | Quais são as primeiras 5 fontes da allowlist? | 20260131 | ✅ RESOLVIDA | Decisão: SRC-001 (DOU), SRC-002 (Planalto), SRC-003 (IBGE), SRC-004 (BCB), SRC-005 (dados.gov.br). Registrado em DEC-008. (2026-01-30) |

---

## 3. HISTÓRICO DE COMMITS

| Data | Commit | Tarefa | Mensagem       |
| ---- | ------ | ------ | -------------- |
| —    | —      | —      | (nenhum ainda) |

---

## 4. DECISÕES DO ORQUESTRADOR

| ID      | Data     | Decisão                            | Justificativa                            | Impacto | Status   |
| ------- | -------- | ---------------------------------- | ---------------------------------------- | ------- | -------- |
| ORQ-001 | 20260130 | Usar RQ (não Celery) para MVP      | Simplicidade; upgrade futuro documentado | Baixo   | ✓ Aceita |
| ORQ-002 | 20260130 | Estrutura obsidian em `_OBSIDIAN/` | Convenção; separação clara de docs       | Baixo   | ✓ Aceita |

---

## 5. ISSUES INTERNAS (após max_retries ou bloqueios críticos)

(Nenhuma no momento)

---

## 6. BANCO DE IDEIAS (Triagem pendente)

| Ideia    | Data     | Descrição                         | Prioridade | Status  |
| -------- | -------- | --------------------------------- | ---------- | ------- |
| IDEA-001 | 20260130 | Integração com Slack para alertas | Média      | TRIAGEM |
| IDEA-002 | 20260130 | Dashboard Grafana (opcional)      | Baixa      | TRIAGEM |

---

## SLA Tracker

| Tipo         | Total | Aberto | Vencido | Resolvido |
| ------------ | ----- | ------ | ------- | --------- |
| Dúvidas      | 2     | 0      | 0       | 2         |
| Impedimentos | 0     | 0      | 0       | 0         |

**Próxima revisão:** 2026-01-31 (fim de rodada)

---
