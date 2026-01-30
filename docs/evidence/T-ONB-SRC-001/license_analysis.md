# T-ONB-SRC-001 — Análise de Compliance DOU

**Data:** 2026-01-30
**Fonte:** SRC-001 (Diário Oficial da União - in.gov.br)
**Status:** ANÁLISE MANUAL (robots.txt fetch bloqueado com 403)

---

## 1. Robots.txt

**Tentativa de fetch:** BLOQUEADO (403 Forbidden)
**URL testada:** https://www.in.gov.br/robots.txt
**IP:** 191.177.194.151
**Edge:** POA (Azion CDN)

**Conclusão:** O site utiliza proteção anti-bot (Azion WAF). Não foi possível obter robots.txt automaticamente.

**Ação:** Fail-closed — manter METADATA_ONLY até verificação manual ou API oficial.

---

## 2. Termos de Uso e Licença

### 2.1 Portal Imprensa Nacional

- **URL base:** https://www.in.gov.br/
- **Natureza:** Portal governamental brasileiro (dados públicos por Lei de Acesso à Informação - LAI nº 12.527/2011)

### 2.2 Legislação aplicável

- **LAI (Lei 12.527/2011):** Garante acesso a informações públicas produzidas ou custodiadas por órgãos públicos
- **Decreto 7.724/2012:** Regulamenta a LAI
- **Marco Civil da Internet (Lei 12.965/2014):** Princípios de abertura e neutralidade

### 2.3 Análise de permissões

**HIPÓTESE (a confirmar):**

- Documentos do DOU são de domínio público (atos oficiais do governo)
- Reprodução permitida com citação de fonte
- Redistribuição comercial pode ter restrições

**EVIDÊNCIA NECESSÁRIA:**

- Página oficial de termos de uso (a localizar)
- Confirmação de licença em página "Sobre" ou "Institucional"
- API oficial (se existir) com termos explícitos

---

## 3. Policy Gate Decision (PROVISÓRIA)

**Decisão:** METADATA_ONLY (fail-closed)

**Justificativa:**

1. Robots.txt inacessível (403 Forbidden) — indica proteção anti-scraping
2. Termos de uso não localizados automaticamente
3. Ausência de API oficial documentada
4. Princípio de precaução (fail-closed)

**Upgrade para ALLOW_FULLTEXT exige:**

- [ ] Confirmação de licença/ToS permitindo scraping ou API oficial
- [ ] Robots.txt verificado (manualmente ou via contato)
- [ ] Autorização explícita ou LAI confirmando domínio público para scraping

---

## 4. Próximos passos

1. **DUV-004:** Abrir dúvida no Backlog: "SRC-001 (DOU) - Como obter dados sem violar proteção anti-bot?"
2. Pesquisar API oficial do DOU (ex.: dados.gov.br, Portal da Transparência)
3. Contato com Imprensa Nacional (se necessário)
4. Revisão em 30 dias ou quando API oficial for identificada

---

## 5. Alternativas identificadas

- **dados.gov.br:** Verificar se DOU está catalogado com API
- **Portal da Transparência:** Possível fonte alternativa
- **RSS feeds oficiais:** Verificar se in.gov.br oferece feeds RSS

---

**Criado por:** ORQ
**Data:** 2026-01-30 23:08 UTC

---
