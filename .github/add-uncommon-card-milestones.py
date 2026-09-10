from pathlib import Path
p=Path('index.html'); s=p.read_text()
marker=" {id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:200,type:'commonOwned',goal:'allCommon'},"
insert=marker+"\n {id:'uncommon3',icon:'🟢',name:'Uncommon Collector I',text:'Collect 3 Uncommon cards',reward:25,type:'uncommonOwned',goal:3},\n {id:'uncommon7',icon:'🟢',name:'Uncommon Collector II',text:'Collect 7 Uncommon cards',reward:50,type:'uncommonOwned',goal:7},\n {id:'uncommon14',icon:'🟢',name:'Uncommon Collector III',text:'Collect 14 Uncommon cards',reward:100,type:'uncommonOwned',goal:14},\n {id:'uncommonAll',icon:'🏆',name:'Uncommon Collector IV',text:'Collect all Uncommon cards',reward:200,type:'uncommonOwned',goal:'allUncommon'},"
if marker not in s: raise SystemExit('common milestone marker not found')
s=s.replace(marker,insert,1)
old=""" if(q.type==='commonOwned'){
   const commonKeys=Object.keys(animals).filter(k=>animals[k].rarity==='Common');
   progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Common').length;
   goal=q.goal==='allCommon'?commonKeys.length:Number(q.goal||commonKeys.length);
 }"""
new=old+"""
 if(q.type==='uncommonOwned'){
   const uncommonKeys=Object.keys(animals).filter(k=>animals[k].rarity==='Uncommon');
   progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Uncommon').length;
   goal=q.goal==='allUncommon'?uncommonKeys.length:Number(q.goal||uncommonKeys.length);
 }"""
if old not in s: raise SystemExit('common questState tracking block not found')
s=s.replace(old,new,1)
p.write_text(s)
