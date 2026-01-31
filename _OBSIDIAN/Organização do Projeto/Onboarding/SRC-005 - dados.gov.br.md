# Source Onboarding Checklist — SRC-005 (dados.gov.br)

**Objetivo:** garantir que toda nova fonte entre no pipeline de forma **segura, auditável e reprodutível**.
**Regra de ouro:** **Fail-closed**. Se houver dúvida de licença/permissão/ToS/robots → **não ingerir texto integral** (no máximo METADATA_ONLY).

---

## 0) Identificação

- **Source ID:** SRC-005
- **Nome da Fonte:** dados.gov.br — Catálogo de Dados Abertos
- **Owner / Organização:** Governo Federal
- **País/Região:** Brasil
- **Categoria:** (x) Governo ( ) Academia ( ) Empresa ( ) ONG ( ) Outro
- **Tags:** catálogo, ckan, dados abertos
- **Data de Onboarding:** 31/01/2026 **Hora:** 01:00
- **Aprovador (Orquestrador):** ORQ
- **Contato/Canal (se existir):** https://dados.gov.br/faq

---

## 1) Domínios e Entrypoints

- **Domínio(s) base (allow):**
  - dados.gov.br
- **Entrypoints (páginas iniciais / APIs / catálogo):**
  - https://dados.gov.br/
  - https://dados.gov.br/dados/conjuntos-dados
- **Escopo de paths permitidos (allow_paths):**
  - /dados/
- **Escopo de paths proibidos (deny_paths):**
  - (nenhum definido)

**Decisão:** o crawler deve operar **somente** dentro de `base_domains` e `allow_paths`.
Qualquer URL fora disso deve ser descartada automaticamente.

---

## 2) Robots.txt e Termos de Uso (ToS)

### 2.1 Robots.txt

- **Robots verificado?** ( ) Sim (x) Não
- **URL do robots.txt:** https://dados.gov.br/robots.txt
- **Regras relevantes (resumo curto):**
  - Conteúdo retornou HTML do portal (não regras de robots)

### 2.2 Termos de Uso / ToS

- **ToS/Licença encontrada?** ( ) Sim (x) Não
- **URL oficial dos termos/licença:** https://dados.gov.br/termos-de-uso
- **Resumo do que é permitido (curto, objetivo):** Não confirmado (login requerido)
- **Restrições explícitas (ex.: “no scraping”, “no republication”):** Não identificado

✅ **Policy Gate (obrigatório — fail-closed):**

- Robots/ToS/licença **não verificados** → `default_storage_mode = METADATA_ONLY`

---

## 3) Licença / Direitos Autorais / Permissão de Armazenamento

- **Status da licença:** ( ) verified (x) unknown ( ) restricted
- **Evidência (link + trecho/resumo do que autoriza):**
  - Não encontrada nesta rodada (login gov.br exigido)
- **Permite armazenar texto integral?** ( ) Sim ( ) Não (x) Incerto
- **Permite armazenar snippets?** ( ) Sim ( ) Não (x) Incerto
- **Permite apenas metadados + link?** (x) Sim ( ) Não ( ) Incerto

✅ **Escolha do modo padrão (obrigatório):**

- ( ) ALLOW_FULLTEXT
- ( ) ALLOW_SNIPPETS
- (x) METADATA_ONLY
- ( ) BLOCK

**Justificativa curta da escolha:**
Licença por dataset não verificada e ToS inacessível sem login.

---

## 4) Método de Discovery (como achar URLs/dados)

- **Método principal:** ( ) sitemap ( ) rss (x) api (x) html_index ( ) outro
- **URLs de discovery (sitemap/rss/docs/api/index):**
  - https://dados.gov.br/dados/conjuntos-dados
  - https://dados.gov.br/api/3
- **Padrões/seletores para discovery (se html_index):**
  - Links de conjuntos sob /dados/conjuntos-dados

---

## 5) Escopo de Conteúdo

- **Tipos de conteúdo esperados:** HTML, JSON (API CKAN)
- **Exclusões obrigatórias:** Nenhuma definida (aguardar robots válido)
- **Observações:** Licença varia por dataset

---

## 6) Rate limits e budget

- **Rate limit (rps):** 0.2
- **Concurrency:** 1
- **Crawl delay:** não verificado (robots inválido)
- **Budget (pages/day):** 500 (provisório)
- **Budget (bytes/day):** 50 MB (provisório)

---

## 7) PII / LGPD

- **PII esperado:** ( ) baixo (x) médio ( ) alto
- **Ações obrigatórias:** detectar + redigir

---

## 8) Policy Gate Decision

- **Decisão final:** METADATA_ONLY
- **Motivo:** robots/ToS/licença não verificáveis + licenças variáveis por dataset
- **Revisão necessária:** Sim (licença por dataset)

---

## 9) Evidence Pack

- **Diretório:** docs/evidence/T-ONB-SRC-005/
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
- **Próxima revisão:** Quando ToS/licença estiverem acessíveis

---

**Observação final:** Sem evidência de licença, manter fail-closed.
