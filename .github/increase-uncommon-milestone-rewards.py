from pathlib import Path
p=Path('index.html'); s=p.read_text()
changes={
"{id:'uncommon3',icon:'🟢',name:'Uncommon Collector I',text:'Collect 3 Uncommon cards',reward:25,type:'uncommonOwned',goal:3}":"{id:'uncommon3',icon:'🟢',name:'Uncommon Collector I',text:'Collect 3 Uncommon cards',reward:31,type:'uncommonOwned',goal:3}",
"{id:'uncommon7',icon:'🟢',name:'Uncommon Collector II',text:'Collect 7 Uncommon cards',reward:50,type:'uncommonOwned',goal:7}":"{id:'uncommon7',icon:'🟢',name:'Uncommon Collector II',text:'Collect 7 Uncommon cards',reward:63,type:'uncommonOwned',goal:7}",
"{id:'uncommon14',icon:'🟢',name:'Uncommon Collector III',text:'Collect 14 Uncommon cards',reward:100,type:'uncommonOwned',goal:14}":"{id:'uncommon14',icon:'🟢',name:'Uncommon Collector III',text:'Collect 14 Uncommon cards',reward:125,type:'uncommonOwned',goal:14}",
"{id:'uncommonAll',icon:'🏆',name:'Uncommon Collector IV',text:'Collect all Uncommon cards',reward:200,type:'uncommonOwned',goal:'allUncommon'}":"{id:'uncommonAll',icon:'🏆',name:'Uncommon Collector IV',text:'Collect all Uncommon cards',reward:250,type:'uncommonOwned',goal:'allUncommon'}"
}
for old,new in changes.items():
    if old not in s: raise SystemExit('uncommon reward marker not found: '+old)
    s=s.replace(old,new,1)
p.write_text(s)
