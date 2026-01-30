# WorkOrder T-006 — Redis + RQ setup

**ID:** T-006
**Data criação:** 20260130
**Persona:** TL (Tech Lead)
**Roadmap link:** [[Roadmap detalhado do Projeto#T-006]]

---

## 1. Objetivo

Configurar Redis e RQ (Redis Queue) para orquestração de jobs/workers:

- Redis instalado/configurado (Docker recomendado)
- RQ instalado e testado
- Worker example criado
- Integração com schema de database v0

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-005 completa (Postgres schema v0 ✅ DONE)
- [x] docker-compose.yml criado (será criado nesta tarefa)
- [x] Redis image disponível
- [x] RQ library documentado em requirements.txt

---

## 3. Entradas

- PostgreSQL schema v0 (src/database/schema.sql)
- Python environment com rq, redis packages
- Docker (para Redis) ou Redis local instalado

---

## 4. Saídas (Artefatos esperados)

- `docker-compose.yml` — Postgres + Redis + pgAdmin (opcional)
- `src/jobs/` — Module para job definitions
- `src/jobs/example.py` — Job exemplo
- `src/jobs/worker.py` — Worker script
- `tests/test_redis.py` — Redis connection test
- Evidence pack em `docs/evidence/T-006/`

---

## 5. Comandos previstos

```powershell
# 1. Criar docker-compose.yml
# (será criado manualmente)

# 2. Validar sintaxe
docker-compose -f docker-compose.yml config

# 3. Iniciar serviços
docker-compose up -d

# 4. Verificar Redis
redis-cli ping  # or docker exec redis redis-cli ping

# 5. Testar conexão Python
python -m pytest tests/test_redis.py -v

# 6. Criar job exemplo
# (criado em src/jobs/)

# 7. Testar worker
python src/jobs/worker.py --burst
```

---

## 6. Riscos

| Risco                                | Severidade | Mitigação                         |
| ------------------------------------ | ---------- | --------------------------------- |
| Docker não instalado                 | Média      | Usar Redis local (alternativa)    |
| Redis port 6379 em uso               | Baixa      | Mudar port em docker-compose.yml  |
| RQ incompatibilidade com Python 3.14 | Baixa      | Verificar compatibility           |
| Network isolation issues             | Baixa      | Testar inter-container networking |

---

## 7. Evidência mínima necessária

- [x] commands.log (comandos executados)
- [x] docker-compose.yml validado
- [x] Redis connectivity verified
- [x] RQ worker testado
- [x] files_changed.json
- [x] notes.md

---

## 8. Quality Gate aplicável

- [x] docker-compose.yml: valid syntax
- [x] Redis: accessible
- [x] RQ: imports successfully
- [x] Worker: can be spawned
- [x] Pytest: test_redis passes

---

## 9. Próximo passo

- T-007: Bot: source registry (UNBLOCKED → T-005, T-004 ✅)

---

**Criado por:** ORQ
**Data:** 20260130

---
