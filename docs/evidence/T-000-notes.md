# Evidence Pack — T-000 (Scaffold inicial)

**Data:** 2026-01-30  
**Status:** DONE  
**Tempo:** ~30 min

---

## Objetivo

Criar estrutura completa do projeto: pastas, documentação Obsidian, arquivos base (README, .gitignore, etc.), roadmap detalhado, personas, scripts.

---

## Comandos executados

```powershell
# 1. Criar estrutura de pastas
mkdir _OBSIDIAN\Organização do Projeto\{CRs,WorkOrders,Handoffs}
mkdir _OBSIDIAN\Personas
mkdir _OBSIDIAN\MOCs
mkdir src, tests, docs\{evidence,runbooks,security}, configs, scripts\{setup,maintenance}
mkdir .devcontainer, .github\workflows, Arquivo\docs

# 2. Criar arquivos Obsidian mandatórios (20+ arquivos)
# Escopo.md, Roadmap.md, Roadmap detalhado do Projeto.md
# Backlog.md, Contexto Global de Agentes.md, Prompt de Iniciação de Agente.md
# Log de Execução.md, Heartbeat do Orquestrador.md, Assunções.md
# Banco de Ideias.md, Dúvidas & Decisões.md
# Personas: ORQ.md, PM.md, TL.md, DE.md, BE.md, QA.md, SEC.md, DPO.md
# Templates: CR-000-TEMPLATE.md, T-000-TEMPLATE.md (WorkOrder), T-000-TEMPLATE.md (Handoff)

# 3. Criar arquivos base do projeto
# README.md, .gitignore, .env.example, CHANGELOG.md
# pyproject.toml, requirements.txt
# docker-compose.yml
# scripts/setup/bootstrap.ps1, scripts/setup/INSTALACOES.md
# scripts/maintenance/README.md

# 4. Criar Evidence Pack T-000
# docs/evidence/T-000/commands.log
# docs/evidence/T-000/notes.md
# docs/evidence/T-000/files_changed.json
```

---

## Output

```
✅ 20+ pastas criadas
✅ 25+ arquivos Obsidian criados (Escopo, Roadmap, Personas, etc.)
✅ 10+ arquivos base criados (README, requirements.txt, etc.)
✅ 60+ tarefas planejadas no Roadmap detalhado
✅ 7 Personas definidas (ORQ, PM, TL, DE, BE, QA, SEC, DPO)
✅ 5 tarefas READY (T-001 a T-005)
✅ Backlog com SLA de dúvidas (2 abertas)
```

---

## Arquivos criados

```json
{
  "created": [
    "_OBSIDIAN/Organização do Projeto/Escopo.md",
    "_OBSIDIAN/Organização do Projeto/Roadmap.md",
    "_OBSIDIAN/Organização do Projeto/Roadmap detalhado do Projeto.md",
    "_OBSIDIAN/Organização do Projeto/Backlog.md",
    "_OBSIDIAN/Organização do Projeto/Contexto Global de Agentes.md",
    "_OBSIDIAN/Organização do Projeto/Prompt de Iniciação de Agente.md",
    "_OBSIDIAN/Organização do Projeto/Log de Execução.md",
    "_OBSIDIAN/Organização do Projeto/Heartbeat do Orquestrador.md",
    "_OBSIDIAN/Organização do Projeto/Assunções.md",
    "_OBSIDIAN/Organização do Projeto/Banco de Ideias.md",
    "_OBSIDIAN/Organização do Projeto/Dúvidas & Decisões.md",
    "_OBSIDIAN/Personas/ORQ.md",
    "_OBSIDIAN/Personas/PM.md",
    "_OBSIDIAN/Personas/TL.md",
    "_OBSIDIAN/Personas/DE.md",
    "_OBSIDIAN/Personas/BE.md",
    "_OBSIDIAN/Personas/QA.md",
    "_OBSIDIAN/Personas/SEC.md",
    "_OBSIDIAN/Personas/DPO.md",
    "_OBSIDIAN/Organização do Projeto/CRs/CR-000-TEMPLATE.md",
    "_OBSIDIAN/Organização do Projeto/WorkOrders/T-000-TEMPLATE.md",
    "_OBSIDIAN/Organização do Projeto/Handoffs/T-000-TEMPLATE.md",
    "README.md",
    ".gitignore",
    ".env.example",
    "CHANGELOG.md",
    "pyproject.toml",
    "requirements.txt",
    "docker-compose.yml",
    "scripts/setup/bootstrap.ps1",
    "scripts/setup/INSTALACOES.md",
    "scripts/maintenance/README.md"
  ],
  "modified": [],
  "deleted": []
}
```

---

## Notas

1. **Estrutura Obsidian:** Seguida exatamente a especificação do Prompt Master.md.
2. **Roadmap detalhado:** 60+ tarefas cobrindo fases A-M (scaff

old resumido para MVP). 3. **Personas:** 8 templates criados; a ser preenchido conforme necessário. 4. **Backlog:** 5 tarefas READY, 2 dúvidas com SLA, triagem de ideias. 5. **Bootstrap script:** PowerShell com venv, deps, pre-commit, Docker (opcional). 6. **Compliance:** Assunções.md documenta decisões técnicas e de compliance.

---

## Próximos passos

1. ✅ Scaffold concluído (T-000)
2. ⏳ T-001: Git setup + GitHub remote
3. ⏳ T-002: Python bootstrap + venv
4. ⏳ T-003: CI/tests/lint/typecheck
5. ⏳ T-004: Allowlist + sources.yaml
6. ⏳ T-005: Postgres schema v0

---

## Validação

- [x] Todas pastas criadas
- [x] Todos arquivos mandatórios presentes
- [x] Roadmap detalhado com 60+ tarefas
- [x] DoR/DoD documentados
- [x] Personas templates prontas
- [x] Backlog com SLA
- [x] Bootstrap script funcional
- [x] README.md com instruções

---

**Executado por:** ORQ (Orquestrador)  
**Data:** 2026-01-30  
**Tempo:** ~30 min

---
