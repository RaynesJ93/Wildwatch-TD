from pathlib import Path
p=Path('index.html'); s=p.read_text()
old="{id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:200,type:'commonOwned',goal:'allCommon'}"
new="{id:'commonAll',icon:'🏆',name:'Common Collector IV',text:'Collect all Common cards',reward:500,rewardType:'exp',type:'commonOwned',goal:'allCommon'}"
if old not in s: raise SystemExit('common all milestone marker not found')
s=s.replace(old,new,1)
old2="<span>🟡 ${q.reward}</span>"
new2="<span>${q.rewardType==='exp'?'⭐':'🟡'} ${q.reward}${q.rewardType==='exp'?' EXP':''}</span>"
if old2 not in s: raise SystemExit('quest reward display marker not found')
s=s.replace(old2,new2,1)
p.write_text(s)
