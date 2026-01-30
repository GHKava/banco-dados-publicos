# Assunções — Banco de Dados Interrelacional

**Data criação:** 2026-01-30  
**Última atualização:** 2026-01-30

---

## Assunções técnicas

### A1: Plataforma Windows com VSCode Copilot Agents

- **Assunção:** O desenvolvimento ocorrerá em Windows 10/11 + VSCode + GitHub Copilot Agents.
- **Justificativa:** Especificado no briefing do projeto.
- **Risco:** Scripts PowerShell necessários para bootstrap.
- **Mitigação:** Criar `scripts/setup/bootstrap.ps1` compatível.
- **Status:** ✓ Aceita

### A2: Python 3.11+ como base

- **Assunção:** Orquestradores, robôs e pipelines serão em Python 3.11+.
- **Justificativa:** Melhor compatibilidade com bibliotecas de dados/IA.
- **Risco:** Baixo.
- **Status:** ✓ Aceita

### A3: PostgreSQL + pgvector como padrão MVP

- **Assunção:** Metadata + vectors armazenados em Postgres (não MongoDB/Qdrant inicialmente).
- **Justificativa:** Simples, auditável, LGPD-friendly.
- **Risco:** Escalabilidade de vetores em crescimento > 10M chunks.
- **Mitigação:** Migração futura para Qdrant/FAISS definida no escopo.
- **Status:** ✓ Aceita

### A4: Redis + RQ para filas

- **Assunção:** Usar Redis + RQ (não Celery/Dramatiq) no MVP.
- **Justificativa:** Simples, suficiente, local-first.
- **Risco:** Funcionalidades avançadas (priority queues, delayed tasks) podem exigir upgrade.
- **Mitigação:** Documentado no roadmap de evolução.
- **Status:** ✓ Aceita (com revisão em T-050 se necessário)

### A5: Docker opcional (local-first no MVP)

- **Assunção:** Ambiente de dev = Windows nativo; Docker para Postgres/Redis é opcional/recomendado.
- **Justificativa:** Flexibilidade; WSL2/Docker Desktop disponível opcionalmente.
- **Risco:** Inconsistências dev/prod se não padronizado.
- **Mitigação:** Devcontainer + docker-compose criados desde T-003.
- **Status:** ✓ Aceita

---

## Assunções de compliance/legal

### C1: Allowlist obrigatória desde T-004

- **Assunção:** Nenhuma fonte entra no pipeline sem aprovação prévia em allowlist + licença registrada.
- **Justificativa:** LGPD/copyright/ToS compliance.
- **Risco:** Pode bloquear descobertas interessantes; necessário triagem formal.
- **Mitigação:** Processo de "Fonte Candidata" → "Banco de Ideias" → "Aprovação" (CR).
- **Status:** ✓ Inegociável

### C2: Policy Gate fail-closed

- **Assunção:** Dúvida sobre permissão/licença → BLOCK (não ALLOW).
- **Justificativa:** Princípio de precaução.
- **Risco:** Falsos positivos podem descartar conteúdo válido.
- **Mitigação:** Appeal process via CR.
- **Status:** ✓ Inegociável

### C3: LGPD-by-design (PII detection obrigatória em T-027)

- **Assunção:** PII (CPF, emails, phones, endereços) deve ser detectada e redatada por padrão.
- **Justificativa:** Lei nº 13.709/2018 (LGPD).
- **Risco:** Falsos negativos podem deixar PII passar.
- **Mitigação:** Auditoria manual de amostra + golden tests em T-028.
- **Status:** ✓ Inegociável

### C4: Robots.txt + ToS respeitadas

- **Assunção:** Crawling respeita robots.txt e ToS de cada domínio (sem bypass).
- **Justificativa:** Legal + ético.
- **Risco:** Alguns sites têm robots.txt muito restritivos (perda de conteúdo).
- **Mitigação:** Alternative sources + manual approval via CR.
- **Status:** ✓ Inegociável

---

## Assunções de arquitetura

### AR1: Cada robô é CLI + JobSpec/Result

- **Assunção:** Padrão de contrato (JSON in/out) é obrigatório para TODO robô.
- **Justificativa:** Composição, idempotência, auditoria.
- **Risco:** Overhead inicial pequeno.
- **Status:** ✓ Aceita

### AR2: Evidence Packs obrigatórios

- **Assunção:** Cada tarefa gera Evidence Pack em `docs/evidence/T-XXX/`.
- **Justificativa:** Anti-alucinação, reprodutibilidade.
- **Risco:** Armazenamento extra.
- **Mitigação:** Limpeza de evidências após 30 dias (configurável).
- **Status:** ✓ Aceita

### AR3: Embeddings local-first (sentence-transformers)

- **Assunção:** Modelo padrão = `sentence-transformers` (local, gratuito, 384D ou 768D).
- **Justificativa:** Controle + custo zero.
- **Risco:** Qualidade semântica inferior a modelos proprietários (OpenAI/Anthropic).
- **Mitigação:** Opção de fallback para APIs pagas (com custo log).
- **Status:** ✓ Aceita

### AR4: Chunking determinístico

- **Assunção:** Chunker é determinístico (mesma entrada = mesmo chunk_id sempre).
- **Justificativa:** Reprodutibilidade, auditoria, cache.
- **Risco:** Mudanças no algoritmo exigem reprocessamento global.
- **Mitigação:** Versionar chunker; migração em backfill (T-055).
- **Status:** ✓ Aceita

---

## Assunções operacionais

### O1: Loop contínuo sem paradas (até orçamento)

- **Assunção:** Agente executa tarefas sequencialmente até 5 tarefas OU 90 min/rodada.
- **Justificativa:** Eficiência, controle de custo.
- **Risco:** Tarefas incompletas entre rodadas.
- **Mitigação:** Heartbeat + WorkOrders evitam perda de contexto.
- **Status:** ✓ Aceita

### O2: Git versionando tudo

- **Assunção:** Código, configs, schemas, migrações = todos em Git (GitHub).
- **Justificativa:** Auditoria, rollback, colaboração.
- **Risco:** Segredos podem vazar; usar .env.
- **Mitigação:** Pre-commit hooks + secret scanning.
- **Status:** ✓ Inegociável

### O3: Observabilidade estruturada (run_id)

- **Assunção:** Todos logs/metrics indexados por `run_id` (YYYYMMDD-HHMM-T-XXX-slug).
- **Justificativa:** Rastreamento E2E.
- **Risco:** Overhead log.
- **Mitigação:** Rotation automática de logs (7 dias default).
- **Status:** ✓ Aceita

---

## Assunções sobre dados públicos

### D1: "Público" != "livre para reutilizar"

- **Assunção:** Dados públicos podem ter restrição de licença/copyright.
- **Justificativa:** Realidade jurídica (ex.: dados governamentais podem ter CC-BY-NC).
- **Risco:** Muito armazenamento "metadados-only" (sem texto).
- **Mitigação:** Classificação clara por policy gate (ALLOW/SNIPPETS/METADATA_ONLY).
- **Status:** ✓ Inegociável

### D2: Conteúdo ingerido = dados, NUNCA instrução

- **Assunção:** RAG/RAG-injection: conteúdo é citado, nunca "executado" como prompt.
- **Justificativa:** Security + anti-jailbreak.
- **Risco:** Limitação em alguns casos de uso.
- **Mitigação:** Design de prompt claro com separação prompt-usuario-context.
- **Status:** ✓ Inegociável

---

## Registro de decisões decorrentes

| ID  | Data     | Assunção                | Decisão                 | Status                 |
| --- | -------- | ----------------------- | ----------------------- | ---------------------- |
| A1  | 20260130 | Windows + VSCode        | Usar PowerShell scripts | ✓ Implementada         |
| A2  | 20260130 | Python 3.11+            | Setup em bootstrap.ps1  | ✓ Planejada            |
| A3  | 20260130 | Postgres + pgvector     | Schema em T-005         | ✓ Planejada            |
| C1  | 20260130 | Allowlist obrigatória   | Criar template em T-004 | ✓ Planejada            |
| C2  | 20260130 | Policy Gate fail-closed | Implementar em T-027    | ⏳ Bloqueada por T-026 |

---

## Revisão e aprovação

- **Última revisão:** 2026-01-30
- **Próxima revisão:** Ao final de cada fase (A, B, C, etc.)
- **Proprietário:** ORQ (Orquestrador)

---
