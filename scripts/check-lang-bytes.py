"""Check actual bytes of lang button content + fix mojibake to 中文"""
from pathlib import Path

P = Path('pages/projects/project1.html')
data = P.read_bytes()
i = data.find(b'Toggle Language">')
if i < 0:
    print('NOT FOUND')
else:
    # 找 </button> 闭合
    end = data.find(b'</button>', i)
    content = data[i+len(b'Toggle Language">'):end]
    print('current bytes:', content.hex())
    print('current text (utf-8 lossy):', content.decode('utf-8', errors='replace'))

# 找含涓\u8bf6\u67e5\u8868 的任何字节序列
print('\n--- searching for any 3-byte CJK between lang and button ---')
import re
# 抓 'Toggle Language">' 后的中文
m = re.search(rb'Toggle Language">([^<]{2,30})</button>', data)
if m:
    s = m.group(1)
    print('match bytes:', s.hex())
    try:
        print('match as utf-8:', s.decode('utf-8'))
    except UnicodeDecodeError as e:
        print('UTF-8 decode failed:', e)
        # 试 GBK / CP936
        for enc in ('gbk', 'cp936', 'gb2312', 'big5'):
            try:
                print(f'as {enc}:', s.decode(enc))
                break
            except UnicodeDecodeError:
                pass
