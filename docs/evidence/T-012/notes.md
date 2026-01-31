# Notes — T-012 (Discovery: Sitemap)

**Data:** 2026-01-31  
**Duração:** ~22 min  
**Persona:** DE

---

## Objetivo

Implementar bot para descobrir URLs via sitemaps XML (urlset + sitemap index recursivo).

---

## Execução

### 1. WorkOrder criado

- [T-012-WorkOrder.md](../../\_OBSIDIAN/Organização do Projeto/WorkOrders/T-012-WorkOrder.md)

### 2. Design decisions

- **Parser:** xml.etree.ElementTree (stdlib, leve)
- **Namespace handling:** sitemaps.org xmlns
- **Sitemap index:** Recursive fetch com max_depth=2
- **Heuristic para index:** Se primeiros 3 URLs terminam em .xml → index
- **Timeout:** 30s por fetch

### 3. Implementação discovery_sitemap.py

- **Funções:**
  - `fetch_sitemap()`: Fetch XML com Content-Type validation
  - `parse_sitemap()`: Parse urlset OU sitemapindex
  - `discover_from_sitemap()`: Recursive sitemap index handling
  - `discover_from_source()`: Integração com sources.yaml (explicit sitemap_urls ou infer /sitemap.xml)
- **Dataclass:** SitemapURL (loc, lastmod, priority, changefreq)

### 4. Testes

- **Arquivo:** tests/test_discovery_sitemap.py
- **Cobertura:** 96% (78/81 statements)
- **Testes:** 14/14 PASS
  1. test_fetch_sitemap_success
  2. test_fetch_sitemap_404
  3. test_fetch_sitemap_not_xml
  4. test_fetch_sitemap_timeout
  5. test_parse_sitemap_urlset
  6. test_parse_sitemap_index
  7. test_parse_sitemap_malformed
  8. test_parse_sitemap_empty
  9. test_discover_from_sitemap_simple
  10. test_discover_from_sitemap_index (recursive)
  11. test_discover_from_sitemap_max_depth
  12. test_discover_from_source (explicit)
  13. test_discover_from_source_infer_sitemap
  14. test_discover_from_source_not_found

### 5. Quality Gate

- ✅ Lint (black + flake8 + isort) PASS
- ✅ Tests (pytest 14/14) PASS
- ✅ Coverage 96%
- ✅ Mock HTTP requests

---

## Decisões

1. **XML parser:** ElementTree (stdlib, suficiente para sitemap MVP)
2. **Recursive sitemap index:** Max depth=2 (evitar loops infinitos)
3. **Content-Type check:** Validar "xml" in Content-Type antes de parse
4. **Sitemap inference:** Se sitemap_urls ausente em sources.yaml → tentar /sitemap.xml
5. **Error handling:** Try/except em parse + fetch, log warnings

---

## Riscos mitigados

- ✅ Sitemap malformed: Try/except em parse → retorna []
- ✅ Sitemap index recursivo: Max depth limit
- ✅ Slow network: Timeout 30s
- ✅ Non-XML response: Content-Type validation

---

## Próximos passos

1. **T-013:** Bot - discovery RSS (READY após T-012 DONE)
2. **Integration test:** T-020 (Observability) testará fetch real

---

## Artefatos

- [x] src/bots/discovery_sitemap.py (201 linhas, 81 statements)
- [x] tests/test_discovery_sitemap.py (183 linhas, 14 testes)
- [x] WorkOrder T-012
- [x] Evidence Pack (este arquivo)

---

**Status:** ✅ DONE  
**Commit:** Pendente

---
