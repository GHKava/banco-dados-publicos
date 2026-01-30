# T-ONB-SRC-002 — Handoff: Planalto Onboarding

**Data:** 2026-01-31
**Status:** ✅ DONE (METADATA_ONLY)
**Persona:** PM + LEGAL

---

## O que foi feito

- Executadas tentativas de fetch para robots.txt, homepage e ccivil_03 (falharam por erro de conexão).
- Evidence pack criado com logs, robots.txt (erro de fetch), análise de licença e URLs golden.
- Checklist de onboarding preenchido com decisão fail-closed.
- Policy gate final: **METADATA_ONLY** (sem evidência de robots/ToS/licença).
- DUV-005 aberta para revalidar conectividade e verificação de permissões.

---

## Decisões

1. **Fail-closed:** manter METADATA_ONLY até confirmar robots/ToS/licença.
2. **Sem upgrade para ALLOW_FULLTEXT** nesta rodada (falta de evidência primária).

---

## Como validar

1. Revisar evidence pack: [docs/evidence/T-ONB-SRC-002/](../../docs/evidence/T-ONB-SRC-002/)
2. Reexecutar fetch quando conectividade permitir:
   ```powershell
   Invoke-WebRequest -Uri "https://www.planalto.gov.br/robots.txt" -UserAgent "PublicDataPipelineBot/1.0" -TimeoutSec 30
   Invoke-WebRequest -Uri "https://www.planalto.gov.br/" -UseBasicParsing -TimeoutSec 30
   Invoke-WebRequest -Uri "https://www.planalto.gov.br/ccivil_03/" -UseBasicParsing -TimeoutSec 30
   ```
3. Se houver ToS/licença explícita permitindo scraping, atualizar policy gate.

---

## DUVs

- **DUV-005:** Falha de conectividade impede verificação de robots/ToS (SLA 2026-02-01)

---

## Próxima tarefa

- **T-ONB-SRC-003** — Onboarding IBGE
