# Dúvidas & Decisões — Banco de Dados Interrelacional

**Data criação:** 2026-01-30
**Última atualização:** 2026-01-30

---

## 📋 Dúvidas abertas (SLA 24h)

### DUV-004: Container Postgres existente sem pgvector — usar ou recriar? ✅ RESOLVIDA

**Data:** 2026-01-30
**Tarefa bloqueadora:** T-005
**Descrição:** Container `governanca-postgres` já ocupa porta 5432 (Postgres 16.11), mas não tem pgvector extension instalada.
**Opções:**

- A) Usar container existente, criar schema sem embeddings.vector (TEXT temporário)
- B) Parar container existente, subir `public_db_postgres` com pgvector
- C) Usar porta alternativa (5433) para novo container
- D) Instalar pgvector manualmente no container existente

**SLA:** Resolvido na própria rodada (auto-decisão ORQ)
**Status:** ✅ RESOLVIDA (2026-01-30)
**Resolução:** **Decisão: Opção A (schema sem vector type, usar TEXT para embeddings).**
Justificativa: MVP não precisa busca vetorial imediatamente; pgvector pode ser adicionado em T-015 (semantic search) via migration. TEXT permite armazenar embeddings como JSON array `[0.123, 0.456, ...]` temporariamente.
Registrado como DEC-013.

**Impacto:** T-005 pode prosseguir sem bloqueio; T-015 (semantic search) precisará migration `ALTER COLUMN embeddings.vector TYPE vector(384)` + CREATE INDEX.

---

### DUV-001: GitHub remoto — usar org pessoal ou criar nova? ✅ RESOLVIDA

**Data:** 2026-01-30
**Tarefa bloqueadora:** T-001
**Descrição:** Criar repo GitHub em qual organização?
**Opções:**

- A) Org pessoal do usuário (ex.: @gustavo)
- B) Nova org para projeto (ex.: @banco-dados-publicos-org)
- C) GitHub Free (sem org, público)

**SLA:** 2026-01-31 09:00 UTC
**Status:** ✅ RESOLVIDA (2026-01-30)
**Resolução:** **Decisão: GitHub pessoal FREE (opção A/C).**
Repo criado na conta pessoal do usuário, plano free, público. Registrado como DEC-007.

**Impacto:** T-001 desbloqueada.

---

### DUV-002: Allowlist inicial — quais as primeiras 5 fontes? ✅ RESOLVIDA

**Data:** 2026-01-30
**Tarefa bloqueadora:** T-004
**Descrição:** Qual é o escopo inicial de fontes públicas a ingerir?
**Questões:**

- Governamentais (IBGE, legislativo, judicial)?
- Acadêmicas (arXiv, SciELO)?
- Notícias/jornalismo (portais públicos)?
- Bases de dados abertas específicas (Wikidata, OpenStreetMap)?

**SLA:** 2026-01-31 09:00 UTC
**Status:** ✅ RESOLVIDA (2026-01-30)
**Resolução:** **Decisão: 5 fontes governamentais brasileiras (policy fail-closed):**

1. **SRC-001:** Diário Oficial da União (DOU) - in.gov.br
2. **SRC-002:** Planalto - Legislação - planalto.gov.br
3. **SRC-003:** IBGE - APIs e Dados - ibge.gov.br / servicodados.ibge.gov.br
4. **SRC-004:** Banco Central - Dados Abertos - dadosabertos.bcb.gov.br
5. **SRC-005:** dados.gov.br - Catálogo

**Regra:** METADATA_ONLY até licença verificada (fail-closed). Registrado como DEC-008.

**Impacto:** T-004 desbloqueada. Template + sources.yaml + Fontes_Licencas.md criados.

---

## ✅ Decisões registradas (resolvidas ou implementadas)

### DEC-001: Stack Python 3.11+ + FastAPI + Postgres + pgvector

**Data:** 2026-01-30
**Tipo:** Técnica
**Decisão:** Seguir stack especificado no Escopo.md exatamente.
**Justificativa:** Compliance, performance, suporte local-first.
**Impacto:** Baixo (já no escopo)
**Status:** ✅ IMPLEMENTADA (em Assunções.md A2, A3)

---

### DEC-002: Organização Obsidian em `_OBSIDIAN/Organização do Projeto/`

**Data:** 2026-01-30
**Tipo:** Operacional
**Decisão:** Pasta `_OBSIDIAN/` como raiz; `Organização do Projeto/` como subfolder mandatória.
**Justificativa:** Separação clara, versionagem, facilita backup/export.
**Impacto:** Estrutura estabelecida
**Status:** ✅ IMPLEMENTADA (em Roadmap.md, Backlog.md, etc.)

---

### DEC-003: RQ (não Celery) para MVP

**Data:** 2026-01-30
**Tipo:** Técnica
**Decisão:** Redis + RQ para filas no MVP. Upgrade documentado se necessário.
**Justificativa:** Simplicidade; suficiente para v1.0.
**Impacto:** Baixo; mitigado com doc de evolução
**Status:** ✅ IMPLEMENTADA (em Assunções.md A4)

---

### DEC-004: Policy Gate fail-closed (sem exceção)

**Data:** 2026-01-30
**Tipo:** Compliance
**Decisão:** Dúvida sobre permissão/licença → BLOCK sempre (jamais ALLOW por padrão).
**Justificativa:** Princípio de precaução; LGPD-compliance.
**Impacto:** Possível perda de conteúdo válido; mitigado por appeal process (CR).
**Status:** ✅ IMPLEMENTADA (em Assunções.md C2, Escopo.md)

---

### DEC-005: Embeddings local-first (sentence-transformers)

**Data:** 2026-01-30
**Tipo:** Técnica
**Decisão:** Modelo padrão: `sentence-transformers` (384D ou 768D, local, gratuito).
**Justificativa:** Controle total, custo zero, compatível com pgvector.
**Impacto:** Qualidade semântica pode ser inferior a modelos proprietários; fallback documentado.
**Status:** ✅ IMPLEMENTADA (em Assunções.md AR3, Escopo.md)

---

### DEC-006: OCR só quando necessário (fail-closed)

**Data:** 2026-01-30
**Tipo:** Operacional/Custo
**Decisão:** OCR é "fallback" somente quando PDF não tem texto nativo.
**Justificativa:** Custo (tempo + compute), qualidade variável.
**Impacto:** Alguns PDFs scaneados podem ser ignorados; aceitável.
**Status:** ✅ IMPLEMENTADA (em Escopo.md Fase D)

---

### DEC-007: GitHub pessoal FREE (resolução DUV-001)

**Data:** 2026-01-30
**Tipo:** Operacional
**Decisão:** Usar GitHub pessoal do usuário, plano FREE, repositório público.
**Justificativa:** Simplicidade, custo zero, suficiente para MVP. Migração para org dedicada pode ser feita futuramente se necessário.
**Impacto:** Baixo; repo público facilita colaboração.
**Status:** ✅ IMPLEMENTADA (Git init + remote configurado em T-001)

---

### DEC-008: Allowlist inicial com 5 fontes governamentais (resolução DUV-002)

**Data:** 2026-01-30
**Tipo:** Compliance + Produto
**Decisão:** Iniciar MVP com 5 fontes governamentais brasileiras:

- SRC-001: DOU (in.gov.br)
- SRC-002: Planalto (planalto.gov.br)
- SRC-003: IBGE (ibge.gov.br)
- SRC-004: BCB (dadosabertos.bcb.gov.br)
- SRC-005: dados.gov.br

**Regra obrigatória:** METADATA_ONLY até licença verificada com evidência (fail-closed).
**Justificativa:** Fontes públicas por natureza, mas compliance exige verificação explícita de ToS/licença antes de armazenar fulltext.
**Impacto:** MVP focado em fontes seguras; expansão via CR após onboarding completo.
**Status:** ✅ IMPLEMENTADA (configs/sources.yaml + Fontes_Licencas.md + 5 onboarding notes criados)

---

### DEC-013: Embeddings como TEXT (não pgvector) para MVP (resolução DUV-004)

**Data:** 2026-01-30
**Tipo:** Técnica
**Decisão:** Usar TEXT para armazenar embeddings no MVP (JSON array format: `[0.123, 0.456, ...]`). pgvector extension será adicionada em T-015 (semantic search) via migration.
**Justificativa:** Container Postgres existente não tem pgvector instalado; evitar reconfiguração de infra para desbloquear T-005. Busca vetorial não é crítica para MVP initial (metadata queries suficientes).
**Impacto:** Schema inicial sem índices vetoriais; T-015 precisará `ALTER COLUMN embeddings.vector TYPE vector(384)` + CREATE INDEX USING hnsw. Performance de busca semântica será subótima até migration.
**Status:** ✅ IMPLEMENTADA (em T-005 models.py)

---

## 📊 Matriz de rastreamento

| ID      | Tipo     | Status       | Bloqueador | Próx. ação | Data resolução |
| ------- | -------- | ------------ | ---------- | ---------- | -------------- |
| DUV-001 | Decisão  | ✅ RESOLVIDA | —          | —          | 2026-01-30     |
| DUV-002 | Decisão  | ✅ RESOLVIDA | —          | —          | 2026-01-30     |
| DEC-001 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-002 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-003 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-004 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-005 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-006 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-007 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |
| DEC-008 | Registro | ✅ DONE      | —          | —          | 2026-01-30     |

---

## 🔄 Próxima revisão

**Data:** Fim de cada Sprint (após T-005, T-010, etc.)
**Processo:** Resolver dúvidas abertas + registrar novas decisões

---
