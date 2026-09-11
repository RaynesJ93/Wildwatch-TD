from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Repair the later compatibility helpers so they write to the same state the UI reads.
old_weekly = '''function addWeeklyProgress(type,n=1){
  if(typeof save==='undefined')return;
  save.weeklyProgress=save.weeklyProgress||{};
  save.weeklyProgress[type]=(save.weeklyProgress[type]||0)+n;
}'''
new_weekly = '''function addWeeklyProgress(type,n=1){
  if(typeof save==='undefined')return;
  ensureWeeklyQuests();
  const q=WEEKLY_QUESTS.find(x=>x.type===type);
  if(!q||save.weeklyQuests.claimed[q.id])return;
  save.weeklyQuests.progress[type]=Math.min(Number(q.goal||1),Math.max(0,Number(save.weeklyQuests.progress[type]||0)+(Number(n)||0)));
  persist();
  if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards();
}'''
if old_weekly not in s:
    raise SystemExit('Could not find weekly compatibility helper')
s = s.replace(old_weekly, new_weekly, 1)

old_challenge = '''function addChallengeProgress(type,n=1){
  if(typeof save==='undefined')return;
  save.challengeProgress=save.challengeProgress||{};
  save.challengeProgress[type]=(save.challengeProgress[type]||0)+n;
}'''
new_challenge = '''function addChallengeProgress(type,n=1){
  if(typeof save==='undefined')return;
  ensureChallengeQuests();
  const q=CHALLENGE_QUESTS.find(x=>x.type===type);
  if(!q||save.challengeQuests.claimed[q.id])return;
  save.challengeQuests.progress[type]=Math.min(Number(q.goal||1),Math.max(0,Number(save.challengeQuests.progress[type]||0)+(Number(n)||0)));
  persist();
  if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards();
}'''
if old_challenge not in s:
    raise SystemExit('Could not find challenge compatibility helper')
s = s.replace(old_challenge, new_challenge, 1)

# 2) Add complete weekly state/reset/render/claim support if it is missing.
anchor = '''const MILESTONE_QUESTS=['''
if 'function ensureWeeklyQuests()' not in s:
    weekly_impl = r'''
function weeklyKey(){
  const d=new Date(),day=(d.getUTCDay()+6)%7;
  d.setUTCDate(d.getUTCDate()-day);
  return d.toISOString().slice(0,10);
}
function ensureWeeklyQuests(){
  const key=weeklyKey();
  const old=save.weeklyProgress&&typeof save.weeklyProgress==='object'?save.weeklyProgress:{};
  if(!save.weeklyQuests||typeof save.weeklyQuests!=='object'||save.weeklyQuests.week!==key){
    save.weeklyQuests={week:key,progress:{...old},claimed:{}};
    save.weeklyProgress={};
    persist();
  }
  save.weeklyQuests.progress=save.weeklyQuests.progress&&typeof save.weeklyQuests.progress==='object'?save.weeklyQuests.progress:{};
  save.weeklyQuests.claimed=save.weeklyQuests.claimed&&typeof save.weeklyQuests.claimed==='object'?save.weeklyQuests.claimed:{};
}
function weeklyQuestCards(){
  ensureWeeklyQuests();
  return WEEKLY_QUESTS.map(q=>{
    const progress=Math.max(0,Number(save.weeklyQuests.progress[q.type]||0));
    const goal=Number(q.goal||1),done=progress>=goal,claimed=!!save.weeklyQuests.claimed[q.id];
    const reward=q.rewardType==='tierExp'?`${q.reward} ${q.rewardTier} XP`:`🟡 ${q.reward}`;
    const button=claimed?'<button class="secondary" disabled style="width:100%;margin-top:10px">✓ Claimed</button>':done?`<button class="primary weeklyClaimBtn" data-id="${q.id}" style="width:100%;margin-top:10px">Claim ${reward}</button>`:'<button class="secondary" disabled style="width:100%;margin-top:10px">In progress</button>';
    return `<div class="info-box"><div style="display:flex;justify-content:space-between;gap:8px"><b>${q.icon} ${q.name}</b><b>${reward}</b></div><div class="small" style="margin:6px 0">${q.text}</div><div class="progress"><i style="width:${Math.min(100,progress/goal*100)}%"></i></div><div class="small" style="margin-top:7px">${Math.min(progress,goal)}/${goal}</div>${button}</div>`;
  }).join('');
}
function bindWeeklyClaimButtons(){
  ensureWeeklyQuests();
  document.querySelectorAll('.weeklyClaimBtn').forEach(btn=>btn.onclick=()=>{
    const q=WEEKLY_QUESTS.find(x=>x.id===btn.dataset.id);
    if(!q||save.weeklyQuests.claimed[q.id])return;
    const progress=Math.max(0,Number(save.weeklyQuests.progress[q.type]||0));
    if(progress<Number(q.goal||1))return;
    if(q.rewardType==='tierExp'){
      save.cardXP=save.cardXP||{};
      Object.keys(animals).filter(k=>animals[k]?.rarity===q.rewardTier&&(save.unlocked||[]).includes(k)).forEach(k=>addCardXp(k,Number(q.reward||0)));
    }else{
      save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);
    }
    save.weeklyQuests.claimed[q.id]=true;
    persist();renderHome();renderCards();renderExtraQuestBoards();
  });
}
'''
    if anchor not in s:
        raise SystemExit('Could not find milestone anchor')
    s = s.replace(anchor, weekly_impl + '\n' + anchor, 1)

# 3) Ensure weekly claim buttons are rebound every time the board rerenders.
old_render = ''' if(w)w.innerHTML=weeklyQuestCards();
 if(m)m.innerHTML=questDropdownCards(MILESTONE_QUESTS,document.getElementById('milestoneSort')?.value||'not-completed');
 if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
 bindMilestoneClaimButtons();'''
new_render = ''' if(w)w.innerHTML=weeklyQuestCards();
 if(m)m.innerHTML=questDropdownCards(MILESTONE_QUESTS,document.getElementById('milestoneSort')?.value||'not-completed');
 if(c)c.innerHTML=questDropdownCards(CHALLENGE_QUESTS,document.getElementById('challengeSort')?.value||'not-completed');
 bindWeeklyClaimButtons();
 bindMilestoneClaimButtons();'''
if old_render not in s:
    raise SystemExit('Could not find extra quest board renderer')
s = s.replace(old_render, new_render, 1)

p.write_text(s, encoding='utf-8')
print('Repaired weekly and challenge quests')
