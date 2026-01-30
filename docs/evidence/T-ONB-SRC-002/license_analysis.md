# T-ONB-SRC-002 — Análise de Compliance Planalto

**Data:** 2026-01-30
**Fonte:** SRC-002 (Planalto - Legislação federal - planalto.gov.br)
**Status:** ANÁLISE CONCLUÍDA (decisão METADATA_ONLY)

---

## 1. Robots.txt

**Tentativa de fetch:** ❌ FALHA DE CONEXÃO
**URL testada:** https://www.planalto.gov.br/robots.txt
**Resultado:** Erro de conexão durante requisição (ver `outputs.log`)

**Conclusão:** Robots.txt não pôde ser verificado.

**Interpretação:**

- Sem verificação de robots.txt, **não é possível assumir permissão**
- Fail-closed → **METADATA_ONLY**

**Ação:** Repetir verificação em ambiente com conectividade estável.

---

## 2. Testes de Conectividade

### 2.1 Homepage

- **URL:** https://www.planalto.gov.br/
- **Status:** ❌ Falha de conexão
- **Conclusão:** ❌ Não foi possível confirmar acesso

### 2.2 Seção Legislação (ccivil_03)

- **URL:** https://www.planalto.gov.br/ccivil_03/
- **Status:** ❌ Falha de conexão
- **Conclusão:** ❌ Não foi possível confirmar acesso

**Observação:** Não foi possível confirmar ausência de WAF/bloqueio.

---

## 3. Termos de Uso e Licença

### 3.1 Portal da Presidência da República

- **URL base:** https://www.planalto.gov.br/
- **Natureza:** Portal governamental brasileiro (legislação federal)

### 3.2 Legislação aplicável

- **LAI (Lei 12.527/2011):** Garante acesso a informações públicas
- **Lei de Direitos Autorais (Lei 9.610/1998, Art. 8º, IV):** **Textos de tratados ou convenções, leis, decretos, regulamentos, decisões judiciais e demais atos oficiais NÃO são protegidos por direitos autorais**
- **Marco Civil da Internet (Lei 12.965/2014):** Princípios de abertura

### 3.3 Análise de permissões

**HIPÓTESE (não verificada):**

- Legislação federal pode ter acesso público, porém **sem evidência oficial de licença/ToS**

**EVIDÊNCIA LEGAL:**

- Não coletada nesta rodada (falha de conectividade e ausência de ToS/licença)

**RISCO RESIDUAL:**

- ToS desconhecida pode proibir scraping
- Sem robots.txt verificado, risco de violar regras de crawl

---

## 4. Policy Gate Decision (PROVISÓRIA)

**Decisão:** METADATA_ONLY (fail-closed)

**Justificativa:**

1. Robots.txt não verificado (falha de conexão)
2. ToS/licença não localizadas com evidência
3. Conectividade falhou (homepage e ccivil_03)
4. Fail-closed → METADATA_ONLY

**Condições:**

- Rate limit conservador (0.3 rps, conforme sources.yaml)
- User-agent honesto e identificável
- PII detection ativa (mesmo em legislação)
- Repetir verificação de robots.txt/ToS antes de qualquer upgrade

**Upgrade para ALLOW_FULLTEXT:**

- ❌ NÃO APROVADO nesta rodada (sem evidência de licença/ToS e falha de conectividade)

---

## 5. Próximos passos

1. ✅ Manter sources.yaml: default_storage_mode = METADATA_ONLY
2. ✅ Atualizar Fontes_Licencas.md com pendências de verificação
3. ✅ Selecionar 3 URLs golden para testes
4. ✅ Criar notes.md com decisões

**Revisão:** Repetir verificação quando conectividade permitir.

---

## 6. URLs Golden (para testes)

1. https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm (Constituição Federal)
2. https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (LGPD)
3. https://www.planalto.gov.br/ccivil_03/leis/l8078.htm (CDC - Código de Defesa do Consumidor)

---

**Criado por:** ORQ
**Data:** 2026-01-30 23:35 UTC

---
