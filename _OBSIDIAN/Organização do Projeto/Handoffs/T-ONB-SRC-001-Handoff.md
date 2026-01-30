# Handoff — T-ONB-SRC-001 (DOU Onboarding)

**Data:** 2026-01-30
**Executor:** ORQ (Agente Orquestrador)
**Persona:** PM + LEGAL
**Status:** ✅ DONE (resultado: BLOCK provisório)

---

## 🎯 O que foi feito

Realizado compliance check completo para SRC-001 (Diário Oficial da União - in.gov.br) com resultado **BLOCK provisório** devido a proteção anti-bot.

**Artefatos criados:**
1. WorkOrder completo ([T-ONB-SRC-001-WorkOrder.md](../WorkOrders/T-ONB-SRC-001-WorkOrder.md))
2. Evidence Pack em `docs/evidence/T-ONB-SRC-001/`:
   - `license_analysis.md` (análise de LAI + legislação)
   - `fetch_test.log` (log de tentativa com erro 403)
   - `sample_urls.txt` (URLs golden para testes futuros)
   - `notes.md` (resumo + decisões)
3. Atualização em `Fontes_Licencas.md` (SRC-001 marcado como BLOCKED)
4. Atualização em `configs/sources.yaml` (default_storage_mode: BLOCK)
5. DUV-004 criada no Backlog

---

## 🔴 Decisões críticas

### Policy Gate Decision: BLOCK (fail-closed)

**Justificativa:**
1. **Proteção WAF ativa:** Azion CDN bloqueou fetch de robots.txt com 403 Forbidden
2. **Robots.txt inacessível:** Não foi possível verificar regras de scraping
3. **ToS não localizado:** Termos de uso não encontrados em página oficial
4. **Princípio de precaução:** Dados públicos ≠ scraping permitido

### Licença identificada (provável)
- **LAI (Lei 12.527/2011):** Garante acesso a informações públicas
- **Marco Civil (Lei 12.965/2014):** Princípios de abertura
- **MAS:** Acesso público ≠ autorização para scraping automatizado

---

## 🚨 Impedimentos e DUVs

**DUV-004 criada:** "Como obter dados do DOU sem violar proteção anti-bot?"

**Próximos passos sugeridos:**
1. Verificar se DOU está catalogado em dados.gov.br com API oficial
2. Pesquisar feeds RSS oficiais (https://www.in.gov.br/rss)
3. Considerar contato formal com Imprensa Nacional (LAI)
4. Alternativa: usar apenas metadados públicos até autorização formal

---

## 📋 Evidências e validação

**Evidence Pack:** [docs/evidence/T-ONB-SRC-001/](../../docs/evidence/T-ONB-SRC-001/)

**Arquivos criados:**
- [x] `license_analysis.md` (3 seções: robots, ToS, legislação)
- [x] `fetch_test.log` (erro 403 documentado)
- [x] `sample_urls.txt` (3 URLs golden)
- [x] `notes.md` (resumo + tempo gasto)
- [ ] `robots.txt` (não obtido - bloqueado)
- [ ] `tos_screenshot.png` (não obtido - ToS não localizado)

**Como validar:**
```powershell
# Verificar evidence pack
Test-Path "C:\Dev\banco-dados-publicos\docs\evidence\T-ONB-SRC-001\*.md"

# Verificar sources.yaml atualizado
Select-String -Path "C:\Dev\banco-dados-publicos\configs\sources.yaml" -Pattern "BLOCK"

# Verificar DUV-004 no Backlog
Select-String -Path "C:\Dev\banco-dados-publicos\_OBSIDIAN\Organização do Projeto\Backlog.md" -Pattern "DUV-004"
```

---

## 🔄 Mudanças nos arquivos

| Arquivo                  | Mudança                                      | Motivo                          |
| ------------------------ | -------------------------------------------- | ------------------------------- |
| `sources.yaml`           | SRC-001: default_storage_mode = BLOCK        | Proteção WAF + ToS não verificado |
| `Fontes_Licencas.md`     | SRC-001 marcado como BLOCKED PROVISORIAMENTE | Policy gate fail-closed         |
| `Backlog.md`             | DUV-004 criada + T-ONB-SRC-001 DONE          | Documentar impedimento          |
| `WorkOrders/T-ONB-SRC-001-WorkOrder.md` | Criado                        | DoR + Artefatos + Riscos        |

---

## 🎓 Lições aprendidas

1. **Fail-closed funciona:** Bloqueio proativo evitou violação de ToS
2. **Scraping ≠ acesso público:** LAI garante acesso humano, não scraping automatizado
3. **APIs oficiais são preferíveis:** Para fontes gov, sempre buscar API primeiro
4. **Proteção anti-bot é indicador:** WAF/CDN indica que scraping não é welcome
5. **Evidência é obrigatória:** Sem robots.txt/ToS → BLOCK (não assumir permissão)

---

## ⏭️ Próxima tarefa sugerida

**T-ONB-SRC-002:** Onboarding SRC-002 (Planalto - Legislação)
**Dependências:** T-004 ✅ DONE
**DoR:** Template disponível, sources.yaml pronto

---

## 📊 Métricas

- **Tempo total:** ~25 min (análise + documentação)
- **Retry count:** 0 (fail-fast em 403)
- **Arquivos criados:** 5 (WorkOrder + 4 evidence)
- **Arquivos modificados:** 2 (sources.yaml, Fontes_Licencas.md, Backlog.md)

---

**Aprovado por:** ORQ
**Data:** 2026-01-30 23:15 UTC

---
