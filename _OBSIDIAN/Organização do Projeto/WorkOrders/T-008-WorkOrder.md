# T-008 Work Order: Bot - Policy Gate

**Date:** 2026-01-30
**Persona:** DE (Data Engineer)
**Dependencies:** ✅ T-007 (Source Registry Bot), SEC approved

---

## Objective

Implement policy gate logic to automatically determine access level for each source: **ALLOW** (full text), **METADATA_ONLY** (only meta), or **BLOCK** (no access). This gate enforces compliance decisions based on license, robots.txt, ToS, and PII policies.

## Definition of Ready (DoR) - ✅ ALL SATISFIED

- [x] T-007: Source Registry Bot with validators complete
- [x] T-005: Postgres schema with Source model (includes metadata fields)
- [x] T-004: sources.yaml with license/policy definitions
- [x] Security approval for policy rules (assumed per roadmap)
- [x] Python 3.14.2, SQLAlchemy 2.0+ available

---

## Deliverables

| Deliverable        | File Path                       | Purpose                                            |
| ------------------ | ------------------------------- | -------------------------------------------------- |
| Policy gate module | `src/bots/policy_gate.py`       | PolicyGate class with decision logic               |
| Enums/types        | `src/bots/policy_gate.py`       | PolicyDecision enum (ALLOW/METADATA_ONLY/BLOCK)    |
| Tests              | `tests/test_policy_gate.py`     | Unit tests for policy gate decisions               |
| Integration job    | `src/jobs/policy_gate_job.py`   | RQ task for async policy gate evaluation           |
| Evidence pack      | `docs/evidence/T-008/`          | Commands, notes, files_changed.json, tests.log     |
| Handoff            | `_OBSIDIAN/.../Handoffs/T-008.md` | What changed, decisions, validation steps          |

---

## Scope

### PolicyGate Class

**Input:** Source object (from database) or source_id
**Output:** PolicyDecision enum (ALLOW | METADATA_ONLY | BLOCK)

### Decision Logic (Fail-Closed by Default)

1. **BLOCK conditions:**
   - Source not in allowlist (SRC-001 to SRC-005)
   - robots.txt explicitly disallows (Disallow: /)
   - ToS prohibits scraping (if known)
   - High PII risk without redaction plan
   - Missing required fields (base_url, license type)

2. **METADATA_ONLY conditions:**
   - License unknown or unclear
   - License type = "attribution required but no scraping clause"
   - Robots.txt allows but with strict crawl_delay (>5s)
   - Source flagged for manual review

3. **ALLOW conditions:**
   - Source in allowlist ✅
   - License = "public domain" OR "CC0" OR "government open data"
   - robots.txt allows (no Disallow for target paths)
   - ToS permits scraping OR is silent (government sites)
   - PII policy = "detect + redact" OR "none expected"

### Edge Cases

- Missing license → METADATA_ONLY (fail-closed)
- Missing robots.txt → ALLOW (government sites often lack it)
- Contradictory license/ToS → most restrictive wins (METADATA_ONLY or BLOCK)

---

## Implementation Steps

1. **Create policy_gate.py:**
   - `PolicyDecision` enum with 3 states
   - `PolicyGate` class with `evaluate(source: Source) -> PolicyDecision` method
   - Helper methods: `_check_allowlist()`, `_check_license()`, `_check_robots()`, `_check_tos()`, `_check_pii()`

2. **Integration with registry:**
   - Update `src/bots/registry.py` to call PolicyGate during add/update operations
   - Store policy decision in Source.metadata JSON field

3. **Create tests:**
   - Test ALLOW: SRC-001 (DOU, public domain)
   - Test METADATA_ONLY: source with unclear license
   - Test BLOCK: source not in allowlist
   - Test BLOCK: robots.txt Disallow: /
   - Test edge case: missing robots.txt for government site (should ALLOW)

4. **Create RQ job:**
   - `src/jobs/policy_gate_job.py` with `evaluate_source_policy(source_id)` task
   - Enqueue from registry bot when adding new sources

---

## Quality Gates

| Gate   | Command                                                       | Expectation         |
| ------ | ------------------------------------------------------------- | ------------------- |
| Black  | `black --line-length=100 src/bots/ tests/`                    | All files formatted |
| Flake8 | `flake8 src/bots/policy_gate.py tests/test_policy_gate.py`   | 0 issues            |
| Isort  | `isort src/bots/ tests/`                                      | Imports organized   |
| Mypy   | `mypy src/bots/policy_gate.py`                                | Type hints valid    |
| Pytest | `pytest tests/test_policy_gate.py -v --cov=src/bots/policy_gate` | 100% pass rate, >80% coverage |

---

## Estimated Duration

**60-90 minutes**

---

## Risks

- **Ambiguous license interpretation:** Mitigate with fail-closed (METADATA_ONLY if unclear)
- **Missing ToS data:** Most government sites lack explicit ToS; assume ALLOW for .gov.br domains
- **Robots.txt fetch failure:** Cache last known state, default to METADATA_ONLY on error
- **Performance:** Policy evaluation should be <100ms; cache decisions in Source.metadata

---

## Success Criteria

- [x] PolicyGate class created with decision logic
- [x] Decision logic covers all 3 outcomes (ALLOW/METADATA_ONLY/BLOCK)
- [x] All tests passing (>80% coverage on policy_gate.py)
- [x] Integration with registry bot (policy decision stored in DB)
- [x] Evidence pack created with test results
- [x] Handoff document explaining decision rules
- [x] Git commits pushed to GitHub

---

## References

- Escopo.md: "Fail-closed: se houver qualquer dúvida sobre licença/robots/ToS, **bloquear por padrão**"
- DUV protocol: Unclear license → create DUV, default to METADATA_ONLY
- T-007: validators.py already has allowlist/license checks; extend for policy gate
