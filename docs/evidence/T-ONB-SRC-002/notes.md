# Notes — T-ONB-SRC-002 (Planalto Onboarding)

**Data:** 2026-01-30
**Executor:** ORQ (Agente Orquestrador)
**Status:** ✅ DONE com METADATA_ONLY (fail-closed)

---

## Resumo Executivo

Onboarding de SRC-002 (Planalto - Legislação federal) resultou em **METADATA_ONLY** por falta de evidências verificáveis (robots/ToS/licença).

**Policy Gate Decision:** METADATA_ONLY (fail-closed)

---

## Descobertas

1. **Robots.txt:** Fetch falhou (erro de conexão). Não foi possível confirmar regras.
2. **ToS/Licença:** Não localizados nem confirmados com evidência.
3. **Conectividade:** Requests para homepage e ccivil_03 falharam (erro de conexão).
4. **DUV:** DUV-005 aberta para revalidar conectividade/robots/ToS.

---

## Decisões

1. **Policy gate:** METADATA_ONLY (fail-closed)
2. **Fundamentação legal:** Não confirmada com evidência primária (ToS/licença)
3. **Rate limit:** 0.3 rps (conservador, conforme sources.yaml)
4. **PII detection:** Obrigatória (mesmo para legislação)
5. **Citação:** Obrigatória (boa prática + rastreabilidade)

---

## Evidências criadas

- [x] `license_analysis.md` (análise com incertezas, sem evidência oficial)
- [x] `fetch_test.log` (requests falharam — erro de conexão)
- [x] `sample_urls.txt` (4 URLs golden: Constituição, LGPD, CDC, índice)
- [x] `notes.md` (este arquivo)
- [x] `robots.txt` (arquivo criado com status de falha de fetch)
- [ ] `tos_screenshot.png` (ToS oficial não localizado)

---

## Como validar

1. Verificar se `configs/sources.yaml` mantém METADATA_ONLY
2. Verificar se `Fontes_Licencas.md` registra METADATA_ONLY + pendências de ToS/licença
3. Testar fetch de URL golden:
   ```powershell
   Invoke-WebRequest -Uri "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm" -UseBasicParsing -TimeoutSec 30
   ```

---

## Lições aprendidas

- **Sem evidência primária, não aprovar fulltext:** Fail-closed deve prevalecer
- **Erros de conexão não equivalem a permissão:** Tratar como bloqueio temporário para scraping
- **Manter METADATA_ONLY até confirmação formal**

---

## Tempo gasto

- Análise + execução: ~15 min
- Documentação: ~8 min
- Total: ~23 min

---

**Status final:** T-ONB-SRC-002 → DONE (com resultado METADATA_ONLY)
**Próxima tarefa:** T-ONB-SRC-003 (IBGE)

---
