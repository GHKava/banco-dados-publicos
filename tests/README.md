# Banco de Dados Interrelacional — Tests

Este diretório contém os testes automatizados do projeto.

## Estrutura (planejada)

```
tests/
├── __init__.py
├── conftest.py       # Fixtures compartilhadas
├── unit/             # Testes unitários
├── integration/      # Testes de integração
└── e2e/              # Testes end-to-end (golden tests)
```

## Como rodar

```bash
# Todos os testes
pytest tests/

# Com coverage
pytest tests/ --cov=src --cov-report=term-missing

# Apenas unit tests
pytest tests/unit/

# Verbose
pytest tests/ -v
```

**Status:** EM CONSTRUÇÃO
**Primeira tarefa:** T-061 (Unit tests)
