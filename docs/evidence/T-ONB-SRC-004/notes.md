# Notes — T-ONB-SRC-004 (BCB Onboarding)

**Data:** 2026-01-31
**Executor:** ORQ (Agente Orquestrador)
**Status:** ✅ DONE (fail-closed)

---

## Resumo Executivo

Onboarding de SRC-004 (BCB Dados Abertos) concluído. Robots.txt disponível e restringe `/api/` com crawl-delay 10s. Termos do site permitem reprodução com citação, mas licença aberta dos datasets não é explicitada. Decisão final: **METADATA_ONLY**.

---

## Descobertas

1. **robots.txt (dadosabertos):** 200 OK; `Disallow: /api/`; `Crawl-Delay: 10`
2. **robots.txt (bcb.gov.br):** 200 OK
3. **ToS (bcb.gov.br):** reprodução permitida com citação
4. **FAQ dados abertos:** menciona licença aberta, mas não especifica qual

---

## Decisões

1. **Policy gate:** METADATA_ONLY (fail-closed)
2. **Respeitar robots:** não acessar `/api/`
3. **Crawl delay:** manter >= 10s

---

## Evidências criadas

- [x] `robots.txt`
- [x] `outputs.log`
- [x] `fetch_test.log`
- [x] `license_analysis.md`
- [x] `sample_urls.txt`
- [x] `notes.md`

---

## Próximos passos

1. Confirmar licença por dataset no portal
2. Ajustar policy gate se licença explícita for localizada
3. DUV-007 aberta para verificação de licença por dataset

---
