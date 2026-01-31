# WorkOrder — T-015 (Frontier Scheduler)

**Data de criação:** 2026-01-31
**Persona responsável:** DE (Data Engineer)
**Status:** IN_PROGRESS
**Prioridade:** Alta

---

## Objetivo

Implementar scheduler para processar frontier queue periodicamente (fetch-decode-execute loop).

---

## Dependências

- ✅ T-011 (URL frontier) - DONE (commit 5a310b2)

---

## Escopo

### Entradas

- URLFrontier (Redis-backed priority queue)
- Schedule configuration (interval, batch size, max workers)

### Saídas

- Scheduled job executing periodically
- Metrics (URLs processed, errors, throughput)
- Graceful shutdown support

### Funcionalidades

1. **Scheduler**: Executar job em intervalos fixos (ex: 60s)
2. **Batch processing**: Fetch N URLs por execução (ex: 10)
3. **Worker loop**: Fetch → Process → Store → Repeat
4. **Error handling**: Retry failed URLs com exponential backoff
5. **Metrics**: Log throughput, queue size, errors

---

## Critérios de Aceitação

- [ ] Função `schedule_frontier_worker(interval, batch_size, frontier)`
- [ ] Função `worker_iteration(frontier, batch_size) -> dict` (stats)
- [ ] Graceful shutdown (SIGINT/SIGTERM)
- [ ] Testes: 8+ tests, 90%+ coverage
- [ ] Lint: black, flake8, isort PASS
- [ ] Integra com URL frontier (T-011)

---

## Decisões de Design

### Scheduler Choice

**Opções avaliadas:**

1. **APScheduler** (library): Robusto, suporta cron, persistência
2. **asyncio + sleep()**: Simples, stdlib, suficiente para MVP
3. **Celery Beat**: Overkill, requer broker adicional

**Decisão**: asyncio + sleep() para MVP (pode migrar para APScheduler em produção)

### Batch Size

- **Default: 10 URLs/batch**: Balanceado (throughput vs. memory)
- **Configurable**: Permitir tuning por environment

### Error Handling

- **Retry strategy**: Exponential backoff (1s, 2s, 4s, ..., max 60s)
- **Max retries**: 3 (após isso, marcar como failed e logar)
- **Dead letter queue**: URLs falhados vão para `frontier:urls:failed` (Redis)

---

## Riscos & Mitigações

- **Risco**: Scheduler não para gracefully (perde trabalho em progresso)
  - **Mitigação**: Signal handlers (SIGINT/SIGTERM) + atexit cleanup
- **Risco**: Queue vazia por longo período (polling desperdiçado)
  - **Mitigação**: Adaptive interval (aumenta para 5min se queue vazia)

---

## Integração com Componentes

- **T-011 (URL frontier)**: `get_next_url()` para fetch batch
- **T-014 (Change detector)**: Detectar mudanças antes de processar (futuro)
- **T-016 (HTTP fetcher)**: Será chamado por este scheduler

---

## Notas

- Usar asyncio para permitir concorrência futura (aiohttp)
- Logging estruturado com timestamps (facilita debugging)
- Configuração via environment vars (BATCH_SIZE, INTERVAL_SECONDS)

---

## Checklist de Execução

- [ ] WorkOrder criado
- [ ] Implementação (src/bots/frontier_scheduler.py)
- [ ] Testes (tests/test_frontier_scheduler.py)
- [ ] Lint PASS (black, flake8, isort)
- [ ] Evidence Pack (docs/evidence/T-015/notes.md)
- [ ] Commit + Push
