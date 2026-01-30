# Roadmap detalhado do Projeto

**Data criação:** 2026-01-30
**Atualização:** 2026-01-30
**Estado:** INICIALIZADO (5 primeiras tarefas READY)

---

## 📊 Tabela de tarefas (versão resumida para MVP)

| Ordem | ID            | Nome                              | Descrição                                              | Persona  | Dependências        | Status  | retry_count | Início     | Fim        | Link WorkOrder                               | Link Evidence                | Link Handoff                               |
| ----- | ------------- | --------------------------------- | ------------------------------------------------------ | -------- | ------------------- | ------- | ----------- | ---------- | ---------- | -------------------------------------------- | ---------------------------- | ------------------------------------------ |
| 1     | T-001         | Git setup + GitHub                | Init repo, .gitignore, GitHub remote                   | TL       | Nenhuma             | READY   | 0           | —          | —          | [T-001](WorkOrders/T-001.md)                 | docs/evidence/T-001/         | [T-001](Handoffs/T-001.md)                 |
| 2     | T-002         | Python bootstrap                  | venv, deps, pre-commit hooks                           | TL       | T-001               | DONE    | 0           | 2026-01-30 | 2026-01-30 | [T-002](WorkOrders/T-002-WorkOrder.md)       | docs/evidence/T-002/         | [T-002](Handoffs/T-002-Handoff.md)         |
| 3     | T-003         | CI/tests/lint/typecheck           | GitHub Actions, pytest, mypy                           | TL       | T-002               | DONE    | 0           | 2026-01-30 | 2026-01-30 | [T-003](WorkOrders/T-003-WorkOrder.md)       | docs/evidence/T-003/         | [T-003](Handoffs/T-003-Handoff.md)         |
| 4     | T-004         | Allowlist + sources.yaml          | Definir fontes iniciais, regras                        | PM       | Nenhuma (paralela)  | DONE    | 0           | 2026-01-30 | 2026-01-30 | [T-004](WorkOrders/T-004.md)                 | docs/evidence/T-004/         | [T-004](Handoffs/T-004.md)                 |
| 4.1   | T-ONB-SRC-001 | Onboarding SRC-001 (DOU)          | Compliance check: robots/ToS/licença DOU               | PM+LEGAL | T-004               | READY   | 0           | —          | —          | [T-ONB-SRC-001](WorkOrders/T-ONB-SRC-001.md) | docs/evidence/T-ONB-SRC-001/ | [T-ONB-SRC-001](Handoffs/T-ONB-SRC-001.md) |
| 4.2   | T-ONB-SRC-002 | Onboarding SRC-002 (Planalto)     | Compliance check: robots/ToS/licença Planalto          | PM+LEGAL | T-004               | READY   | 0           | —          | —          | [T-ONB-SRC-002](WorkOrders/T-ONB-SRC-002.md) | docs/evidence/T-ONB-SRC-002/ | [T-ONB-SRC-002](Handoffs/T-ONB-SRC-002.md) |
| 4.3   | T-ONB-SRC-003 | Onboarding SRC-003 (IBGE)         | Compliance check: robots/ToS/licença IBGE APIs         | PM+LEGAL | T-004               | READY   | 0           | —          | —          | [T-ONB-SRC-003](WorkOrders/T-ONB-SRC-003.md) | docs/evidence/T-ONB-SRC-003/ | [T-ONB-SRC-003](Handoffs/T-ONB-SRC-003.md) |
| 4.4   | T-ONB-SRC-004 | Onboarding SRC-004 (BCB)          | Compliance check: robots/ToS/licença BCB Dados Abertos | PM+LEGAL | T-004               | READY   | 0           | —          | —          | [T-ONB-SRC-004](WorkOrders/T-ONB-SRC-004.md) | docs/evidence/T-ONB-SRC-004/ | [T-ONB-SRC-004](Handoffs/T-ONB-SRC-004.md) |
| 4.5   | T-ONB-SRC-005 | Onboarding SRC-005 (dados.gov.br) | Compliance check + license tracking table              | PM+LEGAL | T-004               | READY   | 0           | —          | —          | [T-ONB-SRC-005](WorkOrders/T-ONB-SRC-005.md) | docs/evidence/T-ONB-SRC-005/ | [T-ONB-SRC-005](Handoffs/T-ONB-SRC-005.md) |
| 5     | T-005         | Postgres schema v0                | Tables: sources, docs, chunks, embeddings              | DE       | T-002               | DONE    | 0           | 2026-01-30 | 2026-01-30 | [T-005](WorkOrders/T-005-WorkOrder.md)       | docs/evidence/T-005/         | [T-005](Handoffs/T-005-Handoff.md)         |
| 6     | T-006         | Redis + RQ setup                  | Redis, RQ job queue, workers                           | TL       | T-005               | BLOCKED | 0           | —          | —          | —                                            | —                            | —                                          |
| 7     | T-007         | Bot: source registry              | CLI: CRUD de fontes + rules                            | DE       | T-005, T-004        | BLOCKED | 0           | —          | —          | —                                            | —                            | —                                          |
| 8     | T-008         | Bot: policy gate                  | Lógica: ALLOW/BLOCK/METADATA_ONLY                      | DE       | T-007, SEC approved | BLOCKED | 0           | —          | —          | —                                            | —                            | —                                          |
| ...   | ...           | ...                               | ...                                                    | ...      | ...                 | ...     | ...         | ...        | ...        | ...                                          | ...                          | ...                                        |

---

## Fases (visão estruturada)

### **FASE 0 — Setup & Infraestrutura** (T-001 a T-006)

- [ ] T-001 — Git setup (READY)
- [ ] T-002 — Python bootstrap (READY)
- [ ] T-003 — CI/tests/lint (READY)
- [ ] T-004 — Allowlist + sources.yaml (READY)
- [ ] T-005 — Postgres schema v0 (READY)
- [ ] T-006 — Redis + RQ (BLOCKED → T-005)

### **FASE A — Governança & Compliance** (T-007 a T-010)

- [ ] T-007 — Bot: source registry (BLOCKED → T-005, T-004)
- [ ] T-008 — Bot: policy gate (BLOCKED → T-007)
- [ ] T-009 — Bot: robots checker (BLOCKED → T-008)
- [ ] T-010 — Audit logging (BLOCKED → T-008)

### **FASE B — Discovery & Frontier** (T-011 a T-015)

- [ ] T-011 — Bot: URL frontier (BLOCKED → T-010)
- [ ] T-012 — Bot: discovery sitemap (BLOCKED → T-011)
- [ ] T-013 — Bot: discovery RSS (BLOCKED → T-011)
- [ ] T-014 — Bot: change detector (BLOCKED → T-011)
- [ ] T-015 — Frontier scheduler (BLOCKED → T-011)

### **FASE C — Fetch & Raw Storage** (T-016 a T-020)

- [ ] T-016 — Bot: HTTP fetcher (BLOCKED → T-015)
- [ ] T-017 — Bot: fetch validator (BLOCKED → T-016)
- [ ] T-018 — Bot: raw store (BLOCKED → T-016)
- [ ] T-019 — Bot: content safety (BLOCKED → T-018)
- [ ] T-020 — Observability (logs estruturados) (BLOCKED → T-018)

### **FASE D — Parsing & Extraction** (T-021 a T-026)

- [ ] T-021 — Bot: HTML parser (BLOCKED → T-020)
- [ ] T-022 — Bot: PDF parser (BLOCKED → T-020)
- [ ] T-023 — Bot: OCR detector (BLOCKED → T-022)
- [ ] T-024 — Bot: OCR executor (BLOCKED → T-023)
- [ ] T-025 — Bot: text normalizer (BLOCKED → T-024)
- [ ] T-026 — Test: golden parsing (BLOCKED → T-025)

### **FASE E — Cleaning & Dedup** (T-027 a T-031)

- [ ] T-027 — Bot: quality scorer (BLOCKED → T-026)
- [ ] T-028 — Bot: dedup exact (BLOCKED → T-027)
- [ ] T-029 — Bot: dedup near (BLOCKED → T-028)
- [ ] T-030 — Bot: language detector (BLOCKED → T-029)
- [ ] T-031 — Bot: version manager (BLOCKED → T-030)

### **FASE F — Compliance Gate & PII** (T-032 a T-036)

- [ ] T-032 — Bot: PII detector (BLOCKED → T-031)
- [ ] T-033 — Bot: redactor (BLOCKED → T-032)
- [ ] T-034 — Bot: sensitivity classifier (BLOCKED → T-033)
- [ ] T-035 — Golden tests: PII (BLOCKED → T-034)
- [ ] T-036 — Retenção policies (BLOCKED → T-034)

### **FASE G — Enrichment** (T-037 a T-040)

- [ ] T-037 — Bot: metadata extractor (BLOCKED → T-036)
- [ ] T-038 — Bot: entity extractor (BLOCKED → T-037)
- [ ] T-039 — Bot: topic classifier (BLOCKED → T-038)
- [ ] T-040 — Bot: link graph (BLOCKED → T-039)

### **FASE H — Chunking** (T-041 a T-044)

- [ ] T-041 — Bot: chunker (BLOCKED → T-040)
- [ ] T-042 — Bot: chunk validator (BLOCKED → T-041)
- [ ] T-043 — Bot: citation mapper (BLOCKED → T-042)
- [ ] T-044 — Bot: chunk store (BLOCKED → T-043)

### **FASE I — Embeddings & Indexing** (T-045 a T-049)

- [ ] T-045 — Bot: embedder (BLOCKED → T-044)
- [ ] T-046 — Bot: embedding cache (BLOCKED → T-045)
- [ ] T-047 — Bot: vector indexer (pgvector) (BLOCKED → T-046)
- [ ] T-048 — Bot: hybrid ranker (BLOCKED → T-047)
- [ ] T-049 — Bot: retrieval evaluator (BLOCKED → T-048)

### **FASE J — Persistence** (T-050 a T-052)

- [ ] T-050 — Zone management (raw/processed/curated) (BLOCKED → T-049)
- [ ] T-051 — Metadata DB finalization (BLOCKED → T-050)
- [ ] T-052 — Vector store finalization (BLOCKED → T-050)

### **FASE K — RAG Serving API** (T-053 a T-055)

- [ ] T-053 — BE: retrieval endpoint (BLOCKED → T-052)
- [ ] T-054 — Auth + rate limits (BLOCKED → T-053)
- [ ] T-055 — API documentation (BLOCKED → T-054)

### **FASE L — Operations** (T-056 a T-060)

- [ ] T-056 — Scheduler + job orchestration (BLOCKED → T-055)
- [ ] T-057 — Monitoring + dashboards (BLOCKED → T-056)
- [ ] T-058 — Runbooks (BLOCKED → T-057)
- [ ] T-059 — Cost guard + budgets (BLOCKED → T-057)
- [ ] T-060 — Change governance (ADRs, schemas) (BLOCKED → T-059)

### **FASE M — Testing & QA** (T-061 a T-065) [PARALLEL com outras fases]

- [ ] T-061 — Unit tests (BLOCKED → fases correspondentes)
- [ ] T-062 — Integration tests (BLOCKED → T-061)
- [ ] T-063 — E2E golden tests (BLOCKED → T-062)
- [ ] T-064 — Security scan (BLOCKED → T-063)
- [ ] T-065 — Performance tests (BLOCKED → T-064)

### **FINAL — Encerramento** (T-066+)

- [ ] T-066 — Release v1.0.0 (BLOCKED → todas DONE)
- [ ] T-067 — Relatório final (BLOCKED → T-066)
- [ ] T-068 — Operator guide (BLOCKED → T-067)

---

## Legenda

- **Status:** READY = pronto; IN_PROGRESS = em execução; VERIFYING = validação; DONE = concluído; BLOCKED = aguardando dependência; BYPASSED = pulado com CR; FAILED = falhou.
- **retry_count:** Quantas vezes já foi tentada (max = 3).
- **Dependências:** Outras tarefas que devem estar DONE antes.
- **Persona:** Quem executa (TL, DE, BE, QA, SEC, PM, etc.).

---

## Estatísticas

| Métrica          | Valor                  |
| ---------------- | ---------------------- |
| Total de tarefas | ~68                    |
| Prontas (READY)  | 5                      |
| Bloqueadas       | ~60                    |
| Estimativa total | 15-20 dias (part-time) |
| Velocidade alvo  | 5 tarefas/rodada       |

---

## Próxima ação

✅ Completar T-001 a T-005 (primeira rodada de sprint)

---
