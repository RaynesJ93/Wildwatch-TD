from pathlib import Path
p=Path('index.html')
s=p.read_text()

if 'QUEST_TIERS_V1' in s:
    print('Quest tiers already installed')
    raise SystemExit(0)

start=s.index('// CHALLENGE_SET_15_V1:')
end=s.index('function evaluateMapChallenges()', start)
new_block=r'''// QUEST_TIERS_V1: 3 permanent tiers for every Challenge Quest.
const CHALLENGE_QUESTS=[
 {id:'challengeCommonMap1',icon:'⚪',name:'Common Ground I',text:'Complete 1 map using only Common cards',reward:100,type:'challengeCommonMap',goal:1,tier:1},
 {id:'challengeCommonMap2',icon:'⚪',name:'Common Ground II',text:'Complete 3 maps using only Common cards',reward:200,type:'challengeCommonMap',goal:3,tier:2},
 {id:'challengeCommonMap3',icon:'⚪',name:'Common Ground III',text:'Complete 5 maps using only Common cards',reward:300,type:'challengeCommonMap',goal:5,tier:3},
 {id:'challengeNoLifeMap1',icon:'❤️',name:'Untouchable I',text:'Complete 1 map without losing a life',reward:125,type:'challengeNoLifeMap',goal:1,tier:1},
 {id:'challengeNoLifeMap2',icon:'❤️',name:'Untouchable II',text:'Complete 3 maps without losing a life',reward:250,type:'challengeNoLifeMap',goal:3,tier:2},
 {id:'challengeNoLifeMap3',icon:'❤️',name:'Untouchable III',text:'Complete 5 maps without losing a life',reward:375,type:'challengeNoLifeMap',goal:5,tier:3},
 {id:'challengeSpeedWaves1',icon:'⏩',name:'Full Speed Ahead I',text:'Clear 5 waves at 3× speed',reward:75,type:'challengeSpeedWaves',goal:5,tier:1},
 {id:'challengeSpeedWaves2',icon:'⏩',name:'Full Speed Ahead II',text:'Clear 15 waves at 3× speed',reward:150,type:'challengeSpeedWaves',goal:15,tier:2},
 {id:'challengeSpeedWaves3',icon:'⏩',name:'Full Speed Ahead III',text:'Clear 30 waves at 3× speed',reward:225,type:'challengeSpeedWaves',goal:30,tier:3},
 {id:'challengeOneAnimal1',icon:'🐾',name:'One Animal Army I',text:'Complete 1 map using only one animal type',reward:175,type:'challengeOneAnimal',goal:1,tier:1},
 {id:'challengeOneAnimal2',icon:'🐾',name:'One Animal Army II',text:'Complete 3 maps using only one animal type',reward:350,type:'challengeOneAnimal',goal:3,tier:2},
 {id:'challengeOneAnimal3',icon:'🐾',name:'One Animal Army III',text:'Complete 5 maps using only one animal type',reward:525,type:'challengeOneAnimal',goal:5,tier:3},
 {id:'challengeNoUpgrades1',icon:'💰',name:'Big Spender I',text:'Complete 1 map without upgrading any towers',reward:150,type:'challengeNoUpgrades',goal:1,tier:1},
 {id:'challengeNoUpgrades2',icon:'💰',name:'Big Spender II',text:'Complete 3 maps without upgrading any towers',reward:300,type:'challengeNoUpgrades',goal:3,tier:2},
 {id:'challengeNoUpgrades3',icon:'💰',name:'Big Spender III',text:'Complete 5 maps without upgrading any towers',reward:450,type:'challengeNoUpgrades',goal:5,tier:3},
 {id:'challengeFourLevel101',icon:'🛠️',name:'Master Builder I',text:'Get 4 towers to Level 10 in 1 battle',reward:150,type:'challengeFourLevel10',goal:1,tier:1},
 {id:'challengeFourLevel102',icon:'🛠️',name:'Master Builder II',text:'Do this in 3 battles',reward:300,type:'challengeFourLevel10',goal:3,tier:2},
 {id:'challengeFourLevel103',icon:'🛠️',name:'Master Builder III',text:'Do this in 5 battles',reward:450,type:'challengeFourLevel10',goal:5,tier:3},
 {id:'challengePerfect1',icon:'🎯',name:'Perfect Defence I',text:'Complete 1 map without losing a life',reward:150,type:'challengePerfect3',goal:1,tier:1},
 {id:'challengePerfect2',icon:'🎯',name:'Perfect Defence II',text:'Complete 3 maps without losing a life',reward:300,type:'challengePerfect3',goal:3,tier:2},
 {id:'challengePerfect3',icon:'🎯',name:'Perfect Defence III',text:'Complete 5 maps without losing a life',reward:450,type:'challengePerfect3',goal:5,tier:3},
 {id:'challengeRareMap1',icon:'💎',name:'Rare Breed I',text:'Complete 1 map using only Rare cards',reward:175,type:'challengeRareMap',goal:1,tier:1},
 {id:'challengeRareMap2',icon:'💎',name:'Rare Breed II',text:'Complete 3 maps using only Rare cards',reward:350,type:'challengeRareMap',goal:3,tier:2},
 {id:'challengeRareMap3',icon:'💎',name:'Rare Breed III',text:'Complete 5 maps using only Rare cards',reward:525,type:'challengeRareMap',goal:5,tier:3},
 {id:'challengeLegendaryMap1',icon:'🌟',name:'Legendary Squad I',text:'Complete 1 map using only Legendary cards',reward:250,type:'challengeLegendaryMap',goal:1,tier:1},
 {id:'challengeLegendaryMap2',icon:'🌟',name:'Legendary Squad II',text:'Complete 3 maps using only Legendary cards',reward:500,type:'challengeLegendaryMap',goal:3,tier:2},
 {id:'challengeLegendaryMap3',icon:'🌟',name:'Legendary Squad III',text:'Complete 5 maps using only Legendary cards',reward:750,type:'challengeLegendaryMap',goal:5,tier:3},
 {id:'challengeFourTowers1',icon:'⚔️',name:'Minimalist I',text:'Complete 1 map with 4 or fewer towers placed',reward:250,type:'challengeFourTowers',goal:1,tier:1},
 {id:'challengeFourTowers2',icon:'⚔️',name:'Minimalist II',text:'Complete 3 maps with 4 or fewer towers placed',reward:500,type:'challengeFourTowers',goal:3,tier:2},
 {id:'challengeFourTowers3',icon:'⚔️',name:'Minimalist III',text:'Complete 5 maps with 4 or fewer towers placed',reward:750,type:'challengeFourTowers',goal:5,tier:3},
 {id:'challengeNoSell1',icon:'🚫',name:'No Second Chances I',text:'Complete 1 map without selling a tower',reward:100,type:'challengeNoSell',goal:1,tier:1},
 {id:'challengeNoSell2',icon:'🚫',name:'No Second Chances II',text:'Complete 3 maps without selling a tower',reward:200,type:'challengeNoSell',goal:3,tier:2},
 {id:'challengeNoSell3',icon:'🚫',name:'No Second Chances III',text:'Complete 5 maps without selling a tower',reward:300,type:'challengeNoSell',goal:5,tier:3},
 {id:'challengeHardPerfect1',icon:'🔥',name:'Hardcore Defender I',text:'Complete 1 Hard Mode map without losing a life',reward:350,type:'challengeHardPerfect',goal:1,tier:1},
 {id:'challengeHardPerfect2',icon:'🔥',name:'Hardcore Defender II',text:'Complete 3 Hard Mode maps without losing a life',reward:700,type:'challengeHardPerfect',goal:3,tier:2},
 {id:'challengeHardPerfect3',icon:'🔥',name:'Hardcore Defender III',text:'Complete 5 Hard Mode maps without losing a life',reward:1050,type:'challengeHardPerfect',goal:5,tier:3},
 {id:'challenge1000Coins1',icon:'🪙',name:'Penny Pincher I',text:'Finish 1 map with at least 1,000 battle coins remaining',reward:200,type:'challenge1000Coins',goal:1,tier:1},
 {id:'challenge1000Coins2',icon:'🪙',name:'Penny Pincher II',text:'Finish 3 maps with at least 1,000 battle coins remaining',reward:400,type:'challenge1000Coins',goal:3,tier:2},
 {id:'challenge1000Coins3',icon:'🪙',name:'Penny Pincher III',text:'Finish 5 maps with at least 1,000 battle coins remaining',reward:600,type:'challenge1000Coins',goal:5,tier:3},
 {id:'challengeFull3x1',icon:'🌊',name:'Speed Demon I',text:'Complete 1 entire map at 3× speed',reward:300,type:'challengeFull3x',goal:1,tier:1},
 {id:'challengeFull3x2',icon:'🌊',name:'Speed Demon II',text:'Complete 3 entire maps at 3× speed',reward:600,type:'challengeFull3x',goal:3,tier:2},
 {id:'challengeFull3x3',icon:'🌊',name:'Speed Demon III',text:'Complete 5 entire maps at 3× speed',reward:900,type:'challengeFull3x',goal:5,tier:3},
 {id:'challengeUltimate1',icon:'👑',name:'Ultimate Defender I',text:'Complete 1 Hard Mode map using only 4 towers, without losing a life',reward:750,type:'challengeUltimate',goal:1,tier:1},
 {id:'challengeUltimate2',icon:'👑',name:'Ultimate Defender II',text:'Complete 2 Hard Mode maps using only 4 towers, without losing a life',reward:1250,type:'challengeUltimate',goal:2,tier:2},
 {id:'challengeUltimate3',icon:'👑',name:'Ultimate Defender III',text:'Complete 3 Hard Mode maps using only 4 towers, without losing a life',reward:2000,type:'challengeUltimate',goal:3,tier:3}
];
'''
s=s[:start]+new_block+s[end:]

old=r'''function addChallengeProgress(type,n=1){
 ensureChallengeQuests();
 const q=CHALLENGE_QUESTS.find(x=>x.type===type);
 if(!q||save.challengeQuests.claimed[q.id])return;
 save.challengeQuests.progress[type]=Math.min(Number(q.goal||1),Math.max(0,Number(save.challengeQuests.progress[type]||0)+(Number(n)||0)));
 persist();renderExtraQuestBoards();
}'''
new=r'''function addChallengeProgress(type,n=1){
 ensureChallengeQuests();
 const qs=CHALLENGE_QUESTS.filter(x=>x.type===type);
 if(!qs.length)return;
 const maxGoal=Math.max(...qs.map(q=>Number(q.goal||1)));
 save.challengeQuests.progress[type]=Math.min(maxGoal,Math.max(0,Number(save.challengeQuests.progress[type]||0)+(Number(n)||0)));
 persist();renderExtraQuestBoards();
}'''
if old not in s: raise SystemExit('addChallengeProgress block not found')
s=s.replace(old,new,1)

# Immediate visual feedback for weekly, milestone and challenge claims.
s=s.replace("save.weeklyQuests.claimed[q.id]=true;\n    persist();renderHome();renderCards();renderExtraQuestBoards();", "save.weeklyQuests.claimed[q.id]=true;\n    btn.textContent='✓ Claimed';btn.disabled=true;btn.className='secondary';\n    persist();renderHome();renderCards();renderExtraQuestBoards();",1)
s=s.replace("save.milestoneClaims[q.id]=true;persist();renderHome();renderCards();renderExtraQuestBoards();", "save.milestoneClaims[q.id]=true;btn.textContent='✓ Claimed';btn.disabled=true;btn.className='secondary';persist();renderHome();renderCards();renderExtraQuestBoards();",1)
s=s.replace("save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);save.challengeQuests.claimed[q.id]=true;persist();renderHome();renderCards();renderExtraQuestBoards();", "save.metaCoins=(save.metaCoins||0)+Number(q.reward||0);save.challengeQuests.claimed[q.id]=true;btn.textContent='✓ Claimed';btn.disabled=true;btn.className='secondary';persist();renderHome();renderCards();renderExtraQuestBoards();",1)

# Daily already had direct visual feedback; make sure text is consistent.
s=s.replace("b.textContent='✓ Claimed';b.disabled=true;b.className='secondary questClaim';", "b.textContent='✓ Claimed';b.disabled=true;b.className='secondary questClaim';")

p.write_text(s)
print('Installed 3-tier challenge system and instant claimed-state UI')
