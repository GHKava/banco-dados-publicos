# Notes — T-013 (Discovery: RSS)

**Data:** 2026-01-31  
**Duração:** ~18 min  
**Persona:** DE

---

## Objetivo

Implementar bot para descobrir URLs via RSS/Atom feeds usando feedparser.

---

## Execução

### 1. WorkOrder criado

- [T-013-WorkOrder.md](../../\_OBSIDIAN/Organização do Projeto/WorkOrders/T-013-WorkOrder.md)

### 2. Dependência instalada

- feedparser 6.0.12 + sgmllib3k 1.0.0

### 3. Implementação discovery_rss.py

- **Funções:**
  - `fetch_feed()`: Fetch feed com requests
  - `parse_feed()`: Parse RSS/Atom com feedparser (tolerante a erros)
  - `discover_from_feed()`: Fetch + parse workflow
  - `discover_from_source()`: Integração sources.yaml (explicit feed_urls ou infer /feed + /rss)
- **Dataclass:** FeedEntry (link, title, published, summary)

### 4. Testes

- **Arquivo:** tests/test_discovery_rss.py
- **Cobertura:** 92% (56/61 statements)
- **Testes:** 12/12 PASS
  1-3: test_fetch_feed (success, 404, timeout)
  4-7: test_parse_feed (RSS2, Atom, empty, malformed)
  8-9: test_discover_from_feed (success, not_found)
  10-12: test_discover_from_source (explicit, infer, not_found)

### 5. Quality Gate

- ✅ Lint (black + flake8 + isort) PASS
- ✅ Tests (pytest 12/12) PASS
- ✅ Coverage 92%
- ✅ feedparser installed

---

## Decisões

1. **feedparser:** Biblioteca padrão de mercado para RSS/Atom (tolerante a erros, suporta múltiplos formatos)
2. **Bozo flag:** feedparser.bozo indica feed malformed → log warning mas continua processamento
3. **Feed inference:** Se feed_urls ausente → tentar /feed e /rss (2 URLs comuns)
4. **Metadata extraction:** title, published (ou updated), summary (ou description) opcionais

---

## Riscos mitigados

- ✅ Feed malformed: feedparser tolera erros (best-effort parse)
- ✅ Feed timeout: requests.get com timeout 30s
- ✅ Feed não disponível: Retorna lista vazia (não bloqueia pipeline)
- ✅ Campos opcionais ausentes: get() com fallback None

---

## Próximos passos

1. **T-014:** Bot - change detector (READY após T-013 DONE)
2. **Integration test:** T-020 (Observability) testará feed real

---

## Artefatos

- [x] src/bots/discovery_rss.py (158 linhas, 61 statements)
- [x] tests/test_discovery_rss.py (177 linhas, 12 testes)
- [x] WorkOrder T-013
- [x] Evidence Pack (este arquivo)

---

**Status:** ✅ DONE  
**Commit:** Pendente

---
