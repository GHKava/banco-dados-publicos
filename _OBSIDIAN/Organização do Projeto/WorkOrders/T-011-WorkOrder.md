# WorkOrder T-011 — Bot: URL Frontier

**ID:** T-011  
**Data criação:** 20260131  
**Persona:** DE (Data Engineer)  
**Roadmap link:** [[Roadmap detalhado do Projeto#T-011]]

---

## 1. Objetivo

Implementar URL frontier (priority queue) para gerenciar URLs a crawlar, com suporte a prioridade, dedup, e persistência Redis.

---

## 2. DoR Checklist

- [x] T-010 (Audit logging) completo
- [x] Redis disponível (T-006)
- [x] sources.yaml com 5 fontes (T-004)
- [x] Policy gate implementado (T-008)

---

## 3. Entradas

- URLs de entrypoints (sources.yaml)
- URLs descobertos por bots (sitemap, RSS, links)
- Prioridade (0-100, default 50)

---

## 4. Saídas (Artefatos esperados)

- `src/bots/url_frontier.py`:
  - `URLFrontier` class (Redis-backed priority queue)
  - `add_url(url, priority, source_id)` (adicionar com dedup)
  - `get_next_url()` (pop por prioridade)
  - `get_queue_stats()` (tamanho, breakdown por source)
- `tests/test_url_frontier.py` (8+ testes)
- Evidence Pack em `docs/evidence/T-011/`

---

## 5. Design

### Data Structure (Redis)

```
frontier:urls:pending (sorted set, score = priority + timestamp)
frontier:urls:seen (set, URLs já vistos)
frontier:stats:{source_id} (hash, contadores)
```

### Priority Formula

```
final_score = priority * 1000 + (current_timestamp - added_timestamp)
```

Maior score = maior prioridade. Timestamp break ties.

---

## 6. Comandos previstos

```powershell
# Rodar testes
pytest tests/test_url_frontier.py -v

# Lint
black src/bots/url_frontier.py
flake8 src/bots/url_frontier.py
mypy src/bots/url_frontier.py
```

---

## 7. Riscos

| Risco                                            | Severidade | Mitigação                                              |
| ------------------------------------------------ | ---------- | ------------------------------------------------------ |
| Redis OOM (muitas URLs)                          | Média      | TTL em frontier:urls:seen (30 dias)                    |
| Dedup collision (URL variants)                   | Baixa      | Canonicalizar URLs antes de add (urlparse + normalize) |
| Priority starvation (low priority never crawled) | Baixa      | Timestamp offset garante eventual processing           |

---

## 8. Evidência mínima necessária

- [x] url_frontier.py implementado (class URLFrontier com 5+ métodos)
- [x] tests_url_frontier.py (8+ testes, 100% pass)
- [x] commands.log (pytest)
- [x] outputs.log (saídas de testes)
- [x] notes.md (decisões + tempo)

---

## 9. Quality Gate

- [ ] Lint (black, flake8, isort) ✅
- [ ] Tests (pytest 8/8 passing) ✅
- [ ] Typecheck (mypy) ✅
- [ ] Redis integration working

---

## 10. Próximo passo

T-012: Bot - discovery sitemap

---

**Criado por:** ORQ  
**Data:** 20260131 00:15 UTC

---
