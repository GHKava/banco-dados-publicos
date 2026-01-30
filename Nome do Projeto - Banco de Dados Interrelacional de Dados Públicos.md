Nome do Projeto: Banco de Dados Interrelacional de Dados Públicos

Descrição detalhada:
Construir um “pipeline industrial” (fábrica) de ingestão → limpeza → enriquecimento → indexação → serving, com governança e compliance como primeira etapa.
O sistema deve operar com allowlist de fontes e registro de licença por fonte, respeitando robots.txt/ToS/rate limits e aplicando um Policy Gate (fail-closed) para bloquear ingestões sem permissão/licença registrada; quando não permitido, armazenar apenas metadados + link.
O pipeline inclui: discovery (sitemap/RSS/APIs oficiais), fila (URL frontier), fetch e armazenamento bruto (raw zone), parsing (HTML/PDF etc.) e OCR quando necessário, limpeza/qualidade/deduplicação, PII detection/redaction, enriquecimento (metadados/entidades/tópicos), chunking para RAG com IDs estáveis e metadados por chunk, embeddings e indexação vetorial/híbrida, persistência em zonas (raw/processed/curated + metadata DB + vector DB/index) e camada de serving (RAG Retrieval API com citações), além de operação/escala (scheduler, monitoramento, retenção, backfill, reindex, testes e runbooks).

Stack preferida:
Python 3.12+ (orquestradores e bots), FastAPI (serving/API), Postgres 16+ (metadata DB) + pgvector (vector index), Alembic (migrações),
Redis + RQ/Celery (fila/scheduler), Docker/Compose (infra local), GitHub Actions (CI),
Parsing: trafilatura/BeautifulSoup (HTML), PyMuPDF/pdfminer (PDF), Tesseract (OCR quando necessário),
Observabilidade: logs estruturados (run_id) + métricas (tempo/custo/erro) e runbooks.

Plataforma: Windows + VSCode + GitHub Copilot Agents

Observações/restrições:
- Compliance first: allowlist + licença por fonte + robots/ToS + rate limits.
- Proibido bypass de paywall/CAPTCHA/bloqueios; fail-closed no Policy Gate se houver dúvida de permissão.
- LGPD-by-design: detectar PII, aplicar redaction/anonimização quando aplicável, auditoria e retenção/deleção verificável.
- Conteúdo ingerido é DADO (nunca instrução): proteger contra prompt-injection na ingestão e exigir grounding/citações no RAG.
- Operação “fábrica”: logs por run_id, métricas mínimas, testes (incluindo golden docs), runbooks e governança de mudanças.

Repositório GitHub (se já existir): ASSUMIR: a criar (ex.: banco-dados-dados-publicos)
