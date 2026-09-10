from pathlib import Path
p=Path('index.html'); s=p.read_text()
old="""const MILESTONE_QUESTS=[
 {icon:'🃏',name:'Growing Collection',text:'Own 10 animal cards',reward:150},
 {icon:'⭐',name:'Veteran Defender',text:'Clear 100 total waves',reward:250},
 {icon:'🏆',name:'Master Collector',text:'Own your first Legendary card',reward:300}
];"""
new="""const MILESTONE_QUESTS=[
 {id:'common3',icon:'⚪',name:'Common Collector I',text:'Collect 3 Common cards',reward:50,type:'commonOwned',goal:3},
 {id:'common7',icon:'⚪',name:'Common Collector II',text:'Collect 7 Common cards',reward:100,type:'commonOwned',goal:7},
 {id:'common14',icon:'⚪',name:'Common Collector III',text:'Collect 14 Common cards',reward:200,type:'commonOwned',goal:14},
 {id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:400,type:'commonOwned',goal:'allCommon'},
 {icon:'🃏',name:'Growing Collection',text:'Own 10 animal cards',reward:150},
 {icon:'⭐',name:'Veteran Defender',text:'Clear 100 total waves',reward:250},
 {icon:'🏆',name:'Master Collector',text:'Own your first Legendary card',reward:300}
];"""
if old not in s: raise SystemExit('milestone quest block not found')
s=s.replace(old,new,1)
old2="""function questState(q){
 const goal=Number(q.goal||1),progress=Math.max(0,Number(q.progress||0));
 const completed=!!q.completed||progress>=goal;
 return {goal,progress,completed,ratio:goal?Math.min(1,progress/goal):0};
}"""
new2="""function questState(q){
 let goal=Number(q.goal||1),progress=Math.max(0,Number(q.progress||0));
 if(q.type==='commonOwned'){
   const commonKeys=Object.keys(animals).filter(k=>animals[k].rarity==='Common');
   progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Common').length;
   goal=q.goal==='allCommon'?commonKeys.length:Number(q.goal||commonKeys.length);
 }
 const completed=!!q.completed||progress>=goal;
 return {goal,progress,completed,ratio:goal?Math.min(1,progress/goal):0};
}"""
if old2 not in s: raise SystemExit('questState block not found')
s=s.replace(old2,new2,1)
p.write_text(s)
