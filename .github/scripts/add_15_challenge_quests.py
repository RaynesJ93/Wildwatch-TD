from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'CHALLENGE_SET_15_V1' in s:
    print('15 challenge quest set already installed')
    raise SystemExit(0)
old="""const CHALLENGE_QUESTS=[
 {id:'challengeCommonMap',icon:'⚪',name:'Common Ground',text:'Complete a map using only Common cards',reward:100,type:'challengeCommonMap',goal:1},
 {id:'challengeNoLifeMap',icon:'❤️',name:'Untouchable',text:'Complete a map without losing a life',reward:125,type:'challengeNoLifeMap',goal:1},
 {id:'challengeSpeedWaves',icon:'⏩',name:'Full Speed Ahead',text:'Clear 5 waves at 3× speed',reward:75,type:'challengeSpeedWaves',goal:5}
];"""
new="""// CHALLENGE_SET_15_V1: permanent one-time challenge achievements.
const CHALLENGE_QUESTS=[
 {id:'challengeCommonMap',icon:'⚪',name:'Common Ground',text:'Complete a map using only Common cards',reward:100,type:'challengeCommonMap',goal:1},
 {id:'challengeNoLifeMap',icon:'❤️',name:'Untouchable',text:'Complete a map without losing a life',reward:125,type:'challengeNoLifeMap',goal:1},
 {id:'challengeSpeedWaves',icon:'⏩',name:'Full Speed Ahead',text:'Clear 5 waves at 3× speed',reward:75,type:'challengeSpeedWaves',goal:5},
 {id:'challengeOneAnimal',icon:'🐾',name:'One Animal Army',text:'Complete a map using only one animal type',reward:175,type:'challengeOneAnimal',goal:1},
 {id:'challengeNoUpgrades',icon:'💰',name:'Big Spender',text:'Complete a map without upgrading any towers',reward:150,type:'challengeNoUpgrades',goal:1},
 {id:'challengeFourLevel10',icon:'🛠️',name:'Master Builder',text:'Get 4 towers to Level 10 in one battle',reward:150,type:'challengeFourLevel10',goal:1},
 {id:'challengePerfect3',icon:'🎯',name:'Perfect Defence',text:'Complete 3 maps without losing a life',reward:300,type:'challengePerfect3',goal:3},
 {id:'challengeRareMap',icon:'💎',name:'Rare Breed',text:'Complete a map using only Rare cards',reward:175,type:'challengeRareMap',goal:1},
 {id:'challengeLegendaryMap',icon:'🌟',name:'Legendary Squad',text:'Complete a map using only Legendary cards',reward:250,type:'challengeLegendaryMap',goal:1},
 {id:'challengeFourTowers',icon:'⚔️',name:'Minimalist',text:'Complete a map with 4 or fewer towers placed',reward:250,type:'challengeFourTowers',goal:1},
 {id:'challengeNoSell',icon:'🚫',name:'No Second Chances',text:'Complete a map without selling a tower',reward:100,type:'challengeNoSell',goal:1},
 {id:'challengeHardPerfect',icon:'🔥',name:'Hardcore Defender',text:'Complete a Hard Mode map without losing a life',reward:350,type:'challengeHardPerfect',goal:1},
 {id:'challenge1000Coins',icon:'🪙',name:'Penny Pincher',text:'Finish a map with at least 1,000 battle coins remaining',reward:200,type:'challenge1000Coins',goal:1},
 {id:'challengeFull3x',icon:'🌊',name:'Speed Demon',text:'Complete an entire map at 3× speed',reward:300,type:'challengeFull3x',goal:1},
 {id:'challengeUltimate',icon:'👑',name:'Ultimate Defender',text:'Complete a Hard Mode map using only 4 towers, without losing a life',reward:750,type:'challengeUltimate',goal:1}
];
function evaluateMapChallenges(){
  const used=[...new Set(battle.usedCards||[])];
  const perfect=battle.lives===(battle.mapStartLives??battle.lives);
  const placed=Math.max(0,Number(battle.totalPlaced??battle.towers?.length??0));
  const upgraded=Math.max(0,Number(battle.upgradeCount||0));
  const sold=Math.max(0,Number(battle.soldCount||0));
  if(used.length&&used.every(k=>animals[k]?.rarity==='Common'))addChallengeProgress('challengeCommonMap',1);
  if(perfect){addChallengeProgress('challengeNoLifeMap',1);addChallengeProgress('challengePerfect3',1);}
  if(used.length===1)addChallengeProgress('challengeOneAnimal',1);
  if(upgraded===0)addChallengeProgress('challengeNoUpgrades',1);
  if(used.length&&used.every(k=>animals[k]?.rarity==='Rare'))addChallengeProgress('challengeRareMap',1);
  if(used.length&&used.every(k=>animals[k]?.rarity==='Legendary'))addChallengeProgress('challengeLegendaryMap',1);
  if(placed<=4)addChallengeProgress('challengeFourTowers',1);
  if(sold===0)addChallengeProgress('challengeNoSell',1);
  if(hardMode&&perfect)addChallengeProgress('challengeHardPerfect',1);
  if(Number(battle.coins||0)>=1000)addChallengeProgress('challenge1000Coins',1);
  if(battle.allMapAt3x===true)addChallengeProgress('challengeFull3x',1);
  if(hardMode&&perfect&&placed<=4)addChallengeProgress('challengeUltimate',1);
}"""
if old not in s: raise SystemExit('challenge definition block not found')
s=s.replace(old,new,1)
# Reset battle tracking fields.
old="""    mapKills:0,mapCoinsEarned:0,
    spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false"""
new="""    mapKills:0,mapCoinsEarned:0,totalPlaced:0,upgradeCount:0,soldCount:0,allMapAt3x:true,
    spawning:false,spawnLeft:0,spawnTimer:0,waveActive:false,ended:false"""
if old not in s: raise SystemExit('resetBattle tracking block not found')
s=s.replace(old,new,1)
# Count placements.
old='''  battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost});
  addQuestProgress("placed",1);'''
new='''  battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost});
  battle.totalPlaced=Math.max(0,Number(battle.totalPlaced||0))+1;
  addQuestProgress("placed",1);'''
if old not in s: raise SystemExit('tower placement block not found')
s=s.replace(old,new,1)
# Count upgrades and complete Master Builder as soon as four towers are level 10.
old='''  battle.coins-=cost;selectedTower.spent+=cost;selectedTower.level++;updateHud();openTowerModal();'''
new='''  battle.coins-=cost;selectedTower.spent+=cost;selectedTower.level++;battle.upgradeCount=Math.max(0,Number(battle.upgradeCount||0))+1;
  if((battle.towers||[]).filter(t=>t.level>=10).length>=4)addChallengeProgress("challengeFourLevel10",1);
  updateHud();openTowerModal();'''
if old not in s: raise SystemExit('upgrade block not found')
s=s.replace(old,new,1)
# Track sells.
old='''  if(!selectedTower)return; battle.coins+=Math.floor(selectedTower.spent*.65);battle.towers=battle.towers.filter(t=>t!==selectedTower);selectedTower=null;towerModal.classList.remove("show");updateHud();'''
new='''  if(!selectedTower)return; battle.coins+=Math.floor(selectedTower.spent*.65);battle.soldCount=Math.max(0,Number(battle.soldCount||0))+1;battle.towers=battle.towers.filter(t=>t!==selectedTower);selectedTower=null;towerModal.classList.remove("show");updateHud();'''
if old not in s: raise SystemExit('sell block not found')
s=s.replace(old,new,1)
# Mark a map as not entirely 3x if any wave starts at another speed.
old='''  battle.waveStartLives=battle.lives;
  battle.waveActive=true;'''
new='''  battle.waveStartLives=battle.lives;
  if(speed!==3)battle.allMapAt3x=false;
  battle.waveActive=true;'''
if old not in s: raise SystemExit('start wave tracking block not found')
s=s.replace(old,new,1)
# Mark switching away from 3x during a live wave.
old='''speedBtn.onclick=()=>{speed=speed===1?2:speed===2?3:1;speedBtn.textContent=`⏩ Speed: ${speed}×`};'''
new='''speedBtn.onclick=()=>{speed=speed===1?2:speed===2?3:1;if(battle?.waveActive&&speed!==3)battle.allMapAt3x=false;speedBtn.textContent=`⏩ Speed: ${speed}×`};'''
if old not in s: raise SystemExit('speed button block not found')
s=s.replace(old,new,1)
# Replace existing two map-completion challenge checks with centralized evaluator.
old='''    const usedForChallenge=[...new Set(battle.usedCards||[])];
    if(usedForChallenge.length&&usedForChallenge.every(k=>animals[k]?.rarity==='Common'))addChallengeProgress("challengeCommonMap",1);
    if(battle.lives===(battle.mapStartLives??battle.lives))addChallengeProgress("challengeNoLifeMap",1);'''
new='''    evaluateMapChallenges();'''
if old not in s: raise SystemExit('map completion challenge block not found')
s=s.replace(old,new,1)
p.write_text(s)
print('Added 15 permanent challenge quests and tracking rules')
