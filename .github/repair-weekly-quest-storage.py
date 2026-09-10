from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='function ensureWeeklyQuests(){const k=weekKey();if(!save.weeklyQuests||save.weeklyQuests.week!==k)save.weeklyQuests={week:k,progress:{},claimed:{}}}\nfunction addWeeklyProgress(type,n=1){ensureWeeklyQuests();save.weeklyQuests.progress[type]=(save.weeklyQuests.progress[type]||0)+n;persist();renderExtraQuestBoards()}'
new='''function ensureWeeklyQuests(){
 const k=weekKey();
 if(!save.weeklyQuests||save.weeklyQuests.week!==k)save.weeklyQuests={week:k,progress:{},claimed:{}};
 // Repair/migrate older weekly save formats so progress cannot fail silently.
 save.weeklyQuests.progress=save.weeklyQuests.progress&&typeof save.weeklyQuests.progress==="object"?save.weeklyQuests.progress:{};
 save.weeklyQuests.claimed=save.weeklyQuests.claimed&&typeof save.weeklyQuests.claimed==="object"?save.weeklyQuests.claimed:{};
 ["weeklyWaves","weeklyCoins","weeklyCommonPlaced","weeklyLegendaryPlaced","weeklyLevels"].forEach(t=>{
   if(save.weeklyQuests.progress[t]==null && Number.isFinite(Number(save[t])))save.weeklyQuests.progress[t]=Number(save[t]);
 });
}
function addWeeklyProgress(type,n=1){
 ensureWeeklyQuests();
 const amount=Number(n)||0;
 save.weeklyQuests.progress[type]=Math.max(0,Number(save.weeklyQuests.progress[type]||0)+amount);
 persist();
 renderExtraQuestBoards();
}'''
if old not in s: raise SystemExit('Weekly storage functions marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
