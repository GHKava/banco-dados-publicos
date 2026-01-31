# WorkOrder T-012 — Bot: Discovery (Sitemap)

**ID:** T-012  
**Data criação:** 20260131  
**Persona:** DE (Data Engineer)  
**Roadmap link:** [[Roadmap detalhado do Projeto#T-012]]

---

## 1. Objetivo

Implementar bot para descobrir URLs via sitemaps XML (https://example.com/sitemap.xml ou robots.txt Sitemap: directive).

---

## 2. DoR Checklist

- [x] T-011 (URL frontier) completo
- [x] T-009 (Robots checker) completo
- [x] requests/lxml disponível
- [x] sources.yaml com sitemap_urls (opcional)

---

## 3. Entradas

- `sources.yaml` com sitemap_urls (ou inferir /sitemap.xml)
- robots.txt Sitemap: directives (fallback)
- Sitemap index (pode apontar para outros sitemaps)

---

## 4. Saídas (Artefatos esperados)

- `src/bots/discovery_sitemap.py`:
  - `fetch_sitemap(url)` (fetch XML + parse)
  - `parse_sitemap(content)` (extract URLs + metadata)
  - `discover_from_source(source_id)` (fetch sitemap de fonte + add to frontier)
- `tests/test_discovery_sitemap.py` (8+ testes)
- Evidence Pack em `docs/evidence/T-012/`

---

## 5. Formato Sitemap XML

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2024-01-01</lastmod>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Sitemap Index

```xml
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-1.xml</loc>
  </sitemap>
</sitemapindex>
```

---

## 6. Comandos previstos

```powershell
# Rodar testes
pytest tests/test_discovery_sitemap.py -v

# Lint
black src/bots/discovery_sitemap.py
flake8 src/bots/discovery_sitemap.py
mypy src/bots/discovery_sitemap.py
```

---

## 7. Riscos

| Risco                        | Severidade | Mitigação                                    |
| ---------------------------- | ---------- | -------------------------------------------- |
| Sitemap muito grande (>10MB) | Média      | Limit 50MB, streaming parse (lxml iterparse) |
| Sitemap malformed (não-XML)  | Baixa      | Try/except + log error                       |
| Sitemap index recursivo      | Baixa      | Depth limit = 2                              |
| Slow network                 | Baixa      | Timeout 30s                                  |

---

## 8. Evidência mínima necessária

- [x] discovery_sitemap.py implementado (3+ funções)
- [x] tests_discovery_sitemap.py (8+ testes, 100% pass)
- [x] commands.log (pytest)
- [x] outputs.log (saídas de testes)
- [x] notes.md (decisões + tempo)

---

## 9. Quality Gate

- [ ] Lint (black, flake8, isort) ✅
- [ ] Tests (pytest 8/8 passing) ✅
- [ ] Typecheck (mypy) ✅
- [ ] Mock sitemap XML parsing

---

## 10. Próximo passo

T-013: Bot - discovery RSS

---

**Criado por:** ORQ  
**Data:** 20260131 00:30 UTC

---
