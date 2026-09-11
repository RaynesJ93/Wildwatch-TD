from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='ctx.scale(pulse,pulse);ctx.font="26px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";'
new='ctx.scale(pulse,pulse);ctx.font="78px system-ui";ctx.textAlign="center";ctx.textBaseline="middle";'
if old not in s: raise SystemExit('Active pineapple size marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
