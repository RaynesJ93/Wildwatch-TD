from pathlib import Path
p=Path('index.html'); s=p.read_text()
changes={
"{id:'common3',icon:'⚪',name:'Common Collector I',text:'Collect 3 Common cards',reward:50,type:'commonOwned',goal:3}":"{id:'common3',icon:'⚪',name:'Common Collector I',text:'Collect 3 Common cards',reward:25,type:'commonOwned',goal:3}",
"{id:'common7',icon:'⚪',name:'Common Collector II',text:'Collect 7 Common cards',reward:100,type:'commonOwned',goal:7}":"{id:'common7',icon:'⚪',name:'Common Collector II',text:'Collect 7 Common cards',reward:50,type:'commonOwned',goal:7}",
"{id:'common14',icon:'⚪',name:'Common Collector III',text:'Collect 14 Common cards',reward:200,type:'commonOwned',goal:14}":"{id:'common14',icon:'⚪',name:'Common Collector III',text:'Collect 14 Common cards',reward:100,type:'commonOwned',goal:14}",
"{id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:400,type:'commonOwned',goal:'allCommon'}":"{id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:200,type:'commonOwned',goal:'allCommon'}"
}
for old,new in changes.items():
    if old not in s: raise SystemExit('reward marker not found: '+old)
    s=s.replace(old,new,1)
p.write_text(s)
