# T-ONB-SRC-004 — Handoff: BCB Onboarding

**Data:** 2026-01-31
**Status:** ✅ DONE (METADATA_ONLY)
**Persona:** PM + LEGAL

---

## O que foi feito

- WorkOrder criado e evidências coletadas para SRC-004 (BCB Dados Abertos).
- robots.txt disponível e restringe `/api/`, crawl-delay 10s.
- Termos do site permitem reprodução com citação (bcb.gov.br), mas licença por dataset não especificada.
- Policy gate final: **METADATA_ONLY** (fail-closed).
- DUV-007 criada para verificação de licença por dataset.

---

## Decisões

1. **Fail-closed:** manter METADATA_ONLY até licença explícita por dataset.
2. **Respeitar robots.txt:** sem acesso `/api/`, crawl-delay 10s.

---

## Como validar

1. Revisar evidence pack: [docs/evidence/T-ONB-SRC-004/](../../docs/evidence/T-ONB-SRC-004/)
2. Verificar licença por dataset no portal:
   - https://dadosabertos.bcb.gov.br/pages/perguntas-frequentes
   - https://dadosabertos.bcb.gov.br/pages/sobre-o-portal
3. Se licença explícita for encontrada, atualizar policy gate.

---

## DUVs

- **DUV-007:** Licença aberta não especificada por dataset (SLA 2026-02-01)

---

## Próxima tarefa

- **T-ONB-SRC-005** — Onboarding dados.gov.br
