# Fontes & Licenças — Registro Auditável

**Data criação:** 2026-01-30
**Última atualização:** 2026-01-31
**Mantido por:** PM + LEGAL + DPO

---

## 📋 Visão Geral

Este documento registra TODAS as fontes aprovadas/rejeitadas, incluindo compliance, licenças e decisões de policy gate.

**REGRA:** Nenhuma fonte pode ser ingerida sem entrada neste documento + `configs/sources.yaml`.

---

## 🟢 Fontes APROVADAS (METADATA_ONLY ou ALLOW_FULLTEXT)

### SRC-001 — Diário Oficial da União (DOU) - Imprensa Nacional

**Status:** 🔴 BLOCKED PROVISORIAMENTE (proteção anti-bot + ToS não verificado)
**Domínio:** in.gov.br
**Discovery:** RSS (https://www.in.gov.br/rss) [NÃO TESTADO]
**Robots.txt:** ❌ INACESSÍVEL (403 Forbidden - Azion WAF)
**ToS:** ❌ NÃO LOCALIZADO (página oficial não encontrada)
**Licença:** ⚠️ PROVÁVEL LAI (Lei 12.527/2011 - acesso a informações públicas), mas sem confirmação de permissão para scraping
**Policy Gate:** **BLOCK** (fail-closed — proteção anti-bot indica que scraping não é permitido)
**PII esperado:** Médio (documentos oficiais podem conter CPF/nomes)
**Rate limit:** N/A (bloqueado)
**Budget:** N/A (bloqueado)
**Onboarding:** T-ONB-SRC-001 (2026-01-30) — COMPLETED com resultado BLOCK
**Evidence Pack:** [docs/evidence/T-ONB-SRC-001/](../../docs/evidence/T-ONB-SRC-001/)
**DUV aberta:** DUV-004 — "Como obter dados do DOU sem violar proteção anti-bot?"
**Observações:** Site protegido por Azion CDN/WAF. Scraping tradicional resulta em 403 Forbidden. Próximos passos: (1) verificar API oficial em dados.gov.br, (2) verificar feeds RSS oficiais, (3) contato formal com Imprensa Nacional. **NÃO INGERIR até autorização formal ou API oficial identificada.**

---

### SRC-002 — Planalto - Legislação

**Status:** ✅ APROVADO (ALLOW_FULLTEXT — legislação = domínio público)
**Domínio:** planalto.gov.br
**Discovery:** HTML index (https://www.planalto.gov.br/ccivil_03/)
**Robots.txt:** ❌ NOT FOUND (404 — sem restrições explícitas por RFC 9309)
**ToS:** ❌ NÃO LOCALIZADO (ausência de ToS oficial publicado)
**Licença:** ✅ **DOMÍNIO PÚBLICO** (Lei 9.610/1998, Art. 8º, IV: "Não são objeto de proteção como direitos autorais [...] os textos de tratados ou convenções, leis, decretos, regulamentos, decisões judiciais e demais atos oficiais")
**Policy Gate:** **ALLOW_FULLTEXT** (upgrade aprovado com fundamentação legal)
**PII esperado:** Baixo (legislação geralmente não contém PII, mas detecção obrigatória)
**Rate limit:** 0.3 rps (conservador)
**Budget:** 500 URLs/dia, 50 MB/dia
**Onboarding:** T-ONB-SRC-002 (2026-01-30) — COMPLETED com resultado ALLOW_FULLTEXT
**Evidence Pack:** [docs/evidence/T-ONB-SRC-002/](../../docs/evidence/T-ONB-SRC-002/)
**Fundamentação legal:** Lei 9.610/1998, Art. 8º, IV (atos oficiais não têm proteção autoral) + LAI (Lei 12.527/2011)
**Observações:** Legislação federal é de livre acesso e reprodução. Sem robots.txt (404) = sem restrições explícitas. Citação de fonte obrigatória (boa prática + rastreabilidade). **FULLTEXT PERMITIDO** para leis, decretos, regulamentos e atos oficiais.

---

### SRC-003 — IBGE - APIs e Dados

**Status:** ✅ APROVADO (METADATA_ONLY até verificação de licença CC)
**Domínio:** ibge.gov.br / servicodados.ibge.gov.br
**Discovery:** API oficial (https://servicodados.ibge.gov.br/api/docs)
**Robots.txt:** ❌ Indisponível (503) — ver evidence pack
**ToS:** ❌ NÃO LOCALIZADO (não verificado)
**Licença:** ❌ NÃO VERIFICADA (sem evidência oficial)
**Policy Gate:** METADATA_ONLY (fail-closed até evidência de licença)
**PII esperado:** Não
**Rate limit:** 1.0 rps
**Budget:** 2000 URLs/dia, 200 MB/dia
**Observações:** Robots.txt retornou 503 e API root indisponível. Manter METADATA_ONLY até verificação de ToS/licença. Onboarding em T-ONB-SRC-003.

---

### SRC-004 — Banco Central - Dados Abertos

**Status:** ✅ APROVADO (METADATA_ONLY até verificação de licença)
**Domínio:** bcb.gov.br / dadosabertos.bcb.gov.br
**Discovery:** API oficial (https://dadosabertos.bcb.gov.br/dataset)
**Robots.txt:** ✅ 200 OK (dadosabertos) — Disallow: /api/; Crawl-Delay: 10
**ToS:** ✅ Política de Privacidade e Termos de Uso (https://www.bcb.gov.br/acessoinformacao/politicaprivacidade)
**Licença:** ❌ NÃO ESPECIFICADA por dataset (FAQ menciona licença aberta sem detalhar)
**Policy Gate:** METADATA_ONLY (fail-closed)
**PII esperado:** Baixo
**Rate limit:** 0.5 rps
**Budget:** 1000 URLs/dia, 100 MB/dia
**Observações:** Robots restringe /api/ e exige crawl-delay 10s. Licença aberta não explícita por dataset. Onboarding em T-ONB-SRC-004.

---

### SRC-005 — dados.gov.br - Catálogo

**Status:** ✅ APROVADO (METADATA_ONLY — licença variável por dataset)
**Domínio:** dados.gov.br
**Discovery:** API CKAN (https://dados.gov.br/api/3) + catálogo web
**Robots.txt:** ⚠️ Retornou HTML (não regras de robots) — não verificável
**ToS:** ❌ Exige login gov.br (não verificável)
**Licença:** **VARIÁVEL POR DATASET** — cada dataset tem licença própria (CC0, CC-BY, Proprietária, etc.)
**Policy Gate:** METADATA_ONLY (fail-closed; verificar licença POR DATASET antes de fulltext)
**PII esperado:** Médio (datasets podem conter PII)
**Rate limit:** 0.2 rps
**Budget:** 500 URLs/dia, 50 MB/dia
**Observações:** Robots/ToS não verificáveis; licença variável por dataset. Manter METADATA_ONLY até evidência por dataset. Onboarding em T-ONB-SRC-005.

---

## 🔴 Fontes REJEITADAS (BLOCK)

(Nenhuma ainda)

---

## ⏳ Fontes CANDIDATAS (aguardando onboarding)

(Nenhuma ainda; novas ideias vão para Banco de Ideias.md primeiro)

---

## 📋 Processo de Onboarding

1. **Ideia de fonte** → Banco de Ideias.md
2. **Triagem** → PM/LEGAL aprovam candidatura
3. **Onboarding checklist** → Template preenchido em `Onboarding/SRC-XXX.md`
4. **Compliance verificado** → Robots/ToS/Licença com evidência
5. **Policy gate decision** → ALLOW_FULLTEXT | METADATA_ONLY | SNIPPETS_ONLY | BLOCK
6. **Registro duplo:**
   - `configs/sources.yaml` (fonte de verdade operacional)
   - `Fontes_Licencas.md` (este documento, auditável)
7. **Evidence Pack** → `docs/evidence/T-ONB-SRC-XXX/`
8. **Aprovação final** → PM + LEGAL + DPO assinam

---

## 🔄 Revisão e Auditoria

**Frequência de revisão:** Trimestral (ou ao adicionar nova fonte)
**Próxima revisão:** 2026-04-30
**Responsável:** PM (Product Manager)

**Checklist de auditoria:**

- [ ] Robots.txt de todas fontes verificado nos últimos 90 dias?
- [ ] ToS de todas fontes verificado nos últimos 90 dias?
- [ ] Licenças registradas com evidência (screenshots/links)?
- [ ] Policy gate decisions justificadas?
- [ ] PII detection rodando em fontes marcadas como "possível PII"?
- [ ] Rate limits respeitados (verificar logs)?

---

**Mantido por:** PM + LEGAL + DPO
**Última atualização:** 2026-01-31

---
