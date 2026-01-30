# SRC-002 — Planalto - Legislação

**Source ID:** SRC-002  
**Source Name:** Planalto - Legislação  
**Domain:** planalto.gov.br  
**Data criação:** 2026-01-30  
**Status:** IN_REVIEW

---

## 1. Identificação

- **ID:** SRC-002
- **Nome:** Planalto - Legislação Federal
- **URL base:** https://www.planalto.gov.br
- **Tipo:** Governo
- **Escopo:** Legislação federal brasileira (leis, decretos, constituição, códigos)

---

## 2. Discovery & Acesso

- **Discovery method:**
  - [x] Sitemap XML (URL: https://www.planalto.gov.br/sitemap.xml — PENDENTE VERIFICAÇÃO)
  - [x] HTML index (URL: https://www.planalto.gov.br/ccivil_03/)
  - [ ] API oficial: Não disponível

- **Autenticação requerida?** [x] Não

---

## 3. Compliance & Legal

### 3.1 Robots.txt

- **URL robots.txt:** https://www.planalto.gov.br/robots.txt
- **Verificado em:** PENDENTE
- **Status:** ⏳ PENDENTE VERIFICAÇÃO
- **Notas:** Verificar antes de T-ONB-SRC-002

### 3.2 Termos de Serviço (ToS)

- **URL ToS:** PENDENTE (buscar em footer/sobre)
- **Verificado em:** PENDENTE
- **Permite scraping/crawling?** [ ] PENDENTE VERIFICAÇÃO
- **Restrições:** PENDENTE
- **Evidência:** PENDENTE

### 3.3 Licença de dados

- **Tipo de licença:** PENDENTE (legislação é pública por LAI, mas confirmar termos de redistribuição)
- **URL licença:** PENDENTE
- **Permite armazenamento integral?** [ ] CONDICIONAL
- **Permite redistribuição?** [ ] CONDICIONAL (LAI permite acesso, mas confirmar republicação)
- **Atribuição obrigatória?** [x] Sim (assumir que sim por transparência)
- **Uso comercial permitido?** [ ] CONDICIONAL
- **Evidência:** PENDENTE

### 3.4 LGPD / Privacidade

- **Fonte contém PII?** [ ] Não (legislação é despersonalizada)
- **Tipos de PII esperados:** Nenhum esperado
- **Consentimento para coleta?** [x] N/A
- **Política de retenção:** 365 dias

---

## 4. Policy Gate Decision

**Decisão de armazenamento:**

- [x] **METADATA_ONLY** — Somente metadados + link (sem texto completo até licença verificada)
- [ ] ALLOW_FULLTEXT (após verificação)
- [ ] SNIPPETS_ONLY
- [ ] BLOCK

**Justificativa:** Fail-closed. Legislação é pública por LAI, mas precisamos confirmar ToS explícito e termos de redistribuição antes de fulltext.

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

- **Max URLs/dia:** 500
- **Max bandwidth/dia:** 50MB
- **Horários permitidos:** 24/7

### 5.3 Tipos de conteúdo

- **Formatos esperados:** HTML
- **Formatos proibidos:** Executáveis

---

## 6. Discovery Específico

### 6.1 Sitemap

- **URL sitemap:** https://www.planalto.gov.br/sitemap.xml (VERIFICAR SE EXISTE)
- **Frequência de atualização:** PENDENTE

### 6.2 HTML Index

- **URL index:** https://www.planalto.gov.br/ccivil_03/
- **Navegação:** Por tipo de norma / ano

---

## 7. Testes & Validação

### 7.1 Golden docs (amostras)

- **URL amostra 1:** PENDENTE
- **URL amostra 2:** PENDENTE
- **URL amostra 3:** PENDENTE

### 7.2 Parsing

- **Parser recomendado:** trafilatura (HTML)
- **Boilerplate removal:** [x] Sim
- **OCR necessário?** [ ] Não

### 7.3 Quality checks

- **Densidade de texto esperada:** Alta
- **Idioma principal:** pt-BR

---

## 8. Riscos & Mitigações

| Risco                             | Severidade | Mitigação                     |
| --------------------------------- | ---------- | ----------------------------- |
| Licença restritiva redistribuição | Alta       | METADATA_ONLY até confirmação |
| Rate limit                        | Baixa      | Respeitar 0.5 rps             |

---

## 9. Evidence Pack

**Localização:** `docs/evidence/T-ONB-SRC-002/`

Arquivos obrigatórios:

- [ ] `robots.txt`
- [ ] `tos_screenshot.png`
- [ ] `license_screenshot.png`
- [ ] `sample_urls.txt`
- [ ] `fetch_test.log`
- [ ] `notes.md`

---

## 10. Aprovação Final

- [x] Fonte identificada
- [ ] Compliance verificado — PENDENTE T-ONB-SRC-002
- [x] Policy gate decision registrada (METADATA_ONLY)
- [x] Rate limits definidos
- [ ] Golden docs — PENDENTE
- [ ] Evidence pack — PENDENTE
- [x] Entrada em `configs/sources.yaml`
- [x] Entrada em `Fontes_Licencas.md`

**Status final:** [x] IN_REVIEW [ ] APROVADO [ ] REJEITADO

**Próxima ação:** T-ONB-SRC-002

---

**Mantido por:** PM + LEGAL + DPO  
**Última revisão:** 2026-01-30
