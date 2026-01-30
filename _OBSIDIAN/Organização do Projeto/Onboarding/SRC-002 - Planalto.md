# Source Onboarding Checklist — SRC-002 (Planalto - Legislação)
**Objetivo:** garantir que toda nova fonte entre no pipeline de forma **segura, auditável e reprodutível**.
**Regra de ouro:** **Fail-closed**. Se houver dúvida de licença/permissão/ToS/robots → **não ingerir texto integral** (no máximo METADATA_ONLY).

---

## 0) Identificação
- **Source ID:** SRC-002
- **Nome da Fonte:** Planalto — Legislação Federal
- **Owner / Organização:** Presidência da República
- **País/Região:** Brasil
- **Categoria:** (x) Governo  ( ) Academia  ( ) Empresa  ( ) ONG  ( ) Outro
- **Tags:** legislação, atos oficiais, normas
- **Data de Onboarding:** 30/01/2026  **Hora:** 20:25
- **Aprovador (Orquestrador):** ORQ
- **Contato/Canal (se existir):** Não identificado

---

## 1) Domínios e Entrypoints
- **Domínio(s) base (allow):**
  - planalto.gov.br
- **Entrypoints (páginas iniciais / APIs / catálogo):**
  - https://www.planalto.gov.br/
  - https://www.planalto.gov.br/ccivil_03/
- **Escopo de paths permitidos (allow_paths):**
  - /ccivil_03/
- **Escopo de paths proibidos (deny_paths):**
  - (nenhum definido)

**Decisão:** o crawler deve operar **somente** dentro de `base_domains` e `allow_paths`.
Qualquer URL fora disso deve ser descartada automaticamente.

---

## 2) Robots.txt e Termos de Uso (ToS)
### 2.1 Robots.txt
- **Robots verificado?** ( ) Sim  (x) Não
- **URL do robots.txt:** https://www.planalto.gov.br/robots.txt
- **Regras relevantes (resumo curto):**
  - Fetch falhou por erro de conexão (ver evidence pack)

### 2.2 Termos de Uso / ToS
- **ToS/Licença encontrada?** ( ) Sim  (x) Não
- **URL oficial dos termos/licença:** Não localizado
- **Resumo do que é permitido (curto, objetivo):** Não confirmado
- **Restrições explícitas (ex.: “no scraping”, “no republication”):** Não identificado

✅ **Policy Gate (obrigatório — fail-closed):**
- Robots/ToS/licença **não verificados** → `default_storage_mode = METADATA_ONLY`

---

## 3) Licença / Direitos Autorais / Permissão de Armazenamento
- **Status da licença:** ( ) verified  (x) unknown  ( ) restricted
- **Evidência (link + trecho/resumo do que autoriza):**
  - Não encontrada nesta rodada
- **Permite armazenar texto integral?** ( ) Sim  ( ) Não  (x) Incerto
- **Permite armazenar snippets?** ( ) Sim  ( ) Não  (x) Incerto
- **Permite apenas metadados + link?** (x) Sim  ( ) Não  ( ) Incerto

✅ **Escolha do modo padrão (obrigatório):**
- ( ) ALLOW_FULLTEXT
- ( ) ALLOW_SNIPPETS
- (x) METADATA_ONLY
- ( ) BLOCK

**Justificativa curta da escolha:**
Sem evidência de robots/ToS/licença e falha de conectividade. Fail-closed aplicado.

---

## 4) Método de Discovery (como achar URLs/dados)
- **Método principal:** ( ) sitemap  ( ) rss  ( ) api  (x) html_index  ( ) outro
- **URLs de discovery (sitemap/rss/docs/api/index):**
  - https://www.planalto.gov.br/ccivil_03/
- **Padrões/seletores para discovery (se html_index):**
  - Links HTML sob /ccivil_03/

---

## 5) Escopo de Conteúdo
- **Tipos de conteúdo esperados:** HTML (textos legais)
- **Exclusões obrigatórias:** Fora de /ccivil_03/
- **Observações:** PII pode aparecer em alguns documentos anexos, manter detecção.

---

## 6) Rate limits e budget
- **Rate limit (rps):** 0.3
- **Concurrency:** 1
- **Crawl delay:** não verificado (robots indisponível)
- **Budget (pages/day):** 500 (provisório)
- **Budget (bytes/day):** 50 MB (provisório)

---

## 7) PII / LGPD
- **PII esperado:** ( ) baixo  (x) médio  ( ) alto
- **Ações obrigatórias:** detectar + redigir

---

## 8) Policy Gate Decision
- **Decisão final:** METADATA_ONLY
- **Motivo:** Robots/ToS/licença não verificados + erro de conexão
- **Revisão necessária:** Sim (repetir fetch robots/ToS)

---

## 9) Evidence Pack
- **Diretório:** docs/evidence/T-ONB-SRC-002/
- **Arquivos presentes:**
  - robots.txt (com erro de fetch)
  - fetch_test.log
  - outputs.log
  - license_analysis.md
  - sample_urls.txt
  - notes.md

---

## 10) Aprovação
- **Status:** ✅ APROVADO PARA METADATA_ONLY
- **Próxima revisão:** Quando conectividade permitir verificação de ToS/licença

---

**Observação final:** Sem evidência de permissão para texto integral, mantém-se fail-closed.
