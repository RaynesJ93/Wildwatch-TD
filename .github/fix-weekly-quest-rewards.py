from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
marker="function renderExtraQuestBoards(){"
if marker not in s: raise SystemExit('renderExtraQuestBoards marker missing')
if 'function claimWeeklyQuest(' not in s:
    helper=r'''function weeklyRewardLabel(q){return q.rewardType==='tierExp'?`✨ ${q.reward} EXP • ${q.rewardTier} cards`:`🟡 ${q.reward} Coins`}
function weeklyQuestCards(){
 ensureWeeklyQuests();
 return WEEKLY_QUESTS.map((q,i)=>{
  const progress=Math.max(0,Number(save.weeklyQuests.progress[q.type]||0)), done=progress>=q.goal, claimed=!!save.weeklyQuests.claimed[q.id];
  const status=claimed?'✓ Reward claimed':done?'✓ Completed — reward ready':`${Math.min(progress,q.goal)}/${q.goal}`;
  const btn=done&&!claimed?`<button class="primary" style="margin-top:9px;width:100%" onclick="claimWeeklyQuest('${q.id}')">Claim ${weeklyRewardLabel(q)}</button>`:'';
  return `<details class="info-box questDrop" ${i===0?'open':''}><summary style="cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px"><b>${q.icon} ${q.name}</b><b>${weeklyRewardLabel(q)}</b></summary><div class="small" style="margin-top:7px">${q.text}</div><div class="small" style="margin-top:7px">${status}</div>${btn}</details>`;
 }).join('')
}
function claimWeeklyQuest(id){
 ensureWeeklyQuests();
 const q=WEEKLY_QUESTS.find(x=>x.id===id);if(!q)return;
 const progress=Math.max(0,Number(save.weeklyQuests.progress[q.type]||0));
 if(progress<q.goal||save.weeklyQuests.claimed[q.id])return;
 if(q.rewardType==='tierExp'){
  save.cardXP=save.cardXP||{};
  Object.keys(animals).filter(k=>animals[k].rarity===q.rewardTier&&save.unlocked.includes(k)).forEach(k=>save.cardXP[k]=(save.cardXP[k]||0)+q.reward);
 }else save.metaCoins=(save.metaCoins||0)+q.reward;
 save.weeklyQuests.claimed[q.id]=true;
 persist();renderMeta();renderExtraQuestBoards();renderHome();
}
'''
    s=s.replace(marker,helper+marker,1)
old="if(w)w.innerHTML=questDropdownCards(WEEKLY_QUESTS,'progress');"
if old not in s: raise SystemExit('weekly renderer line missing')
s=s.replace(old,"if(w)w.innerHTML=weeklyQuestCards();",1)
for required in ['function claimWeeklyQuest(','weeklyQuestCards()','save.weeklyQuests.claimed[q.id]=true','save.metaCoins=(save.metaCoins||0)+q.reward']:
    if required not in s: raise SystemExit('missing final marker: '+required)
p.write_text(s,encoding='utf-8')
print('Weekly quests now have real claim buttons and award their displayed rewards')
