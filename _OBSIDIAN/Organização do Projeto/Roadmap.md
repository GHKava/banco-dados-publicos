# Roadmap Executivo — Banco de Dados Interrelacional de Dados Públicos

**Status:** INICIALIZADO  
**Data:** 2026-01-30  
**Orquestrador:** v1.0

---

## Visão geral (fases principais)

1. **FASE 0 — Setup & Infraestrutura (EM PROGRESSO)**
   - Estrutura Git/GitHub
   - Bootstrap Python/venv
   - Stack base (Postgres/Redis/Docker)
   - CI/Tests/Lint
   - _Link:_ [[Roadmap detalhado do Projeto#Fase 0]]

2. **FASE A — Governança & Compliance (READY)**
   - Definir policy gate
   - Allowlist de fontes
   - Registro de licenças
   - Robots/ToS rules
   - LGPD-by-design
   - _Link:_ [[Roadmap detalhado do Projeto#Fase A]]

3. **FASE B — Discovery & Frontier (BLOCKED → Fase A)**
   - Source Registry
   - URL discovery
   - Frontier scheduler
   - _Link:_ [[Roadmap detalhado do Projeto#Fase B]]

4. **FASE C — Fetch & Raw Storage (BLOCKED → Fase B)**
   - HTTP crawler
   - Raw zone storage
   - Observabilidade
   - _Link:_ [[Roadmap detalhado do Projeto#Fase C]]

5. **FASE D — Parsing & Extraction (BLOCKED → Fase C)**
   - HTML/PDF parsing
   - OCR (quando necessário)
   - Normalização
   - _Link:_ [[Roadmap detalhado do Projeto#Fase D]]

6. **FASE E — Cleaning & Dedup (BLOCKED → Fase D)**
   - Quality scoring
   - Exact + near-dup detection
   - Versioning
   - _Link:_ [[Roadmap detalhado do Projeto#Fase E]]

7. **FASE F — Compliance Gate & PII (BLOCKED → Fase E)**
   - Policy decision engine
   - PII detection/redaction
   - Audit logging
   - _Link:_ [[Roadmap detalhado do Projeto#Fase F]]

8. **FASE G — Enrichment (BLOCKED → Fase F)**
   - Metadata extraction
   - Entity extraction (NER)
   - Topic classification
   - _Link:_ [[Roadmap detalhado do Projeto#Fase G]]

9. **FASE H — Chunking (BLOCKED → Fase G)**
   - Deterministic chunker
   - Stable IDs
   - Metadata per chunk
   - _Link:_ [[Roadmap detalhado do Projeto#Fase H]]

10. **FASE I — Embeddings & Indexing (BLOCKED → Fase H)**
    - Local embeddings (sentence-transformers)
    - Pgvector integration
    - Hybrid search (FTS + vector)
    - _Link:_ [[Roadmap detalhado do Projeto#Fase I]]

11. **FASE J — Persistence & Storage (BLOCKED → Fase I)**
    - Postgres schema (metadata + vectors)
    - Zone management (raw/processed/curated)
    - Retention policies
    - _Link:_ [[Roadmap detalhado do Projeto#Fase J]]

12. **FASE K — RAG Serving API (BLOCKED → Fase J)**
    - FastAPI retrieval endpoint
    - Citation/grounding
    - Authorization
    - _Link:_ [[Roadmap detalhado do Projeto#Fase K]]

13. **FASE L — Operations & Scale (BLOCKED → Fase K)**
    - Scheduler/job queues
    - Monitoring/dashboards
    - Runbooks
    - Governance of changes
    - _Link:_ [[Roadmap detalhado do Projeto#Fase L]]

14. **FASE M — Testing & Quality (PARALLEL)**
    - Unit tests
    - Integration tests
    - Golden tests (E2E)
    - Security scanning
    - _Link:_ [[Roadmap detalhado do Projeto#Fase M]]

15. **FINAL — Project Closure**
    - Release v1.0.0
    - Operator guide
    - Bank of ideas
    - _Link:_ [[Roadmap detalhado do Projeto#Final]]

---

## Documentos associados

- _Roadmap detalhado:_ [[Roadmap detalhado do Projeto]]
- _Backlog & Issues:_ [[Backlog]]
- _Personas:_ [[../_OBSIDIAN/Personas/ORQ.md|ORQ]], [[../_OBSIDIAN/Personas/PM.md|PM]], [[../_OBSIDIAN/Personas/TL.md|TL]], etc.
- _Contexto global:_ [[Contexto Global de Agentes]]
- _Heartbeat:_ [[Heartbeat do Orquestrador]]
- _Log de execução:_ [[Log de Execução]]

---

## Próximas ações (THIS SPRINT)

[ ] T-001: Git setup + GitHub remote  
[ ] T-002: Python bootstrap + venv  
[ ] T-003: CI/tests/lint/typecheck  
[ ] T-004: Define allowlist + sources.yaml  
[ ] T-005: Postgres + pgvector schema (v0)

---
