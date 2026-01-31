# WorkOrder — T-014 (Bot: Change Detector)

**Data de criação:** 2026-01-31  
**Persona responsável:** DE (Data Engineer)  
**Status:** IN_PROGRESS  
**Prioridade:** Alta

---

## Objetivo

Implementar bot para detectar mudanças em URLs já crawlados (hash comparison, last-modified headers).

---

## Dependências

- ✅ T-011 (URL frontier) - DONE (commit 5a310b2)

---

## Escopo

### Entradas

- URL previamente crawlado (com hash SHA256 armazenado)
- Novo conteúdo fetched

### Saídas

- Boolean: `has_changed` (True se conteúdo diferente)
- Novo hash SHA256 (se mudou)
- Last-Modified header (se disponível)
- Change metadata (size diff, timestamp)

### Funcionalidades

1. **Hash comparison**: SHA256 do conteúdo atual vs. armazenado
2. **Last-Modified header**: Verificar se servidor informa mudança
3. **ETag support**: Usar ETag para validação rápida (se disponível)
4. **Change metadata**: Registrar tamanho da mudança, timestamp, tipo

---

## Critérios de Aceitação

- [ ] Função `compute_content_hash(content: bytes) -> str` (SHA256)
- [ ] Função `has_content_changed(old_hash: str, new_content: bytes) -> bool`
- [ ] Função `check_last_modified(url: str, last_known_date: datetime) -> bool`
- [ ] Função `detect_change(url, old_hash, new_content, headers) -> ChangeResult`
- [ ] Testes: 8+ tests, 90%+ coverage
- [ ] Lint: black, flake8, isort PASS

---

## Riscos & Mitigações

- **Risco**: Hash computation lento para arquivos grandes
  - **Mitigação**: Usar hashlib incremental, limitar a 10MB
- **Risco**: Last-Modified header ausente em muitos sites
  - **Mitigação**: Hash comparison como fallback

---

## Notas

- Seguir exemplo de url_frontier.py (Redis + dataclass)
- Usar hashlib.sha256() (stdlib, não instalar deps)
- Armazenar hash no Redis para comparação rápida
- Logging via audit_log.py (T-010)

---

## Checklist de Execução

- [ ] WorkOrder criado
- [ ] Implementação (src/bots/change_detector.py)
- [ ] Testes (tests/test_change_detector.py)
- [ ] Lint PASS (black, flake8, isort)
- [ ] Evidence Pack (docs/evidence/T-014/notes.md)
- [ ] Commit + Push
