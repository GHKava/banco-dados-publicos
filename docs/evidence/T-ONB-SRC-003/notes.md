# Notes — T-ONB-SRC-003 (IBGE Onboarding)

**Data:** 2026-01-31
**Executor:** ORQ (Agente Orquestrador)
**Status:** ✅ DONE (fail-closed)

---

## Resumo Executivo

Onboarding de SRC-003 (IBGE APIs) iniciado. Robots.txt retornou **503**, API docs acessível (200), API root **503**. Sem evidência de ToS/licença explícita. Decisão provisória: **METADATA_ONLY** (fail-closed).

---

## Descobertas

1. **robots.txt:** Status 503 (indisponível)
2. **API docs:** 200 OK
3. **API root:** 503 Service Unavailable
4. **ToS/licença:** não localizada com evidência nesta rodada

---

## Decisões

1. **Policy gate:** METADATA_ONLY (fail-closed)
2. **Rate limit:** 1.0 rps (conforme sources.yaml)
3. **PII detection:** Obrigatória

---

## Evidências criadas

- [x] `robots.txt` (status 503 registrado)
- [x] `outputs.log`
- [x] `fetch_test.log`
- [x] `license_analysis.md`
- [x] `sample_urls.txt`
- [x] `notes.md`

---

## Próximos passos

1. Revalidar robots.txt e API root
2. Localizar termos/licença oficial do IBGE para APIs
3. DUV-006 aberta para revalidar conectividade/ToS/licença

---
