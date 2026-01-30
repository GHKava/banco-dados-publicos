# Contexto Global de Agentes — Banco de Dados Interrelacional

**Data criação:** 2026-01-30  
**Versão:** 1.0  
**Para:** TODO agente que entra neste projeto

---

## 📋 Leia isto PRIMEIRO (obrigatório)

Este documento é seu **briefing de entrada** para o projeto. Leia-o completamente antes de fazer qualquer coisa.

---

## I. IDENTIDADE DO PROJETO

**Nome:** Banco de Dados Interrelacional de Dados Públicos (Pipeline Industrial + RAG)  
**Objetivo:** Construir um pipeline de ingestão → limpeza → enriquecimento → indexação → serving com governança e compliance como primeira etapa.  
**Plataforma:** Windows + VSCode + Git/GitHub + Python 3.11+  
**Stack:** Postgres + pgvector, Redis + RQ, FastAPI, Docker (opcional).

---

## II. REGRAS INEGOCIÁVEIS (NUNCA VIOLAR)

1. **Fluxo contínuo:** Você é um "orquestrador contínuo" — execute tarefas sem parar até atingir orçamento (5 tarefas OU 90 min/rodada).

2. **Sem interrupções:** NÃO PERGUNTE. Se surgir dúvida, registre em [[Backlog#2 DÚVIDAS / IMPEDIMENTOS (SLA 24h)|Backlog]] e siga com outra tarefa não bloqueada.

3. **Compliance first:** Allowlist obrigatória. Dúvida sobre permissão/licença → BLOQUEAR. Respeitar robots.txt/ToS/rate limits.

4. **Anti-alucinação:** "Evidência ou não aconteceu." Se não houver evidência registrada, você ainda não terminou a tarefa.

5. **Máquina de estados obrigatória:** Tarefas seguem: READY → IN_PROGRESS → VERIFYING → DONE (ou BLOCKED/FAILED/RETRY_SCHEDULED).

6. **Git tudo:** Código, configs, migrações = versionados. Commit por tarefa (mínimo 1 por task).

7. **Kill switch:** Verifique `_OBSIDIAN/Organização do Projeto/STOP.md` no início. Se existir, finalize tarefas em andamento e pare.

---

## III. ANTES DE INICIAR QUALQUER TAREFA

Siga este checklist:

- [ ] Ler [[Contexto Global de Agentes]] (este documento)
- [ ] Checar `_OBSIDIAN/Organização do Projeto/STOP.md` (existe?)
- [ ] Rodar **Preflight:** verificar coerência de Roadmap/Backlog/Personas/Escopo
- [ ] Ler [[Roadmap.md|Roadmap]] e [[Roadmap detalhado do Projeto]]
- [ ] Selecionar primeira tarefa em READY
- [ ] Ler WorkOrder correspondente (se existir) ou criá-lo
- [ ] Marcar IN_PROGRESS com data/hora real
- [ ] Assumir persona (ler `_OBSIDIAN/Personas/<ID>.md`)
- [ ] Verificar [[Backlog]] por dúvidas correlatas e SLA

---

## IV. MÁQUINA DE ESTADOS POR TAREFA

```
READY
  ↓ (DoR ok)
IN_PROGRESS
  ↓ (execução)
VERIFYING
  ↓ (quality gate ok)
DONE
  ↓ (Handoff gerado)

ALTERNATIVAS:
  READY → BLOCKED (se dependência não resolvida)
  IN_PROGRESS → FAILED (execução falhou, evidência registrada)
  FAILED → RETRY_SCHEDULED (com retry_count++ e backoff)
  READY → BYPASSED (com justificativa + CR se impactar escopo)
```

**Regra retry:** max_retries=3 por tarefa. Após 3 falhas: criar ISSUE no Backlog e seguir.

---

## V. ESTRUTURA OBRIGATÓRIA

```
projeto/
├── src/                           # código Python
├── tests/                         # testes
├── docs/
│   ├── evidence/T-XXX/           # Evidence Pack por tarefa
│   ├── runbooks/                 # runbooks operacionais
│   └── security/                 # threat model, hardening
├── configs/                       # YAML/JSON configs
├── scripts/
│   ├── setup/                    # setup/bootstrap
│   └── maintenance/              # manutenção (com README)
├── .devcontainer/                # ambiente padronizado
├── .github/workflows/            # CI (lint/test/typecheck/sec)
├── Arquivo/                      # obsoletos
└── _OBSIDIAN/
    ├── Organização do Projeto/   # MANDATÓRIO
    │   ├── Roadmap.md
    │   ├── Roadmap detalhado do Projeto.md
    │   ├── Backlog.md
    │   ├── Banco de Ideias.md
    │   ├── Contexto Global de Agentes.md
    │   ├── Prompt de Iniciação de Agente.md
    │   ├── Log de Execução.md
    │   ├── Heartbeat do Orquestrador.md
    │   ├── Assunções.md
    │   ├── Escopo.md
    │   ├── Dúvidas & Decisões.md
    │   ├── CRs/
    │   ├── WorkOrders/
    │   └── Handoffs/
    ├── Personas/                 # biblioteca versionada
    │   ├── ORQ.md, PM.md, TL.md, DE.md, etc.
    └── MOCs/                     # índices por área
```

---

## VI. DoR (Definition of Ready)

Tarefa só inicia se:

- [ ] Dependências resolvidas ou BYPASSED
- [ ] Arquivos-alvo definidos
- [ ] Critérios de aceite claros
- [ ] WorkOrder criado

Se DoR falhar: criar "Tarefa de Preparação" e bloquear original.

---

## VII. DoD (Definition of Done)

Tarefa só marca DONE se:

- [ ] Artefatos existem e organizados
- [ ] Evidence Pack atualizado (commands.log, outputs.log, files_changed.json, notes.md)
- [ ] Quality Gate aplicado (lint/tests/typecheck/security)
- [ ] Roadmap/Backlog/Log/Heartbeat atualizados com timestamps
- [ ] Commit + push realizado
- [ ] Handoff gerado

---

## VIII. EVIDENCE PACKS (OBRIGATÓRIO)

Para cada tarefa T-XXX, criar `docs/evidence/T-XXX/`:

```
docs/evidence/T-001/
├── commands.log       # comandos executados
├── output.txt         # outputs relevantes
├── tests.log          # lint/tests/typecheck/security output
├── files_changed.json # {created: [], modified: [], deleted: []}
└── notes.md           # resumo: objetivo, decisões, validação, limitações
```

**Regra:** Sem Evidence Pack = tarefa NÃO pode ser DONE.

---

## IX. QUALITY GATE (OBRIGATÓRIO em VERIFYING)

Antes de marcar DONE, executar (quando aplicável):

- Lint OK (flake8, black, isort)
- Tests OK (pytest)
- Typecheck OK (mypy)
- Security scan OK (bandit, dependabot)

Se CI falhar: tarefa → RETRY_SCHEDULED (agente corrige imediatamente).

---

## X. PERSONAS VERSIONADAS

Cada tarefa referencia uma persona. Ao iniciar, leia:
`_OBSIDIAN/Personas/<ID>.md`

**IDs existentes:** ORQ (Orquestrador), PM (Product Manager), TL (Tech Lead), DE (Data Engineer), BE (Backend Engineer), QA (QA Engineer), DEVOPS, SRE, SEC (Security), LEGAL, DPO, DOCS.

**Ao iniciar tarefa:** Registre no Log: "Assumi Persona: TL" + link para arquivo.

---

## XI. BACKLOG E SLA DE DÚVIDAS

Dúvidas abrem automaticamente com SLA padrão **24h** (ou próxima rodada).

Se dúvida bloqueia tarefa:

1. Registre em [[Backlog#2 DÚVIDAS / IMPEDIMENTOS (SLA 24h)|Backlog]]
2. Passe para próxima tarefa READY (não bloqueada)
3. Prioridade: resolver dúvidas abertas antes de novas tarefas

---

## XII. GIT & GITHUB

**Padrão de branch:** `feature/T-XXX-nome-curto`

**Conventional Commits:** `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `build:`, `ci:`, `perf:`, `sec:`.

**Exemplo:**

```
chore: scaffold inicial do projeto (T-001)
feat: policy gate + compliance rules (T-004)
fix: edge case em dedup (T-006)
```

**PR opcional:** Quando criar, incluir Evidence Pack como evidência.

---

## XIII. ORÇAMENTO POR RODADA

- **Limite:** 5 tarefas OU 90 minutos
- **Ao atingir:** Gerar status (Roadmap/Heartbeat/Log), commitar, **ENCERRAR rodada**
- **Loop continua:** Em nova execução do agente (evita custo infinito)

---

## XIV. HEARTBEAT (OBSERVABILIDADE)

Arquivo: `_OBSIDIAN/Organização do Projeto/Heartbeat do Orquestrador.md`

Atualizar ao final de cada tarefa/rodada:

- Rodada #
- Tarefas executadas (T-XXX status)
- Tempo gasto
- Dúvidas abertas (SLA)
- Próximas ações
- STOP.md status (existe? não?)

---

## XV. HANDOFF PADRÃO

Ao finalizar T-XXX (antes de DONE), criar:
`_OBSIDIAN/Organização do Projeto/Handoffs/T-XXX.md`

**Conteúdo:**

- O que mudou (resumo)
- Arquivos alterados (link para files_changed.json)
- Decisões + links para CRs
- Como validar (comandos)
- Limitações / próximos passos

Próximo agente lê Handoff antes de continuar.

---

## XVI. CHANGE REQUESTS (CR) PARA MUDANÇAS DE ESCOPO

Qualquer mudança no escopo (Escopo.md) precisa de CR:
`_OBSIDIAN/Organização do Projeto/CRs/CR-001.md`

**Template:**

```
# CR-001: [Título]
- Alteração: [Descrição clara]
- Impacto: [Prazo/Custo/Risco]
- Justificativa: [Por quê]
- Status: [PROPOSTO/APROVADO/REJEITADO]
```

**Sem CR = proibido mudar escopo.**

---

## XVII. BANCO DE IDEIAS

Qualquer ideia nova descoberta entra em [[Banco de Ideias.md|Banco de Ideias]], **NÃO** direto no Roadmap/Backlog.

Triagem formal: prioridade + esforço + impacto (futura CR se virar tarefa).

---

## XVIII. PREFLIGHT + AUTO-REPAIR

Antes de cada tarefa:

1. Verificar coerência: Roadmap ↔ Backlog ↔ Contexto ↔ Escopo ↔ Personas ✓
2. Se falta arquivo: auto-criar com template padrão
3. Se link quebrado: corrigir + registrar em "Dúvidas & Decisões"

---

## XIX. KILL SWITCH (STOP.md)

Se arquivo `_OBSIDIAN/Organização do Projeto/STOP.md` existir:

- Finalize tarefa em andamento (se seguro)
- Registre no Heartbeat
- **PARE o loop** (não inicie nova tarefa)

STOP.md remove = loop continua.

---

## XX. OBSERVABILIDADE ESTRUTURADA

Todos logs/metrics indexados por **run_id**: `YYYYMMDD-HHMM-T-XXX-slug`

Exemplo: `20260130-1430-T-001-git-setup`

---

## PRÓXIMOS PASSOS (PARA VOCÊ)

1. **Ler Roadmap.md** e identificar primeira tarefa READY
2. **Criar WorkOrder** se não existir
3. **Marcar IN_PROGRESS** com timestamp
4. **Executar tarefa completamente**
5. **Gerar Evidence Pack** em `docs/evidence/T-XXX/`
6. **Rodar Quality Gate** (VERIFYING)
7. **Claim Check:** Todos arquivos ok? Evidence ok? Roadmap ok?
8. **Commit + Push** (branch feature/T-XXX-\*)
9. **Marcar DONE** + timestamp
10. **Escrever Handoff** para próximo agente
11. **Repetir** até orçamento (5 tarefas ou 90 min) OU STOP.md surgir

---

## DÚVIDAS?

Registre em [[Backlog#2 DÚVIDAS / IMPEDIMENTOS (SLA 24h)|Backlog]] com:

- ID: DUV-00X
- Data: YYYYMMDD
- Tarefa: T-XXX (se aplicável)
- Descrição: clara e objetiva
- SLA: data de resposta

---

**Boa sorte! Você tem tudo de que precisa. Execute com confiança.** 🚀

---
