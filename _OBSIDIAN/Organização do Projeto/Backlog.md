# Backlog — Banco de Dados Interrelacional

**Data criação:** 2026-01-30
**Última atualização:** 2026-01-31 02:10 UTC
**SLA padrão de dúvidas:** 24h ou próxima rodada

---

## 1. TAREFAS DO BACKLOG

### READY (próximas tarefas a executar)

- **T-005:** Postgres schema v0 (metadata + pgvector)
  - Descrição: Criar schema Postgres: sources, docs, chunks, embeddings, audit log. Instalar pgvector extension.
  - Persona: DE (Data Engineer)
  - DoR: [x] T-002 concluído; DB acessível
  - Dependências: T-002 ✅ DONE
  - Link WorkOrder: `_OBSIDIAN/Organização do Projeto/WorkOrders/T-005.md`
  - Status: READY

- **T-ONB-SRC-001 a T-ONB-SRC-005:** Onboarding de fontes (compliance check)
  - Descrição: Verificar robots.txt, ToS, licenças para DOU, Planalto, IBGE, BCB, dados.gov.br
  - Persona: PM + LEGAL
  - DoR: [x] T-004 concluído (sources.yaml)
  - Dependências: T-004 ✅ DONE
  - Link WorkOrders: (serão criados ao iniciar)

### IN_PROGRESS

(Nenhuma no momento)

### BLOCKED

(Nenhuma no momento — T-002 DESBLOQUEADA)

### DONE

- **T-001:** Git setup + GitHub remote
  - Data: 2026-01-30
  - Tempo: ~10 min
  - Resultado: Repo criado (https://github.com/GHKava/banco-dados-publicos), push inicial completo
  - Evidence: [T-001-notes.md](../../docs/evidence/T-001-notes.md)
  - Handoff: [T-001-Handoff.md](Handoffs/T-001-Handoff.md)

- **T-002:** Python bootstrap + venv + pre-commit
  - Data: 2026-01-30
  - Tempo: ~60 min
  - Resultado: 66 packages instalados, .venv criado, pre-commit configurado
  - Correções: requirements.txt atualizado para Python 3.14, bootstrap.ps1 fixado
  - Evidence: [T-002 Evidence Pack](../../docs/evidence/T-002/)
  - Handoff: [T-002-Handoff.md](Handoffs/T-002-Handoff.md)
  - Commit: d0c256b

- **T-003:** CI/tests/lint/typecheck
  - Data: 2026-01-30
  - Tempo: ~40 min
  - Resultado: GitHub Actions CI configurado (matrix 3.11/3.12/3.14), 7 testes dummy (100% coverage)
  - Correções: pytest-cov instalado, pre-commit fixes aplicados
  - Evidence: [T-003 Evidence Pack](../../docs/evidence/T-003/)
  - Handoff: [T-003-Handoff.md](Handoffs/T-003-Handoff.md)
  - Commit: eb19ff3

- **T-004:** Define allowlist + sources.yaml
  - Data: 2026-01-30
  - Tempo: ~30 min (incluído em DUV-002)
  - Resultado: 5 fontes gov brasileiras + policy fail-closed
  - Evidence: Commit d411ce9

- **T-005:** Postgres schema v0 (metadata + pgvector)
  - Data: 2026-01-30
  - Tempo: ~40 min
  - Resultado: Schema completo criado (sources, documents, chunks, embeddings, audit_log)
  - Deliverables: schema.sql (275 linhas), models.py, init.py, tests
  - Deferred: Postgres instance validation (requires Docker)
  - Evidence: [T-005 Evidence Pack](../../docs/evidence/T-005/)
  - Handoff: [T-005-Handoff.md](Handoffs/T-005-Handoff.md)
  - Commit: 534a519

- **T-ONB-SRC-001:** Onboarding SRC-001 (DOU)
  - Data: 2026-01-30
  - Tempo: ~25 min
  - Resultado: BLOCK provisório (proteção Azion WAF). DUV-004 criada. Evidence pack completo.
  - Deliverables: WorkOrder, license_analysis.md, fetch_test.log, sample_urls.txt, notes.md
  - Decision: default_storage_mode = BLOCK (fail-closed)
  - Evidence: [T-ONB-SRC-001 Evidence Pack](../../docs/evidence/T-ONB-SRC-001/)
  - Handoff: [T-ONB-SRC-001-Handoff.md](Handoffs/T-ONB-SRC-001-Handoff.md)
  - DUV relacionada: DUV-004

- **T-ONB-SRC-002:** Onboarding SRC-002 (Planalto)
  - Data: 2026-01-30
  - Tempo: ~23 min
  - Resultado: ALLOW_FULLTEXT (legislação = domínio público, Lei 9.610/1998, Art. 8º, IV). Evidence pack completo.
  - Deliverables: WorkOrder, license_analysis.md, fetch_test.log, sample_urls.txt, notes.md
  - Decision: default_storage_mode = ALLOW_FULLTEXT (upgrade de METADATA_ONLY)
  - Fundamentação: Lei 9.610/1998, Art. 8º, IV + LAI (Lei 12.527/2011)
  - Evidence: [T-ONB-SRC-002 Evidence Pack](../../docs/evidence/T-ONB-SRC-002/)
  - Handoff: [T-ONB-SRC-002-Handoff.md](Handoffs/T-ONB-SRC-002-Handoff.md)
  - Commit: 3484970

- **T-ONB-SRC-002:** Onboarding SRC-002 (Planalto)
  - Data: 2026-01-30
  - Tempo: ~20 min
  - Resultado: METADATA_ONLY (fail-closed — evidências não verificadas)
  - Deliverables: WorkOrder, license_analysis.md, fetch_test.log, sample_urls.txt, notes.md, robots.txt
  - Decision: default_storage_mode = METADATA_ONLY (fail-closed)
  - Evidence: [T-ONB-SRC-002 Evidence Pack](../../docs/evidence/T-ONB-SRC-002/)
  - Handoff: [T-ONB-SRC-002-Handoff.md](Handoffs/T-ONB-SRC-002.md)
  - DUV relacionada: DUV-005

- **T-ONB-SRC-003:** Onboarding SRC-003 (IBGE)
  - Data: 2026-01-31
  - Tempo: ~15 min
  - Resultado: METADATA_ONLY (fail-closed — robots/ToS/licença não verificados)
  - Deliverables: WorkOrder, license_analysis.md, fetch_test.log, sample_urls.txt, notes.md, robots.txt
  - Decision: default_storage_mode = METADATA_ONLY (fail-closed)
  - Evidence: [T-ONB-SRC-003 Evidence Pack](../../docs/evidence/T-ONB-SRC-003/)
  - Handoff: [T-ONB-SRC-003-Handoff.md](Handoffs/T-ONB-SRC-003.md)
  - DUV relacionada: DUV-006

- **T-ONB-SRC-004:** Onboarding SRC-004 (BCB)
  - Data: 2026-01-31
  - Tempo: ~15 min
  - Resultado: METADATA_ONLY (fail-closed — licença por dataset não explícita)
  - Deliverables: WorkOrder, license_analysis.md, fetch_test.log, sample_urls.txt, notes.md, robots.txt
  - Decision: default_storage_mode = METADATA_ONLY (fail-closed)
  - Evidence: [T-ONB-SRC-004 Evidence Pack](../../docs/evidence/T-ONB-SRC-004/)
  - Handoff: [T-ONB-SRC-004-Handoff.md](Handoffs/T-ONB-SRC-004.md)
  - DUV relacionada: DUV-007

- **T-ONB-SRC-005:** Onboarding SRC-005 (dados.gov.br)
  - Data: 2026-01-31
  - Tempo: ~35 min
  - Resultado: METADATA_ONLY (fail-closed — ToS/robots/licença não verificáveis)
  - Deliverables: WorkOrder, license_analysis.md, fetch_test.log, sample_urls.txt, notes.md, robots.txt
  - Decision: default_storage_mode = METADATA_ONLY (fail-closed)
  - Evidence: [T-ONB-SRC-005 Evidence Pack](../../docs/evidence/T-ONB-SRC-005/)
  - Handoff: [T-ONB-SRC-005.md](Handoffs/T-ONB-SRC-005.md)
  - DUV relacionada: DUV-008

- **T-009:** Bot: robots checker
  - Data: 2026-01-31
  - Tempo: ~25 min
  - Resultado: RobotsChecker com status allowed/disallowed/unknown + testes
  - Deliverables: src/bots/robots_checker.py, tests/test_robots_checker.py, WorkOrder, evidence pack
  - Evidence: [T-009 Evidence Pack](../../docs/evidence/T-009/)
  - Handoff: [T-009.md](Handoffs/T-009.md)

---

## 2. DÚVIDAS / IMPEDIMENTOS (SLA 24h)

| ID          | Data         | Tarefa            | Descrição                                                   | SLA          | Status           | Resolução                                                                                                                                                                                                                                                                                                  |
| ----------- | ------------ | ----------------- | ----------------------------------------------------------- | ------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DUV-001     | 20260130     | Geral             | GitHub remoto: usar org pessoal ou novo?                    | 20260131     | ✅ RESOLVIDA     | Decisão: GitHub pessoal FREE. Registrado em DEC-007. (2026-01-30)                                                                                                                                                                                                                                          |
| DUV-002     | 20260130     | T-004             | Quais fontes incluir na allowlist inicial?                  | 20260131     | ✅ RESOLVIDA     | Decisão: 5 fontes gov brasileiras (DOU, Planalto, IBGE, BCB, dados.gov.br). Registrado em DEC-008. (2026-01-30)                                                                                                                                                                                            |
| **DUV-003** | **20260130** | **T-002**         | **Windows path limit (260 caracteres)**                     | **20260131** | **✅ RESOLVIDA** | **Resolução**: Projeto movido para C:\Dev\banco-dados-publicos (path curto). robocopy completado com sucesso. (2026-01-30)                                                                                                                                                                                 |
| DUV-002     | 20260130     | T-004             | Quais são as primeiras 5 fontes da allowlist?               | 20260131     | ✅ RESOLVIDA     | Decisão: SRC-001 (DOU), SRC-002 (Planalto), SRC-003 (IBGE), SRC-004 (BCB), SRC-005 (dados.gov.br). Registrado em DEC-008. (2026-01-30)                                                                                                                                                                     |
| **DUV-004** | **20260130** | **T-ONB-SRC-001** | **DOU bloqueado por WAF - Como obter dados?**               | **20260201** | **🔴 ABERTA**    | **Contexto**: in.gov.br protegido por Azion WAF (403 em robots.txt). Scraping não permitido. **Próximos passos**: (1) Verificar API oficial em dados.gov.br, (2) Pesquisar feeds RSS oficiais, (3) Considerar contato formal com Imprensa Nacional. **Impacto**: SRC-001 marcado como BLOCK até resolução. |
| **DUV-005** | **20260130** | **T-ONB-SRC-002** | **Falha de conectividade impede verificação de robots/ToS** | **20260201** | **🔴 ABERTA**    | **Contexto**: fetch para planalto.gov.br falhou (erro de conexão). Sem robots/ToS/licença verificáveis. **Impacto**: SRC-002 permanece METADATA_ONLY (fail-closed) até verificação em ambiente com conectividade estável.                                                                                  |
| **DUV-006** | **20260131** | **T-ONB-SRC-003** | **Robots.txt 503 e ToS/licença não verificáveis (IBGE)**    | **20260201** | **🔴 ABERTA**    | **Contexto**: robots.txt em servicodados.ibge.gov.br retornou 503; API root também 503. ToS/licença não localizadas com evidência. **Impacto**: SRC-003 permanece METADATA_ONLY (fail-closed) até verificação.                                                                                             |
| **DUV-007** | **20260131** | **T-ONB-SRC-004** | **Licença aberta não especificada por dataset (BCB)**       | **20260201** | **🔴 ABERTA**    | **Contexto**: FAQ menciona licença aberta, porém sem especificação por dataset. **Impacto**: SRC-004 permanece METADATA_ONLY até licença explícita.                                                                                                                                                        |
| **DUV-008** | **20260131** | **T-ONB-SRC-005** | **ToS/licença exigem login; robots.txt inválido (HTML)**    | **20260201** | **🔴 ABERTA**    | **Contexto**: dados.gov.br retornou HTML em robots.txt e páginas de termos exigem login gov.br. **Impacto**: SRC-005 permanece METADATA_ONLY até evidência de licença por dataset.                                                                                                                         |

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
| Dúvidas      | 8     | 5      | 0       | 3         |
| Impedimentos | 0     | 0      | 0       | 0         |

**Próxima revisão:** 2026-01-31 (fim de rodada)

---
