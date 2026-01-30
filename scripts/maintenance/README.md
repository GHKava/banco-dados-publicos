# README.md — Scripts de Manutenção

**Data criação:** 2026-01-30

---

## Índice de scripts

Todos scripts de manutenção estão em `scripts/maintenance/`.

### 🧹 Limpeza e manutenção geral

| Script                    | Objetivo                | Quando usar    |
| ------------------------- | ----------------------- | -------------- |
| (A implementar em T-060+) | Cleanup de logs antigos | Quinzenalmente |
| (A implementar em T-060+) | Reindex de vetores      | Após backfill  |
| (A implementar em T-060+) | Backup de dados         | Semanalmente   |

---

## Como adicionar novo script

1. Criar arquivo em `scripts/maintenance/script_name.py`
2. Adicionar entrada neste README
3. Documentar:
   - Objetivo
   - Uso (comando exato)
   - Quando executar
   - Cuidados / side effects

---

## Scripts de setup (bootstrap)

Ver `scripts/setup/`:

- `bootstrap.ps1` — Setup inicial (venv, deps, Docker, pre-commit)
- `INSTALACOES.md` — Log de instalações

---

**Mantido por:** TL (Tech Lead) / DEVOPS

---
