from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='for(let level=3;level<=lvl;level++)need=Math.ceil(need*1.60);'
new='for(let level=3;level<=lvl;level++)need=Math.ceil(need*1.15);'
if old not in s:
    raise SystemExit('60 percent XP growth marker not found')
s=s.replace(old,new,1)
p.write_text(s)
