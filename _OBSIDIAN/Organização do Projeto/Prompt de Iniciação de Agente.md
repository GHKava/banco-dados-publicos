# Prompt de Iniciação de Agente — Banco de Dados Interrelacional

**Versão:** 1.0  
**Data:** 2026-01-30  
**Para:** Qualquer agente entrando no projeto

---

## 🚀 VOCÊ ACABOU DE ENTRAR. LEIA ISTO AGORA.

Este é o **guia de inicialização obrigatório** para qualquer agente neste projeto. Siga **exatamente na ordem abaixo**. Sem desvios.

---

## PASSO 1 — Leia os documentos de verdade (NÃO PULE)

1. [ ] Ler **`Contexto Global de Agentes.md`** (20 seções, ~15 min)
   - Este arquivo contém TUDO que você precisa saber sobre regras, máquinas de estado, DoR/DoD, personas, etc.
   - Bookmarks recomendados: seções II (regras inegociáveis), III (checklist), VI-VII (DoR/DoD), VIII (Evidence Packs), IX (Quality Gate), XIII (orçamento).

2. [ ] Ler **`Escopo.md`** (fonte de verdade imutável)
   - Define O QUÊ o projeto faz, limites, objetivos, não-objetivos.
   - Qualquer mudança aqui = CR (Change Request).

3. [ ] Ler **`Roadmap.md`** (executivo)
   - Visão geral das 15 fases (A-M + final).
   - Links para Roadmap detalhado.

---

## PASSO 2 — Verifique o KILL SWITCH

[ ] Verificar se arquivo `_OBSIDIAN/Organização do Projeto/STOP.md` **existe**:

- **SIM** → Finalize tarefa em andamento (se seguro) e **PARE** (não inicie nova tarefa).
- **NÃO** → Continue para PASSO 3.

---

## PASSO 3 — Rodar PREFLIGHT (verificação de integridade)

[ ] Antes de qualquer tarefa, verificar coerência:

```
✓ Roadmap.md existe e tem links válidos?
✓ Roadmap detalhado do Projeto.md existe?
✓ Backlog.md existe com tarefas READY/IN_PROGRESS?
✓ Personas/ folder existe com templates?
✓ Contexto Global de Agentes.md está atualizado?
✓ Escopo.md é imutável (nenhuma mudança não-CR)?
✓ Assunções.md documenta decisões?
✓ Evidence/ folder existe?
✓ Git está inicializado? (git status)
```

**Se algo faltar:** Auto-repair (criar arquivo com template) e registrar em "Dúvidas & Decisões.md".

---

## PASSO 4 — Ler Roadmap detalhado + Backlog

[ ] Ler **`Roadmap detalhado do Projeto.md`**

- Tabela completa com: ID, Nome, Requisitos, Artefatos, Persona, Dependências, DoR, DoD, Status, etc.
- Identificar primeira tarefa em **READY** (não BLOCKED).

[ ] Ler **`Backlog.md`**

- Seção 2: DÚVIDAS / IMPEDIMENTOS com SLA
- Seção 3: HISTÓRICO DE COMMITS
- Seção 4: DECISÕES
- Seção 5: ISSUES INTERNAS
- **Prioridade:** Resolver dúvidas abertas (SLA < hoje) **antes** de iniciar nova tarefa.

---

## PASSO 5 — Selecione a tarefa

[ ] Identificar primeira tarefa **em READY** no Roadmap detalhado:

- [ ] Dependências resolvidas? (ou BYPASSED com CR?)
- [ ] Arquivos-alvo definidos? (Artefatos esperados)
- [ ] Critérios de aceite claros?
- [ ] WorkOrder existe?

**Se DoR falhar:** Criar "Tarefa de Preparação" (T-XXX-Prep) e bloquear original.

---

## PASSO 6 — Criar/Ler WorkOrder

[ ] WorkOrder deve existir em `_OBSIDIAN/Organização do Projeto/WorkOrders/T-XXX.md`:

- Objetivo
- DoR checklist (dependências, arquivos-alvo, critérios)
- Entradas/Saídas
- Artefatos esperados (paths)
- Comandos previstos
- Riscos
- Evidência mínima necessária
- Quality gate aplicável

**Se não existir:** Criar antes de iniciar.

---

## PASSO 7 — Marcar IN_PROGRESS

[ ] Atualizar Roadmap detalhado do Projeto.md:

- Status: `IN_PROGRESS`
- Data/hora início: `2026-01-30 14:35 UTC` (real)
- Marcar em Log de Execução.md também

---

## PASSO 8 — Assumir Persona

[ ] Ler arquivo da persona assignada à tarefa:

- Exemplo: Para tarefa TL → ler `_OBSIDIAN/Personas/TL.md`
- Personas existentes: ORQ, PM, TL, DE, BE, QA, DEVOPS, SRE, SEC, LEGAL, DPO, DOCS

[ ] Registrar no Log de Execução.md:

```
[HH:MM UTC] Assumi Persona: TL (link para \_OBSIDIAN/Personas/TL.md)
```

---

## PASSO 9 — Verificar Backlog por dúvidas correlatas

[ ] Checar seção "DÚVIDAS / IMPEDIMENTOS" em Backlog.md:

- Alguma dúvida aberta que impacte sua tarefa?
- **Se SLA vencido:** Resolver imediatamente (ou criar ISSUE interna).
- **Se SLA aberto:** Aguardar resposta OU prosseguir com ASSUNÇÃO documentada em Assunções.md.

---

## PASSO 10 — Executar tarefa COMPLETAMENTE

[ ] Implementar 100% da tarefa:

- [ ] Seguir DoR/DoD exatamente
- [ ] Criar artefatos em paths especificados
- [ ] Registrar comandos em `docs/evidence/T-XXX/commands.log`
- [ ] Executar comandos e capturar outputs em `docs/evidence/T-XXX/output.txt`
- [ ] Sem "simulações" — tudo deve ser FATO VERIFICADO ou ASSUNÇÃO documentada

---

## PASSO 11 — Gerar Evidence Pack

[ ] Criar `docs/evidence/T-XXX/` com:

- [ ] `commands.log` — comandos executados (cópia exata)
- [ ] `output.txt` — outputs relevantes (stdout/stderr)
- [ ] `tests.log` — lint/tests/typecheck/security output
- [ ] `files_changed.json` — lista de arquivos criados/alterados/removidos (JSON)
- [ ] `notes.md` — resumo: objetivo, decisões, validação, limitações

**Regra:** Sem Evidence Pack = tarefa NÃO pode ser DONE.

---

## PASSO 12 — Rodar Quality Gate (VERIFYING)

[ ] Antes de marcar DONE, executar (quando aplicável):

- [ ] Lint OK (flake8, black, isort para Python)
- [ ] Tests OK (pytest)
- [ ] Typecheck OK (mypy)
- [ ] Security scan OK (bandit, OWASP)

[ ] Registrar outputs em `docs/evidence/T-XXX/tests.log`

**Se falhar:** Tarefa → RETRY_SCHEDULED (agente corrige imediatamente, retry_count++).

---

## PASSO 13 — CLAIM CHECK

[ ] Antes de commitar, verificar:

- [ ] Todos arquivos prometidos existem (artefatos em paths corretos)?
- [ ] Evidence Pack está completo (5 arquivos + conteúdo)?
- [ ] Roadmap detalhado atualizado com status/timestamps?
- [ ] Backlog.md atualizado (se novas dúvidas/decisões)?
- [ ] Log de Execução.md atualizado?
- [ ] Heartbeat do Orquestrador.md atualizado?
- [ ] Quality Gate passou (ou registrado como BYPASSED com justificativa)?

**Se falhar:** Corrigir **imediatamente** (não commitar com claim check errado).

---

## PASSO 14 — COMMIT + PUSH

[ ] Git add + commit (padrão obrigatório):

```bash
git add .
git commit -m "feat: [descrição tarefa] (T-XXX)

Artefatos: [lista de arquivos principais]
Evidência: docs/evidence/T-XXX/
Quality gate: [PASSED/BYPASSED com justificativa]
Próx. passo: [tarefa dependente ou observação]"
```

[ ] Push para branch `feature/T-XXX-nome-curto`:

```bash
git push origin feature/T-XXX-nome-curto
```

---

## PASSO 15 — Marcar DONE

[ ] Atualizar Roadmap detalhado do Projeto.md:

- Status: `DONE`
- Data/hora fim: `2026-01-30 15:45 UTC` (real)
- Link Evidence Pack: `docs/evidence/T-XXX/`
- Link Handoff: `_OBSIDIAN/Organização do Projeto/Handoffs/T-XXX.md`

---

## PASSO 16 — Escrever HANDOFF

[ ] Criar `_OBSIDIAN/Organização do Projeto/Handoffs/T-XXX.md`:

- O que mudou (resumo)
- Arquivos alterados (link para files_changed.json)
- Decisões + links para CRs (se houver)
- Como validar (comandos exatos + expected outcome)
- Limitações / próximos passos (tarefa que vem depois)

**Próximo agente lê isto primeiro.**

---

## PASSO 17 — Atualizar Heartbeat + Log

[ ] Atualizar `_OBSIDIAN/Organização do Projeto/Heartbeat do Orquestrador.md`:

- Rodada: incrementar (de #0 para #1, etc.)
- Tarefas executadas: adicionar T-XXX com status DONE
- Tempo: total da rodada (min)
- Dúvidas: listar abertas com SLA
- STOP.md status: existe? não?

[ ] Atualizar `_OBSIDIAN/Organização do Projeto/Log de Execução.md`:

- Timestamp: HH:MM UTC
- Tarefa: T-XXX
- Status: DONE
- Evidência: path para Evidence Pack

---

## PASSO 18 — Verificar orçamento da rodada

[ ] Contar:

- **Tarefas concluídas:** X (limite = 5)
- **Tempo total:** Y minutos (limite = 90)

**Se X >= 5 OU Y >= 90:**

- [ ] Gerar status (Roadmap/Heartbeat/Log)
- [ ] Commitar com mensagem `chore: end of sprint (rodada #N)`
- [ ] **ENCERRAR RODADA** (não inicie nova tarefa)
- [ ] Próximo agente continua em nova rodada

**Senão:**

- [ ] Voltar para PASSO 4 (selecionar próxima tarefa READY)

---

## PASSO 19 — Loop ou encerramento

**OPÇÃO A: Há mais tarefas READY e orçamento restante?**

- SIM → Voltar para PASSO 4 (próxima tarefa)
- NÃO → Ir para OPÇÃO B

**OPÇÃO B: Projeto completo (todos tarefas DONE)?**

- SIM → Gerar Relatório Final, tag release v1.0.0, ENCERRAR projeto.
- NÃO → Finalize rodada, passe para próximo agente.

---

## 📋 CHECKLIST RÁPIDO

```
□ Ler Contexto Global de Agentes.md (OBRIGATÓRIO)
□ Ler Escopo.md + Roadmap.md
□ Checar STOP.md (existe?)
□ Rodar Preflight
□ Ler Roadmap detalhado + Backlog
□ Selecionar tarefa READY
□ Ler/criar WorkOrder
□ Marcar IN_PROGRESS
□ Assumir Persona + registrar Log
□ Checar dúvidas (Backlog) com SLA
□ Executar tarefa 100%
□ Gerar Evidence Pack (5 arquivos)
□ Rodar Quality Gate
□ Claim Check (tudo ok?)
□ Commit + Push
□ Marcar DONE + timestamps
□ Escrever Handoff
□ Atualizar Heartbeat + Log
□ Checar orçamento (5 tarefas ou 90 min?)
□ Loop ou encerrar rodada
```

---

## 🆘 Se ficar preso...

1. **Dúvida técnica?** → Registre em [[Backlog#2 DÚVIDAS / IMPEDIMENTOS (SLA 24h)|Backlog]] com SLA.
2. **Tarefa bloqueada?** → Procure próxima tarefa READY (não bloqueada).
3. **Quality Gate falhou?** → Marca RETRY_SCHEDULED, corrige, roda novamente.
4. **Não tem próxima tarefa?** → Encerre rodada, espere próximo agente.

---

## ✨ AGORA VÃO. EXECUTE COM CONFIANÇA.

Você tem tudo de que precisa. As regras são claras. Os documentos são precisos. Não há ambiguidade.

**Boa execução!** 🚀

---

**Data criação:** 2026-01-30  
**Última atualização:** 2026-01-30  
**Versão:** 1.0

---
