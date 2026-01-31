# Handoff — T-ONB-SRC-002 (Planalto Onboarding)

**Data:** 2026-01-30  
**Executor:** ORQ (Agente Orquestrador)  
**Persona:** PM + LEGAL  
**Status:** ✅ DONE (resultado: ALLOW_FULLTEXT)

---

## 🎯 O que foi feito

Realizado compliance check completo para SRC-002 (Planalto - Legislação federal) com resultado **ALLOW_FULLTEXT** com fundamentação legal robusta.

**Artefatos criados:**
1. WorkOrder completo ([T-ONB-SRC-002-WorkOrder.md](../WorkOrders/T-ONB-SRC-002-WorkOrder.md))
2. Evidence Pack em `docs/evidence/T-ONB-SRC-002/`:
   - `license_analysis.md` (análise legal: Lei 9.610/1998, Art. 8º, IV + LAI)
   - `fetch_test.log` (3 testes: robots.txt 404, homepage 200, ccivil_03 200)
   - `sample_urls.txt` (4 URLs golden: Constituição, LGPD, CDC, índice)
   - `notes.md` (resumo + decisões)
3. Atualização em `Fontes_Licencas.md` (SRC-002 marcado como ALLOW_FULLTEXT)
4. Atualização em `configs/sources.yaml` (default_storage_mode: ALLOW_FULLTEXT)
5. Handoff criado (este arquivo)

---

## ✅ Decisões críticas

### Policy Gate Decision: ALLOW_FULLTEXT (upgrade aprovado)

**Justificativa:**
1. **Legislação = domínio público:** Lei 9.610/1998, Art. 8º, IV garante que atos oficiais não têm proteção autoral
2. **Robots.txt ausente (404):** Sem restrições explícitas por RFC 9309
3. **LAI aplicável:** Lei 12.527/2011 reforça acesso a informações públicas
4. **Sem proteção WAF:** Site acessível sem bloqueios (diferente de SRC-001)
5. **Conectividade confirmada:** Homepage (200 OK) + ccivil_03 (200 OK)

### Licença identificada (confirmada)
- **Lei 9.610/1998, Art. 8º, IV:** "Não são objeto de proteção como direitos autorais [...] os textos de tratados ou convenções, leis, decretos, regulamentos, decisões judiciais e demais atos oficiais"
- **Jurisprudência consolidada:** Legislação é de livre acesso e reprodução
- **LAI (Lei 12.527/2011):** Garante acesso a informações públicas governamentais

---

## 🚨 Condições e restrições

**Rate limit conservador:**
- 0.3 rps (1 request a cada ~3.3 segundos)
- Concurrency: 1
- Budget: 500 URLs/dia, 50 MB/dia

**Obrigações:**
- User-agent honesto e identificável
- Citação de fonte obrigatória (boa prática + rastreabilidade)
- PII detection ativa (mesmo para legislação)

---

## 📋 Evidências e validação

**Evidence Pack:** [docs/evidence/T-ONB-SRC-002/](../../docs/evidence/T-ONB-SRC-002/)

**Arquivos criados:**
- [x] `license_analysis.md` (análise legal completa)
- [x] `fetch_test.log` (3 testes documentados)
- [x] `sample_urls.txt` (4 URLs golden)
- [x] `notes.md` (resumo + tempo gasto)
- [ ] `robots.txt` (não existe - 404)
- [ ] `tos_screenshot.png` (ToS oficial não localizado)

**Como validar:**
```powershell
# Verificar evidence pack
Test-Path "C:\Dev\banco-dados-publicos\docs\evidence\T-ONB-SRC-002\*.md"

# Verificar sources.yaml atualizado
Select-String -Path "C:\Dev\banco-dados-publicos\configs\sources.yaml" -Pattern "ALLOW_FULLTEXT"

# Teste de fetch (URL golden)
Invoke-WebRequest -Uri "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm" -UseBasicParsing -TimeoutSec 30
```

---

## 🔄 Mudanças nos arquivos

| Arquivo                  | Mudança                                      | Motivo                          |
| ------------------------ | -------------------------------------------- | ------------------------------- |
| `sources.yaml`           | SRC-002: default_storage_mode = ALLOW_FULLTEXT | Legislação = domínio público (Lei 9.610/1998) |
| `Fontes_Licencas.md`     | SRC-002 marcado como ALLOW_FULLTEXT          | Fundamentação legal + robots.txt ausente |
| `WorkOrders/T-ONB-SRC-002-WorkOrder.md` | Criado                        | DoR + Artefatos + Riscos        |
| `Handoffs/T-ONB-SRC-002-Handoff.md` | Criado (este arquivo)       | Documentação de decisões        |

---

## 🎓 Lições aprendidas

1. **Legislação federal = domínio público:** Lei 9.610/1998, Art. 8º, IV é fundamentação legal sólida
2. **Robots.txt ausente ≠ permissão automática:** Verificar ToS/licença antes de assumir permissão (mas para legislação, domínio público prevalece)
3. **Diferença entre fontes:** SRC-001 (WAF) vs. SRC-002 (sem WAF) indica políticas diferentes
4. **Fail-closed com exceção legal:** Mesmo sem robots.txt/ToS, legislação tem status especial por lei
5. **Rate limit conservador é sempre boa prática:** Mesmo com permissão legal

---

## ⏭️ Próxima tarefa sugerida

**T-ONB-SRC-003:** Onboarding SRC-003 (IBGE - APIs e Dados)  
**Dependências:** T-004 ✅ DONE  
**DoR:** Template disponível, sources.yaml pronto  
**Características:** API oficial, provável CC-BY, rate limit maior (1.0 rps)

---

## 📊 Métricas

- **Tempo total:** ~23 min (análise + documentação)
- **Retry count:** 0 (sucesso no primeiro fetch)
- **Arquivos criados:** 5 (WorkOrder + 4 evidence)
- **Arquivos modificados:** 2 (sources.yaml, Fontes_Licencas.md)
- **URLs testadas:** 3 (robots.txt, homepage, ccivil_03)
- **Policy gate:** METADATA_ONLY → ALLOW_FULLTEXT (upgrade)

---

**Aprovado por:** ORQ  
**Data:** 2026-01-30 23:40 UTC  
**Rodada:** #9

---
