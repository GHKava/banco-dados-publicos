# WorkOrder T-ONB-SRC-002 — Onboarding SRC-002 (Planalto - Legislação)

**ID:** T-ONB-SRC-002
**Data criação:** 20260130
**Persona:** PM + LEGAL
**Roadmap link:** [[Roadmap detalhado do Projeto#T-ONB-SRC-002]]

---

## 1. Objetivo

Realizar compliance check completo para SRC-002 (Planalto - Legislação federal) verificando robots.txt, ToS, licença e criando evidence pack para aprovar ou bloquear ingestão de texto integral.

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-004 (Allowlist + sources.yaml) completa
- [x] Template de onboarding disponível
- [x] SRC-002 cadastrado em sources.yaml com status "unknown"
- [x] Persona PM+LEGAL designada
- [x] Lições de T-ONB-SRC-001 aplicadas (fail-closed, WAF awareness)

---

## 3. Entradas

- `configs/sources.yaml` (entrada SRC-002 com domínios base e policy inicial METADATA_ONLY)
- `_OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md`
- URLs de referência:
  - https://www.planalto.gov.br/
  - https://www.planalto.gov.br/ccivil_03/
  - https://www.planalto.gov.br/robots.txt

---

## 4. Saídas (Artefatos esperados)

- `_OBSIDIAN/Organização do Projeto/Onboarding/SRC-002 - Planalto.md` (checklist preenchido)
- `docs/evidence/T-ONB-SRC-002/`:
  - `robots.txt` (cópia do robots.txt da fonte)
  - `tos_screenshot.png` (screenshot de ToS/licença - se existir)
  - `license_analysis.md` (análise de licença e permissões)
  - `sample_urls.txt` (3+ URLs golden para testes)
  - `fetch_test.log` (teste de fetch simples)
  - `notes.md` (resumo e decisão de policy gate)
- `_OBSIDIAN/Organização do Projeto/Fontes_Licencas.md` (atualizado com SRC-002)
- Atualização em `configs/sources.yaml` (se necessário upgrade)

---

## 5. Comandos previstos

```powershell
# Fetch robots.txt
Invoke-WebRequest -Uri "https://www.planalto.gov.br/robots.txt" -OutFile "docs/evidence/T-ONB-SRC-002/robots.txt" -UserAgent "PublicDataPipelineBot/1.0" -TimeoutSec 30

# Teste de fetch básico (página principal)
Invoke-WebRequest -Uri "https://www.planalto.gov.br/" -UseBasicParsing -TimeoutSec 30 | Select-Object StatusCode, Headers

# Teste de fetch legislação (ccivil_03)
Invoke-WebRequest -Uri "https://www.planalto.gov.br/ccivil_03/" -UseBasicParsing -TimeoutSec 30 | Select-Object StatusCode, Headers
```

---

## 6. Riscos

| Risco                                   | Severidade | Mitigação                                                                  |
| --------------------------------------- | ---------- | -------------------------------------------------------------------------- |
| Proteção WAF (como SRC-001)             | Média      | Fail-closed: manter METADATA_ONLY ou BLOCK                                 |
| Licença/ToS não encontrados             | Média      | Fail-closed: METADATA_ONLY                                                 |
| Robots.txt proíbe scraping              | Média      | Bloquear scraping; buscar alternativa (sitemap/RSS)                        |
| Conteúdo legislativo = domínio público? | Baixa      | Verificar ToS; legislação é pública mas redistribuição pode ter restrições |
| PII em documentos legais                | Baixa      | Legislação geralmente não contém PII, mas detecção obrigatória             |

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

T-ONB-SRC-003: Onboarding SRC-003 (IBGE)

---

**Criado por:** ORQ
**Data:** 20260130
**Rodada:** #9

---
