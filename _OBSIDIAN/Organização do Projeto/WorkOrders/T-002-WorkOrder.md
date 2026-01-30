# WorkOrder — T-002: Python bootstrap + venv + pre-commit

**ID:** T-002  
**Criado:** 2026-01-30 16:15 UTC  
**Persona:** TL (Tech Lead)  
**Dependências:** T-001 ✅ DONE  
**Status:** IN_PROGRESS

---

## Objetivo

Executar script de bootstrap, criar ambiente virtual Python, instalar dependências e configurar pre-commit hooks.

---

## DoR Checklist

- [x] T-001 concluído (Git + GitHub configurado)
- [x] Python 3.11+ instalado
- [x] `bootstrap.ps1` existe em `scripts/setup/`
- [x] `requirements.txt` existe
- [x] `.env.example` existe

---

## Entradas

- `scripts/setup/bootstrap.ps1` (script PowerShell)
- `requirements.txt` (30+ dependencies)
- `.env.example` (template de config)
- `pyproject.toml` (build config)

---

## Saídas / Artefatos

- [ ] Ambiente virtual criado (`.venv/`)
- [ ] Dependencies instaladas (30+ packages)
- [ ] Pre-commit hooks configurados
- [ ] `.env` criado (cópia de `.env.example`)
- [ ] Verificação: lint/typecheck passa
- [ ] `scripts/setup/INSTALACOES.md` atualizado com log

---

## Comandos previstos

```powershell
# Executar bootstrap
.\scripts\setup\bootstrap.ps1

# Ou manualmente:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pre-commit install
copy .env.example .env
```

---

## Riscos

| Risco                     | Mitigação                                                  |
| ------------------------- | ---------------------------------------------------------- |
| Python < 3.11             | Verificar versão primeiro                                  |
| Permissão PowerShell      | Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass |
| Dependencies conflitantes | Pin versions no requirements.txt                           |
| Docker não disponível     | Bootstrap tem flag `-NoDocker`                             |

---

## Evidência mínima

- [ ] Output de `python --version` (>= 3.11)
- [ ] Output de `pip list` mostrando 30+ packages
- [ ] Output de `pre-commit run --all-files`
- [ ] `.env` existe
- [ ] Log em `INSTALACOES.md`

---

## Quality gate

- [ ] Black lint passa
- [ ] Flake8 lint passa
- [ ] Mypy typecheck passa (ou warnings documentados)

---

**WorkOrder criado por:** AGENTE ORQUESTRADOR (Persona: TL)  
**Data:** 2026-01-30 16:15 UTC
