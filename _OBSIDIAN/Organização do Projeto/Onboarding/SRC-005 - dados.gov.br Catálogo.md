# SRC-005 — dados.gov.br - Catálogo

**Source ID:** SRC-005  
**Source Name:** dados.gov.br - Catálogo de Dados Abertos  
**Domain:** dados.gov.br  
**Data criação:** 2026-01-30  
**Status:** IN_REVIEW

---

## 1. Identificação

- **ID:** SRC-005
- **Nome:** dados.gov.br - Catálogo Nacional de Dados Abertos
- **URL base:** https://dados.gov.br
- **Tipo:** Governo (catálogo agregador)
- **Escopo:** Catálogo de datasets públicos de diversos órgãos governamentais brasileiros

---

## 2. Discovery & Acesso

- **Discovery method:**
  - [x] API CKAN (Docs: https://dados.gov.br/api/3)
  - [ ] Sitemap: PENDENTE VERIFICAÇÃO
  - [ ] RSS: PENDENTE VERIFICAÇÃO

- **Autenticação requerida?** [x] Não (API pública)

---

## 3. Compliance & Legal

### 3.1 Robots.txt

- **URL robots.txt:** https://dados.gov.br/robots.txt
- **Verificado em:** PENDENTE
- **Status:** ⏳ PENDENTE VERIFICAÇÃO

### 3.2 Termos de Serviço (ToS)

- **URL ToS:** PENDENTE (buscar em footer/sobre)
- **Verificado em:** PENDENTE
- **Permite scraping/crawling?** [x] API pública (assumir sim, mas confirmar)
- **Restrições:** PENDENTE
- **Evidência:** PENDENTE

### 3.3 Licença de dados

- **Tipo de licença:** **VARIÁVEL POR DATASET** (cada dataset tem licença própria)
- **URL licença:** PENDENTE (verificar POR DATASET via API)
- **Permite armazenamento integral?** [ ] CONDICIONAL (depende de cada dataset)
- **Permite redistribuição?** [ ] CONDICIONAL (depende de cada dataset)
- **Atribuição obrigatória?** [ ] CONDICIONAL (depende da licença do dataset)
- **Uso comercial permitido?** [ ] CONDICIONAL
- **Evidência:** PENDENTE (verificar campo `license_id` na API)

### 3.4 LGPD / Privacidade

- **Fonte contém PII?** [x] POSSÍVEL (alguns datasets podem conter PII; verificar POR DATASET)
- **Tipos de PII esperados:** Variável (CPF, nomes, endereços possíveis em alguns datasets)
- **Consentimento para coleta?** [x] N/A (dados públicos, mas PII detection obrigatória)
- **Política de retenção:** 365 dias

---

## 4. Policy Gate Decision

**Decisão de armazenamento:**

- [x] **METADATA_ONLY** — Somente metadados + link (licença variável POR DATASET)
- [ ] ALLOW_FULLTEXT (SOMENTE após verificação de licença POR DATASET individualmente)
- [ ] SNIPPETS_ONLY
- [ ] BLOCK

**Justificativa:** Fail-closed. Catálogo misto; cada dataset tem licença própria (CC0, CC-BY, Proprietária, etc.). Precisamos:

1. Verificar licença POR DATASET via API (`license_id`)
2. PII detection obrigatória (alguns datasets podem ter PII)
3. Upgrade para ALLOW_FULLTEXT SOMENTE após verificação individual

**Regra especial:** Criar tabela de tracking de datasets individuais com licenças verificadas.

**Aprovado por:** PM (preliminar; upgrade condicional POR DATASET)  
**Data aprovação:** 2026-01-30

---

## 5. Regras Operacionais

### 5.1 Rate Limits

- **Rate limit (requests/segundo):** 0.5
- **Concurrency (workers):** 1
- **Backoff strategy:** exponential
- **Max retries:** 3
- **Timeout (segundos):** 30

### 5.2 Budget / Limites

- **Max URLs/dia:** 500
- **Max bandwidth/dia:** 50MB
- **Horários permitidos:** 24/7

### 5.3 Tipos de conteúdo

- **Formatos esperados:** JSON, CSV, HTML
- **Formatos proibidos:** Executáveis

---

## 6. Discovery Específico

### 6.1 API CKAN

- **Docs API:** https://dados.gov.br/api/3
- **Endpoints relevantes:**
  - `/api/3/action/package_list` (listar datasets)
  - `/api/3/action/package_show?id={dataset_id}` (detalhes do dataset, incluindo `license_id`)
- **Formato resposta:** JSON
- **Paginação:** CKAN pagination (verificar docs)

---

## 7. Testes & Validação

### 7.1 Golden docs (amostras)

- **Dataset amostra 1:** PENDENTE (selecionar dataset com licença CC0 ou CC-BY)
- **Dataset amostra 2:** PENDENTE
- **Dataset amostra 3:** PENDENTE

### 7.2 Parsing

- **Parser recomendado:** JSON nativo (CKAN API), CSV/JSON para datasets
- **Boilerplate removal:** N/A
- **OCR necessário?** [ ] Não

### 7.3 Quality checks

- **Densidade de texto esperada:** Variável (metadados + datasets estruturados)
- **Idioma principal:** pt-BR

---

## 8. Riscos & Mitigações

| Risco                        | Severidade | Mitigação                                      |
| ---------------------------- | ---------- | ---------------------------------------------- |
| Licença variável por dataset | ALTA       | METADATA_ONLY; tracking table de licenças      |
| PII em datasets              | ALTA       | PII detection obrigatória em TODOS os datasets |
| Rate limit                   | Baixa      | Respeitar 0.5 rps                              |
| Datasets inacessíveis        | Média      | Retry + log de falhas                          |

---

## 9. Evidence Pack

**Localização:** `docs/evidence/T-ONB-SRC-005/`

Arquivos obrigatórios:

- [ ] `api_docs_screenshot.png`
- [ ] `license_tracking_table.csv` (tabela de datasets + licenças verificadas)
- [ ] `sample_datasets.json`
- [ ] `fetch_test.log`
- [ ] `notes.md`

**Especial:** Criar `license_tracking_table.csv` com colunas:

- `dataset_id`
- `dataset_name`
- `license_id` (da API)
- `license_verified` (bool)
- `storage_mode` (METADATA_ONLY | ALLOW_FULLTEXT)
- `pii_detection_required` (bool)
- `verified_date`

---

## 10. Aprovação Final

- [x] Fonte identificada
- [ ] Compliance verificado — PENDENTE T-ONB-SRC-005 (POR DATASET)
- [x] Policy gate decision registrada (METADATA_ONLY; upgrade POR DATASET)
- [x] Rate limits definidos
- [ ] Golden datasets — PENDENTE
- [ ] Evidence pack — PENDENTE
- [ ] License tracking table criada — PENDENTE
- [x] Entrada em `configs/sources.yaml`
- [x] Entrada em `Fontes_Licencas.md`

**Status final:** [x] IN_REVIEW [ ] APROVADO [ ] REJEITADO

**Próxima ação:** T-ONB-SRC-005 (criar license tracking table + verificar 3-5 datasets iniciais)

---

**Mantido por:** PM + LEGAL + DPO  
**Última revisão:** 2026-01-30
