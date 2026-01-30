# WorkOrder T-ONB-SRC-003 — Onboarding SRC-003 (IBGE)

**ID:** T-ONB-SRC-003
**Data criação:** 20260131
**Persona:** PM + LEGAL
**Roadmap link:** [[Roadmap detalhado do Projeto#T-ONB-SRC-003]]

---

## 1. Objetivo

Realizar compliance check completo para SRC-003 (IBGE APIs e dados) verificando robots.txt, ToS, licença e criando evidence pack para aprovar ou bloquear ingestão.

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-004 (Allowlist + sources.yaml) completa
- [x] Template de onboarding disponível
- [x] SRC-003 cadastrado em sources.yaml com status "unknown"
- [x] Persona PM+LEGAL designada

---

## 3. Entradas

- `configs/sources.yaml` (entrada SRC-003 com domínios base e policy inicial)
- `_OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md`
- URLs de referência:
  - https://servicodados.ibge.gov.br/api/docs
  - https://servicodados.ibge.gov.br/api/
  - https://servicodados.ibge.gov.br/robots.txt
  - https://www.ibge.gov.br/

---

## 4. Saídas (Artefatos esperados)

- `_OBSIDIAN/Organização do Projeto/Onboarding/SRC-003 - IBGE.md` (checklist preenchido)
- `docs/evidence/T-ONB-SRC-003/`:
  - `robots.txt` (cópia do robots.txt da fonte)
  - `tos_screenshot.png` (screenshot de ToS/licença - se existir)
  - `license_analysis.md` (análise de licença e permissões)
  - `sample_urls.txt` (3+ URLs golden para testes)
  - `fetch_test.log` (teste de fetch simples)
  - `notes.md` (resumo e decisão de policy gate)
- `_OBSIDIAN/Organização do Projeto/Fontes_Licencas.md` (atualizado com SRC-003)
- `configs/sources.yaml` (ajustar default_storage_mode conforme decisão)

---

## 5. Comandos previstos

```powershell
# Fetch robots.txt
Invoke-WebRequest -Uri "https://servicodados.ibge.gov.br/robots.txt" -OutFile "docs/evidence/T-ONB-SRC-003/robots.txt" -UserAgent "PublicDataPipelineBot/1.0" -TimeoutSec 30

# Teste de fetch API docs
Invoke-WebRequest -Uri "https://servicodados.ibge.gov.br/api/docs" -UseBasicParsing -TimeoutSec 30 | Select-Object StatusCode, Headers

# Teste de fetch endpoint API
Invoke-WebRequest -Uri "https://servicodados.ibge.gov.br/api/" -UseBasicParsing -TimeoutSec 30 | Select-Object StatusCode, Headers
```

---

## 6. Riscos

| Risco                             | Severidade | Mitigação                             |
| --------------------------------- | ---------- | ------------------------------------- |
| ToS/licença não encontrados       | Média      | Fail-closed: METADATA_ONLY            |
| Rate limits de API (throttling)   | Média      | Respeitar rps e headers de rate-limit |
| Conteúdo com PII (dados pessoais) | Média      | PII detection obrigatória             |
| Robots.txt proíbe scraping        | Média      | BLOCK ou METADATA_ONLY                |

---

## 7. Evidência mínima necessária

- [x] robots.txt copiado (ou documentado bloqueio)
- [x] ToS/licença analisados (ou documentado ausência)
- [x] 3+ URLs golden selecionados
- [x] Fetch test executado
- [x] Policy gate decision documentada
- [x] notes.md com justificativa

---

## 8. Quality Gate aplicável

- [ ] Checklist completo (100% preenchido)
- [ ] Evidence pack com 6 arquivos mínimos
- [ ] Policy gate decision validada (METADATA_ONLY | ALLOW_FULLTEXT | BLOCK)
- [ ] Sem DUVs bloqueantes (ou DUVs criadas no Backlog)

---

## 9. Próximo passo (tarefa dependente)

T-ONB-SRC-004: Onboarding SRC-004 (BCB)

---

**Criado por:** ORQ
**Data:** 20260131
**Rodada:** #9
