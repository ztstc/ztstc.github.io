"""Find illegal control characters in lang JSON files."""
from pathlib import Path

for p in ['lang/zh.json', 'lang/en.json']:
    raw = Path(p).read_bytes()
    found = []
    for i, b in enumerate(raw):
        if b < 0x20 and b not in (0x09, 0x0A, 0x0D):
            found.append((i, b))
    if found:
        print(f"{p}: {len(found)} illegal control char(s)")
        for i, b in found[:5]:
            line_no = raw[:i].count(b'\n') + 1
            line_start = raw.rfind(b'\n', 0, i) + 1
            line_end = raw.find(b'\n', i)
            if line_end == -1: line_end = len(raw)
            line = raw[line_start:line_end]
            col = i - line_start
            print(f"  offset {i} byte 0x{b:02x} at line {line_no} col {col}")
            print(f"  line: {line!r}")
            print(f"  context: {raw[max(0,i-15):i+15]!r}")
    else:
        print(f"{p}: no illegal control chars")
