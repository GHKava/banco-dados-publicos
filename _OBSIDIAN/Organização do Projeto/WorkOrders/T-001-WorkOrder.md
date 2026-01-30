# WorkOrder — T-001: Git setup + GitHub remote

**ID:** T-001  
**Criado:** 2026-01-30  
**Persona:** TL (Tech Lead)  
**Dependências:** Nenhuma (DESBLOQUEADA após DUV-001)  
**Status:** IN_PROGRESS

---

## Objetivo

Configurar repositório Git remoto no GitHub pessoal (FREE) e fazer push inicial do código.

---

## DoR Checklist (Definition of Ready)

- [x] DUV-001 resolvida (GitHub org definida: pessoal FREE)
- [x] Git local inicializado (commit 53a2fe6, d411ce9, defa893)
- [x] .gitignore criado
- [x] Estrutura de arquivos completa (47 files)
- [x] Persona TL assumida

---

## Entradas

- Git repo local existente (`.git/`)
- 3 commits locais (53a2fe6, d411ce9, defa893)
- Decisão DEC-007: GitHub pessoal FREE

---

## Saídas / Artefatos

- [ ] Repositório GitHub criado (nome: `banco-dados-publicos` ou similar)
- [ ] Remote `origin` configurado
- [ ] Branch `main` (ou `master`) com proteção básica
- [ ] Push inicial completo (3 commits sincronizados)
- [ ] README.md visível no GitHub

---

## Comandos previstos

```powershell
# 1. Criar repo GitHub via gh CLI (ou manual via web)
gh repo create banco-dados-publicos --public --source=. --remote=origin --push

# OU se gh CLI não disponível:
# - Criar repo manualmente via GitHub web
# - Configurar remote:
git remote add origin https://github.com/<USERNAME>/banco-dados-publicos.git
git branch -M main
git push -u origin main
```

---

## Riscos

| Risco                               | Probabilidade | Mitigação                                  |
| ----------------------------------- | ------------- | ------------------------------------------ |
| `gh` CLI não instalado              | Média         | Usar web UI + manual remote config         |
| Nome de usuário GitHub desconhecido | Alta          | Criar assunção ASS-GIT-002 + placeholder   |
| Repo já existe                      | Baixa         | Usar nome alternativo ou deletar existente |

---

## Evidência mínima

- [ ] Screenshot ou output de `git remote -v` mostrando origin
- [ ] Screenshot ou output de `git log --oneline` mostrando 3 commits
- [ ] Output de `git push` bem-sucedido
- [ ] URL do repositório GitHub (https://github.com/<user>/banco-dados-publicos)

---

## Quality gate

- [x] Lint: N/A (sem código Python novo)
- [x] Typecheck: N/A
- [x] Tests: N/A
- [x] Git commit message: Conventional Commits (chore:, docs:)

---

## Próximo passo

**Após T-001 DONE:**

- Iniciar T-002 (Python bootstrap + venv)
- Atualizar Heartbeat
- Escrever Handoff T-001

---

**WorkOrder criado por:** AGENTE ORQUESTRADOR (Persona: TL)  
**Data:** 2026-01-30 16:00 UTC
