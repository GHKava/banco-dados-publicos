# Banco de Dados Interrelacional — Source Code

Este diretório contém o código-fonte principal do projeto.

## Estrutura (planejada)

```
src/
├── __init__.py
├── config/           # Configurações e settings
├── db/               # Database models e migrations
├── bots/             # Robôs/CLIs individuais
│   ├── source_registry/
│   ├── policy_gate/
│   ├── frontier/
│   ├── fetcher/
│   ├── parser/
│   ├── dedup/
│   ├── pii_detector/
│   ├── chunker/
│   ├── embedder/
│   └── retriever/
├── api/              # FastAPI serving
├── scheduler/        # RQ job orchestration
└── utils/            # Utilidades comuns
```

**Status:** EM CONSTRUÇÃO
**Primeira tarefa:** T-007 (Bot: source registry)
