-- ============================================================================
-- Banco de Dados Interrelacional - Schema v0
-- PostgreSQL + pgvector
-- ============================================================================
-- Autor: AGENTE ORQUESTRADOR (DE Persona)
-- Data: 2026-01-30
-- Versão: 0.1.0
-- Descrição: Schema inicial para metadados, documentos, chunks e embeddings
-- ============================================================================

-- Extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- ============================================================================
-- 1. SOURCES (Fontes de dados permitidas)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_org VARCHAR(255),
    base_domains TEXT[],
    entrypoints TEXT[],

    -- Crawl policy
    robots_respect BOOLEAN DEFAULT TRUE,
    user_agent VARCHAR(255),
    rate_limit_rps DECIMAL(5,2) DEFAULT 0.2,
    concurrency INTEGER DEFAULT 1,
    allow_paths TEXT[],
    deny_paths TEXT[],

    -- License & compliance
    license_status VARCHAR(50) DEFAULT 'unknown',  -- unknown, public_domain, CC-BY, etc.
    license_evidence TEXT,
    default_storage_mode VARCHAR(50) DEFAULT 'METADATA_ONLY',  -- FULL, METADATA_ONLY, BLOCK

    -- Data handling (LGPD)
    pii_expected VARCHAR(20) DEFAULT 'low',  -- low, medium, high
    pii_actions TEXT[],  -- detect, redact, anonymize
    retention_days INTEGER DEFAULT 365,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT
);

CREATE INDEX idx_sources_active ON sources(is_active) WHERE is_active = TRUE;

-- ============================================================================
-- 2. DOCUMENTS (Documentos coletados e processados)
-- ============================================================================
CREATE TABLE IF NOT EXISTS documents (
    doc_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id VARCHAR(50) NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,

    -- URL & Identity
    url TEXT NOT NULL,
    url_canonical TEXT,
    url_hash VARCHAR(64) UNIQUE NOT NULL,  -- blake3 or sha256 of canonical URL

    -- Content identity
    content_hash VARCHAR(64),  -- blake3 or sha256 of normalized content
    content_type VARCHAR(100),  -- text/html, application/pdf, etc.

    -- Fetch metadata
    fetched_at TIMESTAMP,
    http_status INTEGER,
    http_headers JSONB,

    -- Processing status
    status VARCHAR(50) DEFAULT 'raw',  -- raw, parsed, cleaned, curated, failed
    processing_errors JSONB,

    -- Content (storage policy dependent)
    title TEXT,
    author TEXT,
    published_date DATE,
    language VARCHAR(10) DEFAULT 'pt',

    raw_content TEXT,  -- NULL if storage_mode != FULL
    clean_content TEXT,  -- normalized, cleaned text
    content_length INTEGER,

    -- Quality & dedup
    quality_score DECIMAL(3,2),  -- 0.00 to 1.00
    is_duplicate BOOLEAN DEFAULT FALSE,
    duplicate_of UUID REFERENCES documents(doc_id),

    -- Compliance & PII
    has_pii BOOLEAN DEFAULT FALSE,
    pii_detected JSONB,  -- {types: ['cpf', 'email'], redacted: true}

    -- Enrichment
    entities JSONB,  -- NER results
    topics JSONB,  -- Topic classification

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Versioning
    version INTEGER DEFAULT 1,
    previous_version_id UUID REFERENCES documents(doc_id)
);

CREATE INDEX idx_documents_source ON documents(source_id);
CREATE INDEX idx_documents_url_hash ON documents(url_hash);
CREATE INDEX idx_documents_content_hash ON documents(content_hash);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_published_date ON documents(published_date);
CREATE INDEX idx_documents_language ON documents(language);
CREATE INDEX idx_documents_duplicate ON documents(is_duplicate) WHERE is_duplicate = FALSE;

-- ============================================================================
-- 3. CHUNKS (Segmentos de texto para RAG)
-- ============================================================================
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doc_id UUID NOT NULL REFERENCES documents(doc_id) ON DELETE CASCADE,

    -- Chunk identity
    chunk_hash VARCHAR(64) UNIQUE NOT NULL,  -- blake3 of normalized chunk text
    chunk_index INTEGER NOT NULL,  -- ordem no documento (0-based)

    -- Content
    content TEXT NOT NULL,
    content_length INTEGER NOT NULL,

    -- Position in document
    start_char INTEGER,
    end_char INTEGER,

    -- Metadata inheritance from document
    title TEXT,  -- document title for context
    published_date DATE,
    source_id VARCHAR(50),

    -- Chunking metadata
    chunk_method VARCHAR(50) DEFAULT 'fixed_size',  -- fixed_size, semantic, etc.
    overlap_tokens INTEGER DEFAULT 0,

    -- Quality
    quality_score DECIMAL(3,2),

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_doc_chunk_index UNIQUE (doc_id, chunk_index)
);

CREATE INDEX idx_chunks_doc ON chunks(doc_id);
CREATE INDEX idx_chunks_hash ON chunks(chunk_hash);
CREATE INDEX idx_chunks_source ON chunks(source_id);

-- ============================================================================
-- 4. EMBEDDINGS (Vetores para busca semântica)
-- ============================================================================
CREATE TABLE IF NOT EXISTS embeddings (
    embedding_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chunk_id UUID NOT NULL REFERENCES chunks(chunk_id) ON DELETE CASCADE,

    -- Vector
    vector vector(384),  -- sentence-transformers default dimension

    -- Model info
    model_name VARCHAR(255) NOT NULL,  -- e.g., 'all-MiniLM-L6-v2'
    model_version VARCHAR(50),

    -- Cache key
    content_hash VARCHAR(64) NOT NULL,  -- for reuse across chunks

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_chunk_model UNIQUE (chunk_id, model_name)
);

CREATE INDEX idx_embeddings_chunk ON embeddings(chunk_id);
CREATE INDEX idx_embeddings_content_hash ON embeddings(content_hash);
-- Vector similarity index (HNSW is faster for large datasets)
CREATE INDEX idx_embeddings_vector ON embeddings USING hnsw (vector vector_cosine_ops);

-- ============================================================================
-- 5. AUDIT_LOG (Rastreabilidade e compliance)
-- ============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Event
    event_type VARCHAR(50) NOT NULL,  -- fetch, parse, embed, policy_decision, etc.
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Context
    source_id VARCHAR(50),
    doc_id UUID,
    chunk_id UUID,

    -- Actor
    actor VARCHAR(100),  -- bot name, user, system

    -- Action details
    action VARCHAR(50),  -- create, update, delete, block, redact
    details JSONB,

    -- Result
    result VARCHAR(20),  -- success, failure, skipped
    error_message TEXT,

    -- Metadata
    run_id UUID,  -- correlation ID for batch operations
    job_id UUID
);

CREATE INDEX idx_audit_log_event_type ON audit_log(event_type);
CREATE INDEX idx_audit_log_timestamp ON audit_log(event_timestamp);
CREATE INDEX idx_audit_log_source ON audit_log(source_id);
CREATE INDEX idx_audit_log_doc ON audit_log(doc_id);
CREATE INDEX idx_audit_log_run ON audit_log(run_id);

-- ============================================================================
-- TRIGGERS (auto-update timestamps)
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_sources_updated_at BEFORE UPDATE ON sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chunks_updated_at BEFORE UPDATE ON chunks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS (convenience queries)
-- ============================================================================

-- Active sources ready for crawling
CREATE OR REPLACE VIEW v_active_sources AS
SELECT
    source_id,
    name,
    owner_org,
    base_domains,
    entrypoints,
    rate_limit_rps,
    license_status,
    default_storage_mode
FROM sources
WHERE is_active = TRUE AND license_status != 'blocked';

-- Documents ready for RAG (curated + not duplicate + no critical PII)
CREATE OR REPLACE VIEW v_curated_documents AS
SELECT
    doc_id,
    source_id,
    url,
    title,
    author,
    published_date,
    language,
    clean_content,
    quality_score
FROM documents
WHERE status = 'curated'
  AND is_duplicate = FALSE
  AND (has_pii = FALSE OR pii_detected->>'redacted' = 'true');

-- ============================================================================
-- COMMENTS (documentation)
-- ============================================================================
COMMENT ON TABLE sources IS 'Registro de fontes de dados permitidas com políticas de crawl e compliance';
COMMENT ON TABLE documents IS 'Documentos coletados e processados com metadados e controle de qualidade';
COMMENT ON TABLE chunks IS 'Segmentos de texto para indexação e RAG';
COMMENT ON TABLE embeddings IS 'Vetores semânticos gerados por sentence-transformers';
COMMENT ON TABLE audit_log IS 'Log de auditoria para rastreabilidade e compliance (LGPD)';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
