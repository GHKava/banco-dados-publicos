# PRÓXIMAS AÇÕES — Banco de Dados Interrelacional

**Data:** 2026-01-30 14:45 UTC  
**Status:** Rodada #0 CONCLUÍDA

---

## 🎯 Para o próximo agente

**Você deve:**

1. **Ler obrigatoriamente:**
   - [Contexto Global de Agentes.md](\_OBSIDIAN/Organização do Projeto/Contexto Global de Agentes.md) (20 seções)
   - [Prompt de Iniciação de Agente.md](\_OBSIDIAN/Organização do Projeto/Prompt de Iniciação de Agente.md) (19 passos)

2. **Resolver dúvidas (SLA 2026-01-31):**
   - **DUV-001:** Qual GitHub org usar? (pessoal, nova, ou free)
   - **DUV-002:** Quais são as primeiras 5 fontes allowlist?

3. **Iniciar Rodada #1:**
   - **T-001:** Git setup + GitHub remote (Persona: TL)
   - **T-002:** Python bootstrap + venv (Persona: TL)
   - **T-003:** CI/tests/lint/typecheck (Persona: TL)
   - **T-004:** Allowlist + sources.yaml (Persona: PM)
   - **T-005:** Postgres schema v0 (Persona: DE)

---

## 📊 Status atual

| Métrica                   | Valor                                   |
| ------------------------- | --------------------------------------- |
| **Rodas executadas:**     | #0 (CONCLUÍDA)                          |
| **Tarefas DONE:**         | 1 (T-000: scaffold)                     |
| **Tarefas READY:**        | 5 (T-001 a T-005)                       |
| **Tarefas BLOCKED:**      | ~60 (aguardando dependências)           |
| **Dúvidas abertas:**      | 2 (SLA 2026-01-31)                      |
| **Ideias em triagem:**    | 10                                      |
| **Tempo gasto (rodada):** | ~30 min                                 |
| **Orçamento restante:**   | ✅ 5 tarefas OU 60 min ainda disponível |

---

## 🔄 Checklist para próximo agente (antes de iniciar T-001)

```
[ ] Ler Contexto Global de Agentes.md completamente
[ ] Checar se STOP.md existe (não deve existir ainda)
[ ] Rodar Preflight (coerência de Roadmap/Backlog/Personas)
[ ] Ler Roadmap.md + Roadmap detalhado do Projeto.md
[ ] Ler Backlog.md (dúvidas, SLA)
[ ] Resolver DUV-001 (ou registrar ASSUNÇÃO)
[ ] Resolver DUV-002 (ou registrar ASSUNÇÃO)
[ ] Selecionar T-001 (Git setup) como primeira tarefa
[ ] Criar WorkOrder T-001 (se não existir)
[ ] Marcar T-001 como IN_PROGRESS (com timestamp real)
[ ] Assumir Persona TL (ler _OBSIDIAN/Personas/TL.md)
[ ] Executar T-001 completamente (sem pular nada)
[ ] Gerar Evidence Pack em docs/evidence/T-001/
[ ] Rodar Quality Gate
[ ] Claim Check
[ ] Commit + Push
[ ] Marcar DONE + timestamp
[ ] Escrever Handoff
[ ] Atualizar Heartbeat + Log
[ ] Continuar com T-002... T-005 (até orçamento)
```

---

## 📝 Arquivos críticos (bookmark esses)

1. **[Contexto Global de Agentes.md](\_OBSIDIAN/Organização do Projeto/Contexto Global de Agentes.md)**
   - 20 seções: identidade, regras, preflight, DoR/DoD, Evidence Packs, Quality Gate, personas, SLA, etc.

2. **[Roadmap.md](\_OBSIDIAN/Organização do Projeto/Roadmap.md)**
   - Visão executiva (15 fases + final)

3. **[Roadmap detalhado do Projeto.md](\_OBSIDIAN/Organização do Projeto/Roadmap%20detalhado%20do%20Projeto.md)**
   - Tabela completa (60+ tarefas, status, dependências, personas)

4. **[Backlog.md](\_OBSIDIAN/Organização do Projeto/Backlog.md)**
   - Tarefas READY, dúvidas (SLA), histórico, decisões, issues internas

5. **[Assunções.md](\_OBSIDIAN/Organização do Projeto/Assunções.md)**
   - Decisões técnicas, compliance, operacionais registradas

---

## 🎯 Foco da Rodada #1

**OBJETIVO:** Criar infrastructure base e governance:

- ✅ Git versionando tudo
- ✅ CI (GitHub Actions) rodando
- ✅ Python/deps pronto
- ✅ Postgres acessível
- ✅ Allowlist inicial definida

**ENTRADA:** 5 tarefas READY  
**SAÍDA:** 5 tarefas DONE + infrastructure pronta para Fase A  
**BLOQUEADOR:** DUV-001 e DUV-002 (resolver ANTES de iniciar)

---

## ⏰ Orçamento atual

- **Rodada #0:** ~30 min (CONCLUÍDO)
- **Rodada #1 (próxima):** até 90 min OU 5 tarefas (iniciando com T-001)

---

## 🚨 Kill switch (STOP.md)

Se arquivo `_OBSIDIAN/Organização do Projeto/STOP.md` aparecer:

- Finalize tarefa em andamento (se seguro)
- **PARE o loop** (não inicie nova tarefa)
- Registre no Heartbeat do Orquestrador.md

**Status atual:** ❌ STOP.md não existe → Loop autorizado

---

## 📞 Suporte

**Dúvidas?** Registre em [Backlog — Dúvidas & Impedimentos](/_OBSIDIAN/Organização%20do%20Projeto/Backlog.md#2-dúvidas--impedimentos-sla-24h):

- ID: DUV-00X
- Data: hoje
- Tarefa: T-XXX (se aplicável)
- Descrição: clara e objetiva
- SLA: YYYYMMDD HH:00 UTC

---

## 🎉 Você está pronto!

Tudo que você precisa está aqui:

- ✅ Estrutura Git/GitHub (pronto para T-001)
- ✅ Roadmap (60+ tarefas planejadas)
- ✅ Personas (8 templates)
- ✅ Regras obrigatórias (Contexto Global de Agentes)
- ✅ Evidence framework (20 seções em docs/evidence)
- ✅ Bootstrap script (pronto para T-002)
- ✅ CI template (pronto para T-003)

**Execute com confiança!** 🚀

---

**Criado por:** ORQ (Orquestrador)  
**Data:** 2026-01-30 14:45 UTC  
**Próxima atualização:** Ao final de T-005 (ou antes, se orçamento exceder 90 min)

---
