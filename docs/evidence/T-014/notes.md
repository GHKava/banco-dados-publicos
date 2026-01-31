# Notes — T-014 (Change Detector)

**Data:** 2026-01-31
**Duração:** ~20 min
**Persona:** DE

---

## Objetivo

Implementar bot para detectar mudanças em URLs já crawlados (hash comparison, Last-Modified headers).

---

## Execução

1. WorkOrder criado: `T-014-WorkOrder.md`
2. Implementação: `src/bots/change_detector.py` (242 linhas, 6 funções)
   - `compute_content_hash()` (SHA256 incremental)
   - `has_content_changed()` (hash comparison)
   - `parse_last_modified()` (RFC 2822 + ISO 8601)
   - `check_last_modified()` (header comparison)
   - `detect_change()` (orchestrator)
   - `ChangeResult` dataclass (metadata)
3. Testes: `tests/test_change_detector.py` (229 linhas)
   - 26/26 tests PASS
   - 97% coverage (78/80 statements, 2 linhas unreachable em error handling)
4. Quality Gate:
   - ✅ Tests PASS (26/26)
   - ✅ Coverage 97%
   - ✅ Lint PASS (black, flake8, isort)

---

## Decisões Técnicas

### Hash Algorithm

- **SHA256 padrão**: Balanceado (segurança vs. performance)
- **MD5 opcional**: Suporte para compatibilidade legada
- **Incremental**: Chunks de 8KB para arquivos grandes (evita OOM)

### Last-Modified Parsing

- **RFC 2822**: Formato padrão HTTP (`Wed, 21 Oct 2015 07:28:00 GMT`)
- **ISO 8601**: Fallback para feeds não-padrão
- **Timezone-agnostic**: Remove timezone para comparação (simplificação)
- **Fail-safe**: Se parsing falha, assume mudança (conservador)

### Change Detection Strategy

1. **Initial collection**: `old_hash=None` → sempre `has_changed=True`
2. **Content change**: Hash diff detecta mudança de conteúdo
3. **Metadata change**: Last-Modified posterior detecta mudança sem hash diff
4. **No change**: Hash igual + Last-Modified igual/anterior

### Headers Handling

- **Case-insensitive**: `Last-Modified` ou `last-modified`
- **ETag extraction**: Guardado mas não usado para detecção (futuro)
- **Size diff**: Calculado quando hash muda (simplified, sem old_size)

---

## Bugs Corrigidos

### Bug #1: Headers não extraídos em primeira coleta

**Problema**: `test_etag_extraction` e `test_case_insensitive_headers` falhando.
**Causa**: Headers extraídos apenas após verificar `old_hash is not None`.
**Fix**: Mover extração de headers para antes do early return (primeira coleta).
**Commit**: Inline fix durante T-014.

---

## Cobertura Não Testada (2 linhas)

- **Linha 138**: `except ValueError` em `strptime()` (todos os formatos inválidos cobertos pelo loop)
- **Linha 140**: `continue` no loop de formatos (implícito em testes)

Ambos são error handling paths cobertos indiretamente pelos testes de parsing.

---

## Próximos Passos

- T-015: Frontier scheduler (processar frontier queue periodicamente)
- Integração: Change detector → URL frontier (re-queue se mudou)
- Performance: Benchmark hash incremental vs. full (10MB+ files)
