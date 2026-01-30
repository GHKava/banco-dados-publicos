# SRC-003 — IBGE - APIs e Dados

**Source ID:** SRC-003  
**Source Name:** IBGE - APIs e Dados  
**Domain:** ibge.gov.br / servicodados.ibge.gov.br  
**Data criação:** 2026-01-30  
**Status:** IN_REVIEW

---

## 1. Identificação

- **ID:** SRC-003
- **Nome:** IBGE - APIs e Dados Públicos
- **URL base:** https://servicodados.ibge.gov.br
- **Tipo:** Governo
- **Escopo:** Dados estatísticos e geográficos do Brasil (censos, pesquisas, mapas, APIs oficiais)

---

## 2. Discovery & Acesso

- **Discovery method:**
  - [x] API oficial (Docs: https://servicodados.ibge.gov.br/api/docs)
  - [ ] Sitemap: Não aplicável (API)
  - [ ] RSS: Não aplicável

- **Autenticação requerida?** [x] Não (APIs públicas)

---

## 3. Compliance & Legal

### 3.1 Robots.txt

- **URL robots.txt:** https://servicodados.ibge.gov.br/robots.txt
- **Verificado em:** PENDENTE
- **Status:** ⏳ PENDENTE VERIFICAÇÃO (APIs geralmente permitem, mas confirmar)

### 3.2 Termos de Serviço (ToS)

- **URL ToS:** PENDENTE (buscar em https://www.ibge.gov.br/acesso-informacao/termos-de-uso)
- **Verificado em:** PENDENTE
- **Permite scraping/crawling?** [x] APIs públicas (assumir sim, mas confirmar termos)
- **Restrições:** PENDENTE VERIFICAÇÃO
- **Evidência:** PENDENTE

### 3.3 Licença de dados

- **Tipo de licença:** PENDENTE (IBGE frequentemente usa CC-BY ou similar; confirmar)
- **URL licença:** PENDENTE (buscar em docs oficiais)
- **Permite armazenamento integral?** [ ] CONDICIONAL (aguardando confirmação CC-BY)
- **Permite redistribuição?** [ ] CONDICIONAL (CC-BY permite com atribuição)
- **Atribuição obrigatória?** [x] Sim (assumir que sim)
- **Uso comercial permitido?** [ ] CONDICIONAL (CC-BY permite)
- **Evidência:** PENDENTE

### 3.4 LGPD / Privacidade

- **Fonte contém PII?** [ ] Não (dados agregados, anonimizados)
- **Tipos de PII esperados:** Nenhum (estatísticas agregadas)
- **Consentimento para coleta?** [x] N/A
- **Política de retenção:** 365 dias

---

## 4. Policy Gate Decision

**Decisão de armazenamento:**

- [x] **METADATA_ONLY** — Somente metadados + link (até verificação CC-BY ou similar)
- [ ] ALLOW_FULLTEXT (após confirmação de licença CC-BY/aberta)
- [ ] SNIPPETS_ONLY
- [ ] BLOCK

**Justificativa:** Fail-closed. APIs públicas, mas precisamos confirmar licença CC-BY explícita antes de fulltext. Se confirmado CC-BY → upgrade para ALLOW_FULLTEXT.

**Aprovado por:** PM (preliminar; upgrade condicional à verificação LEGAL)  
**Data aprovação:** 2026-01-30

---

## 5. Regras Operacionais

### 5.1 Rate Limits

- **Rate limit (requests/segundo):** 1.0 (APIs geralmente permitem mais; ajustar se necessário)
- **Concurrency (workers):** 2
- **Backoff strategy:** exponential
- **Max retries:** 3
- **Timeout (segundos):** 30

### 5.2 Budget / Limites

- **Max URLs/dia:** 2000
- **Max bandwidth/dia:** 200MB
- **Horários permitidos:** 24/7

### 5.3 Tipos de conteúdo

- **Formatos esperados:** JSON, HTML
- **Formatos proibidos:** Executáveis

---

## 6. Discovery Específico

### 6.1 API

- **Docs API:** https://servicodados.ibge.gov.br/api/docs
- **Endpoints relevantes:** Diversos (censos, pesquisas, agregados, localidades)
- **Formato resposta:** JSON
- **Paginação:** Varia por endpoint (confirmar documentação)

---

## 7. Testes & Validação

### 7.1 Golden docs (amostras)

- **Endpoint amostra 1:** PENDENTE (ex.: /api/v1/agregados)
- **Endpoint amostra 2:** PENDENTE
- **Endpoint amostra 3:** PENDENTE

### 7.2 Parsing

- **Parser recomendado:** JSON nativo (Python `json`)
- **Boilerplate removal:** N/A (APIs)
- **OCR necessário?** [ ] Não

### 7.3 Quality checks

- **Densidade de texto esperada:** Média (metadados + dados estruturados)
- **Idioma principal:** pt-BR

---

## 8. Riscos & Mitigações

| Risco             | Severidade | Mitigação                           |
| ----------------- | ---------- | ----------------------------------- |
| Licença não-CC-BY | Alta       | METADATA_ONLY até confirmação       |
| Rate limit API    | Baixa      | Respeitar 1.0 rps                   |
| Mudanças de API   | Média      | Monitorar docs; versionar endpoints |

---

## 9. Evidence Pack

**Localização:** `docs/evidence/T-ONB-SRC-003/`

Arquivos obrigatórios:

- [ ] `api_docs_screenshot.png`
- [ ] `license_screenshot.png`
- [ ] `sample_responses.json`
- [ ] `fetch_test.log`
- [ ] `notes.md`

---

## 10. Aprovação Final

- [x] Fonte identificada
- [ ] Compliance verificado — PENDENTE T-ONB-SRC-003
- [x] Policy gate decision registrada (METADATA_ONLY → ALLOW_FULLTEXT condicional)
- [x] Rate limits definidos
- [ ] Golden endpoints — PENDENTE
- [ ] Evidence pack — PENDENTE
- [x] Entrada em `configs/sources.yaml`
- [x] Entrada em `Fontes_Licencas.md`

**Status final:** [x] IN_REVIEW [ ] APROVADO [ ] REJEITADO

**Próxima ação:** T-ONB-SRC-003 (verificar licença CC-BY → upgrade para ALLOW_FULLTEXT se confirmado)

---

**Mantido por:** PM + LEGAL + DPO  
**Última revisão:** 2026-01-30
