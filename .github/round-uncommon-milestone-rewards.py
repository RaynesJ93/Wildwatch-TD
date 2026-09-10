from pathlib import Path
p=Path('index.html'); s=p.read_text()
changes={
"{id:'uncommon3',icon:'🟢',name:'Uncommon Collector I',text:'Collect 3 Uncommon cards',reward:31,type:'uncommonOwned',goal:3}":"{id:'uncommon3',icon:'🟢',name:'Uncommon Collector I',text:'Collect 3 Uncommon cards',reward:30,type:'uncommonOwned',goal:3}",
"{id:'uncommon7',icon:'🟢',name:'Uncommon Collector II',text:'Collect 7 Uncommon cards',reward:63,type:'uncommonOwned',goal:7}":"{id:'uncommon7',icon:'🟢',name:'Uncommon Collector II',text:'Collect 7 Uncommon cards',reward:60,type:'uncommonOwned',goal:7}"
}
for old,new in changes.items():
    if old not in s: raise SystemExit('reward marker not found: '+old)
    s=s.replace(old,new,1)
p.write_text(s)
