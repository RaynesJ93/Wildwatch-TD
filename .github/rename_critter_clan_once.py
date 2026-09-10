from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('content="WildWatch TD"','content="Critter Clan Tower Defence"')
s=s.replace('<title>Wildwatch TD</title>','<title>Critter Clan Tower Defence</title>')
s=s.replace('<span>WILDWATCH TD</span>','<span>CRITTER CLAN TOWER DEFENCE</span>')
p.write_text(s)

r=Path('README.md')
if r.exists():
    t=r.read_text()
    t=t.replace('# Wildwatch-TD','# Critter Clan Tower Defence')
    r.write_text(t)
