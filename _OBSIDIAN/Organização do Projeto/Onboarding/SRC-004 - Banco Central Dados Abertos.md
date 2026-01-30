# SRC-004 — Banco Central - Dados Abertos

**Source ID:** SRC-004  
**Source Name:** Banco Central - Dados Abertos  
**Domain:** bcb.gov.br / dadosabertos.bcb.gov.br  
**Data criação:** 2026-01-30  
**Status:** IN_REVIEW

---

## 1. Identificação

- **ID:** SRC-004
- **Nome:** Banco Central do Brasil - Dados Abertos
- **URL base:** https://dadosabertos.bcb.gov.br
- **Tipo:** Governo
- **Escopo:** Dados abertos financeiros, econômicos e regulatórios do BCB

---

## 2. Discovery & Acesso

- **Discovery method:**
  - [x] API oficial (Docs: https://dadosabertos.bcb.gov.br/dataset)
  - [ ] Catálogo de datasets
  - [ ] RSS: PENDENTE VERIFICAÇÃO

- **Autenticação requerida?** [x] Não (APIs públicas de dados abertos)

---

## 3. Compliance & Legal

### 3.1 Robots.txt

- **URL robots.txt:** https://dadosabertos.bcb.gov.br/robots.txt
- **Verificado em:** PENDENTE
- **Status:** ⏳ PENDENTE VERIFICAÇÃO

### 3.2 Termos de Serviço (ToS)

- **URL ToS:** PENDENTE (buscar em https://www.bcb.gov.br/acessoinformacao/termos-de-uso)
- **Verificado em:** PENDENTE
- **Permite scraping/crawling?** [x] APIs de dados abertos (assumir sim, mas confirmar)
- **Restrições:** PENDENTE
- **Evidência:** PENDENTE

### 3.3 Licença de dados

- **Tipo de licença:** PENDENTE (BCB frequentemente libera dados abertos; confirmar licença LAI/CC)
- **URL licença:** PENDENTE
- **Permite armazenamento integral?** [ ] CONDICIONAL
- **Permite redistribuição?** [ ] CONDICIONAL
- **Atribuição obrigatória?** [x] Sim (assumir que sim)
- **Uso comercial permitido?** [ ] CONDICIONAL
- **Evidência:** PENDENTE

### 3.4 LGPD / Privacidade

- **Fonte contém PII?** [ ] Não (dados agregados, regulatórios, despersonalizados)
- **Tipos de PII esperados:** Nenhum
- **Consentimento para coleta?** [x] N/A
- **Política de retenção:** 365 dias

---

## 4. Policy Gate Decision

**Decisão de armazenamento:**

- [x] **METADATA_ONLY** — Somente metadados + link (até verificação de licença)
- [ ] ALLOW_FULLTEXT (após confirmação LAI/CC ou similar)
- [ ] SNIPPETS_ONLY
- [ ] BLOCK

**Justificativa:** Fail-closed. Dados abertos BCB, mas precisamos confirmar licença explícita (LAI, CC-BY ou similar) antes de fulltext.

**Aprovado por:** PM (preliminar)  
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

- **Max URLs/dia:** 1000
- **Max bandwidth/dia:** 100MB
- **Horários permitidos:** 24/7

### 5.3 Tipos de conteúdo

- **Formatos esperados:** JSON, CSV
- **Formatos proibidos:** Executáveis

---

## 6. Discovery Específico

### 6.1 API/Catálogo

- **Docs API:** https://dadosabertos.bcb.gov.br/dataset
- **Endpoints relevantes:** PENDENTE (explorar catálogo)
- **Formato resposta:** JSON, CSV
- **Paginação:** PENDENTE VERIFICAÇÃO

---

## 7. Testes & Validação

### 7.1 Golden docs (amostras)

- **URL amostra 1:** PENDENTE
- **URL amostra 2:** PENDENTE
- **URL amostra 3:** PENDENTE

### 7.2 Parsing

- **Parser recomendado:** JSON/CSV nativo
- **Boilerplate removal:** N/A
- **OCR necessário?** [ ] Não

### 7.3 Quality checks

- **Densidade de texto esperada:** Média (dados estruturados)
- **Idioma principal:** pt-BR

---

## 8. Riscos & Mitigações

| Risco              | Severidade | Mitigação                     |
| ------------------ | ---------- | ----------------------------- |
| Licença restritiva | Alta       | METADATA_ONLY até confirmação |
| Rate limit         | Baixa      | Respeitar 0.5 rps             |

---

## 9. Evidence Pack

**Localização:** `docs/evidence/T-ONB-SRC-004/`

Arquivos obrigatórios:

- [ ] `license_screenshot.png`
- [ ] `tos_screenshot.png`
- [ ] `sample_data.json`
- [ ] `fetch_test.log`
- [ ] `notes.md`

---

## 10. Aprovação Final

- [x] Fonte identificada
- [ ] Compliance verificado — PENDENTE T-ONB-SRC-004
- [x] Policy gate decision registrada (METADATA_ONLY)
- [x] Rate limits definidos
- [ ] Golden docs — PENDENTE
- [ ] Evidence pack — PENDENTE
- [x] Entrada em `configs/sources.yaml`
- [x] Entrada em `Fontes_Licencas.md`

**Status final:** [x] IN_REVIEW [ ] APROVADO [ ] REJEITADO

**Próxima ação:** T-ONB-SRC-004

---

**Mantido por:** PM + LEGAL + DPO  
**Última revisão:** 2026-01-30
