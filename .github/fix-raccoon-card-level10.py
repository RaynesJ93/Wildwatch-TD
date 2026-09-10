from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''    if(t.level>=10){
      battle.trashZones=battle.trashZones||[];
      battle.trashZones.push({x:target.x,y:target.y,life:4,maxLife:4,radius:78});
    }'''
new='''    if(cardLevel(t.key)>=10){
      battle.trashZones=battle.trashZones||[];
      battle.trashZones.push({x:target.x,y:target.y,life:4,maxLife:4,radius:78});
    }'''
if old not in s: raise SystemExit('Raccoon level-10 marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
