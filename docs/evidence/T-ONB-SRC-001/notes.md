# Notes — T-ONB-SRC-001 (DOU Onboarding)

**Data:** 2026-01-30
**Executor:** ORQ (Agente Orquestrador)
**Status:** COMPLETED com BLOCK (fail-closed)

---

## Resumo Executivo

Tentativa de onboarding de SRC-001 (Diário Oficial da União - in.gov.br) resultou em **BLOCK provisório** devido a proteção anti-bot (Azion WAF).

**Policy Gate Decision:** METADATA_ONLY → upgrade para **BLOCK** (não ingerir até autorização formal)

---

## Descobertas

1. **Proteção WAF:** Site protegido por Azion CDN/WAF com bloqueio 403 em tentativas de scraping
2. **Robots.txt inacessível:** Não foi possível verificar robots.txt (bloqueado)
3. **LAI aplicável:** Conteúdo é governamental (LAI nº 12.527/2011), mas acesso deve ser por meios oficiais
4. **Sem API oficial identificada:** Não foi encontrada API documentada para acesso programático

---

## Decisões

1. **DUV-004 criada:** "Como obter dados do DOU sem violar proteção anti-bot?"
2. **Status atualizado em sources.yaml:** `default_storage_mode: BLOCK` (provisório)
3. **Próximos passos:**
   - Verificar dados.gov.br para API oficial
   - Pesquisar feeds RSS oficiais
   - Considerar contato formal com Imprensa Nacional

---

## Evidências criadas

- [x] `license_analysis.md` (análise de LAI + legislação aplicável)
- [x] `fetch_test.log` (log de tentativa de fetch com erro 403)
- [x] `sample_urls.txt` (URLs golden para testes futuros)
- [x] `notes.md` (este arquivo)
- [ ] `robots.txt` (não obtido - bloqueado)
- [ ] `tos_screenshot.png` (não obtido - ToS não localizado)

---

## Como validar

1. Verificar se DUV-004 foi criada no Backlog
2. Verificar se `configs/sources.yaml` foi atualizado com status BLOCK
3. Verificar se `Fontes_Licencas.md` foi atualizado com SRC-001

---

## Lições aprendidas

- **Fail-closed funciona:** Bloqueio proativo evitou violação de ToS/proteção anti-bot
- **Scraping != acesso público:** Dados públicos não significa scraping permitido
- **APIs oficiais são preferíveis:** Para fontes governamentais, sempre buscar API oficial primeiro

---

## Tempo gasto

- Análise + execução: ~15 min
- Documentação: ~10 min
- Total: ~25 min

---

**Status final:** T-ONB-SRC-001 → DONE (com resultado BLOCK provisório)
**Próxima tarefa:** T-ONB-SRC-002 (Planalto)

---
