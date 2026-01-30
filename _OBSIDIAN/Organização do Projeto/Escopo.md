A ideia é **um “pipeline industrial”** de ingestão → limpeza → enriquecimento → indexação → serving, com **governança e compliance como primeira etapa** (senão vira um aspirador de problemas jurídicos e dados tóxicos).

Vou te passar:

1. **Todas as etapas** de um processo _bem completo_ (nível “fábrica”).
    
2. **Todos os robôs (scripts)** que você tipicamente precisa para automatizar isso, com o que cada um faz e como se encaixa na hierarquia.
    



---

## 1) Etapas de um processo extremamente completo

### Fase A — Governança, compliance e escopo (o que entra e o que é proibido)

**Padrão de repositório (DUV-001):** usar **GitHub pessoal (free)** como `owner` do repo. Se não existir, **assumir: a criar**.

1. **Definição de objetivos e “outputs”**
    
    - RAG para busca/respostas, dataset para analytics, produtos SaaS etc.
        
    - Métricas: cobertura por fonte licenciada, frescor, custo por doc, qualidade de extração, latência de busca.
        
2. **Política de fontes (Allowlist)**
    
    - Só coleta de fontes com: domínio público / Creative Commons compatível / dados governamentais abertos / permissão explícita / dados próprios.

    - **Onboarding obrigatório (sem isso, a fonte NÃO entra):**
        - **Fonte de verdade:** cadastrar/atualizar a fonte em `Sources.yaml` (ver “Arquivos & local” abaixo).
        - **Checklist por fonte:** criar um arquivo por fonte a partir de `Template - Source Onboarding Checklist.md` e salvar em `_OBSIDIAN/Organização do Projeto/Sources/<source_id> - <nome>.md`.
        - **Fail-closed:** se houver qualquer dúvida sobre licença/robots/ToS, **bloquear por padrão** (ingere no máximo metadados + URL) e abrir DUV no `Backlog.md`.
        - **Rate/budget por domínio:** definir *crawl_delay/rps/concurrency* e *pages_per_day/bytes_per_day* (evita “acidentalmente virar DDoS”).
        - **Política de armazenamento por licença:** definir se pode armazenar **texto integral**, **apenas trechos**, ou **somente metadados/link**.

    - **Campos mínimos recomendados em `Sources.yaml` (MVP + governança):**
        - `source_id`, `name`, `owner`, `base_url`
        - `license`: `type`, `url`, `storage_policy`
        - `discovery`: `method` (`sitemap|rss|api|manual`), `entrypoints`
        - `scope`: `allowed_paths`, `disallowed_paths`, `content_types`
        - `robots`: `checked_at`, `notes`
        - `rate_limit`: `rps`, `concurrency`, `crawl_delay_s`
        - `budget`: `pages_per_day`, `bytes_per_day`
        - `freshness`: `recrawl_days`
        - `pii_policy`: `detect`, `redact`, `threshold`
        - `review`: `last_reviewed_at`, `reviewer`, `status` (`allowed|blocked|metadata_only`)

    - **Onde ficam os arquivos (padrão Obsidian):**
        - `_OBSIDIAN/Organização do Projeto/Sources.yaml` — catálogo/allowlist (fonte de verdade)
        - `_OBSIDIAN/Organização do Projeto/Template - Source Onboarding Checklist.md` — template
        - `_OBSIDIAN/Organização do Projeto/Sources/` — 1 checklist por fonte (`<source_id> - <nome>.md`)
        - `_OBSIDIAN/Organização do Projeto/DUVs.md` (opcional) — índice de dúvidas abertas com IDs (ex.: `DUV-002`)

        
3. **Registro de licença por fonte**
    
    - Fonte → licença → limitações (armazenar texto integral? só trechos? só metadados/link?).
        
4. **Robots/ToS e regras operacionais por domínio**
    
    - Rate limit, horários, endpoints permitidos, user-agent honesto, contato, exclusões.
        
5. **LGPD-by-design**
    
    - Minimização, classificação de PII, redaction/anonimização, retenção, auditoria.
        
6. **Threat model + segurança**
    
    - Segredos, isolamento, proteção contra conteúdo malicioso (PDFs/HTML).
        

**Saída dessa fase:** um “contrato” de ingestão: _o que pode_, _como pode_, _como prova que pode_.

---

### Fase B — Registro de fontes e descoberta de URLs

7. **Catálogo de fontes (Source Registry)**
    
    - Metadados: domínio, categoria, licença, dono/contato, prioridade.
    - **Fonte de verdade:** `Sources.yaml` (Obsidian) + sincronização/validação no Metadata DB.
        
8. **Descoberta (Discovery)**
    
    - Sitemap.xml, RSS/Atom, APIs oficiais, listagens, repositórios de dados abertos.
        
9. **Geração da “URL Frontier” (fila)**
    
    - Normalização de URL, regras de escopo (paths permitidos), seeds.
        
10. **Planejamento de crawl**
    

- Estratégia: breadth-first, focused crawl por tópico, incremental, backfill.
    

11. **Controle de mudanças**
    

- ETag/Last-Modified, hash do conteúdo, diffs.
    

---

### Fase C — Coleta (fetch/download) com rastreabilidade

12. **Agendamento e rate limiting por domínio**
    

- Token bucket, janelas, limites rígidos.
    

13. **Fetch HTTP**
    

- Respeitando status codes, redirects, timeouts, retries com backoff (sem agressividade).
    

14. **Detecção de tipo de conteúdo**
    

- HTML, PDF, DOCX, imagens, JSON, áudio/vídeo (normalmente _fora_ do escopo).
    

15. **Download e armazenamento bruto (Raw Zone)**
    

- Salvar “raw artifact” + metadados + hash + headers.
    

16. **Observabilidade**
    

- Log estruturado por `run_id`, métricas de sucesso/erro, auditoria.
    

---

### Fase D — Extração de texto (parsing + OCR quando necessário)

17. **Parsing de HTML**
    

- Remover boilerplate (menus/rodapé), extrair conteúdo principal, preservar estrutura.
    

18. **Parsing de PDF**
    

- Extrair texto quando “nativo”.
    

19. **OCR (somente quando necessário)**
    

- Detectar % de páginas sem texto, rasterizar páginas, OCR, guardar evidência.
    

20. **Parsing de outros formatos**
    

- DOCX, TXT, CSV/JSON, etc (se permitido/licenciado).
    

21. **Normalização de encoding e caracteres**
    

- Unicode, hífens, quebras, headers repetidos.
    

---

### Fase E — Limpeza, qualidade e deduplicação

22. **Limpeza semântica**
    

- Remover lixo, duplicações internas, normalizar whitespace.
    

23. **Detecção de idioma**
    
24. **Deduplicação**
    

- Por hash exato, fuzzy hash (simhash/minhash) para quase-duplicados.
    

25. **Validação de qualidade**
    

- Tamanho mínimo, densidade de texto, taxa de erro OCR.
    

26. **Versionamento**
    

- Documento v1/v2 conforme mudanças (útil para histórico e auditoria).
    

---

### Fase F — Compliance Gate e privacidade

27. **Policy Gate (bloqueio/permitir)**
    

- Sem licença registrada → **não entra** (ou entra só como metadado/link).
    

28. **PII detection + redaction**
    

- Identificar e remover/mascarar dados pessoais quando aplicável.
    

29. **Classificação de sensibilidade**
    

- Público, restrito, potencialmente pessoal, proibido.
    

30. **Registro de auditoria**
    

- Por que foi permitido/bloqueado, por qual regra, evidências.
    

---

### Fase G — Enriquecimento e estruturação (opcional, mas poderoso)

31. **Extração de entidades e metadados**
    

- Pessoas/organizações/locais/temas, datas, tags.
    

32. **Classificação por tópicos**
    

- Taxonomia do seu produto.
    

33. **Sumarização técnica**
    

- Gerar “abstract” curto para navegação (sem inventar).
    

34. **Detecção de relacionamentos**
    

- Links, referências cruzadas, citações.
    

35. **Indexação de seções**
    

- Títulos/subtítulos para chunking melhor.
    

---

### Fase H — Chunking para RAG

36. **Segmentação inteligente**
    

- Por headings, parágrafos, páginas, blocos lógicos.
    

37. **Chunk policy**
    

- Tamanho alvo, overlap, “janela” por tipo de documento.
    

38. **Identificadores estáveis**
    

- `doc_id`, `chunk_id` determinísticos.
    

39. **Metadados por chunk**
    

- fonte, url, data, licença, seção, idioma, score de qualidade.
    

---

### Fase I — Embeddings e indexação vetorial

40. **Embedding**
    

- Modelo + versão + parâmetros.
    

41. **Vector index**
    

- pgvector / FAISS / Qdrant etc.
    

42. **Indexação híbrida (recomendado)**
    

- BM25 (texto) + vetores (semântica) + re-ranking.
    

43. **Avaliação de recuperação**
    

- Recall@k, MRR, testes com queries reais.
    

---

### Fase J — Persistência (bancos e “zonas”)

44. **Raw Zone** (artefatos brutos)
    
45. **Processed Zone** (texto extraído/limpo)
    
46. **Curated Zone** (aprovado por policy gate, pronto para RAG)
    
47. **Metadata DB**
    

- fontes, licenças, urls, runs, documentos, chunks, auditoria.
    

48. **Vector DB/Index**
    

- embeddings, parâmetros, links para chunks.
    

49. **Data retention**
    

- prazos de retenção, expiração, deleção verificável.
    

---

### Fase K — Serving (RAG API + produtos SaaS)

50. **RAG Retrieval API**
    

- query → retrieval → contexto → resposta (sempre citando fontes).
    

51. **Camada de autorização**
    

- multi-tenant, planos, rate limits.
    

52. **Produtos SaaS em cima disso**
    

- search vertical, alertas, relatórios, monitoramento de mudanças, etc.
    

53. **Proteções**
    

- bloqueio de prompt injection via conteúdo, filtros, limites de contexto.
    

---

### Fase L — Operação e escala

54. **Scheduler e filas**
    

- prioridades, retries, DLQ (dead letter queue).
    

55. **Monitoramento**
    

- dashboards, alertas (falhas por domínio, spikes de erro, custos).
    

56. **Custo e performance**
    

- amostragem, cache, reprocessamento incremental.
    

57. **Backfill e reindex**
    

- reprocessar com novas regras/modelos.
    

58. **Testes**
    

- unit, integração, E2E, “golden docs”.
    

59. **Runbooks**
    

- “como rodar local”, “como depurar”, “como corrigir fonte X”.
    

60. **Governança de mudanças**
    

- ADRs, versionamento de schemas/configs, migrações.
    

---

## 2) Robôs (scripts) necessários — visão hierárquica completa

Abaixo um “catálogo de robôs” bem completo. Você pode começar com um subconjunto (MVP) e ir plugando mais.

### 2.1 Orquestradores (topo da hierarquia)

1. **`orchestrator_master.py`**
    
    - Ponto de entrada: recebe “fonte(s) + pipeline” e dispara o fluxo.
        
2. **`orchestrator_schedule.py`**
    
    - Agenda runs, decide prioridade, respeita janelas por domínio.
        
3. **`orchestrator_ingest_source.py`**
    
    - Executa ingestão end-to-end de uma fonte (discovery → fetch → process → index).
        
4. **`orchestrator_backfill.py`**
    
    - Reprocessa histórico (mudou chunking/modelo/regras).
        
5. **`orchestrator_reindex.py`**
    
    - Recria índice vetorial/híbrido.
        
6. **`orchestrator_healthcheck.py`**
    
    - Checa integridade (DB, índice, filas, configs).
        
7. **`orchestrator_reporting.py`**
    
    - Gera relatórios de cobertura, custos, erros, compliance.
        
8. **`orchestrator_cleanup_retention.py`**
    
    - Expiração/deleção de dados conforme política.
        

---

### 2.2 Robôs de governança e compliance

9. **`bot_source_registry.py`**
    
    - CRUD de fontes, prioridade, categoria, parâmetros de crawl.
        
10. **`bot_license_registry.py`**
    

- Mantém “licença por fonte” + limites (texto integral / trechos / só metadados).
    

11. **`bot_robots_tos_fetch.py`**
    

- Baixa/atualiza robots.txt e registra regras operacionais.
    

12. **`bot_policy_gate.py`**
    

- Permite/bloqueia ingestão com base em licença/ToS/regras.
    

13. **`bot_pii_detector.py`**
    

- Detecta PII (e flags de risco).
    

14. **`bot_redactor.py`**
    

- Mascara/remove PII conforme regras.
    

15. **`bot_audit_logger.py`**
    

- Emite eventos de auditoria (decisões e evidências).
    

---

### 2.3 Robôs de discovery e frontier

16. **`bot_seed_loader.py`**
    

- Carrega seeds iniciais da fonte.
    

17. **`bot_sitemap_discovery.py`**
    

- Descobre URLs via sitemap(s).
    

18. **`bot_rss_discovery.py`**
    

- Descobre URLs via RSS/Atom.
    

19. **`bot_api_discovery.py`**
    

- Consome APIs públicas oficiais (quando existirem).
    

20. **`bot_url_normalizer.py`**
    

- Normaliza, remove tracking, canonicaliza.
    

21. **`bot_url_filter.py`**
    

- Aplica allow/deny rules (paths, extensões, query params).
    

22. **`bot_frontier_manager.py`**
    

- Mantém a fila: estados, prioridades, dedup de URL.
    

---

### 2.4 Robôs de fetch e armazenamento bruto

23. **`bot_rate_limiter.py`**
    

- Rate limit por domínio.
    

24. **`bot_fetch_http.py`**
    

- GET/HEAD, retries com backoff, captura headers, status.
    

25. **`bot_fetch_validator.py`**
    

- Valida tamanho, tipo MIME, “conteúdo inesperado”.
    

26. **`bot_raw_store.py`**
    

- Salva artefatos brutos (raw zone) + hash.
    

27. **`bot_change_detector.py`**
    

- Usa ETag/Last-Modified/hash pra evitar refetch desnecessário.
    

---

### 2.5 Robôs de parsing e OCR

28. **`bot_type_router.py`**
    

- Roteia por tipo: HTML/PDF/DOCX/IMG/JSON etc.
    

29. **`bot_parse_html.py`**
    

- Extrai conteúdo principal + estrutura.
    

30. **`bot_parse_pdf_text.py`**
    

- Extrai texto nativo de PDF.
    

31. **`bot_ocr_needed_detector.py`**
    

- Decide se precisa OCR (por páginas sem texto).
    

32. **`bot_pdf_to_images.py`**
    

- Renderiza páginas para OCR (com limites de custo/tempo).
    

33. **`bot_ocr.py`**
    

- Executa OCR e retorna texto + confiança.
    

34. **`bot_parse_docx.py`**
    
35. **`bot_parse_text.py`**
    
36. **`bot_parse_json_csv.py`** (se aplicável e permitido)
    

---

### 2.6 Robôs de limpeza, qualidade e dedup

37. **`bot_text_cleaner.py`**
    

- Limpa ruído, normaliza.
    

38. **`bot_language_detector.py`**
    
39. **`bot_quality_scorer.py`**
    

- Score de qualidade (OCR, densidade, completude).
    

40. **`bot_dedup_exact.py`**
    

- Hash exato.
    

41. **`bot_dedup_near.py`**
    

- Simhash/minhash para quase duplicados.
    

42. **`bot_version_manager.py`**
    

- Cria versões e mantém histórico.
    

---

### 2.7 Robôs de enriquecimento

43. **`bot_metadata_extractor.py`**
    

- título, autor, datas, headings, etc.
    

44. **`bot_entity_extractor.py`**
    

- entidades (NER).
    

45. **`bot_topic_classifier.py`**
    

- classifica por taxonomia.
    

46. **`bot_summary_generator.py`**
    

- resumos curtos para navegação (com cautela).
    

47. **`bot_link_graph_builder.py`**
    

- grafo de links e relações.
    

---

### 2.8 Robôs de chunking e preparação RAG

48. **`bot_chunker.py`**
    

- chunking por estrutura + overlap.
    

49. **`bot_chunk_validator.py`**
    

- garante tamanho mínimo/máximo e metadados obrigatórios.
    

50. **`bot_chunk_store.py`**
    

- salva chunks no DB (curated zone).
    

51. **`bot_citation_mapper.py`**
    

- guarda offsets/ancoragem para citação (url + seção + página).
    

---

### 2.9 Robôs de embeddings e indexação

52. **`bot_embedder.py`**
    

- gera embeddings (com versionamento do modelo).
    

53. **`bot_vector_indexer.py`**
    

- indexa no vector store.
    

54. **`bot_text_indexer.py`**
    

- BM25/FTS (híbrido).
    

55. **`bot_reranker.py`** (opcional)
    

- melhora ranking final.
    

56. **`bot_retrieval_evaluator.py`**
    

- métricas offline (recall@k, MRR) com conjunto de testes.
    

---

### 2.10 Robôs de serving (API e produtos)

57. **`bot_rag_api.py`**
    

- endpoint de busca + resposta com citações.
    

58. **`bot_query_router.py`**
    

- decide estratégia: lexical/semântica/híbrida.
    

59. **`bot_tenant_manager.py`**
    

- multi-tenant, quotas, rate limits.
    

60. **`bot_prompt_injection_guard.py`**
    

- proteção contra conteúdo malicioso em contexto.
    

---

### 2.11 Robôs de operação e observabilidade

61. **`bot_run_logger.py`**
    

- logs estruturados por `run_id`.
    

62. **`bot_metrics_emitter.py`**
    

- métricas (sucesso/erro, tempo, custo).
    

63. **`bot_alerting_rules.py`**
    

- regras de alerta (falhas por fonte, explosão de OCR, etc).
    

64. **`bot_dead_letter_handler.py`**
    

- trata falhas persistentes e triagem.
    

65. **`bot_config_validator.py`**
    

- valida YAML/JSON e schemas antes de rodar.
    

66. **`bot_db_migrator.py`**
    

- migrações.
    

67. **`bot_retention_enforcer.py`**
    

- aplica política de retenção/deleção.
    

---

## 3) “MVP realista” (pra não construir um megazord antes do motor)

Se você quiser ser esperto (e economizar meses), o MVP mínimo normalmente é:

- `bot_source_registry.py`
    
- `bot_license_registry.py`
    
- `bot_policy_gate.py`
    
- `bot_sitemap_discovery.py`
    
- `bot_frontier_manager.py`
    
- `bot_fetch_http.py`
    
- `bot_parse_html.py` **ou** `bot_parse_pdf_text.py`
    
- `bot_text_cleaner.py`
    
- `bot_chunker.py`
    
- `bot_embedder.py`
    
- `bot_vector_indexer.py`
    
- `orchestrator_ingest_source.py`
    
- `orchestrator_schedule.py`
    
- - logs/auditoria básicos
        

Depois você adiciona OCR, near-dedup, enriquecimento, re-ranking, etc.

---

## 4) Como os robôs se “conversam” sem virar bagunça

Um padrão que funciona bem:

- Cada bot recebe **um JSON de entrada** (com `run_id`, `source_id`, `url_id`, paths e metadados)
    
- Produz **um JSON de saída** padronizado + salva artefatos em “zonas” (raw/processed/curated)
    
- O orquestrador encadeia bots conforme um **pipeline.yaml**
    

Isso te dá:

- rastreabilidade total,
    
- reprocessamento fácil,
    
- testes por etapa,
    
- e modularidade (trocar OCR, trocou só um bot).
    

---

Se você seguir esse desenho, você acaba com uma “fábrica de conhecimento” modular, auditável e plugável — e não um scraping Frankenstein que funciona até o primeiro e-mail do jurídico de alguém.
