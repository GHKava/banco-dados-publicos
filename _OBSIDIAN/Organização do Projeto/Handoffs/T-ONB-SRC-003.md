# T-ONB-SRC-003 — Handoff: IBGE Onboarding

**Data:** 2026-01-31
**Status:** ✅ DONE (METADATA_ONLY)
**Persona:** PM + LEGAL

---

## O que foi feito

- WorkOrder criado e evidências coletadas para SRC-003 (IBGE).
- robots.txt retornou 503 (indisponível).
- API docs acessível (200), API root indisponível (503).
- Policy gate final: **METADATA_ONLY** (fail-closed).
- DUV-006 criada para revalidar robots/ToS/licença.

---

## Decisões

1. **Fail-closed:** manter METADATA_ONLY até evidência de licença/ToS.
2. **Sem upgrade para ALLOW_FULLTEXT** nesta rodada.

---

## Como validar

1. Revisar evidence pack: [docs/evidence/T-ONB-SRC-003/](../../docs/evidence/T-ONB-SRC-003/)
2. Reexecutar fetch quando serviços estiverem disponíveis:
   ```powershell
   Invoke-WebRequest -Uri "https://servicodados.ibge.gov.br/robots.txt" -UserAgent "PublicDataPipelineBot/1.0" -TimeoutSec 30
   Invoke-WebRequest -Uri "https://servicodados.ibge.gov.br/api/docs" -UseBasicParsing -TimeoutSec 30
   Invoke-WebRequest -Uri "https://servicodados.ibge.gov.br/api/" -UseBasicParsing -TimeoutSec 30
   ```
3. Se ToS/licença explícita for encontrada, atualizar policy gate.

---

## DUVs

- **DUV-006:** Robots.txt 503 e ToS/licença não verificáveis (SLA 2026-02-01)

---

## Próxima tarefa

- **T-ONB-SRC-004** — Onboarding BCB
