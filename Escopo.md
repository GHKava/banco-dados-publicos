# Escopo — Banco de Dados Interrelacional de Dados Públicos (Pipeline Industrial + RAG)
**Versão:** v2.0 (estado-da-arte, modular, local-first)  
**Plataforma alvo:** Windows + VSCode + Git + GitHub + (opcional) Docker  
**Princípios inegociáveis:** Compliance-first, modularidade real, rastreabilidade, reprodutibilidade, anti-alucinação (evidência)

---

## 0) Ideia central (resumo executivo)
Construir um **pipeline industrial** de ingestão → limpeza → enriquecimento → indexação → serving, com **governança e compliance como primeira etapa** (senão vira um aspirador de problemas jurídicos e dados tóxicos).

> Nota de realidade (importante): “pegar o máximo possível de informação pública” só é viável **dentro de limites**: robots.txt, ToS, rate limits, licenças/direitos autorais, e privacidade/LGPD. Um pipeline sério tem um **Policy Gate** que bloqueia ingestão sem permissão/licença registradas e **não** faz bypass de paywall/CAPTCHA/bloqueios.

---

## 1) Objetivos e não-objetivos

### 1.1 Objetivos
1. Coletar dados públicos **somente** de fontes permitidas/licenciadas.
2. Extrair texto e estrutura (HTML/PDF/DOCX/TXT/CSV/JSON permitidos), com OCR **apenas quando necessário**.
3. Normalizar, deduplicar e versionar documentos.
4. Aplicar LGPD-by-design (PII detection/redaction, retenção, auditoria).
5. Produzir **chunks estáveis** e embeddings para **RAG** e buscas.
6. Disponibilizar uma **API de retrieval (RAG Retrieval API)** e base para produtos SaaS (search vertical, alertas, relatórios, monitoramento de mudanças etc.).
7. Operar com observabilidade (logs/metrics), retries, DLQ e reprocessamento incremental.

### 1.2 Não-objetivos (proibido / fora de escopo)
- “RAG que inventa”: respostas sem citações/grounding.

---

## 2) Decisões técnicas principais (MVP)
### 2.1 Banco de dados e vetores (recomendação)
- **PostgreSQL + pgvector** como padrão do MVP:
  - Metadados relacionais + vetores no mesmo lugar (consistência, auditoria, joins).
  - Busca híbrida: Postgres FTS (tsvector/BM25-like) + pgvector (semântica).
- **MongoDB Vector Search** só faz sentido se:
  - o sistema for “document-first” por decisão estratégica, e
  - a operação estiver ancorada em Atlas (aceitando custo/lock-in).

### 2.2 IA paga como “segunda opção”
- Tudo que for possível deve ser feito com **bibliotecas Python local-first**.
- LLM/API paga entra como **fallback**, somente quando:
  - heurísticas/regex/NER local não resolverem,
  - ou para “resumos de vitrine” sob demanda,
  - sempre com registro de custo, justificativa e evidência.

---

## 3) Princípios de arquitetura (modularidade real + baixo custo + controle)

### 3.1 Controle-plane vs Data-plane
- **Orquestrador (Control Plane):** coordena jobs, estados, dependências, retries, DLQ, budgets, observabilidade, e atualização do projeto (Obsidian).
- **Robôs/Bots (Data Plane):** executam tarefas atômicas e independentes (fetch, parse, OCR, dedup, chunk, embed etc.).

### 3.2 Contrato obrigatório de entrada/saída (I/O) para TODO robô
Cada robô deve funcionar como **CLI** e seguir um contrato padrão:
- **Entrada:** `JobSpec.json` (via arquivo ou stdin)
- **Saída:** `Result.json` + artefatos em zonas (`raw/processed/curated`)
- Campos mínimos no JobSpec/Result:
  - `run_id`, `task_id`, `source_id`, `job_id`, `attempt`, `inputs[]`, `outputs[]`,
  - `metrics{}`, `errors[]`, `evidence_paths[]`, `policy_decision` (quando aplicável),
  - `files_changed` (para auditoria e “claim-check”).
- **Idempotência obrigatória:** reexecutar um robô não pode duplicar nem corromper dados.
- **Dry-run obrigatório:** estimar impacto/custo sem gravar.

### 3.3 “Evidência ou não aconteceu” (anti-alucinação operacional)
Para cada tarefa técnica do roadmap e/ou job do pipeline:
- Criar **Evidence Pack** em: `docs/evidence/<TASK_ID>/`
  - `commands.log`, `outputs.log`, `tests.log`, `files_changed.json`, `notes.md`
- Regra: **não marcar DONE** sem evidência mínima (teste, lint, comando, build, ou justificativa formal de “não executável aqui” → status VERIFYING).

### 3.4 Organização por “Zonas”
- **Raw Zone:** bytes brutos + headers + hash (e opcionalmente WARC).
- **Processed Zone:** texto extraído, limpo, com métricas de qualidade e OCR.
- **Curated Zone:** somente conteúdo aprovado por policy gate (pronto para RAG).

---

## 4) Ideias campeãs incorporadas (robustez real, custo baixo, modular)
Estas regras/funcionalidades são parte do escopo “estado da arte” e devem ser implementadas:

1) **Fila e execução desacopladas**
- Usar Redis + `rq` (simples) ou `dramatiq` (robusto) para jobs.
- Workers por tipo de robô (fetchers, parsers, ocr, embedders).

2) **Manifesto de artefatos por run (reprodutibilidade)**
- Manifest por `run_id` registrando: inputs, outputs, hashes, decisões de policy.
- **WARC opcional** para capturar HTTP raw (headers+body) quando fizer sentido (auditoria/replay).

3) **Content safety fail-closed**
- Limites rígidos: tamanho, tempo, páginas máximas, tipos permitidos.
- PDFs suspeitos/over-sized → bloquear/quarentenar, nunca “forçar”.

4) **Dedup em dois níveis**
- Dedup de URL canonical + dedup por hash de conteúdo + near-dup (MinHash/SimHash).

5) **Cache agressivo + detecção de mudanças**
- ETag/Last-Modified + hash do corpo.
- Evitar refetch desnecessário.

6) **Observabilidade local barata**
- Logs estruturados (JSON) por `run_id`, métricas por etapa e por domínio.
- Viewer simples local (dash mínimo). Prometheus/Grafana só quando crescer.

7) **Store less por padrão**
- Se licença for restritiva/duvidosa: armazenar somente metadados/link/snippets (conforme policy).

8) **Embeddings locais + cache**
- `sentence-transformers` local-first.
- Cache por hash do texto/chunk (reuso e custo zero).

9) **Índice híbrido real**
- Postgres FTS (tsvector) + pgvector.
- Score combinado + re-ranking opcional (prioridade: local).

---

## 5) Stack recomendada (MVP) — “funciona hoje, escala amanhã”
### 5.1 Core
- Python 3.11+
- FastAPI (serving)
- PostgreSQL + pgvector
- Redis + rq (ou dramatiq)
- Docker (opcional, recomendado para Postgres/Redis)

### 5.2 Bibliotecas por etapa (prioridade local-first)
**Discovery / Frontier**
- `scrapy`, `w3lib`, `urllib.robotparser` (ou `robotexclusionrulesparser`), `feedparser`, `lxml`, `xmltodict`, `tenacity`, `aiolimiter`

**Fetch / Raw**
- `httpx` (ou `aiohttp`), `certifi`, `python-magic`/`filetype`, `blake3`/`xxhash`, `fsspec`, `pathlib`

**Parsing / Extração**
- HTML: `trafilatura`, `readability-lxml`, `beautifulsoup4`, `lxml`
- PDF: `pymupdf`, `pdfminer.six` (fallback), `pypdf`
- DOCX: `python-docx`
- Tabelas: `pandas`, `pyarrow`, `camelot`/`tabula-py` (quando aplicável)

**OCR (somente quando necessário)**
- `pytesseract` + Tesseract instalado
- `opencv-python`, `Pillow`
- (opcional, mais pesado) `docTR`

**Dedup / Qualidade / Normalização**
- `datasketch`, `simhash`, `ftfy`, `regex`, `unidecode`
- Idioma: `fasttext` (preferido) ou `langdetect`

**LGPD / PII**
- `presidio-analyzer`, `presidio-anonymizer`
- `phonenumbers`, `email-validator` + regex auditáveis CPF/CNPJ

**Chunking / Embeddings**
- Chunker determinístico próprio (tamanho/overlap por tipo)
- `sentence-transformers`
- `diskcache` (cache local) + tabelas no Postgres (hash→embedding)

---

## 6) Etapas de um processo extremamente completo (nível “fábrica”)

### Fase A — Governança, compliance e escopo (o que entra e o que é proibido)
1. Definir objetivos e outputs (RAG, analytics, SaaS).
2. Política de fontes (Allowlist).
3. Registro de licença por fonte (o que pode armazenar).
4. Robots/ToS e regras operacionais por domínio (rate, horários, paths).
5. LGPD-by-design (minimização, PII, retenção).
6. Threat model + segurança (PDF/HTML malicioso, isolamento, segredos).
**Saída:** contrato de ingestão (permitido/proibido + prova).

### Fase B — Registro de fontes e descoberta de URLs
7. Catálogo de fontes (Source Registry).
8. Discovery (sitemap, RSS, APIs, listagens).
9. URL Frontier (normalização, canonicalização, escopo por paths).
10. Planejamento de crawl (breadth/focused/incremental/backfill).
11. Controle de mudanças (ETag/Last-Modified/hash).

### Fase C — Coleta (fetch/download) com rastreabilidade
12. Agendamento + rate limit por domínio (token bucket).
13. Fetch HTTP (timeouts, retries com backoff “educado”).
14. Detecção de tipo (HTML/PDF/DOCX/IMG/JSON…).
15. Armazenamento bruto (Raw Zone) + hash + headers (WARC opcional).
16. Observabilidade (logs estruturados, métricas por run_id).

### Fase D — Extração de texto (parsing + OCR quando necessário)
17. Parsing HTML (remover boilerplate, preservar estrutura).
18. Parsing PDF (texto nativo quando existir).
19. OCR (somente quando necessário): detectar necessidade, rasterizar com limites, OCR, guardar evidência.
20. Parsing outros formatos permitidos.
21. Normalização de encoding e caracteres.

### Fase E — Limpeza, qualidade e deduplicação
22. Limpeza semântica e normalização.
23. Detecção de idioma.
24. Dedup exato + near-dup.
25. Validação de qualidade (densidade, tamanho, taxa erro OCR).
26. Versionamento (v1/v2... por mudança real).

### Fase F — Compliance Gate e privacidade
27. Policy Gate (ALLOW/BLOCK/METADATA_ONLY/SNIPPETS_ONLY).
28. PII detection + redaction (quando aplicável).
29. Classificação de sensibilidade (público/restrito/pessoal/proibido).
30. Registro de auditoria (regra + evidência).

### Fase G — Enriquecimento e estruturação (opcional, poderoso)
31. Extração de metadados e entidades (local-first).
32. Classificação por tópicos (local-first).
33. Sumarização técnica curta (preferência local; LLM só fallback).
34. Detecção de relacionamentos (links, referências).
35. Indexação de seções (melhora chunking).

### Fase H — Chunking para RAG
36. Segmentação (headings/parágrafos/páginas/blocos).
37. Chunk policy por tipo (tamanho/overlap).
38. IDs estáveis (`doc_id`, `chunk_id`) determinísticos.
39. Metadados por chunk (fonte, licença, seção, idioma, qualidade, citações/âncoras).

### Fase I — Embeddings e indexação vetorial
40. Embedding local-first (modelo+versão+parâmetros).
41. Vector index (MVP: pgvector; futuro: Qdrant/FAISS se necessário).
42. Indexação híbrida (FTS + vetor) + re-ranking opcional.
43. Avaliação de retrieval (Recall@k, MRR, queries reais; golden set).

### Fase J — Persistência (bancos e zonas)
44. Raw Zone (artefatos brutos).
45. Processed Zone (texto extraído/limpo).
46. Curated Zone (aprovado pelo Policy Gate).
47. **Metadata DB (Postgres)**: fontes, licenças, urls, runs, docs, chunks, auditoria, métricas.
48. **Vector store (Postgres + pgvector)**: embeddings, parâmetros, vínculos a chunks.
49. Retenção e deleção verificável (políticas por fonte/sensibilidade).

### Fase K — Serving (RAG API + produtos SaaS)
50. Retrieval API (sempre com citações/grounding).
51. Autorização (multi-tenant, planos, rate limits).
52. Produtos SaaS (search vertical, alertas, relatórios, monitoramento mudanças).
53. Proteções (anti prompt-injection, limites de contexto, filtros).

### Fase L — Operação e escala
54. Scheduler/filas (prioridades, retries, DLQ).
55. Monitoramento (dashboards, alertas por domínio/custos/erros).
56. Custo e performance (amostragem, cache, incremental).
57. Backfill e reindex (reprocessar com novas regras/modelos).
58. Testes (unit, integração, E2E, golden docs).
59. Runbooks (rodar local, depurar, corrigir fonte X).
60. Governança de mudanças (ADRs, schemas/configs versionados, migrações).

---

## 7) Robôs (scripts) necessários — visão hierárquica (atualizada)
> Regra: cada robô é um CLI isolado com JobSpec/Result, idempotente, com evidência.

### 7.1 Orquestradores (control plane)
- `orchestrator_master.py` — loop principal (fila, estados, budgets, DLQ, evidências)
- `orchestrator_ingest.py` — ingestão incremental
- `orchestrator_backfill.py` — backfill histórico
- `orchestrator_reindex.py` — reprocessamento e reindex
- `orchestrator_healthcheck.py` — checagens e alertas
- `orchestrator_cost_guard.py` — enforce budgets (OCR/embedding/dominio)
- `orchestrator_obsidian_sync.py` — atualiza docs do projeto (roadmap/backlog/evidências)

### 7.2 Robôs de fontes e compliance
- `bot_source_registry.py` — catálogo de fontes + regras
- `bot_license_registry.py` — registro de licença/limitações por fonte
- `bot_robots_checker.py` — robots/ToS + allow/deny por paths
- `bot_policy_gate.py` — decisão ALLOW/BLOCK/METADATA_ONLY/SNIPPETS_ONLY + auditoria

### 7.3 Robôs de discovery/frontier
- `bot_discovery_sitemap.py`
- `bot_discovery_rss.py`
- `bot_discovery_api.py`
- `bot_url_normalizer.py`
- `bot_frontier_scheduler.py` — gera jobs respeitando rate/budget

### 7.4 Robôs de fetch/raw
- `bot_fetch_http.py`
- `bot_fetch_validator.py` — tamanho/MIME/conteúdo inesperado
- `bot_change_detector.py` — ETag/Last-Modified/hash
- `bot_raw_store.py` — raw + headers + hash
- `bot_warc_writer.py` (opcional) — WARC por fonte/run
- `bot_content_safety.py` — limites, timeouts, quarentena (fail-closed)

### 7.5 Robôs de parsing e OCR
- `bot_type_router.py`
- `bot_parse_html.py`
- `bot_parse_pdf_text.py`
- `bot_ocr_needed_detector.py`
- `bot_pdf_to_images.py` — rasterização com limites
- `bot_ocr.py` — OCR + confidence + evidência
- `bot_parse_docx.py`
- `bot_parse_text.py`
- `bot_parse_json_csv.py` (se permitido/licenciado)

### 7.6 Robôs de limpeza, qualidade e dedup
- `bot_text_cleaner.py`
- `bot_language_detector.py`
- `bot_quality_scorer.py`
- `bot_dedup_exact.py`
- `bot_dedup_near.py`
- `bot_version_manager.py`

### 7.7 Robôs de privacidade e auditoria
- `bot_pii_detector.py`
- `bot_redactor.py`
- `bot_sensitivity_classifier.py`
- `bot_audit_logger.py` — trilha de auditoria + evidências

### 7.8 Robôs de enriquecimento (local-first; LLM só fallback)
- `bot_metadata_extractor.py`
- `bot_entity_extractor.py` (NER local)
- `bot_topic_classifier.py` (local)
- `bot_summary_generator.py` (local-first; fallback opcional)
- `bot_link_graph_builder.py`

### 7.9 Robôs de chunking e RAG prep
- `bot_chunker.py`
- `bot_chunk_validator.py`
- `bot_citation_mapper.py` — âncoras/citações (url+seção+página/offset)
- `bot_chunk_store.py`

### 7.10 Robôs de embeddings e indexação
- `bot_embedder.py` (local-first)
- `bot_embedding_cache.py`
- `bot_vector_indexer.py` (pgvector)
- `bot_hybrid_ranker.py` (FTS + vetor)
- `bot_retrieval_evaluator.py` — métricas/queries/golden set

### 7.11 Robôs de operação e QA
- `bot_manifest_writer.py` — manifesto por run
- `bot_quality_gate.py` — lint/tests/typecheck/security scan quando aplicável
- `bot_runbook_generator.py` — runbooks acionáveis
- `bot_metrics_exporter.py` — export métricas locais
- `bot_deadletter_triage.py` — triagem DLQ

---

## 8) Regras de ouro (para o sistema não “se perder”)
1. Todo robô é isolado, idempotente, com contrato JSON e evidência.
2. OCR e IA paga são **segunda opção**: só quando necessário, com justificativa e custo registrado.
3. Fail-closed em segurança: dúvida → bloquear/quarentenar.
4. RAG/Serving sempre com citações; sem grounding suficiente → “não sei com segurança”.
5. Tudo versionado: schema, configs, pipelines, migrações DB.
6. Reprodutibilidade: manifesto por run + hashes + (opcional) WARC.

---

## 9) “Como evolui depois do MVP” (rota de escala)
- Se volume/QPS crescer: manter Postgres como metadados e migrar vetores para Qdrant/Milvus/FAISS.
- Adicionar quantização/compactação de vetores.
- Expandir avaliação contínua de retrieval e qualidade.
- Endurecer hardening (isolamento mais forte, timeouts, quotas por tenant/domínio).

---
