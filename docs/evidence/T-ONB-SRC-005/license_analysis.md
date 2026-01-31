# T-ONB-SRC-005 — Análise de Compliance dados.gov.br

**Data:** 2026-01-31  
**Fonte:** SRC-005 (dados.gov.br)  
**Status:** ANÁLISE CONCLUÍDA (decisão METADATA_ONLY)

---

## 1. Robots.txt

**URL testada:** https://dados.gov.br/robots.txt  
**Resultado:** 200 OK, mas conteúdo retornou HTML do portal (não regras de robots)

**Conclusão:** robots.txt **não verificado** (conteúdo inválido para robots). Tratar como não disponível.

---

## 2. Testes de Conectividade

### 2.1 Homepage

- **URL:** https://dados.gov.br/
- **Status:** 200 OK

### 2.2 API CKAN

- **URL:** https://dados.gov.br/api/3/action/status_show
- **Status:** 200 OK

---

## 3. Termos de Uso / Licença

- **ToS / Política:** páginas exigem login gov.br (não acessíveis sem autenticação)
  - https://dados.gov.br/termos-de-uso
  - https://dados.gov.br/politica-de-privacidade
  - https://dados.gov.br/faq

**Conclusão:** Licença não verificável nesta rodada. Licença é **variável por dataset** (CKAN).

---

## 4. Policy Gate Decision

**Decisão:** METADATA_ONLY (fail-closed)

**Justificativa:**

1. robots.txt não verificável (HTML retornado)
2. ToS/licença não acessíveis sem login
3. Licenças variáveis por dataset

---

## 5. Próximos passos

1. Verificar robots.txt real (se disponível por outro endpoint)
2. Acessar ToS/licença com evidência (login gov.br)
3. Verificar licença por dataset específico antes de ALLOW_FULLTEXT
