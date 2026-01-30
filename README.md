# Banco de Dados Interrelacional de Dados Públicos

**Versão:** 0.1.0-alpha  
**Status:** 🟡 Em Desenvolvimento (Phase 0 — Setup & Infraestrutura)

---

## 🎯 Visão geral

Pipeline industrial de ingestão → limpeza → enriquecimento → indexação → serving de dados públicos, com **governança e compliance como primeira etapa**.

- **Compliance-first:** Allowlist obrigatória, policy gate fail-closed, LGPD-by-design.
- **Local-first:** Embeddings em `sentence-transformers`, chunking determinístico, busca híbrida (FTS + vetor).
- **Reprodutível:** Evidence packs, manifesto por run_id, Git versionando tudo.
- **Modular:** CLI-based bots com contrato JSON (JobSpec/Result), orquestrador coordenador.

---

## 📦 Stack

- **Python 3.11+** (orquestradores, bots, pipelines)
- **PostgreSQL + pgvector** (metadata + vectors)
- **Redis + RQ** (job queue)
- **FastAPI** (RAG Retrieval API)
- **Docker Compose** (Postgres/Redis, opcional)
- **GitHub Actions** (CI: lint, tests, typecheck, security scan)

---

## 🚀 Quick Start

### Pré-requisitos

- Windows 10+ (com WSL2 recomendado para Docker)
- Python 3.11+
- Git

### Bootstrap (Windows PowerShell)

```powershell
cd projeto
scripts/setup/bootstrap.ps1
```

Este script:

- Cria venv (`venv/`)
- Instala dependências (`requirements.lock`)
- Configura pre-commit hooks
- Sobe Postgres/Redis (Docker, se disponível)
- Roda checks básicos

### Primeiros passos

1. **Inicialize o repo:**

   ```bash
   git init
   git add .
   git commit -m "chore: scaffold inicial do projeto (T-000)"
   ```

2. **Ler documentação:**
   - Escopo: `_OBSIDIAN/Organização do Projeto/Escopo.md` (imutável)
   - Roadmap: `_OBSIDIAN/Organização do Projeto/Roadmap.md` (executivo)
   - Contexto: `_OBSIDIAN/Organização do Projeto/Contexto Global de Agentes.md` (regras obrigatórias)

3. **Próxima tarefa:**
   - T-001: Git setup + GitHub remote
   - T-002: Python bootstrap + venv
   - T-003: CI/tests/lint/typecheck
   - [Ver Roadmap detalhado](../\_OBSIDIAN/Organização do Projeto/Roadmap detalhado do Projeto.md)

---

## 📁 Estrutura de pastas

```
.
├── src/                              # Código Python
│   ├── orchestrators/                # Orquestradores (control plane)
│   ├── bots/                         # Bots/scripts (data plane)
│   ├── core/                         # Núcleo (models, schemas, utils)
│   ├── api/                          # FastAPI (RAG Retrieval API)
│   └── db/                           # Database (SQLAlchemy, Alembic)
├── tests/                            # Testes (pytest)
├── docs/
│   ├── evidence/T-XXX/               # Evidence Pack por tarefa
│   ├── runbooks/                     # Runbooks operacionais
│   └── security/                     # Hardening, threat model
├── configs/                          # YAML/JSON (sources.yaml, etc.)
├── scripts/
│   ├── setup/                        # Setup/bootstrap
│   │   ├── bootstrap.ps1             # Bootstrap Windows
│   │   └── INSTALACOES.md            # Log de instalações
│   └── maintenance/                  # Manutenção
│       ├── README.md                 # Índice de scripts
│       └── [scripts de operação]
├── .devcontainer/                    # Ambiente padronizado (Docker)
├── .github/workflows/                # CI (GitHub Actions)
├── Arquivo/                          # Artefatos obsoletos
├── _OBSIDIAN/                        # Vault (documentação de projeto)
│   ├── Organização do Projeto/       # MANDATÓRIO
│   │   ├── Escopo.md                 # (imutável)
│   │   ├── Roadmap.md                # (executivo)
│   │   ├── Roadmap detalhado do Projeto.md
│   │   ├── Backlog.md                # (com SLA)
│   │   ├── Contexto Global de Agentes.md
│   │   ├── Prompt de Iniciação de Agente.md
│   │   ├── Log de Execução.md
│   │   ├── Heartbeat do Orquestrador.md
│   │   ├── Assunções.md
│   │   ├── Banco de Ideias.md
│   │   ├── Dúvidas & Decisões.md
│   │   ├── CRs/                      # Change Requests
│   │   ├── WorkOrders/               # Ordens de serviço (T-XXX)
│   │   └── Handoffs/                 # Transições (T-XXX)
│   ├── Personas/                     # Biblioteca de personas
│   │   ├── ORQ.md, PM.md, TL.md, DE.md, BE.md, QA.md, SEC.md, DPO.md
│   └── MOCs/                         # Índices por área
├── README.md                         # Este arquivo
├── .gitignore
├── .env.example
├── CHANGELOG.md
├── pyproject.toml                    # Deps + build config (ou requirements.txt)
└── docker-compose.yml (opcional)     # Postgres/Redis
```

---

## 📋 Documentos críticos

| Documento                                                                                                     | Objetivo                         | Status |
| ------------------------------------------------------------------------------------------------------------- | -------------------------------- | ------ |
| [Escopo.md](_OBSIDIAN/Organização%20do%20Projeto/Escopo.md)                                                   | Fonte de verdade (imutável)      | ✅     |
| [Roadmap.md](_OBSIDIAN/Organização%20do%20Projeto/Roadmap.md)                                                 | Visão executiva                  | ✅     |
| [Contexto Global de Agentes.md](_OBSIDIAN/Organização%20do%20Projeto/Contexto%20Global%20de%20Agentes.md)     | Regras obrigatórias para agentes | ✅     |
| [Roadmap detalhado do Projeto.md](_OBSIDIAN/Organização%20do%20Projeto/Roadmap%20detalhado%20do%20Projeto.md) | Tabela de tarefas completa       | ✅     |
| [Backlog.md](_OBSIDIAN/Organização%20do%20Projeto/Backlog.md)                                                 | Tarefas + dúvidas (SLA)          | ✅     |
| [Assunções.md](_OBSIDIAN/Organização%20do%20Projeto/Assunções.md)                                             | Decisões documentadas            | ✅     |

---

## 🔄 Fluxo de trabalho (Agente)

1. Ler [Contexto Global de Agentes.md](contexto-global-de-agentes)
2. Checar `STOP.md` (kill switch)
3. Rodar Preflight (integridade)
4. Selecionar tarefa READY em [Roadmap detalhado do Projeto.md](roadmap-detalhado)
5. Criar/ler WorkOrder
6. Marcar IN_PROGRESS + timestamp
7. Assumir persona + executar 100%
8. Gerar Evidence Pack em `docs/evidence/T-XXX/`
9. Rodar Quality Gate
10. Claim Check (tudo ok?)
11. Commit + Push (branch `feature/T-XXX-*`)
12. Marcar DONE + timestamp
13. Escrever Handoff
14. Loop até orçamento (5 tarefas OU 90 min) ou STOP.md

---

## ⚙️ Configuração

### Arquivo `.env`

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/public_db
DATABASE_ECHO=false

# Redis
REDIS_URL=redis://localhost:6379/0

# FastAPI
API_KEY_SECRET=seu-secret-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Embeddings
EMBEDDINGS_MODEL=sentence-transformers/paraphrase-MiniLM-L6-v2
EMBEDDINGS_CACHE_DIR=./data/embeddings_cache

# Logging
LOG_LEVEL=INFO
RUN_ID_PREFIX=YYYYMMDD-HHMM
```

Copie de `.env.example` e configure.

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Cobertura
pytest --cov=src

# Golden tests (E2E)
pytest tests/golden/

# Security scan
bandit -r src/
```

---

## 📝 Git workflow

### Branches

- `main`: versão estável (releases tagged)
- `develop`: integração de features (CI)
- `feature/T-XXX-*`: tarefa individual (uma feature branch por tarefa)

### Commits

Padrão obrigatório:

```
<tipo>(<escopo>): <descrição> (T-XXX)

<corpo: detalhes, decisões, impacto>

Evidence: docs/evidence/T-XXX/
Closes: #<issue> (se houver)
```

**Tipos:** `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`, `sec`.

**Exemplo:**

```
feat(policy-gate): implementar lógica de bloqueio de fontes (T-008)

- ALLOW/BLOCK/METADATA_ONLY/SNIPPETS_ONLY decisões
- Auditoria registrada em DB
- Testes golden em docs/evidence/T-008/

Evidence: docs/evidence/T-008/
```

---

## 🔐 Segurança

- **PII detection:** `presidio-analyzer` + `presidio-anonymizer`
- **Secret scanning:** Pre-commit hooks + GitHub secret scanning
- **Dependency scanning:** `bandit`, `safety`, `dependabot`
- **Hardening checklist:** [docs/security/hardening_checklist.md](docs/security/hardening_checklist.md)

---

## 📊 Observabilidade

- **Logs estruturados:** JSON com `run_id` (YYYYMMDD-HHMM-T-XXX-slug)
- **Métricas:** Por run, por etapa, por domínio
- **Runbooks:** [docs/runbooks/README.md](docs/runbooks/README.md)

---

## 📞 Suporte

- **Dúvidas:** Registre em [Backlog — Dúvidas & Impedimentos](../_OBSIDIAN/Organização%20do%20Projeto/Backlog.md#2-dúvidas--impedimentos-sla-24h) (SLA 24h)
- **Issues:** GitHub Issues (após v1.0)
- **Documentação:** [\_OBSIDIAN/Organização do Projeto/](../_OBSIDIAN/Organização%20do%20Projeto/)

---

## 📜 Licença

[A definir — verificar Escopo.md]

---

## 🎯 Próximos passos

- [ ] Completar T-001 a T-005 (primeira rodada)
- [ ] Decidir GitHub org (DUV-001)
- [ ] Definir allowlist inicial (DUV-002)
- [ ] Revisar Assunções.md

---

**Data criação:** 2026-01-30  
**Última atualização:** 2026-01-30  
**Mantido por:** ORQ (Orquestrador)

---
