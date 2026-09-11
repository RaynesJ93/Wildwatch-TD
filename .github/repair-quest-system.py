from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Make the three old placeholder milestones real tracked milestones.
old=""" {icon:'🃏',name:'Growing Collection',text:'Own 10 animal cards',reward:150},
 {icon:'⭐',name:'Veteran Defender',text:'Clear 100 total waves',reward:250},
 {icon:'🏆',name:'Master Collector',text:'Own your first Legendary card',reward:300}"""
new=""" {id:'growingCollection',icon:'🃏',name:'Growing Collection',text:'Own 10 animal cards',reward:150,type:'allOwned',goal:10},
 {id:'veteranDefender',icon:'⭐',name:'Veteran Defender',text:'Clear 100 total waves',reward:250,type:'totalWaves',goal:100},
 {id:'masterCollector',icon:'🏆',name:'Master Collector',text:'Own your first Legendary card',reward:300,type:'legendaryOwned',goal:1}"""
if old not in s: raise SystemExit('milestone placeholder block not found')
s=s.replace(old,new,1)

# 2) Turn Challenge placeholders into real one-time tracked quests.
old="""const CHALLENGE_QUESTS=[
 {icon:'⚪',name:'Common Ground',text:'Complete a map using only Common cards',reward:100},
 {icon:'❤️',name:'Untouchable',text:'Complete a map without losing a life',reward:125},
 {icon:'⏩',name:'Full Speed Ahead',text:'Clear 5 waves at 3× speed',reward:75}
];"""
new="""const CHALLENGE_QUESTS=[
 {id:'challengeCommonMap',icon:'⚪',name:'Common Ground',text:'Complete a map using only Common cards',reward:100,type:'challengeCommonMap',goal:1},
 {id:'challengeNoLifeMap',icon:'❤️',name:'Untouchable',text:'Complete a map without losing a life',reward:125,type:'challengeNoLifeMap',goal:1},
 {id:'challengeSpeedWaves',icon:'⏩',name:'Full Speed Ahead',text:'Clear 5 waves at 3× speed',reward:75,type:'challengeSpeedWaves',goal:5}
];"""
if old not in s: raise SystemExit('challenge placeholder block not found')
s=s.replace(old,new,1)

# 3) Challenge storage/progress helpers before questState.
marker='function questState(q){'
if marker not in s: raise SystemExit('questState marker not found')
helper=r'''function ensureChallengeQuests(){
 save.challengeQuests=save.challengeQuests&&typeof save.challengeQuests==='object'?save.challengeQuests:{progress:{},claimed:{}};
 save.challengeQuests.progress=save.challengeQuests.progress&&typeof save.challengeQuests.progress==='object'?save.challengeQuests.progress:{};
 save.challengeQuests.claimed=save.challengeQuests.claimed&&typeof save.challengeQuests.claimed==='object'?save.challengeQuests.claimed:{};
}
function addChallengeProgress(type,n=1){
 ensureChallengeQuests();
 const q=CHALLENGE_QUESTS.find(x=>x.type===type);
 if(!q||save.challengeQuests.claimed[q.id])return;
 save.challengeQuests.progress[type]=Math.min(Number(q.goal||1),Math.max(0,Number(save.challengeQuests.progress[type]||0)+(Number(n)||0)));
 persist();renderExtraQuestBoards();
}
'''
if 'function ensureChallengeQuests(' not in s:s=s.replace(marker,helper+marker,1)

# 4) Extend questState for challenges + remaining milestones.
needle="""function questState(q){
 let goal=Number(q.goal||1),progress=Math.max(0,Number(q.progress||0));"""
if needle not in s: raise SystemExit('questState opening not found')
replace=needle+"""
 if(q.type&&q.type.startsWith('challenge')){ensureChallengeQuests();progress=Math.max(0,Number(save.challengeQuests.progress[q.type]||0));}
 if(q.type==='allOwned')progress=(save.unlocked||[]).length;
 if(q.type==='totalWaves')progress=Math.max(0,Number(save.totalWaves||0));
 if(q.type==='legendaryOwned')progress=(save.unlocked||[]).filter(k=>animals[k]?.rarity==='Legendary').length;"""
s=s.replace(needle,replace,1)

# 5) Replace dropdown renderer with claim support for every milestone/challenge.
start=s.find("function questDropdownCards(items,mode='not-completed')")
end=s.find('function bindMilestoneClaimButtons()',start)
if start<0 or end<0: raise SystemExit('quest dropdown/bind markers not found')
new_renderer=r'''function questDropdownCards(items,mode='not-completed'){
 const sorted=sortQuestItems(items,mode);
 if(!sorted.length)return `<div class="info-box center small">No quests in this category yet.</div>`;
 const isMilestone=items===MILESTONE_QUESTS,isChallenge=items===CHALLENGE_QUESTS;
 if(isChallenge)ensureChallengeQuests();
 save.milestoneClaims=save.milestoneClaims||{};
 return sorted.map((q,i)=>{
   const st=questState(q);
   const claimed=isMilestone?!!save.milestoneClaims[q.id]:isChallenge?!!save.challengeQuests.claimed[q.id]:false;
   const status=claimed?'✓ Reward claimed':st.completed?'✓ Completed — reward ready':st.progress>0?`${Math.min(st.progress,st.goal)}/${st.goal}`:'Not started';
   let reward=q.rewardType==='exp'?`✨ ${q.reward} EXP each`:`🟡 ${q.reward}`;
   let claim='';
   if(q.id&&st.completed&&!claimed){
     if(isMilestone)claim=`<button class="primary milestoneClaimBtn" data-id="${q.id}" style="width:100%;margin-top:10px">Claim ${reward}</button>`;
     if(isChallenge)claim=`<button class="primary challengeClaimBtn" data-id="${q.id}" style="width:100%;margin-top:10px">Claim ${reward}</button>`;
   }
   return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px"><b>${q.icon} ${q.name}</b><b>${reward}</b></summary><div class="small" style="margin-top:7px">${q.text}</div><div class="small" style="margin-top:7px">${status}</div>${claim}</details>`;
 }).join('')
}
'''
s=s[:start]+new_renderer+s[end:]

# 6) Replace milestone binder with generic milestone + challenge claimers.
start=s.find('function bindMilestoneClaimButtons()')
end=s.find('function renderExtraQuestBoards()',start)
if start<0 or end<0: raise SystemExit('claim binder/render markers not found')
claimers=r'''function bindMilestoneClaimButtons(){
 save.milestoneClaims=save.milestoneClaims||{};
 document.querySelectorAll('.milestoneClaimBtn').forEach(btn=>btn.onclick=()=>{
   const q=MILESTONE_QUESTS.find(x=>x.id===btn.dataset.id);if(!q||save.milestoneClaims[q.id]||!questState(q).completed)return;
   if(q.rewardType==='exp'){
     save.cardXP=save.cardXP||{};
     const tier=q.type==='commonOwned'?'Common':q.type==='uncommonOwned'?'Uncommon':null;
     Object.keys(animals).filter(k=>!tier||animals[k].rarity===tier).forEach(k=>{if((save.unlocked||[]).includes(k))addCardXp(k,q.reward)});
   }else save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);
   save.milestoneClaims[q.id]=true;persist();renderHome();renderCards();renderExtraQuestBoards();
 });
 document.querySelectorAll('.challengeClaimBtn').forEach(btn=>btn.onclick=()=>{
   ensureChallengeQuests();const q=CHALLENGE_QUESTS.find(x=>x.id===btn.dataset.id);if(!q||save.challengeQuests.claimed[q.id]||!questState(q).completed)return;
   save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);save.challengeQuests.claimed[q.id]=true;persist();renderHome();renderCards();renderExtraQuestBoards();
 });
}
'''
s=s[:start]+claimers+s[end:]

# 7) Daily no-life wave: remember lives at wave start.
needle='''  battle.waveActive=true;
  battle.spawning=true;'''
if needle not in s: raise SystemExit('wave start marker not found')
s=s.replace(needle,'''  battle.waveStartLives=battle.lives;
  battle.waveActive=true;
  battle.spawning=true;''',1)

# 8) Count total waves + daily no-loss + challenge 3x waves on every clear.
needle='''  addQuestProgress("waves",1);
    addWeeklyProgress("weeklyWaves",1);
  if(speed===3)addQuestProgress("speedWaves",1);'''
if needle not in s: raise SystemExit('wave quest marker not found')
s=s.replace(needle,'''  addQuestProgress("waves",1);
  addWeeklyProgress("weeklyWaves",1);
  save.totalWaves=Math.max(0,Number(save.totalWaves||0))+1;
  if(battle.lives===(battle.waveStartLives??battle.lives))addQuestProgress("noLossWaves",1);
  if(speed===3){addQuestProgress("speedWaves",1);addChallengeProgress("challengeSpeedWaves",1);}''',1)

# 9) Fix Normal/Hard map daily quests and map challenges at completion.
needle='''  if(clearedWave>=15){
    const cardXp=awardUsedCardXp(true);'''
if needle not in s: raise SystemExit('map completion marker not found')
s=s.replace(needle,'''  if(clearedWave>=15){
    addQuestProgress(hardMode?"hardMaps":"normalMaps",1);
    const usedForChallenge=[...new Set(battle.usedCards||[])];
    if(usedForChallenge.length&&usedForChallenge.every(k=>animals[k]?.rarity==='Common'))addChallengeProgress("challengeCommonMap",1);
    if(battle.lives===(battle.mapStartLives??battle.lives))addChallengeProgress("challengeNoLifeMap",1);
    const cardXp=awardUsedCardXp(true);''',1)

# 10) Store map start lives in resetBattle.
needle='battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,wave:1,'
if needle not in s: raise SystemExit('reset battle object marker not found')
s=s.replace(needle,'battle={started:true,hardMode,coins:hardMode?110:130,lives:hardMode?15:20,mapStartLives:hardMode?15:20,wave:1,',1)

# 11) Make renderExtraQuestBoards always rebind new claim buttons.
# Insert before closing brace of function by replacing known render lines block tail.
needle=""" if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
 bindMilestoneClaimButtons();
}"""
if needle not in s:
    needle2=""" if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
}"""
    if needle2 not in s: raise SystemExit('renderExtraQuestBoards tail not found')
    s=s.replace(needle2,""" if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
 bindMilestoneClaimButtons();
}""",1)

for req in ['addQuestProgress(hardMode?"hardMaps":"normalMaps",1)','addQuestProgress("noLossWaves",1)','addChallengeProgress("challengeSpeedWaves",1)','challengeCommonMap','challengeNoLifeMap','save.totalWaves','challengeClaimBtn','growingCollection']:
    if req not in s: raise SystemExit('missing repair marker '+req)
p.write_text(s,encoding='utf-8')
print('Quest system repaired: daily map/no-loss, weekly retained, milestones claimable, challenges active')
