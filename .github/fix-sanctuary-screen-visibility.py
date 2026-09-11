from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='#battleScreen.map-select-mode{display:block!important;height:auto!important;overflow:visible!important}'
new='#battleScreen.active.map-select-mode{display:block!important;height:auto!important;overflow:visible!important}\n#battleScreen.map-select-mode:not(.active){display:none!important}'
if old not in s:
    raise SystemExit('sanctuary visibility CSS marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Fixed Sanctuary visibility so it only appears on the Battle screen')
