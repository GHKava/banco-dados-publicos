# T-007 Work Order: Bot - Source Registry

**Date:** 2026-01-30
**Persona:** DE (Data Engineer)
**Dependencies:** ✅ T-005, ✅ T-004, ✅ T-006 (ALL SATISFIED)

---

## Objective

Implement CLI bot for source registry CRUD operations with policy enforcement.

## Definition of Ready (DoR) - ✅ ALL SATISFIED

- [x] T-005: Postgres schema with Source model (source_id, name, url, metadata)
- [x] T-004: sources.yaml with allowlist and policy definitions
- [x] T-006: RQ job queue infrastructure for async operations
- [x] Python 3.14.2, SQLAlchemy 2.0+ available
- [x] Pre-commit hooks configured for code quality

---

## Deliverables

| Deliverable     | File Path                    | Purpose                                |
| --------------- | ---------------------------- | -------------------------------------- |
| Bot CLI module  | `src/bots/registry.py`       | CRUD operations on sources             |
| Validators      | `src/bots/validators.py`     | Policy compliance checks (fail-closed) |
| Tests           | `tests/test_bot_registry.py` | Unit tests for bot and validators      |
| Integration job | `src/jobs/registry_job.py`   | RQ task for async registry operations  |
| Evidence pack   | `docs/evidence/T-007/`       | Commands, notes, files_changed.json    |

---

## Scope

### CLI Commands

1. **list-sources** - Display all registered sources with compliance status
2. **add-source** - Register new source (validates allowlist, policy)
3. **update-source** - Modify existing source metadata
4. **remove-source** - Deregister source (soft delete)
5. **validate-source** - Check source compliance with policy

### Policy Enforcement

- **Fail-closed:** Default = METADATA_ONLY (most restrictive)
- **Allowlist:** Only SRC-001, SRC-002, SRC-003, SRC-004, SRC-005 permitted
- **Robots.txt:** Respect robots.txt and rate limits
- **License:** Require license metadata for full access

---

## Quality Gates

| Gate   | Command                                                        | Expectation         |
| ------ | -------------------------------------------------------------- | ------------------- |
| Black  | `black --line-length=100 src/bots/ tests/test_bot_registry.py` | All files formatted |
| Flake8 | `flake8`                                                       | 0 issues            |
| Isort  | `isort`                                                        | Imports organized   |
| Mypy   | `mypy src/bots/`                                               | Type hints valid    |
| Pytest | `pytest tests/test_bot_registry.py -v`                         | 100% pass rate      |

---

## Estimated Duration

**45-60 minutes**

---

## Success Criteria

- [x] CLI bot created and functional
- [x] Policy validation rules implemented
- [x] Database CRUD operations working
- [x] All tests passing (100% coverage on new code)
- [x] Evidence pack created and committed
- [x] Git commits pushed to GitHub
