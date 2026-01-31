# WorkOrder T-013 — Bot: Discovery (RSS)

**ID:** T-013  
**Data criação:** 20260131  
**Persona:** DE (Data Engineer)  
**Roadmap link:** [[Roadmap detalhado do Projeto#T-013]]

---

## 1. Objetivo

Implementar bot para descobrir URLs via RSS/Atom feeds.

---

## 2. DoR Checklist

- [x] T-011 (URL frontier) completo
- [x] feedparser disponível (pip install feedparser)
- [x] sources.yaml com feed_urls (opcional)

---

## 3. Entradas

- `sources.yaml` com feed_urls (ou inferir /feed ou /rss)
- RSS 2.0 / Atom feeds

---

## 4. Saídas (Artefatos esperados)

- `src/bots/discovery_rss.py`:
  - `fetch_feed(url)` (fetch feed + parse)
  - `parse_feed(content)` (extract entries)
  - `discover_from_source(source_id)` (integração sources.yaml)
- `tests/test_discovery_rss.py` (8+ testes)
- Evidence Pack em `docs/evidence/T-013/`

---

## 5. Formato RSS 2.0

```xml
<rss version="2.0">
  <channel>
    <item>
      <title>Title</title>
      <link>https://example.com/article</link>
      <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
```

---

## 6. Comandos previstos

```powershell
# Install feedparser
pip install feedparser

# Rodar testes
pytest tests/test_discovery_rss.py -v

# Lint
black src/bots/discovery_rss.py
flake8 src/bots/discovery_rss.py
```

---

## 7. Riscos

| Risco                     | Severidade | Mitigação                                   |
| ------------------------- | ---------- | ------------------------------------------- |
| Feed malformed            | Baixa      | feedparser tolera erros (best-effort parse) |
| Feed muito grande (>10MB) | Baixa      | Timeout 30s, feedparser streaming           |
| Feed não disponível (404) | Baixa      | Return empty list                           |

---

## 8. Evidência mínima necessária

- [x] discovery_rss.py implementado (3+ funções)
- [x] tests_discovery_rss.py (8+ testes, 100% pass)
- [x] commands.log (pytest + pip install)
- [x] notes.md (decisões + tempo)

---

## 9. Quality Gate

- [x] Lint (black, flake8, isort) ✅
- [x] Tests (pytest 12/12 passing) ✅
- [x] feedparser installed

---

## 10. Próximo passo

T-014: Bot - change detector

---

**Criado por:** ORQ  
**Data:** 20260131 00:45 UTC

---
