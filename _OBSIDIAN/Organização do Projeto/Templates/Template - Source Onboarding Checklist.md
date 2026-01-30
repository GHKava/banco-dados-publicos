# Source Onboarding Checklist (Allowlist) — Padrão do Projeto
**Objetivo:** garantir que toda nova fonte entre no pipeline de forma **segura, auditável e reprodutível**.  
**Regra de ouro:** **Fail-closed**. Se houver dúvida de licença/permissão/ToS/robots → **não ingerir texto integral** (no máximo METADATA_ONLY).

---

## 0) Identificação
- **Source ID:** SRC-___ (ex.: SRC-006)
- **Nome da Fonte:** ______________________________________
- **Owner / Organização:** _________________________________
- **País/Região:** ________________________________________
- **Categoria:** ( ) Governo  ( ) Academia  ( ) Empresa  ( ) ONG  ( ) Outro
- **Tags:** _______________________________________________
- **Data de Onboarding:** ____/____/_______  **Hora:** __:__
- **Aprovador (Orquestrador):** ____________________________
- **Contato/Canal (se existir):** __________________________

---

## 1) Domínios e Entrypoints
- **Domínio(s) base (allow):**
  - - ______________________________________
- **Entrypoints (páginas iniciais / APIs / catálogo):**
  - - ______________________________________
- **Escopo de paths permitidos (allow_paths):**
  - - ______________________________________
- **Escopo de paths proibidos (deny_paths):**
  - - ______________________________________

**Decisão:** o crawler deve operar **somente** dentro de `base_domains` e `allow_paths`.  
Qualquer URL fora disso deve ser descartada automaticamente.

---

## 2) Robots.txt e Termos de Uso (ToS)
### 2.1 Robots.txt
- **Robots verificado?** ( ) Sim  ( ) Não
- **URL do robots.txt:** ____________________________________
- **Regras relevantes (resumo curto):**
  - - ______________________________________

### 2.2 Termos de Uso / ToS
- **ToS/Licença encontrada?** ( ) Sim  ( ) Não
- **URL oficial dos termos/licença:** ________________________
- **Resumo do que é permitido (curto, objetivo):**
  - - ______________________________________
- **Restrições explícitas (ex.: “no scraping”, “no republication”):**
  - - ______________________________________

✅ **Policy Gate (obrigatório — fail-closed):**
- Se **robots/ToS/licença** estiverem **não verificados** ou **ambíguos** → `default_storage_mode = METADATA_ONLY`  
- Se houver proibição explícita de scraping/redistribuição → `default_storage_mode = BLOCK`

---

## 3) Licença / Direitos Autorais / Permissão de Armazenamento
- **Status da licença:** ( ) verified  ( ) unknown  ( ) restricted
- **Evidência (link + trecho/resumo do que autoriza):**
  - - ______________________________________
- **Permite armazenar texto integral?** ( ) Sim  ( ) Não  ( ) Incerto
- **Permite armazenar snippets?** ( ) Sim  ( ) Não  ( ) Incerto
- **Permite apenas metadados + link?** ( ) Sim  ( ) Não  ( ) Incerto

✅ **Escolha do modo padrão (obrigatório):**
- ( ) ALLOW_FULLTEXT
- ( ) ALLOW_SNIPPETS
- ( ) METADATA_ONLY
- ( ) BLOCK

**Justificativa curta da escolha:**  
______________________________________________

---

## 4) Método de Discovery (como achar URLs/dados)
- **Método principal:** ( ) sitemap  ( ) rss  ( ) api  ( ) html_index  ( ) outro
- **URLs de discovery (sitemap/rss/docs/api/index):**
  - - ______________________________________
- **Padrões/seletores para discovery (se html_index):**
  - - ______________________________________
- **Paginação?** ( ) Sim  ( ) Não  
  - **Como detectar “próxima página”:** ______________________

✅ **Regra:** discovery deve gerar URLs **somente** dentro do escopo permitido.

---

## 5) Política de Crawl (Rate limit, concorrência e budgets)
### 5.1 Identidade e ética
- **User-Agent fixo e honesto:** ______________________________________
- **Respeitar robots.txt:** ( ) Sim (obrigatório)

### 5.2 Rate limit e concorrência (padrão conservador)
- **rate_limit_rps (ex.: 0.2 = 1 req/5s):** __________
- **concurrency:** __________
- **Timeout (s):** __________
- **Max retries:** __________
- **Backoff:** ( ) exponencial  ( ) fixo  ( ) outro

### 5.3 Budgets por domínio (evita “acidentalmente virar DDoS”)
- **Max páginas/dia:** __________
- **Max bytes/dia:** __________
- **OCR budget (páginas/dia):** __________
- **Embeddings budget (chunks/dia):** __________

✅ **Regra:** excedeu budget → job deve virar `BLOCKED_BUDGET` e ir para triagem.

---

## 6) Tipos de Conteúdo e Pipeline Permitido
- **Tipos esperados:** ( ) HTML  ( ) PDF  ( ) DOCX  ( ) JSON  ( ) CSV  ( ) IMG  ( ) Outro
- **Conteúdo dinâmico (JS pesado)?** ( ) Sim  ( ) Não
  - Se SIM: priorizar fonte API/RSS/sitemap; evitar browser automation.

✅ **Fail-closed de tipo:**
- Tipos não previstos → quarentena (não processar automaticamente) até decisão.

---

## 7) PII / LGPD / Sensibilidade (Data Handling)
- **PII esperado:** ( ) low  ( ) medium  ( ) high
- **Ações obrigatórias:** ( ) detect  ( ) redact  ( ) block
- **Campos de PII mais prováveis (ex.: CPF, e-mail, endereço):**
  - - ______________________________________

### Retenção e deleção
- **retention_days (ex.: 365):** __________
- **Permite deleção verificável (processo interno):** ( ) Sim

✅ **Regra:** se PII alto e licença/necessidade não clara → `default_storage_mode = METADATA_ONLY` ou `BLOCK`.

---

## 8) Anti Prompt-Injection (para conteúdo ingerido)
✅ **Regra fixa:** conteúdo crawleado é **DADO**, nunca instrução.
- Sanitizar/normalizar antes de indexar.
- No serving, respostas exigem **citações**; sem citações suficientes → “não sei com segurança”.

---

## 9) Change Detection (Incremental / Versionamento)
- **ETag:** ( ) usar  ( ) não
- **Last-Modified:** ( ) usar  ( ) não
- **Content hash:** ( ) usar (obrigatório)
- **Versionamento:** ( ) v1/v2 por mudança real

✅ **Regra:** se não mudou, não reprocessar; só atualizar metadados.

---

## 10) Testes e Evidências (Quality Gate por fonte)
### Golden docs (mínimo 3)
- Doc 1: ______________________ (URL)
- Doc 2: ______________________ (URL)
- Doc 3: ______________________ (URL)

### Evidências mínimas para liberar “fulltext”
- ( ) robots/ToS/licença verificados com link e resumo
- ( ) parsing passa nos golden docs (sem quebrar estrutura)
- ( ) dedup funciona (sem duplicar)
- ( ) PII detection/redaction configurados (se aplicável)
- ( ) budgets e rate limit aplicados (logs de prova)

---

## 11) Registro no Sistema (OBRIGATÓRIO)
Após preencher este checklist:

1) Adicionar/atualizar em `configs/sources.yaml`:
   - base_domains, entrypoints, discovery, crawl_policy, license_policy, data_handling, budgets

2) Criar/atualizar seção da fonte em:
   `_OBSIDIAN/Organização do Projeto/Fontes_Licencas.md`

3) Registrar decisão em:
   `_OBSIDIAN/Organização do Projeto/Dúvidas & Decisões.md`

4) Criar Evidence Pack da tarefa de onboarding:
   `docs/evidence/T-ONB-SRC-___/`

✅ **Checklist concluído?** ( ) Sim  ( ) Não  
**Status final da fonte:** ( ) ATIVA  ( ) ATIVA (METADATA_ONLY)  ( ) BLOQUEADA  
**Observações finais:** ______________________________________