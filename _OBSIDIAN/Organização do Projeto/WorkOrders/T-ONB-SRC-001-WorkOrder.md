# WorkOrder T-ONB-SRC-001 — Onboarding SRC-001 (DOU - Diário Oficial da União)

**ID:** T-ONB-SRC-001
**Data criação:** 20260130
**Persona:** PM + LEGAL
**Roadmap link:** [[Roadmap detalhado do Projeto#T-ONB-SRC-001]]

---

## 1. Objetivo

Realizar compliance check completo para SRC-001 (Diário Oficial da União) verificando robots.txt, ToS, licença e criando evidence pack para aprovar (ou bloquear) ingestão de texto integral.

---

## 2. DoR Checklist (antes de iniciar)

- [x] T-004 (Allowlist + sources.yaml) completa
- [x] Template de onboarding disponível
- [x] SRC-001 cadastrado em sources.yaml com status "unknown"
- [x] Persona PM+LEGAL designada
- [x] Critérios de aceite: evidence pack + decisão de policy gate

---

## 3. Entradas

- `configs/sources.yaml` (entrada SRC-001 com domínios base e policy inicial METADATA_ONLY)
- `_OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md`
- URLs de referência:
  - https://www.in.gov.br/
  - https://www.in.gov.br/leiturajornal
  - https://www.in.gov.br/robots.txt

---

## 4. Saídas (Artefatos esperados)

- `_OBSIDIAN/Organização do Projeto/Onboarding/SRC-001 - DOU.md` (checklist preenchido)
- `docs/evidence/T-ONB-SRC-001/`:
  - `robots.txt` (cópia do robots.txt da fonte)
  - `tos_screenshot.png` (screenshot de ToS/licença - se existir)
  - `license_analysis.md` (análise de licença e permissões)
  - `sample_urls.txt` (3+ URLs golden para testes)
  - `fetch_test.log` (teste de fetch simples)
  - `notes.md` (resumo e decisão de policy gate)
- `_OBSIDIAN/Organização do Projeto/Fontes_Licencas.md` (atualizado com SRC-001)
- Atualização em `configs/sources.yaml` (se necessário upgrade de METADATA_ONLY para ALLOW_FULLTEXT)

---

## 5. Comandos previstos

```powershell
# Fetch robots.txt
Invoke-WebRequest -Uri "https://www.in.gov.br/robots.txt" -OutFile "docs/evidence/T-ONB-SRC-001/robots.txt"

# Teste de fetch básico
Invoke-WebRequest -Uri "https://www.in.gov.br/" -UseBasicParsing | Select-Object StatusCode, Headers

# Verificar conectividade
Test-NetConnection -ComputerName "www.in.gov.br" -Port 443
```

---

## 6. Riscos

| Risco                         | Severidade | Mitigação                                                     |
| ----------------------------- | ---------- | ------------------------------------------------------------- |
| Licença/ToS não encontrados   | Média      | Fail-closed: manter METADATA_ONLY                             |
| Robots.txt proíbe scraping    | Média      | Bloquear scraping; ingerir apenas via API oficial (se houver) |
| ToS restringe redistribuição  | Alta       | BLOCK ou METADATA_ONLY apenas                                 |
| Conteúdo dinâmico (JS pesado) | Baixa      | Priorizar RSS/API se disponível                               |
| PII em documentos oficiais    | Média      | Detecção obrigatória (presidio-analyzer)                      |

---

## 7. Evidência mínima necessária

- [x] robots.txt copiado
- [x] ToS/licença analisados (ou documentado ausência)
- [x] 3+ URLs golden selecionados
- [x] Fetch test executado com sucesso
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

T-ONB-SRC-002: Onboarding SRC-002 (Planalto)

---

**Criado por:** ORQ
**Data:** 20260130

---
