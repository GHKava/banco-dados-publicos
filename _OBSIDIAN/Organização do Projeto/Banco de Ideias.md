# Banco de Ideias — Banco de Dados Interrelacional

**Data criação:** 2026-01-30  
**Última atualização:** 2026-01-30  
**Processo:** Ideias → TRIAGEM → (APROVADO → Roadmap) ou (REJEITADO / DEFERRED)

---

## 🎯 Ideias aprovadas (incorporadas no Roadmap)

(Nenhuma ainda; todas estão em TRIAGEM.)

---

## 📋 Ideias em TRIAGEM (aguardando priorização/esforço)

### IDEA-001: Integração com Slack para alertas

- **Data proposta:** 2026-01-30
- **Descrição:** Notificar via Slack eventos críticos (DLQ, policy blocks, PII detections, etc.).
- **Benefício:** Observabilidade em tempo real, alertas pós-produção.
- **Esforço estimado:** Médio (3-5 dias)
- **Prioridade:** MÉDIA (pós-v1.0)
- **Dependências:** CI funcionando, API de eventos definida
- **Status:** TRIAGEM
- **Próx. ação:** Avaliar em Sprint Review (após T-010)

### IDEA-002: Dashboard Grafana (opcional)

- **Data proposta:** 2026-01-30
- **Descrição:** Dashboard Grafana para métricas (volumes/latência/custo por domínio, embedding cache hit rate, etc.).
- **Benefício:** Visibilidade operacional, debugging.
- **Esforço estimado:** Baixo-Médio (2-3 dias)
- **Prioridade:** BAIXA (v1.1+)
- **Dependências:** Prometheus exporters configurados
- **Status:** TRIAGEM
- **Próx. ação:** Considerar em v1.1

### IDEA-003: Alertas de mudança (change monitoring)

- **Data proposta:** 2026-01-30
- **Descrição:** Detectar mudanças em páginas/documentos fonte e alertar via Slack/email.
- **Benefício:** Produto SaaS "monitoramento de mudanças" (premium).
- **Esforço estimado:** Alto (7-10 dias)
- **Prioridade:** ALTA (pós-v1.0, antes v1.1)
- **Dependências:** RAG API, detecção de mudanças, scheduler robusto
- **Status:** TRIAGEM
- **Próx. ação:** Criar Epic em T-050+

### IDEA-004: Autenticação multi-tenant

- **Data proposta:** 2026-01-30
- **Descrição:** Suporte a múltiplos clientes/organizações na API de retrieval.
- **Benefício:** Plataforma SaaS escalável.
- **Esforço estimado:** Alto (10-15 dias)
- **Prioridade:** ALTA (v1.0+, se necessário comercializar)
- **Dependências:** API design, models Postgres
- **Status:** TRIAGEM
- **Próx. ação:** Decidir em Product review (T-005+)

### IDEA-005: GraphQL API (opcional)

- **Data proposta:** 2026-01-30
- **Descrição:** GraphQL wrapper sobre endpoints REST existentes.
- **Benefício:** Query flexibility, SDK code generation.
- **Esforço estimado:** Médio (4-6 dias)
- **Prioridade:** BAIXA (v2.0+)
- **Dependências:** FastAPI API estável
- **Status:** TRIAGEM
- **Próx. ação:** Considerar pós-v1.0

### IDEA-006: Cache distribuído (Redis avançado)

- **Data proposta:** 2026-01-30
- **Descrição:** Cache de queries (embedding + FTS), resulta em speedup 50-70%.
- **Benefício:** Latência reduzida, economia de embedding.
- **Esforço estimado:** Médio (3-5 dias)
- **Prioridade:** MÉDIA (v1.1, se QPS > 50)
- **Dependências:** Redis configurado, cache invalidation strategy
- **Status:** TRIAGEM
- **Próx. ação:** Implementar se latência for problema (T-040+)

### IDEA-007: Suporte a múltiplos modelos de embedding

- **Data proposta:** 2026-01-30
- **Descrição:** Permitir escolher modelo de embedding (sentence-transformers vs. OpenAI vs. Cohere).
- **Benefício:** Flexibilidade, otimização por caso de uso.
- **Esforço estimado:** Médio (4-6 dias)
- **Prioridade:** MÉDIA (v1.1)
- **Dependências:** Abstração de embedder, versionamento
- **Status:** TRIAGEM
- **Próx. ação:** Considerar em T-030+

### IDEA-008: Avaliação contínua de retrieval

- **Data proposta:** 2026-01-30
- **Descrição:** Pipeline de avaliação de Recall@k/MRR/NDCG em queries reais.
- **Benefício:** Monitoramento de qualidade, detecção de degradação.
- **Esforço estimado:** Alto (7-10 dias)
- **Prioridade:** MÉDIA (v1.1)
- **Dependências:** Golden queries definidas, métricas
- **Status:** TRIAGEM
- **Próx. ação:** Documentar em T-035+

### IDEA-009: Reprocessamento adaptativo (adaptive backfill)

- **Data proposta:** 2026-01-30
- **Descrição:** Reprocessar docs antigos apenas se houver mudança detectada ou nova regra.
- **Benefício:** Economia de compute, espaço.
- **Esforço estimado:** Médio (3-4 dias)
- **Prioridade:** MÉDIA (v1.1)
- **Dependências:** Versioning, change detection
- **Status:** TRIAGEM
- **Próx. ação:** Implementar em T-055+

### IDEA-010: Suporte a Web UI (opcional)

- **Data proposta:** 2026-01-30
- **Descrição:** Interface web para buscas (React/Vue) + admin panel (gerenciar fontes, regras).
- **Benefício:** Acesso não-técnico, demoing.
- **Esforço estimado:** Alto (12-15 dias)
- **Prioridade:** BAIXA (v2.0+)
- **Dependências:** API estável, auth
- **Status:** TRIAGEM
- **Próx. ação:** Considerar pós-v1.0

---

## 📊 Triagem resumida (por prioridade)

| Prioridade | Quantidade | Ideias                                           | Próxima ação     |
| ---------- | ---------- | ------------------------------------------------ | ---------------- |
| **ALTA**   | 2          | IDEA-003, IDEA-004                               | Decidir em T-010 |
| **MÉDIA**  | 5          | IDEA-001, IDEA-006, IDEA-007, IDEA-008, IDEA-009 | Avaliar pós-v1.0 |
| **BAIXA**  | 3          | IDEA-002, IDEA-005, IDEA-010                     | v2.0 ou beyond   |

---

## 🚫 Ideias rejeitadas (com justificativa)

(Nenhuma ainda)

---

## 📌 Procedimento de incorporação

1. Ideia chega via Backlog ou user input
2. Registra em TRIAGEM com: descrição, benefício, esforço, prioridade, dependências
3. Em Product Review (quinzenalmente): APROVADO/REJEITADO/DEFERRED
4. Se APROVADO: criar CR + adicionar ao Roadmap como nova Epic ou tarefa
5. Se REJEITADO: mover para "Rejeitadas" com justificativa
6. Se DEFERRED: marcar data de revisão futura

---

## 🔄 Próxima revisão

**Data:** 2026-02-13 (após Sprint 1 — T-001 a T-010)  
**Quem:** ORQ (Orquestrador) + PM (Product Manager)

---
