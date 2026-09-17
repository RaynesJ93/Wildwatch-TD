// Permanent challenge expansion. Counters live in the active save slot.
const EPIC_CHALLENGE_DEFS=[
 ['hardAtlas','🔥','Hard World Conqueror','Clear all 100 distinct Hard maps across the 10 regions','hardAtlas',100,4000],
 ['hardCommonPerfect','🌱','Humble Heroes','Win a Hard map using only Common animals without losing a life','hardCommonPerfect',1,1500],
 ['hardDuo','🤝','Unbreakable Duo','Win a Hard map using exactly 2 animal types without selling any towers','hardDuo',1,1250],
 ['hardNoUpgradeFive','🛠️','Unmodified Masters','Win 5 Hard maps without upgrading any towers','hardNoUpgrade',5,2500],
 ['epicFirst','⚔️','Epic Debut','Win an Epic Mode round','wins',1,750],
 ['epicVeteran','🏅','Epic Veteran','Win 5 Epic Mode rounds','wins',5,1500],
 ['epicLegend','👑','Epic Legend','Win 25 Epic Mode rounds','wins',25,3500],
 ['epicExplorer','🧭','Epic Explorer','Complete Epic Mode in 3 different regions','regions',3,1800],
 ['epicConqueror','🌍','Epic World Conqueror','Complete Epic Mode in all 10 regions','regions',10,5000],
 ['epicWaves','🌊','Beyond the Limit','Clear 100 Epic Mode waves in total','waves',100,1250],
 ['epicArmy','⚔️','Army Breaker','Defeat 5,000 enemies in Epic Mode','kills',5000,2500],
 ['epicElites','💪','Elite Executioner','Defeat 100 elite enemies in Epic Mode','elites',100,1500],
 ['epicBosses','🐲','Titan Slayer','Defeat the wave 20 boss 10 times in Epic Mode','finalBosses',10,3000],
 ['epicPerfect','🛡️','Untouchable Epic','Win an Epic round without losing a life','perfect',1,2000],
 ['epicPerfectFive','💎','Perfectionist Supreme','Win 5 Epic rounds without losing a life','perfect',5,4000],
 ['epicBudget','🌿','Against All Odds','Win an Epic round using only Common or Uncommon animals','budget',1,3000],
 ['epicFour','🏰','The Last Four','Win an Epic round placing no more than 4 towers in total','four',1,3000],
 ['epicNoUpgrade','🚫','Raw Power','Win an Epic round without upgrading any towers','noUpgrade',1,4000],
 ['epicOneLife','❤️','One Heart Left','Win an Epic round with exactly 1 life remaining','oneLife',1,2000],
 ['epicUltimate','🏆','Impossible Defence','Win an Epic round without losing a life, placing no more than 4 towers in total and selling none','ultimate',1,5000]
].map(([id,icon,name,text,stat,goal,reward])=>({id:'expansion_'+id,icon,name,text,stat,goal,reward,rewardKind:'coins',type:'epicExpansion',tier:1}));
for(const q of EPIC_CHALLENGE_DEFS)if(!CHALLENGE_QUESTS.some(old=>old.id===q.id))CHALLENGE_QUESTS.push(q);
function epicCompletedRegionCount(){return Array.from({length:10},(_,i)=>i+1).filter(r=>save.epicCompleted?.[r]).length;}
function expandedChallengeStats(){
 if(!save.expandedChallengeStats||typeof save.expandedChallengeStats!=='object')save.expandedChallengeStats={wins:epicCompletedRegionCount()};
 return save.expandedChallengeStats;
}
function incrementExpandedChallenge(key){const stats=expandedChallengeStats();stats[key]=Math.max(0,Number(stats[key])||0)+1;}
function recordExpandedChallengeKill(e){
 if(!epicMode)return;
 incrementExpandedChallenge('kills');
 if(e.elite)incrementExpandedChallenge('elites');
 if(e.boss&&battle.wave===20)incrementExpandedChallenge('finalBosses');
}
function recordExpandedChallengeWave(w){
 if(!epicMode||battle.expansionLastWave>=w)return;
 battle.expansionLastWave=w;incrementExpandedChallenge('waves');
}
function recordExpandedChallengeWin(){
 if(battle.expansionWinTracked)return;
 battle.expansionWinTracked=true;
 const used=[...new Set(battle.usedCards||[])],placed=Number(battle.totalPlaced),sold=Number(battle.soldCount),upgraded=Number(battle.upgradeCount);
 const perfect=Number.isFinite(battle.mapStartLives)&&battle.lives===battle.mapStartLives;
 const hasTowers=used.length>0&&placed>0;
 if(epicMode){
  incrementExpandedChallenge('wins');
  if(perfect)incrementExpandedChallenge('perfect');
  if(hasTowers&&used.every(k=>['Common','Uncommon'].includes(animals[k]?.rarity)))incrementExpandedChallenge('budget');
  if(hasTowers&&placed<=4)incrementExpandedChallenge('four');
  if(hasTowers&&upgraded===0)incrementExpandedChallenge('noUpgrade');
  if(battle.lives===1)incrementExpandedChallenge('oneLife');
  if(hasTowers&&perfect&&placed<=4&&sold===0)incrementExpandedChallenge('ultimate');
 }else if(hardMode){
  if(hasTowers&&perfect&&used.every(k=>animals[k]?.rarity==='Common'))incrementExpandedChallenge('hardCommonPerfect');
  if(hasTowers&&used.length===2&&sold===0)incrementExpandedChallenge('hardDuo');
  if(hasTowers&&upgraded===0)incrementExpandedChallenge('hardNoUpgrade');
 }
}
const questStateBeforeExpansion=questState;
questState=function(q){
 if(q.type!=='epicExpansion')return questStateBeforeExpansion(q);
 let progress;
 if(q.stat==='regions')progress=epicCompletedRegionCount();
 else if(q.stat==='hardAtlas'){
  progress=0;for(let r=1;r<=10;r++)for(let m=1;m<=10;m++)if(save.hardCompleted?.[`${r}-${m}`])progress++;
 }else progress=Math.max(0,Number(expandedChallengeStats()[q.stat])||0);
 return {goal:q.goal,progress,completed:progress>=q.goal,ratio:Math.min(1,progress/q.goal)};
};
expandedChallengeStats();
renderExtraQuestBoards();
