# WorkOrder T-ONB-SRC-005 — Onboarding SRC-005 (dados.gov.br)

**ID:** T-ONB-SRC-005
**Data criação:** 20260131
**Persona:** PM + LEGAL
**Roadmap link:** [[Roadmap detalhado do Projeto#T-ONB-SRC-005]]

---

## 1. Objetivo

Realizar compliance check completo para SRC-005 (dados.gov.br — catálogo CKAN) verificando robots.txt, ToS, licença e criando evidence pack para aprovar ou bloquear ingestão.

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-004 (Allowlist + sources.yaml) completa
- [x] Template de onboarding disponível
- [x] SRC-005 cadastrado em sources.yaml com status "unknown"
- [x] Persona PM+LEGAL designada

---

## 3. Entradas

- `configs/sources.yaml` (entrada SRC-005 com domínios base e policy inicial)
- `_OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md`
- URLs de referência:
  - https://dados.gov.br/
  - https://dados.gov.br/api/3
  - https://dados.gov.br/robots.txt
  - https://dados.gov.br/faq

---

## 4. Saídas (Artefatos esperados)

- `_OBSIDIAN/Organização do Projeto/Onboarding/SRC-005 - dados.gov.br.md` (checklist preenchido)
- `docs/evidence/T-ONB-SRC-005/`:
  - `robots.txt` (cópia do robots.txt da fonte)
  - `tos_screenshot.png` (screenshot de ToS/licença - se existir)
  - `license_analysis.md` (análise de licença e permissões)
  - `sample_urls.txt` (3+ URLs golden para testes)
  - `fetch_test.log` (teste de fetch simples)
  - `notes.md` (resumo e decisão de policy gate)
- `_OBSIDIAN/Organização do Projeto/Fontes_Licencas.md` (atualizado com SRC-005)
- `configs/sources.yaml` (ajustar default_storage_mode conforme decisão)

---

## 5. Comandos previstos

```powershell
# Fetch robots.txt
Invoke-WebRequest -Uri "https://dados.gov.br/robots.txt" -OutFile "docs/evidence/T-ONB-SRC-005/robots.txt" -UserAgent "PublicDataPipelineBot/1.0" -TimeoutSec 30

# Teste de fetch homepage
Invoke-WebRequest -Uri "https://dados.gov.br/" -UseBasicParsing -TimeoutSec 30 | Select-Object StatusCode, Headers

# Teste de fetch API CKAN
Invoke-WebRequest -Uri "https://dados.gov.br/api/3/action/status_show" -UseBasicParsing -TimeoutSec 30 | Select-Object StatusCode, Headers
```

---

## 6. Riscos

| Risco                          | Severidade | Mitigação                                          |
| ------------------------------ | ---------- | -------------------------------------------------- |
| Licenças variáveis por dataset | Alta       | Fail-closed: METADATA_ONLY até licença por dataset |
| ToS/licença não encontrados    | Média      | Fail-closed: METADATA_ONLY                         |
| Robots.txt proíbe scraping     | Média      | BLOCK ou METADATA_ONLY                             |
| PII em datasets                | Alta       | PII detection obrigatória                          |

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

- [x] Checklist completo (100% preenchido)
- [x] Evidence pack com 6 arquivos mínimos
- [x] Policy gate decision validada (METADATA_ONLY | ALLOW_FULLTEXT | BLOCK)
- [x] Sem DUVs bloqueantes (ou DUVs criadas no Backlog)

---

## 9. Próximo passo (tarefa dependente)

T-009: Bot - robots checker (após onboarding concluído)

---

**Criado por:** ORQ
**Data:** 20260131
**Rodada:** #10
