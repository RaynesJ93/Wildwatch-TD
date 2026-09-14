from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
original=s

weekly="""const WEEKLY_QUESTS=[
 {id:'wEnemyEradicator',name:'Enemy Eradicator',icon:'⚔️',text:'Kill 1,500 enemies',goal:1500,reward:250,type:'kills'},
 {id:'wMasterBuilder',name:'Master Builder',icon:'🏗️',text:'Place 150 towers',goal:150,reward:250,type:'placed'},
 {id:'wUpgradeFrenzy',name:'Upgrade Frenzy',icon:'⬆️',text:'Upgrade towers 100 times',goal:100,reward:250,type:'upgrades'},
 {id:'wWinningStreak',name:'Winning Streak',icon:'🏆',text:'Complete 10 maps',goal:10,reward:350,type:'maps'},
 {id:'wFlawlessWeek',name:'Flawless Week',icon:'❤️',text:'Complete 5 maps without losing a life',goal:5,reward:400,type:'flawlessMaps'},
 {id:'wHardWeek',name:'Hard Week',icon:'🔥',text:'Complete 5 Hard Mode maps',goal:5,reward:450,type:'hardMaps'},
 {id:'wFirstPriority',name:'First Priority',icon:'🎯',text:'Kill 750 enemies using First targeting',goal:750,reward:300,type:'firstKills'},
 {id:'wBigGameHunter',name:'Big Game Hunter',icon:'💪',text:'Kill 400 enemies using Strongest targeting',goal:400,reward:300,type:'strongestKills'},
 {id:'wVarietyPack',name:'Variety Pack',icon:'🃏',text:'Win maps using 10 different animal cards across the week',goal:10,reward:350,type:'winningCards'},
 {id:'wTrainingWeek',name:'Training Week',icon:'⭐',text:'Earn 1,000 total Card XP',goal:1000,reward:400,type:'cardXp'},
 {id:'wDamageDealer',name:'Damage Dealer',icon:'💥',text:'Deal 500,000 tower damage',goal:500000,reward:350,type:'damage'},
 {id:'wWaveCrusher',name:'Wave Crusher',icon:'🌊',text:'Clear 150 waves',goal:150,reward:300,type:'waves'},
 {id:'wResourceHunter',name:'Resource Hunter',icon:'🪙',text:'Earn 25,000 battle coins/meat',goal:25000,reward:300,type:'battleCurrency'},
 {id:'wMaximumPower',name:'Maximum Power',icon:'🔟',text:'Get 10 towers to Level 10',goal:10,reward:450,type:'level10Towers'},
 {id:'wCommonHeroes',name:'Common Heroes',icon:'🐾',text:'Complete 3 maps using only Common/Uncommon cards',goal:3,reward:450,type:'commonUncommonWins'},
 {id:'wWorldTraveller',name:'World Traveller',icon:'🌍',text:'Complete maps in 4 different regions',goal:4,reward:450,type:'regions'},
 {id:'wAnimalSpecialist',name:'Animal Specialist',icon:'🦍',text:'Get 500 kills with one animal card',goal:500,reward:350,type:'singleCardKills'},
 {id:'wEliteDefence',name:'Elite Defence',icon:'💎',text:'Complete 3 maps using only Rare-or-better cards',goal:3,reward:500,type:'rarePlusWins'}
];"""
s,n=re.subn(r"const WEEKLY_QUESTS=\[[\s\S]*?\n\];",weekly,s,count=1)
if n!=1: raise SystemExit('Could not replace WEEKLY_QUESTS')

ensure_daily="""function questDayV4(now=new Date()){
 const d=new Date(now.getTime()-6*60*60*1000);
 return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
function ensureDailyQuests(){
 save.dailyQuests=save.dailyQuests||{};
 if(save.dailyQuests.day!==questDayV4()||save.dailyQuests.version!==4||!Array.isArray(save.dailyQuests.items)||save.dailyQuests.items.length!==5||save.dailyQuests.items.some(x=>!DAILY_QUEST_POOL.some(q=>q.id===x.id))){
   const pool=[...DAILY_QUEST_POOL].sort(()=>Math.random()-.5).slice(0,5);
   save.dailyQuests={day:questDayV4(),version:4,items:pool.map(q=>({id:q.id,progress:0,claimed:false})),rerolled:false};persist();
 }
}
"""
s,n=re.subn(r"function ensureDailyQuests\(\)\{[\s\S]*?\n\}\n(?=function questDef)",ensure_daily,s,count=1)
if n!=1: raise SystemExit('Could not replace ensureDailyQuests')

ensure_weekly="""function weeklyKeyV4(now=new Date()){
  const d=new Date(now.getTime()-6*60*60*1000);
  const back=(d.getDay()-2+7)%7;
  d.setDate(d.getDate()-back);
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
function ensureWeeklyQuests(){
  const key=weeklyKeyV4();
  const needsNew=!save.weeklyQuests||typeof save.weeklyQuests!=='object'||save.weeklyQuests.week!==key||save.weeklyQuests.version!==4||!Array.isArray(save.weeklyQuests.items)||save.weeklyQuests.items.length!==8||save.weeklyQuests.items.some(id=>!WEEKLY_QUESTS.some(q=>q.id===id));
  if(needsNew){
    const pool=[...WEEKLY_QUESTS].sort(()=>Math.random()-.5).slice(0,8);
    save.weeklyQuests={week:key,version:4,items:pool.map(q=>q.id),progress:{},claimed:{}};
    save.weeklyProgress={};
    persist();
  }
  save.weeklyQuests.progress=save.weeklyQuests.progress&&typeof save.weeklyQuests.progress==='object'?save.weeklyQuests.progress:{};
  save.weeklyQuests.claimed=save.weeklyQuests.claimed&&typeof save.weeklyQuests.claimed==='object'?save.weeklyQuests.claimed:{};
}
"""
s,n=re.subn(r"function ensureWeeklyQuests\(\)\{[\s\S]*?\n\}\n(?=function weeklyQuestCards)",ensure_weekly,s,count=1)
if n!=1: raise SystemExit('Could not replace ensureWeeklyQuests')

old='return WEEKLY_QUESTS.map(q=>{'
new='return save.weeklyQuests.items.map(id=>WEEKLY_QUESTS.find(q=>q.id===id)).filter(Boolean).map(q=>{'
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('Could not update weeklyQuestCards')

s=s.replace('Complete 5 fresh quests each day. Daily quests reset at 6:00 AM.','Complete 5 random Daily quests. Resets every day at 6:00 AM.',1)

if s==original: raise SystemExit('No changes made')
p.write_text(s)
