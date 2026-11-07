"""Check local Markdown file links without network access or third-party packages."""
import re
from pathlib import Path
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
count = 0
for file in root.rglob('*.md'):
    if '.git' in file.parts:
        continue
    for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
        if '://' in target or target.startswith(('#','mailto:')):
            continue
        relative = unquote(target.split('#',1)[0])
        resolved = (file.parent/relative).resolve()
        if not resolved.is_relative_to(root) or not resolved.exists():
            raise SystemExit(f'Broken/escaping link: {file.relative_to(root)} -> {target}')
        count += 1
print(f'LOCAL_LINKS_OK: {count} file links. External URLs and heading anchors not tested.')
