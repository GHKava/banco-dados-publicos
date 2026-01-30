# INSTALACOES.md — Log de instalações de dependências

**Data criação:** 2026-01-30  
**Plataforma:** Windows PowerShell

---

## Histórico de instalações

### 2026-01-30 14:30 UTC — Bootstrap inicial (T-002 futuro)

**Comando:**

```powershell
.\scripts\setup\bootstrap.ps1
```

**Passos executados:**

1. ✅ Verificado Python 3.11+
2. ✅ Criado venv em `venv/`
3. ✅ Instaladas dependências de `requirements.txt`
4. ✅ Configurado pre-commit hooks
5. ✅ Criado `.env` (copiar de `.env.example`)
6. ✅ Docker: Postgres + Redis (se disponível)
7. ✅ Pgvector extension instalada

**Status:** Aguardando execução em T-002

---

## Dependências principais instaladas

| Pacote                | Versão  | Objetivo          |
| --------------------- | ------- | ----------------- |
| fastapi               | 0.104.1 | API REST          |
| sqlalchemy            | 2.0.23  | ORM               |
| psycopg2-binary       | 2.9.9   | Driver PostgreSQL |
| redis                 | 5.0.1   | Cliente Redis     |
| rq                    | 1.14.1  | Job queue         |
| sentence-transformers | 2.2.2   | Embeddings        |
| trafilatura           | 1.6.5   | Parsing HTML      |
| presidio-analyzer     | 2.2.354 | PII detection     |
| pytest                | 7.4.3   | Testing           |
| black                 | 23.12.0 | Code formatter    |
| mypy                  | 1.7.1   | Type checker      |
| pre-commit            | 3.5.0   | Git hooks         |

---

## Notas

- Python 3.11+ é obrigatório (verificar com `python --version`)
- `.env` deve ser preenchido manualmente com dados reais (DB_URL, API_KEY, etc.)
- Docker é opcional mas recomendado (simplifica Postgres/Redis)
- OCR (pytesseract) é opcional; requer instalação do Tesseract no sistema

---

## Para reinstalar

```powershell
# Limpar venv
Remove-Item -Recurse -Force venv/

# Rodar bootstrap novamente
.\scripts\setup\bootstrap.ps1
```

---

**Mantido por:** TL (Tech Lead)

---
