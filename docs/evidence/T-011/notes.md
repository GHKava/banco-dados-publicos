# Notes — T-011 (URL Frontier)

**Data:** 2026-01-31  
**Duração:** ~20 min  
**Persona:** DE

---

## Objetivo

Implementar URL frontier (priority queue) com Redis backend para gerenciar URLs a crawlar.

---

## Execução

### 1. WorkOrder criado

- [T-011-WorkOrder.md](../../\_OBSIDIAN/Organização do Projeto/WorkOrders/T-011-WorkOrder.md)

### 2. Design decisions

- **Backend:** Redis sorted set (score = priority \* 1000 + age)
- **Deduplication:** Redis set com TTL 30 dias
- **Canonicalization:** Lowercase scheme/netloc, remove default ports (80/443)
- **Priority formula:** Higher score = higher priority, timestamp breaks ties

### 3. Implementação url_frontier.py

- **Class:** URLFrontier (Redis-backed)
- **Métodos:**
  - `add_url()`: Adiciona com dedup, canonicalization, stats tracking
  - `get_next_url()`: Pop highest priority (ZPOPMAX)
  - `get_queue_size()`: Total pending URLs
  - `get_seen_count()`: Total unique URLs seen
  - `get_stats()`: Breakdown por source (added/crawled)
  - `clear()`: Limpar frontier (testing/maintenance)

### 4. Testes

- **Arquivo:** tests/test_url_frontier.py
- **Cobertura:** 100% (69 statements)
- **Testes:** 10/10 PASS
  1. test_add_url_new
  2. test_add_url_duplicate (dedup)
  3. test_canonicalize_url
  4. test_get_next_url
  5. test_get_next_url_empty
  6. test_get_queue_size
  7. test_get_seen_count
  8. test_get_stats
  9. test_clear
  10. test_compute_score

### 5. Quality Gate

- ✅ Lint (black + flake8 + isort) PASS
- ✅ Tests (pytest 10/10) PASS
- ✅ Coverage 100%
- ✅ Mock Redis (integration tests defer para T-020)

---

## Decisões

1. **Redis sorted set**: ZREVRANGE + ZPOPMAX para priority queue eficiente
2. **TTL em seen set**: 30 dias (evitar OOM, permite re-crawl eventual)
3. **Score formula**: `priority * 1000 + age_seconds` (prioridade dominante, age desempate)
4. **Canonicalization**: Normaliza URLs para dedup (lowercase, remove default ports)
5. **Stats tracking**: Hash per source com contadores added/crawled

---

## Riscos mitigados

- ✅ Dedup collision: Canonicalization antes de add
- ✅ Redis OOM: TTL 30 dias em seen set
- ✅ Priority starvation: Timestamp offset garante eventual crawl
- ✅ URL variants: Canonicalization (lowercase + port normalization)

---

## Próximos passos

1. **T-012:** Bot - discovery sitemap (READY após T-011 DONE)
2. **Integration test:** T-020 (Observability) testará Redis real

---

## Artefatos

- [x] src/bots/url_frontier.py (219 linhas, 69 statements)
- [x] tests/test_url_frontier.py (136 linhas, 10 testes)
- [x] WorkOrder T-011
- [x] Evidence Pack (este arquivo)

---

**Status:** ✅ DONE  
**Commit:** Pendente

---
