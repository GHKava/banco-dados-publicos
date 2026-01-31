# Notes — T-ONB-SRC-005 (dados.gov.br Onboarding)

**Data:** 2026-01-31
**Executor:** ORQ (Agente Orquestrador)
**Status:** ✅ DONE (fail-closed)

---

## Resumo Executivo

Onboarding de SRC-005 concluído. Robots.txt retornou HTML do portal (não regras). Homepage e API CKAN responderam 200. ToS/licença exigem login gov.br, não verificáveis. Decisão final: **METADATA_ONLY**.

---

## Descobertas

1. **robots.txt:** 200 OK, mas conteúdo inválido (HTML do portal)
2. **Homepage:** 200 OK
3. **API CKAN status_show:** 200 OK
4. **ToS/licença:** páginas exigem login (sem evidência nesta rodada)

---

## Decisões

1. **Policy gate:** METADATA_ONLY (fail-closed)
2. **Licença variável por dataset:** manter apenas metadados e links
3. **PII detection:** obrigatória (datasets podem conter PII)

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

1. Verificar robots.txt real e ToS/licença com autenticação
2. Identificar licenças por dataset antes de qualquer upgrade
3. DUV-008 aberta para pendências de licenciamento

---
