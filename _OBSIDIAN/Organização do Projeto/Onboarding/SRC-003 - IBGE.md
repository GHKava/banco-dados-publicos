# Source Onboarding Checklist — SRC-003 (IBGE APIs)

**Objetivo:** garantir que toda nova fonte entre no pipeline de forma **segura, auditável e reprodutível**.
**Regra de ouro:** **Fail-closed**. Se houver dúvida de licença/permissão/ToS/robots → **não ingerir texto integral** (no máximo METADATA_ONLY).

---

## 0) Identificação

- **Source ID:** SRC-003
- **Nome da Fonte:** IBGE — APIs e Dados
- **Owner / Organização:** IBGE
- **País/Região:** Brasil
- **Categoria:** (x) Governo ( ) Academia ( ) Empresa ( ) ONG ( ) Outro
- **Tags:** dados, estatísticas, APIs
- **Data de Onboarding:** 31/01/2026 **Hora:** 00:20
- **Aprovador (Orquestrador):** ORQ
- **Contato/Canal (se existir):** Não identificado

---

## 1) Domínios e Entrypoints

- **Domínio(s) base (allow):**
  - ibge.gov.br
  - servicodados.ibge.gov.br
- **Entrypoints (páginas iniciais / APIs / catálogo):**
  - https://servicodados.ibge.gov.br/api/docs
- **Escopo de paths permitidos (allow_paths):**
  - /api/
- **Escopo de paths proibidos (deny_paths):**
  - (nenhum definido)

**Decisão:** o crawler deve operar **somente** dentro de `base_domains` e `allow_paths`.
Qualquer URL fora disso deve ser descartada automaticamente.

---

## 2) Robots.txt e Termos de Uso (ToS)

### 2.1 Robots.txt

- **Robots verificado?** ( ) Sim (x) Não
- **URL do robots.txt:** https://servicodados.ibge.gov.br/robots.txt
- **Regras relevantes (resumo curto):**
  - Fetch retornou 503 (indisponível)

### 2.2 Termos de Uso / ToS

- **ToS/Licença encontrada?** ( ) Sim (x) Não
- **URL oficial dos termos/licença:** Não localizado
- **Resumo do que é permitido (curto, objetivo):** Não confirmado
- **Restrições explícitas (ex.: “no scraping”, “no republication”):** Não identificado

✅ **Policy Gate (obrigatório — fail-closed):**

- Robots/ToS/licença **não verificados** → `default_storage_mode = METADATA_ONLY`

---

## 3) Licença / Direitos Autorais / Permissão de Armazenamento

- **Status da licença:** ( ) verified (x) unknown ( ) restricted
- **Evidência (link + trecho/resumo do que autoriza):**
  - Não encontrada nesta rodada
- **Permite armazenar texto integral?** ( ) Sim ( ) Não (x) Incerto
- **Permite armazenar snippets?** ( ) Sim ( ) Não (x) Incerto
- **Permite apenas metadados + link?** (x) Sim ( ) Não ( ) Incerto

✅ **Escolha do modo padrão (obrigatório):**

- ( ) ALLOW_FULLTEXT
- ( ) ALLOW_SNIPPETS
- (x) METADATA_ONLY
- ( ) BLOCK

**Justificativa curta da escolha:**
Robots.txt indisponível (503) e ToS/licença não verificados.

---

## 4) Método de Discovery (como achar URLs/dados)

- **Método principal:** ( ) sitemap ( ) rss (x) api ( ) html_index ( ) outro
- **URLs de discovery (sitemap/rss/docs/api/index):**
  - https://servicodados.ibge.gov.br/api/docs
- **Padrões/seletores para discovery (se html_index):**
  - N/A (API)

---

## 5) Escopo de Conteúdo

- **Tipos de conteúdo esperados:** JSON (APIs)
- **Exclusões obrigatórias:** Fora de /api/
- **Observações:** APIs podem ter limites e termos específicos.

---

## 6) Rate limits e budget

- **Rate limit (rps):** 1.0
- **Concurrency:** 2
- **Crawl delay:** não verificado (robots indisponível)
- **Budget (pages/day):** 2000 (provisório)
- **Budget (bytes/day):** 200 MB (provisório)

---

## 7) PII / LGPD

- **PII esperado:** (x) baixo ( ) médio ( ) alto
- **Ações obrigatórias:** detectar

---

## 8) Policy Gate Decision

- **Decisão final:** METADATA_ONLY
- **Motivo:** Robots/ToS/licença não verificados + API root 503
- **Revisão necessária:** Sim

---

## 9) Evidence Pack

- **Diretório:** docs/evidence/T-ONB-SRC-003/
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
- **Próxima revisão:** Quando robots/ToS/licença estiverem acessíveis

---

**Observação final:** Sem evidência de permissão para fulltext, manter fail-closed.
