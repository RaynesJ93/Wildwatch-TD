from pathlib import Path
import runpy

p=Path('.github/scripts/upgrade_tundra_falls_v2.py')
s=p.read_text(encoding='utf-8')
old="pat=r'// TUNDRA_FALLS_V1:.*?const tundraFallsMaps=.*?\\n\\}\\));\\n'\nns,n=re.subn(pat,new_maps,s,count=1,flags=re.S)"
new="pat=r'// TUNDRA_FALLS_V1:.*?function seriesMaps\\(series\\)'\nns,n=re.subn(pat,new_maps+'function seriesMaps(series)',s,count=1,flags=re.S)"
if old not in s:
    raise SystemExit('Expected broken regex block not found in upgrade script')
p.write_text(s.replace(old,new,1),encoding='utf-8')
runpy.run_path(str(p),run_name='__main__')
