# SRC-001 — Diário Oficial da União (DOU) - Imprensa Nacional

**Source ID:** SRC-001  
**Source Name:** Diário Oficial da União (DOU) - Imprensa Nacional  
**Domain:** in.gov.br  
**Data criação:** 2026-01-30  
**Status:** IN_REVIEW

---

## 1. Identificação

- **ID:** SRC-001
- **Nome:** Diário Oficial da União (DOU) - Imprensa Nacional
- **URL base:** https://www.in.gov.br
- **Tipo:** Governo
- **Escopo:** Publicações oficiais do governo federal brasileiro (leis, decretos, portarias, editais, etc.)

---

## 2. Discovery & Acesso

- **Discovery method:**
  - [x] RSS/Atom feed (URL: https://www.in.gov.br/rss)
  - [x] HTML index (URL: https://www.in.gov.br/leiturajornal)
  - [ ] API oficial: Não disponível

- **Autenticação requerida?** [x] Não

---

## 3. Compliance & Legal

### 3.1 Robots.txt

- **URL robots.txt:** https://www.in.gov.br/robots.txt
- **Verificado em:** PENDENTE
- **Status:** ⏳ PENDENTE VERIFICAÇÃO
- **Notas:** Verificar antes de T-ONB-SRC-001

### 3.2 Termos de Serviço (ToS)

- **URL ToS:** PENDENTE (buscar em footer/sobre)
- **Verificado em:** PENDENTE
- **Permite scraping/crawling?** [ ] PENDENTE VERIFICAÇÃO
- **Restrições:** PENDENTE
- **Evidência:** PENDENTE (criar screenshot em T-ONB-SRC-001)

### 3.3 Licença de dados

- **Tipo de licença:** PENDENTE VERIFICAÇÃO (assumir pública por natureza, mas confirmar)
- **URL licença:** PENDENTE
- **Permite armazenamento integral?** [ ] CONDICIONAL (aguardando verificação)
- **Permite redistribuição?** [ ] CONDICIONAL
- **Atribuição obrigatória?** [x] Sim (assumir que sim por transparência pública)
- **Uso comercial permitido?** [ ] CONDICIONAL
- **Evidência:** PENDENTE

### 3.4 LGPD / Privacidade

- **Fonte contém PII?** [x] Possível (editais, nomeações podem ter nomes/CPF)
- **Tipos de PII esperados:** CPF, nomes, cargos, endereços (em editais/concursos)
- **Consentimento para coleta?** [x] N/A (dados públicos oficiais, mas PII detection obrigatória)
- **Política de retenção:** 365 dias (conforme escopo)

---

## 4. Policy Gate Decision

**Decisão de armazenamento:**

- [x] **METADATA_ONLY** — Somente metadados + link (sem texto completo até licença verificada)
- [ ] ALLOW_FULLTEXT (após verificação ToS/licença)
- [ ] SNIPPETS_ONLY
- [ ] BLOCK

**Justificativa:** Fail-closed. DOU é público por natureza (transparência governamental), mas precisamos confirmar ToS explícito e licença antes de armazenar fulltext. PII detection obrigatória.

**Aprovado por:** PM (decisão preliminar; aguardando LEGAL/DPO)  
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
- **Horários permitidos:** 24/7 (off-peak preferencial)

### 5.3 Tipos de conteúdo

- **Formatos esperados:** HTML, PDF
- **Formatos proibidos:** Executáveis, scripts

---

## 6. Discovery Específico

### 6.1 RSS/Feed

- **URL feed:** https://www.in.gov.br/rss
- **Itens por página:** ~20-50 (verificar)

### 6.2 HTML Index

- **URL index:** https://www.in.gov.br/leiturajornal
- **Navegação:** Por seção/data

---

## 7. Testes & Validação

### 7.1 Golden docs (amostras)

- **URL amostra 1:** PENDENTE (selecionar durante T-ONB-SRC-001)
- **URL amostra 2:** PENDENTE
- **URL amostra 3:** PENDENTE

### 7.2 Parsing

- **Parser recomendado:** trafilatura (HTML), PyMuPDF (PDF)
- **Boilerplate removal:** [x] Sim
- **OCR necessário?** [ ] Não (PDFs já digitalizados)

### 7.3 Quality checks

- **Densidade de texto esperada:** Alta
- **Idioma principal:** pt-BR

---

## 8. Riscos & Mitigações

| Risco              | Severidade | Mitigação                             |
| ------------------ | ---------- | ------------------------------------- |
| Licença restritiva | Alta       | METADATA_ONLY até confirmação         |
| PII em editais     | Alta       | PII detection + redaction obrigatória |
| Rate limit         | Baixa      | Respeitar 0.5 rps                     |
| PDFs grandes       | Média      | Timeout 30s; budget bandwidth         |

---

## 9. Evidence Pack

**Localização:** `docs/evidence/T-ONB-SRC-001/`

Arquivos obrigatórios (criar em T-ONB-SRC-001):

- [ ] `robots.txt` (cópia)
- [ ] `tos_screenshot.png` (ToS)
- [ ] `license_screenshot.png` (licença ou nota de ausência)
- [ ] `sample_urls.txt` (3+ URLs de teste)
- [ ] `fetch_test.log` (log de teste de fetch)
- [ ] `notes.md` (resumo decisões)

---

## 10. Aprovação Final

- [x] Fonte identificada e documentada
- [ ] Compliance verificado (robots + ToS + licença) — PENDENTE T-ONB-SRC-001
- [x] Policy gate decision registrada (METADATA_ONLY)
- [x] Rate limits definidos
- [ ] Golden docs selecionados — PENDENTE T-ONB-SRC-001
- [ ] Evidence pack criado — PENDENTE T-ONB-SRC-001
- [x] Entrada em `configs/sources.yaml` criada
- [x] Entrada em `Fontes_Licencas.md` criada

**Status final:** [ ] APROVADO [x] IN_REVIEW [ ] REJEITADO

**Próxima ação:** T-ONB-SRC-001 (compliance verification + evidence pack)

---

**Mantido por:** PM + LEGAL + DPO  
**Última revisão:** 2026-01-30
