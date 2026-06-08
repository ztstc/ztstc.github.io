"""暴力修 lang 按钮的 mojibake 字节：把 'Toggle Language">' 和 '</button>' 中间所有字节都替换为 '中文' 的合法 UTF-8（E4 B8 AD E6 96 87）。"""
import re
from pathlib import Path

OLD_LANG = b'Toggle Language">'
NEW_LANG = b'Toggle Language">\xe4\xb8\xad\xe6\x96\x87'   # 中文 UTF-8

changed = 0
for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    data = p.read_bytes()
    if OLD_LANG not in data:
        print(f'  SKIP {p.name}: no match')
        continue
    # 找该位置后到 </button> 之间的所有字节
    i = data.find(OLD_LANG)
    end = data.find(b'</button>', i)
    if end < 0:
        print(f'  SKIP {p.name}: no </button> after')
        continue
    # 替换: i + len(OLD_LANG) 到 end 之间的字节清空，换成 中文
    new_data = data[:i + len(OLD_LANG)] + b'\xe4\xb8\xad\xe6\x96\x87' + data[end:]
    p.write_bytes(new_data)
    # 验证
    verify = p.read_bytes()
    after = verify[i + len(OLD_LANG):i + len(OLD_LANG) + 6]
    print(f'  OK   {p.name}: lang 按钮内容 → {after.hex()} = "中文"')
    changed += 1

print(f'\n{changed}/5 project pages 修复完成')
