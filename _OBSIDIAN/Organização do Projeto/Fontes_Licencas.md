# Fontes & Licenças — Registro Auditável

**Data criação:** 2026-01-30  
**Última atualização:** 2026-01-30  
**Mantido por:** PM + LEGAL + DPO

---

## 📋 Visão Geral

Este documento registra TODAS as fontes aprovadas/rejeitadas, incluindo compliance, licenças e decisões de policy gate.

**REGRA:** Nenhuma fonte pode ser ingerida sem entrada neste documento + `configs/sources.yaml`.

---

## 🟢 Fontes APROVADAS (METADATA_ONLY ou ALLOW_FULLTEXT)

### SRC-001 — Diário Oficial da União (DOU) - Imprensa Nacional

**Status:** ✅ APROVADO (METADATA_ONLY até verificação de licença)  
**Domínio:** in.gov.br  
**Discovery:** RSS (https://www.in.gov.br/rss)  
**Robots.txt:** [PENDENTE verificação]  
**ToS:** [PENDENTE verificação formal]  
**Licença:** [PENDENTE — assumir pública, mas confirmar]  
**Policy Gate:** METADATA_ONLY (fail-closed até evidência de licença)  
**PII esperado:** Não  
**Rate limit:** 0.5 rps  
**Budget:** 1000 URLs/dia, 100 MB/dia  
**Observações:** DOU é público por natureza (transparência gov), mas precisamos confirmar ToS e licença específica antes de armazenar fulltext. Onboarding em T-ONB-SRC-001.

---

### SRC-002 — Planalto - Legislação

**Status:** ✅ APROVADO (METADATA_ONLY até verificação de licença)  
**Domínio:** planalto.gov.br  
**Discovery:** Sitemap (https://www.planalto.gov.br/sitemap.xml)  
**Robots.txt:** [PENDENTE verificação]  
**ToS:** [PENDENTE verificação formal]  
**Licença:** [PENDENTE — legislação é pública, mas confirmar termos de redistribuição]  
**Policy Gate:** METADATA_ONLY (fail-closed)  
**PII esperado:** Não  
**Rate limit:** 0.5 rps  
**Budget:** 500 URLs/dia, 50 MB/dia  
**Observações:** Legislação federal pública. Confirmar ToS antes de fulltext. Onboarding em T-ONB-SRC-002.

---

### SRC-003 — IBGE - APIs e Dados

**Status:** ✅ APROVADO (METADATA_ONLY até verificação de licença CC)  
**Domínio:** ibge.gov.br / servicodados.ibge.gov.br  
**Discovery:** API oficial (https://servicodados.ibge.gov.br/api/docs)  
**Robots.txt:** [PENDENTE verificação]  
**ToS:** [PENDENTE — verificar termos de uso de APIs]  
**Licença:** [PENDENTE — IBGE frequentemente usa CC-BY; confirmar]  
**Policy Gate:** METADATA_ONLY (fail-closed até evidência CC-BY ou similar)  
**PII esperado:** Não  
**Rate limit:** 1.0 rps  
**Budget:** 2000 URLs/dia, 200 MB/dia  
**Observações:** IBGE APIs públicas, mas precisamos confirmar licença CC-BY explícita. Se confirmado, upgrade para ALLOW_FULLTEXT. Onboarding em T-ONB-SRC-003.

---

### SRC-004 — Banco Central - Dados Abertos

**Status:** ✅ APROVADO (METADATA_ONLY até verificação de licença)  
**Domínio:** bcb.gov.br / dadosabertos.bcb.gov.br  
**Discovery:** API oficial (https://dadosabertos.bcb.gov.br/dataset)  
**Robots.txt:** [PENDENTE verificação]  
**ToS:** [PENDENTE — verificar termos "dados abertos"]  
**Licença:** [PENDENTE — BCB frequentemente libera dados abertos; confirmar licença]  
**Policy Gate:** METADATA_ONLY (fail-closed)  
**PII esperado:** Não  
**Rate limit:** 0.5 rps  
**Budget:** 1000 URLs/dia, 100 MB/dia  
**Observações:** Dados abertos BCB. Confirmar licença explícita (CC-BY ou LAI). Onboarding em T-ONB-SRC-004.

---

### SRC-005 — dados.gov.br - Catálogo

**Status:** ✅ APROVADO (METADATA_ONLY — licença variável por dataset)  
**Domínio:** dados.gov.br  
**Discovery:** API CKAN (https://dados.gov.br/api/3)  
**Robots.txt:** [PENDENTE verificação]  
**ToS:** [PENDENTE — verificar termos gerais do portal]  
**Licença:** **VARIÁVEL POR DATASET** — cada dataset tem licença própria (CC0, CC-BY, Proprietária, etc.)  
**Policy Gate:** METADATA_ONLY (fail-closed; verificar licença POR DATASET antes de fulltext)  
**PII esperado:** POSSÍVEL (alguns datasets podem conter PII; detector obrigatório)  
**Rate limit:** 0.5 rps  
**Budget:** 500 URLs/dia, 50 MB/dia  
**Observações:** Catálogo misto; precisamos verificar licença individualmente por dataset. PII detection obrigatória. Onboarding em T-ONB-SRC-005.

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
**Última atualização:** 2026-01-30

---
