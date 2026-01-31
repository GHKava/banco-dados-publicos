# T-ONB-SRC-005 — Handoff: dados.gov.br Onboarding

**Data:** 2026-01-31
**Status:** ✅ DONE (METADATA_ONLY)
**Persona:** PM + LEGAL

---

## O que foi feito

- WorkOrder criado e evidências coletadas para SRC-005 (dados.gov.br).
- robots.txt retornou HTML do portal (não verificável).
- Homepage e API CKAN status_show responderam 200 OK.
- ToS/licença exigem login gov.br (sem evidência nesta rodada).
- Policy gate final: **METADATA_ONLY** (fail-closed).
- DUV-008 criada para pendências de ToS/licença/robots.

---

## Decisões

1. **Fail-closed:** manter METADATA_ONLY até licença explícita por dataset.
2. **Robots inválido:** tratar como não verificável até evidência formal.

---

## Como validar

1. Revisar evidence pack: [docs/evidence/T-ONB-SRC-005/](../../docs/evidence/T-ONB-SRC-005/)
2. Validar ToS/licença via acesso autenticado gov.br:
   - https://dados.gov.br/termos-de-uso
   - https://dados.gov.br/politica-de-privacidade
   - https://dados.gov.br/faq
3. Verificar licenças por dataset no CKAN antes de qualquer upgrade.

---

## DUVs

- **DUV-008:** ToS/licença exigem login; robots.txt inválido (HTML) (SLA 2026-02-01)

---

## Próxima tarefa

- **T-009** — Bot: robots checker
