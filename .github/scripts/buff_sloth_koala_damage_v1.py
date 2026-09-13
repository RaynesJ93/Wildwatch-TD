from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='SLOTH_KOALA_DAMAGE_BUFF_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
import re

def buff(key):
    global s
    pat=rf'({key}:\{{name:"[^"]+"[^\n]*?dmg:)(\d+(?:\.\d+)?)'
    m=re.search(pat,s)
    if not m: raise RuntimeError(f'{key} card damage anchor not found')
    old=float(m.group(2)); new=round(old*1.34,2)
    if new.is_integer(): new=int(new)
    s=s[:m.start(2)]+str(new)+s[m.end(2):]
    print(key, old, '->', new)

buff('sloth')
buff('koala')
s=s.replace('const animals={', '// SLOTH_KOALA_DAMAGE_BUFF_V1: Sloth and Koala base damage increased by 34%.\nconst animals={',1)
p.write_text(s,encoding='utf-8')
