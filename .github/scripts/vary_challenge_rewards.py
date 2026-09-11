from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
if 'QUEST_REWARD_VARIETY_V1' in s:
    print('Varied challenge rewards already installed')
    raise SystemExit(0)

# Mark the tiered challenge block and add varied reward types by tier.
s=s.replace('// QUEST_TIERS_V1: 3 permanent tiers for every Challenge Quest.','// QUEST_TIERS_V1: 3 permanent tiers for every Challenge Quest.\n// QUEST_REWARD_VARIETY_V1: challenge tiers now mix coins and card XP.',1)

start=s.index('const CHALLENGE_QUESTS=[')
end=s.index('];', start)+2
block=s[start:end]

# Tier I stays coins. Tier II becomes Card XP. Tier III becomes a coin + Card XP bundle.
def repl(m):
    obj=m.group(0)
    tier_m=re.search(r"tier:(\d)",obj)
    rew_m=re.search(r"reward:(\d+)",obj)
    if not tier_m or not rew_m: return obj
    tier=int(tier_m.group(1)); reward=int(rew_m.group(1))
    if tier==1:
        return obj.replace(f'reward:{reward}',f'reward:{reward},rewardKind:\'coins\'')
    if tier==2:
        xp=max(50,round(reward*0.6/25)*25)
        return obj.replace(f'reward:{reward}',f'reward:{xp},rewardKind:\'xp\'')
    xp=max(100,round(reward*0.35/25)*25)
    coins=max(100,round(reward*0.75/25)*25)
    return obj.replace(f'reward:{reward}',f'reward:{coins},rewardXp:{xp},rewardKind:\'coinsXp\'')

block=re.sub(r"\{id:'challenge[^\n]+?tier:\d\}",repl,block)
s=s[:start]+block+s[end:]

# Add reward label + award helpers before questDropdownCards.
marker='function questDropdownCards(items,mode=\'not-completed\'){'
helper=r'''function challengeRewardLabel(q){
 if(q.rewardKind==='xp')return `✨ ${q.reward} Card XP`;
 if(q.rewardKind==='coinsXp')return `🟡 ${q.reward} + ✨ ${q.rewardXp||0} Card XP`;
 return `🟡 ${q.reward}`;
}
function giveChallengeReward(q){
 if(q.rewardKind==='xp'){
   const owned=(save.unlocked||[]).filter(k=>animals[k]);
   if(owned.length){const k=owned[Math.floor(Math.random()*owned.length)];addCardXp(k,Number(q.reward||0));}
   return;
 }
 save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);
 if(q.rewardKind==='coinsXp'){
   const owned=(save.unlocked||[]).filter(k=>animals[k]);
   if(owned.length){const k=owned[Math.floor(Math.random()*owned.length)];addCardXp(k,Number(q.rewardXp||0));}
 }
}
'''
if marker not in s: raise SystemExit('questDropdownCards marker not found')
s=s.replace(marker,helper+marker,1)

# Challenge cards show their actual varied reward.
s=s.replace("let reward=q.rewardType==='exp'?`✨ ${q.reward} EXP each`:`🟡 ${q.reward}`;", "let reward=isChallenge?challengeRewardLabel(q):q.rewardType==='exp'?`✨ ${q.reward} EXP each`:`🟡 ${q.reward}`;",1)

old="save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);save.challengeQuests.claimed[q.id]=true;btn.textContent='✓ Claimed';btn.disabled=true;btn.className='secondary';persist();renderHome();renderCards();renderExtraQuestBoards();"
new="giveChallengeReward(q);save.challengeQuests.claimed[q.id]=true;btn.textContent='✓ Claimed';btn.disabled=true;btn.className='secondary';persist();renderHome();renderCards();renderExtraQuestBoards();"
if old not in s: raise SystemExit('challenge claim block not found')
s=s.replace(old,new,1)

p.write_text(s)
print('Installed varied challenge rewards: coins, Card XP, and coin+XP bundles')
