# Source Onboarding Checklist — SRC-004 (BCB Dados Abertos)

**Objetivo:** garantir que toda nova fonte entre no pipeline de forma **segura, auditável e reprodutível**.
**Regra de ouro:** **Fail-closed**. Se houver dúvida de licença/permissão/ToS/robots → **não ingerir texto integral** (no máximo METADATA_ONLY).

---

## 0) Identificação

- **Source ID:** SRC-004
- **Nome da Fonte:** Banco Central do Brasil — Dados Abertos
- **Owner / Organização:** Banco Central do Brasil (BCB)
- **País/Região:** Brasil
- **Categoria:** (x) Governo ( ) Academia ( ) Empresa ( ) ONG ( ) Outro
- **Tags:** dados abertos, finanças, estatísticas
- **Data de Onboarding:** 31/01/2026 **Hora:** 00:45
- **Aprovador (Orquestrador):** ORQ
- **Contato/Canal (se existir):** https://www.bcb.gov.br/acessoinformacao/faleconosco

---

## 1) Domínios e Entrypoints

- **Domínio(s) base (allow):**
  - dadosabertos.bcb.gov.br
  - bcb.gov.br
- **Entrypoints (páginas iniciais / APIs / catálogo):**
  - https://dadosabertos.bcb.gov.br/
- **Escopo de paths permitidos (allow_paths):**
  - /
- **Escopo de paths proibidos (deny_paths):**
  - /api/ (robots.txt)

**Decisão:** o crawler deve operar **somente** dentro de `base_domains` e `allow_paths`.
Qualquer URL fora disso deve ser descartada automaticamente.

---

## 2) Robots.txt e Termos de Uso (ToS)

### 2.1 Robots.txt

- **Robots verificado?** (x) Sim ( ) Não
- **URL do robots.txt:** https://dadosabertos.bcb.gov.br/robots.txt
- **Regras relevantes (resumo curto):**
  - Disallow: /api/
  - Crawl-Delay: 10

### 2.2 Termos de Uso / ToS

- **ToS/Licença encontrada?** (x) Sim ( ) Não
- **URL oficial dos termos/licença:** https://www.bcb.gov.br/acessoinformacao/politicaprivacidade
- **Resumo do que é permitido (curto, objetivo):** Reprodução do conteúdo do site com citação da fonte
- **Restrições explícitas (ex.: “no scraping”, “no republication”):** Não explícitas para o portal de dados

✅ **Policy Gate (obrigatório — fail-closed):**

- Licença de dados não especificada → `default_storage_mode = METADATA_ONLY`

---

## 3) Licença / Direitos Autorais / Permissão de Armazenamento

- **Status da licença:** ( ) verified (x) unknown ( ) restricted
- **Evidência (link + trecho/resumo do que autoriza):**
  - Política de Privacidade/Termos do BC permite reprodução com citação
  - FAQ menciona licença aberta, mas não especifica qual
- **Permite armazenar texto integral?** ( ) Sim ( ) Não (x) Incerto
- **Permite armazenar snippets?** ( ) Sim ( ) Não (x) Incerto
- **Permite apenas metadados + link?** (x) Sim ( ) Não ( ) Incerto

✅ **Escolha do modo padrão (obrigatório):**

- ( ) ALLOW_FULLTEXT
- ( ) ALLOW_SNIPPETS
- (x) METADATA_ONLY
- ( ) BLOCK

**Justificativa curta da escolha:**
Licença de dados não explícita por dataset + restrições em robots.txt.

---

## 4) Método de Discovery (como achar URLs/dados)

- **Método principal:** ( ) sitemap ( ) rss ( ) api (x) html_index ( ) outro
- **URLs de discovery (sitemap/rss/docs/api/index):**
  - https://dadosabertos.bcb.gov.br/
- **Padrões/seletores para discovery (se html_index):**
  - Links de dataset (/dataset/)

---

## 5) Escopo de Conteúdo

- **Tipos de conteúdo esperados:** HTML, JSON/CSV (via datasets)
- **Exclusões obrigatórias:** /api/ (robots)
- **Observações:** Priorizar datasets com licença explícita quando disponível.

---

## 6) Rate limits e budget

- **Rate limit (rps):** 0.5
- **Concurrency:** 2
- **Crawl delay:** 10s (robots.txt)
- **Budget (pages/day):** 1000 (provisório)
- **Budget (bytes/day):** 100 MB (provisório)

---

## 7) PII / LGPD

- **PII esperado:** (x) baixo ( ) médio ( ) alto
- **Ações obrigatórias:** detectar

---

## 8) Policy Gate Decision

- **Decisão final:** METADATA_ONLY
- **Motivo:** Licença aberta não especificada por dataset + robots com restrições
- **Revisão necessária:** Sim (licença por dataset)

---

## 9) Evidence Pack

- **Diretório:** docs/evidence/T-ONB-SRC-004/
- **Arquivos presentes:**
  - robots.txt
  - outputs.log
  - fetch_test.log
  - license_analysis.md
  - sample_urls.txt
  - notes.md

---

## 10) Aprovação

- **Status:** ✅ APROVADO PARA METADATA_ONLY
- **Próxima revisão:** Quando licença explícita por dataset estiver disponível

---

**Observação final:** Respeitar robots e manter fail-closed.
