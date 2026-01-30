# T-ONB-SRC-003 — Análise de Compliance IBGE

**Data:** 2026-01-31
**Fonte:** SRC-003 (IBGE - servicodados.ibge.gov.br / ibge.gov.br)
**Status:** ANÁLISE CONCLUÍDA (decisão METADATA_ONLY)

---

## 1. Robots.txt

**URL testada:** https://servicodados.ibge.gov.br/robots.txt
**Resultado:** Status 503 (indisponível) — ver `outputs.log`

**Conclusão:** Robots.txt não pôde ser verificado.

---

## 2. Testes de Conectividade

### 2.1 API Docs

- **URL:** https://servicodados.ibge.gov.br/api/docs
- **Status:** 200 OK
- **Conclusão:** Acessível

### 2.2 API Root

- **URL:** https://servicodados.ibge.gov.br/api/
- **Status:** 503 Service Unavailable
- **Conclusão:** Indisponível no momento

---

## 3. Termos de Uso e Licença

- **ToS/Licença oficial:** Não localizada com evidência explícita nesta rodada
- **Observação:** Página principal do IBGE possui links institucionais e política de privacidade, mas sem licença explícita para dados/APIs.

---

## 4. Policy Gate Decision

**Decisão:** METADATA_ONLY (fail-closed)

**Justificativa:**

1. Robots.txt não verificado (503)
2. API root indisponível (503)
3. ToS/licença não localizada com evidência

---

## 5. Próximos passos

1. Revalidar robots.txt e API root quando disponível
2. Buscar termos/licença específica do IBGE para uso das APIs/dados
3. Se licença explícita for encontrada, considerar upgrade para ALLOW_FULLTEXT
