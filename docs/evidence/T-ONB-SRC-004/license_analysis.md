# T-ONB-SRC-004 — Análise de Compliance BCB

**Data:** 2026-01-31
**Fonte:** SRC-004 (dadosabertos.bcb.gov.br / bcb.gov.br)
**Status:** ANÁLISE CONCLUÍDA (decisão METADATA_ONLY)

---

## 1. Robots.txt

**URL testada:** https://dadosabertos.bcb.gov.br/robots.txt
**Resultado:** 200 OK

**Regras relevantes:**

- `Disallow: /api/`
- `Crawl-Delay: 10`

**Conclusão:** Restrições explícitas para `/api/` e crawl delay elevado.

**URL testada:** https://www.bcb.gov.br/robots.txt
**Resultado:** 200 OK (ver `fetch_test.log`)

---

## 2. Termos de Uso / Direitos Autorais

### 2.1 Política de Privacidade e Termos de Uso (bcb.gov.br)

**URL:** https://www.bcb.gov.br/acessoinformacao/politicaprivacidade

**Trecho relevante (Reprodução do Conteúdo):**

> É permitida a reprodução total ou parcial do conteúdo do site e dos serviços digitais do BC, preservada a integridade das informações e citada a fonte.

**Observação:** Permite reprodução com citação, mas não é uma licença aberta formal (ex.: CC-BY).

### 2.2 Dados Abertos (Portal)

**FAQ:** https://dadosabertos.bcb.gov.br/pages/perguntas-frequentes

**Trecho relevante:**

> Dados públicos ... disponibilizados sob licença aberta que permita sua livre utilização.

**Observação:** Não especifica qual licença aberta é aplicada a cada dataset.

---

## 3. Policy Gate Decision

**Decisão:** METADATA_ONLY (fail-closed)

**Justificativa:**

1. Robots.txt bloqueia `/api/` e exige crawl-delay 10s
2. Licença aberta não especificada por dataset (ambígua)
3. ToS permite reprodução no site institucional, mas não define licença de dados do portal

---

## 4. Próximos passos

1. Verificar licença específica por dataset no portal
2. Observar e respeitar regras de robots (sem acesso `/api/`)
3. Se licença explícita for encontrada, considerar upgrade para ALLOW_FULLTEXT
