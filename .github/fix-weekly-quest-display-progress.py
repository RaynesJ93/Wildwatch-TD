from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""function questState(q){
 let goal=Number(q.goal||1),progress=Math.max(0,Number(q.progress||0));
 if(q.type==='commonOwned'){"""
new="""function questState(q){
 let goal=Number(q.goal||1),progress=Math.max(0,Number(q.progress||0));
 if(q.type&&q.type.startsWith('weekly')){
   ensureWeeklyQuests();
   progress=Math.max(0,Number(save.weeklyQuests?.progress?.[q.type]||0));
 }
 if(q.type==='commonOwned'){"""
if old not in s: raise SystemExit('questState marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
