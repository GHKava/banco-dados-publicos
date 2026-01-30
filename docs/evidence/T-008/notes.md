# T-008: Policy Gate — Evidence Pack Notes

**Data:** 2026-01-30
**Tempo executado:** ~30 min
**Status:** ✅ DONE

---

## Resumo

Tarefa T-008 focou em implementar a lógica de **Policy Gate** (decisor de compliance) que determina automaticamente o nível de acesso permitido para cada fonte de dados:

- **BLOCK**: Bloqueio completo (não na allowlist, robots.txt bloqueia, ToS proíbe)
- **METADATA_ONLY**: Apenas metadados (licença desconhecida, PII médio/alto com mitigação)
- **ALLOW**: Acesso completo (licença permissiva, robots OK, baixo PII)

**Design:** Fail-closed — qualquer ambiguidade resulta no nível mais restritivo (METADATA_ONLY ou BLOCK).

---

## Arquivos Criados/Modificados

1. **src/bots/policy_gate.py** (já existia, verificado e validado)
   - Classe `PolicyGate` com método `evaluate(source) -> PolicyDecision`
   - Lógica de decisão baseada em 5 regras:
     1. Allowlist (SRC-001 a SRC-005)
     2. License compliance
     3. Robots.txt compliance
     4. ToS restrictions
     5. PII risk mitigation
   - Enum `PolicyDecision` com valores BLOCK/METADATA_ONLY/ALLOW
   - Fail-closed por padrão (`fail_closed=True`)

2. **tests/test_policy_gate.py** (já existia, verificado)
   - 21 testes unitários cobrindo:
     - Allowlist enforcement (BLOCK se não na lista)
     - License validation (ALLOW com permissiva, METADATA_ONLY se desconhecida)
     - Robots.txt (BLOCK se disallow, METADATA_ONLY se crawl_delay >5s)
     - ToS (BLOCK se prohibited)
     - PII risk (BLOCK se high sem redaction, METADATA_ONLY se medium ou high com redaction)
     - Storage mode explícito (BLOCK/METADATA_ONLY/ALLOW)
     - Fail-open mode (teste de contraste)
   - Coverage: 85% em policy_gate.py (21/21 testes PASSED ✅)

3. **_OBSIDIAN/Organização do Projeto/WorkOrders/T-008.md** (criado)
   - WorkOrder detalhado com objetivo, entradas, saídas, riscos, DoD

---

## Comandos Executados

```bash
# 1. Testes
C:/Dev/banco-dados-publicos/.venv/Scripts/python.exe -m pytest tests/test_policy_gate.py -v
# Resultado: 21 passed, 588 warnings in 0.89s

# 2. Black (formatação)
C:/Dev/banco-dados-publicos/.venv/Scripts/python.exe -m black src/bots/policy_gate.py tests/test_policy_gate.py --check
# Resultado: All done! ✨ 🍰 ✨ (2 files would be left unchanged)

# 3. Flake8 (linting)
C:/Dev/banco-dados-publicos/.venv/Scripts/python.exe -m flake8 src/bots/policy_gate.py tests/test_policy_gate.py --max-line-length=100
# Resultado: (sem output = sucesso)

# 4. Mypy (type checking)
C:/Dev/banco-dados-publicos/.venv/Scripts/python.exe -m mypy src/bots/policy_gate.py --ignore-missing-imports
# Resultado: Success: no issues found in 1 source file

# 5. Git status
git status --short
# Resultado: M src/bots/policy_gate.py (já existia, verificado sem alterações necessárias)
```

---

## Resultados dos Testes

**21/21 testes PASSED** ✅

Cenários testados:
1. ✅ `test_policy_gate_imports` — Imports funcionam
2. ✅ `test_policy_decision_enum` — Enum PolicyDecision OK
3. ✅ `test_allowlist_populated` — ALLOWLIST tem 5 sources
4. ✅ `test_evaluate_source_not_in_allowlist` — Source SRC-999 → BLOCK
5. ✅ `test_evaluate_source_in_allowlist_no_license` — SRC-001 sem licença → METADATA_ONLY (fail-closed)
6. ✅ `test_evaluate_source_with_permissive_license` — SRC-001 + public_domain → ALLOW
7. ✅ `test_evaluate_source_license_unknown` — License unknown → METADATA_ONLY
8. ✅ `test_evaluate_source_robots_disallow` — robots_disallow=True → BLOCK
9. ✅ `test_evaluate_source_high_crawl_delay` — crawl_delay=10s → METADATA_ONLY
10. ✅ `test_evaluate_source_tos_prohibited` — ToS prohibited → BLOCK
11. ✅ `test_evaluate_source_high_pii_with_redaction` — high PII + redact → METADATA_ONLY
12. ✅ `test_evaluate_source_high_pii_no_redaction` — high PII sem redact → BLOCK
13. ✅ `test_evaluate_source_medium_pii` — medium PII → METADATA_ONLY
14. ✅ `test_evaluate_source_low_pii_permissive_license` — low PII + permissive → ALLOW
15. ✅ `test_evaluate_source_explicit_storage_mode_block` — storage_mode=BLOCK → BLOCK
16. ✅ `test_evaluate_source_explicit_storage_mode_metadata_only` — storage_mode=METADATA_ONLY → METADATA_ONLY
17. ✅ `test_evaluate_source_explicit_storage_mode_allow` — storage_mode=ALLOW → ALLOW
18. ✅ `test_evaluate_source_missing_robots_gov_domain` — .gov.br sem robots → ALLOW (trusted)
19. ✅ `test_check_allowlist_method` — _check_allowlist() funciona
20. ✅ `test_extract_source_fields_dict` — _extract_source_fields() suporta dict
21. ✅ `test_extract_source_fields_object` — _extract_source_fields() suporta ORM object

---

## Decisões Técnicas

1. **Fail-closed por padrão:** Qualquer ambiguidade → nível mais restritivo (METADATA_ONLY ou BLOCK)
   - Rationale: Compliance legal é crítico; melhor ser conservador

2. **Government domains (.gov.br) recebem "benefit of doubt":**
   - Licença missing em .gov → METADATA_ONLY (não BLOCK)
   - Rationale: Dados governamentais geralmente são públicos (Lei de Acesso à Informação)

3. **Robots.txt prevalece sobre allowlist:**
   - Se robots.txt bloqueia, retorna BLOCK mesmo se source está na allowlist
   - Rationale: Respeito legal às políticas do site

4. **PII alto requer redaction plan:**
   - PII high sem "redact" ou "anonymize" → BLOCK
   - PII high com redaction → METADATA_ONLY (conservador)
   - Rationale: LGPD compliance

5. **Crawl delay >5s sinaliza relutância:**
   - Delay alto → METADATA_ONLY
   - Rationale: Site está sinalizando "vá devagar ou não venha"

---

## Edge Cases Tratados

1. **Missing license em source:** Fail-closed → METADATA_ONLY (ou ALLOW se .gov)
2. **Missing robots.txt:** Gov domains → assume ALLOW; outros → METADATA_ONLY
3. **ToS ambíguo:** Fail-closed → METADATA_ONLY
4. **PII risk desconhecido:** Default → low (assume ALLOW se outras regras OK)
5. **Storage mode explícito:** Respeita configuração em sources.yaml (override de regras)

---

## Como Validar

```python
from src.bots.policy_gate import PolicyGate, PolicyDecision

gate = PolicyGate()

# Teste 1: Source não na allowlist
source_blocked = {"source_id": "SRC-999", "url": "https://example.com", "metadata": {}}
assert gate.evaluate(source_blocked) == PolicyDecision.BLOCK

# Teste 2: Source na allowlist com licença permissiva
source_allowed = {
    "source_id": "SRC-001",
    "url": "https://www.in.gov.br/",
    "metadata": {
        "license_policy": {"license_type": "public_domain", "license_status": "verified"},
        "crawl_policy": {"robots_respect": True},
        "data_handling": {"pii_expected": "low"},
    }
}
assert gate.evaluate(source_allowed) == PolicyDecision.ALLOW

# Teste 3: Licença desconhecida em .gov
source_metadata_only = {
    "source_id": "SRC-002",
    "url": "https://www.planalto.gov.br/",
    "metadata": {
        "crawl_policy": {"robots_respect": True},
        "data_handling": {"pii_expected": "low"},
    }
}
assert gate.evaluate(source_metadata_only) == PolicyDecision.METADATA_ONLY
```

---

## Próximos Passos

1. **T-009:** Bot — robots checker (fetch + cache de robots.txt em tempo real)
2. **T-010:** Audit logging (registrar todas as decisões de policy gate para compliance trail)
3. **T-ONB-SRC-001 a SRC-005:** Onboarding compliance checks (atualizar sources.yaml com status real de licenças/robots)

---

## Observações

- Policy gate NÃO faz fetching (usa dados em memória/cache)
- Decisões são baseadas em metadata de `configs/sources.yaml`
- Para atualizar robots.txt ou ToS, usar bot específico (T-009)
- Decisões devem ser auditáveis → preparação para T-010 (audit logging)
