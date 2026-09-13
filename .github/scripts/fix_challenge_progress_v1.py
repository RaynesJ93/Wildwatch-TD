from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CHALLENGE_PROGRESS_FIX_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old='''function addChallengeProgress(type,n=1){
  if(typeof save==='undefined')return;
  ensureChallengeQuests();
  const q=CHALLENGE_QUESTS.find(x=>x.type===type);
  if(!q||save.challengeQuests.claimed[q.id])return;
  save.challengeQuests.progress[type]=Math.min(Number(q.goal||1),Math.max(0,Number(save.challengeQuests.progress[type]||0)+(Number(n)||0)));
  persist();
  if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards();
}'''
new='''// CHALLENGE_PROGRESS_FIX_V1: keep one tier-aware challenge progress implementation.
function addChallengeProgress(type,n=1){
  if(typeof save==='undefined')return;
  ensureChallengeQuests();
  const qs=CHALLENGE_QUESTS.filter(x=>x.type===type);
  if(!qs.length)return;
  const maxGoal=Math.max(...qs.map(q=>Number(q.goal||1)));
  const current=Math.max(0,Number(save.challengeQuests.progress[type]||0));
  save.challengeQuests.progress[type]=Math.min(maxGoal,current+(Number(n)||0));
  persist();
  if(typeof renderExtraQuestBoards==='function')renderExtraQuestBoards();
}'''
if old not in s:
    raise RuntimeError('Duplicate challenge progress function anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Fixed Challenge Quest tier progress tracking')
