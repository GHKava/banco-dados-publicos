"""
Script to generate onboarding notes in an Obsidian vault for each public
data source defined in configs/sources.yaml.

Features:

* Reads YAML configuration (list of sources). Requires PyYAML; if not
  installed, prints a clear message instructing the user to install
  it and exits.
* Creates or updates notes under the path
  `_OBSIDIAN/Organização do Projeto/Onboarding/`.
  Each note file is named `SRC-XXX - <NomeSanitizado>.md` where
  `<NomeSanitizado>` is derived from the source name and safe for
  Windows file systems.
* Uses a template located at
  `_OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md`.
  If the template does not exist, creates a simple default template.
* Inserts an auto-generated section between the markers
  `<!-- AUTO-GENERATED:BEGIN -->` and `<!-- AUTO-GENERATED:END -->`.
  Only this section is overwritten on successive runs; manual edits
  outside the section are preserved.
* Builds an index file listing all source notes with links.
* Produces a report at `docs/evidence/T-GEN-ONBOARDING/notes.md` and
  `docs/evidence/T-GEN-ONBOARDING/files_changed.json` detailing which
  notes were created or updated.

The script is idempotent; running it multiple times with the same
configuration will not duplicate content.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    print("PyYAML is required to run this script. Please install it with 'pip install pyyaml'.")
    sys.exit(1)


def sanitize_filename(name: str) -> str:
    """Sanitize file names by removing invalid Windows characters and
    replacing spaces with underscores."""
    sanitized = re.sub(r"[<>:\\"/\\|?*]", '', name)
    sanitized = sanitized.replace(' ', '_')
    return sanitized


def load_sources(yaml_path: Path) -> list[dict]:
    """Load list of sources from YAML file."""
    with yaml_path.open('r', encoding='utf-8') as f:
        sources = yaml.safe_load(f)
        if not isinstance(sources, list):
            raise ValueError('YAML file must contain a list of sources')
        return sources


def ensure_template(template_path: Path) -> str:
    """Ensure the onboarding template exists. If missing, create a
    minimal template and return its content."""
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    # Create directories if necessary
    template_path.parent.mkdir(parents=True, exist_ok=True)
    default_template = (
        "# Onboarding Checklist\n\n"
        "## Informações Gerais\n"
        "<!-- AUTO-GENERATED:BEGIN -->\n"
        "<!-- AUTO-GENERATED:END -->\n\n"
        "## Observações Manuais\n"
        "Insira aqui observações adicionais ou notas manuais sobre a fonte."
    )
    template_path.write_text(default_template, encoding='utf-8')
    return default_template


def update_note(note_path: Path, template_content: str, auto_content: str) -> bool:
    """Create or update a single note file. Returns True if the file
    was created or the auto-generated block changed."""
    changed = False
    if note_path.exists():
        original = note_path.read_text(encoding='utf-8')
        # Look for auto-generated block
        pattern = re.compile(r"(<!-- AUTO-GENERATED:BEGIN -->)(.*?)(<!-- AUTO-GENERATED:END -->)", re.DOTALL)
        match = pattern.search(original)
        if match:
            before = original[: match.start(2)]
            after = original[match.end(2) :]
            current_auto = match.group(2)
            if current_auto != "\n" + auto_content + "\n":
                new_content = before + "\n" + auto_content + "\n" + after
                note_path.write_text(new_content, encoding='utf-8')
                changed = True
        else:
            # If markers missing, append them at the end of the file
            new_content = original.rstrip() + "\n\n" + "<!-- AUTO-GENERATED:BEGIN -->\n" + auto_content + "\n<!-- AUTO-GENERATED:END -->\n"
            note_path.write_text(new_content, encoding='utf-8')
            changed = True
    else:
        # Create new note based on template
        content = template_content
        # Insert auto-generated section
        if '<!-- AUTO-GENERATED:BEGIN -->' in content:
            content = re.sub(
                r"<!-- AUTO-GENERATED:BEGIN -->.*?<!-- AUTO-GENERATED:END -->",
                f"<!-- AUTO-GENERATED:BEGIN -->\n{auto_content}\n<!-- AUTO-GENERATED:END -->",
                content,
                flags=re.DOTALL,
            )
        else:
            # Append at end
            content = content.rstrip() + "\n\n<!-- AUTO-GENERATED:BEGIN -->\n" + auto_content + "\n<!-- AUTO-GENERATED:END -->\n"
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(content, encoding='utf-8')
        changed = True
    return changed


def main():
    # Paths configuration
    yaml_path = Path('configs/sources.yaml')
    vault_base = Path('_OBSIDIAN/Organização do Projeto/Onboarding')
    template_path = Path('_OBSIDIAN/Organização do Projeto/Templates/Template - Source Onboarding Checklist.md')
    report_dir = Path('docs/evidence/T-GEN-ONBOARDING')

    sources = load_sources(yaml_path)
    template_content = ensure_template(template_path)
    changed_files = []

    for src in sources:
        sid = src['source_id']
        name = src['name']
        sanitized_name = sanitize_filename(name)
        note_file = vault_base / f"{sid} - {sanitized_name}.md"

        # Compose auto-generated section
        lines = []
        lines.append(f"**Fonte:** {name}")
        lines.append(f"**Domínios:** {', '.join(src.get('base_domains', []))}")
        lines.append(f"**Entrypoints:** {', '.join(src.get('entrypoints', []))}")
        discovery = src.get('discovery', {})
        lines.append(f"**Discovery:** {discovery.get('method', 'unknown')} ({', '.join(discovery.get('urls', []))})")
        license_policy = src.get('license_policy', {})
        lines.append(f"**Robots.txt:** {license_policy.get('robots_url', 'unknown')}")
        lines.append(f"**ToS/License:** {license_policy.get('tos_url', 'unknown')}")
        lines.append(f"**License Status:** {license_policy.get('license_status', 'unknown')}")
        lines.append(f"**Storage Mode:** {license_policy.get('default_storage_mode', 'unknown')}")
        crawl_policy = src.get('crawl_policy', {})
        lines.append(f"**Rate Limit (RPS):** {crawl_policy.get('rate_limit_rps', 'unknown')}")
        data_handling = src.get('data_handling', {})
        lines.append(f"**PII Expected:** {data_handling.get('pii_expected', 'unknown')}")
        lines.append(f"**PII Actions:** {', '.join(data_handling.get('pii_actions', []))}")
        budget = src.get('budget', {})
        lines.append(f"**Budget:** {budget.get('max_pages_per_day', '')} pages/day, {budget.get('max_bytes_per_day', '')} bytes/day")
        lines.append(f"**Notas:** {src.get('notes', '')}")
        lines.append(f"**Última atualização:** {datetime.utcnow().isoformat()}Z")
        auto_content = "\n".join(lines)

        if update_note(note_file, template_content, auto_content):
            changed_files.append(str(note_file))

    # Create index
    index_lines = ["# Índice de Fontes", ""]
    for src in sources:
        sid = src['source_id']
        name = src['name']
        sanitized_name = sanitize_filename(name)
        note_rel = f"{sid} - {sanitized_name}.md"
        index_lines.append(f"- [{sid} - {name}]({note_rel})")
    index_path = vault_base / 'INDEX.md'
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(index_lines), encoding='utf-8')

    # Write report files
    report_dir.mkdir(parents=True, exist_ok=True)
    report_markdown = report_dir / 'notes.md'
    report_json = report_dir / 'files_changed.json'
    report_lines = [
        '# Relatório de Geração de Notas',
        '',
        f'Total de fontes processadas: {len(sources)}',
        f'Total de notas criadas/atualizadas: {len(changed_files)}',
        '',
    ]
    if changed_files:
        report_lines.append('## Notas Criadas ou Atualizadas')
        for fpath in changed_files:
            report_lines.append(f'- {fpath}')
    else:
        report_lines.append('Nenhuma nota precisou ser atualizada.')
    report_markdown.write_text("\n".join(report_lines), encoding='utf-8')
    with report_json.open('w', encoding='utf-8') as jf:
        json.dump({'changed_files': changed_files}, jf, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
