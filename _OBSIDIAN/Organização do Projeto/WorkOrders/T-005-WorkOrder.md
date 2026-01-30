# WorkOrder T-005: Postgres schema v0 (metadata + pgvector)

**ID:** T-005
**Nome:** Postgres schema v0
**Status:** IN_PROGRESS
**Persona:** DE (Data Engineer)
**Dependências:** T-002 ✅ DONE
**Criado:** 2026-01-30 20:20 UTC
**Início previsto:** 2026-01-30 20:20 UTC
**Deadline:** Rodada #4 (target: 60-90 min)

---

## 🎯 Objetivo

Criar schema Postgres v0 para armazenar metadata de fontes, documentos, chunks de texto e embeddings vetoriais. Usar SQLAlchemy ORM + Alembic migrations + pgvector extension.

---

## 📋 Requisitos (Definition of Ready)

- [x] T-002 concluído (Python bootstrap + deps)
- [x] docker-compose.yml configurado com Postgres 16 + pgvector
- [x] sqlalchemy, psycopg, pgvector instalados (requirements.txt)
- [x] Alembic instalado (requirements.txt)

---

## 📦 Deliverables (Definition of Done)

1. **Alembic setup:**
   - [ ] `alembic init alembic/` executado
   - [ ] `alembic.ini` configurado com connection string do .env
   - [ ] `alembic/env.py` configurado para importar Base de SQLAlchemy

2. **SQLAlchemy models:**
   - [ ] `src/storage/models.py` criado com 5 tabelas:
     - `sources`: id, name, base_url, source_type, license_info, robots_policy, tos_compliance, status, created_at, updated_at
     - `documents`: id, source_id (FK), url, title, content_hash, metadata (JSONB), fetch_date, status, created_at, updated_at
     - `chunks`: id, document_id (FK), chunk_index, text, metadata (JSONB), created_at
     - `embeddings`: id, chunk_id (FK), model_name, vector (pgvector), created_at
     - `audit_log`: id, entity_type, entity_id, action, old_value (JSONB), new_value (JSONB), user_agent, timestamp
   - [ ] `src/storage/__init__.py` criado

3. **Initial migration:**
   - [ ] `alembic revision --autogenerate -m "Create initial schema v0"` executado
   - [ ] Migration testada com `alembic upgrade head`

4. **Postgres connection test:**
   - [ ] Docker Compose up: `docker compose up -d postgres`
   - [ ] pgvector extension verificada: `docker compose run --rm postgres-init`
   - [ ] Connection test script: `scripts/test_db_connection.py`

5. **Evidence pack:**
   - [ ] `docs/evidence/T-005/notes.md`
   - [ ] `docs/evidence/T-005/schema_diagram.md` (textual ER diagram)
   - [ ] `docs/evidence/T-005/commands.log`
   - [ ] `docs/evidence/T-005/files_changed.json`

6. **Documentation:**
   - [ ] Handoff: `_OBSIDIAN/Organização do Projeto/Handoffs/T-005-Handoff.md`
   - [ ] Roadmap: T-005 marcada DONE
   - [ ] Backlog: T-005 movida para DONE
   - [ ] Heartbeat: Rodada #4 fechada com métricas

---

## 🔧 Decisões Técnicas Pendentes

**DEC-013:** Usar UUID ou BIGSERIAL para primary keys?

- **Contexto:** UUIDs são mais distribuídos, BIGSERIALs são mais performáticos
- **Proposta:** BIGSERIAL para MVP (simplicidade)
- **Status:** A DECIDIR durante execução

**DEC-014:** Usar Alembic ou apenas SQLAlchemy.create_all()?

- **Contexto:** Alembic permite migrations versionadas
- **Proposta:** Alembic (best practice para produção)
- **Status:** A DECIDIR durante execução

**DEC-015:** Índices em embeddings.vector?

- **Contexto:** pgvector suporta HNSW e IVFFlat
- **Proposta:** IVFFlat para MVP (mais simples)
- **Status:** A DECIDIR durante execução

---

## 🧩 Estrutura Proposta

```
src/
  storage/
    __init__.py
    models.py          # SQLAlchemy models
    database.py        # Engine, session factory
alembic/
  env.py
  script.py.mako
  versions/
    xxxx_create_initial_schema_v0.py
scripts/
  test_db_connection.py
docs/
  evidence/
    T-005/
      notes.md
      schema_diagram.md
      commands.log
      files_changed.json
```

---

## 📌 Notas de Implementação

- **Postgres connection string:** `postgresql://postgres:postgres@localhost:5432/public_db` (do .env)
- **pgvector extension:** Instalada via `postgres-init` service no docker-compose
- **SQLAlchemy version:** 2.0.46 (async support disponível, mas usar sync para MVP)
- **Alembic version:** 1.14.2
- **Índices pgvector:** Criar após dados iniciais (~1000 rows mínimo)

---

## ⚠️ Riscos & Mitigações

| Risco                                  | Probabilidade | Impacto | Mitigação                                             |
| -------------------------------------- | ------------- | ------- | ----------------------------------------------------- |
| Docker Compose não starta Postgres     | Baixa         | Alto    | Testar `docker compose up -d` antes de criar schema   |
| pgvector extension falha na instalação | Média         | Alto    | Verificar logs: `docker compose logs postgres-init`   |
| Alembic migration falha                | Média         | Médio   | Testar migration em DB limpo: `alembic downgrade base |

---

## 🔗 Links

- **Roadmap:** [Roadmap detalhado](../Roadmap detalhado do Projeto.md)
- **Backlog:** [Backlog.md](../Backlog.md)
- **Dependências resolvidas:** [T-002 Handoff](../Handoffs/T-002-Handoff.md)
- **Próximas tarefas desbloqueadas:** T-006 (Redis + RQ), T-007 (Bot: source registry)

---

**Início:** 2026-01-30 20:20 UTC
**Status:** IN_PROGRESS
