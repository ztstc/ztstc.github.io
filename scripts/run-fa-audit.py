"""Run FA audit and write results to a file (avoid terminal truncation)."""
import subprocess
import sys
from pathlib import Path

r = subprocess.run([sys.executable, 'scripts/audit-fontawesome.py'], capture_output=True, text=True, encoding='utf-8')
out = (r.stdout or '') + (r.stderr or '')
Path('scripts/fa-audit-result.txt').write_text(out, encoding='utf-8')
print('Wrote scripts/fa-audit-result.txt')
print(f'(exit {r.returncode}, {len(out)} chars)')
